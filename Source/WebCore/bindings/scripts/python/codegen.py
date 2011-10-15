#! /usr/bin/env python
#
# Conversion for use in pywebkit Copyright (C) 2010 Free Software Foundation
#

import getopt
import keyword
import os
import string
import sys
import traceback

import argtypes
import definitions
import defsparser
import override
import reversewrapper
import warnings

class Coverage(object):
    def __init__(self, name):
        self.name = name
        self.wrapped = 0
        self.not_wrapped = 0

    def declare_wrapped(self):
        self.wrapped += 1

    def declare_not_wrapped(self):
        self.not_wrapped += 1

    def printstats(self):
        total = self.wrapped + self.not_wrapped
        fd = sys.stderr
        if total:
            fd.write("***INFO*** The coverage of %s is %.2f%% (%i/%i)\n" %
                     (self.name,
                      float(self.wrapped*100)/total,
                      self.wrapped,
                      total))
        else:
            fd.write("***INFO*** There are no declared %s.\n" % self.name)

def startreplace(fieldname, opts):
    for (opt, replace) in opts:
        if fieldname.startswith(opt):
            return replace+fieldname[3:]
    return fieldname
    
functions_coverage = Coverage("global functions")
methods_coverage = Coverage("methods")
vproxies_coverage = Coverage("virtual proxies")
vaccessors_coverage = Coverage("virtual accessors")
iproxies_coverage = Coverage("interface proxies")

def exc_info():
    warnings.warn("deprecated", DeprecationWarning, stacklevel=2)
    #traceback.print_exc()
    etype, value, tb = sys.exc_info()
    ret = ""
    try:
        sval = str(value)
        if etype == argtypes.ArgTypeError:
            ret = "No ArgType for %s" % (sval,)
        else:
            ret = sval
    finally:
        del etype, value, tb
    return ret

def fixname(name):
    if keyword.iskeyword(name):
        return name + '_'
    return name

class FileOutput:
    '''Simple wrapper for file object, that makes writing #line
    statements easier.''' # "
    def __init__(self, fp, filename=None):
        self.fp = fp
        self.lineno = 1
        if filename:
            self.filename = filename
        else:
            self.filename = self.fp.name
    # handle writing to the file, and keep track of the line number ...
    def write(self, str):
        self.fp.write(str)
        self.lineno = self.lineno + string.count(str, '\n')
    def writelines(self, sequence):
        for line in sequence:
            self.write(line)
    def close(self):
        self.fp.close()
    def flush(self):
        self.fp.flush()

    def setline(self, linenum, filename):
        '''writes out a #line statement, for use by the C
        preprocessor.''' # "
        self.write('#line %d "%s"\n' % (linenum, filename))
    def resetline(self):
        '''resets line numbering to the original file'''
        self.setline(self.lineno + 1, self.filename)

class Wrapper:
    type_tmpl = (
        'PyTypeObject G_GNUC_INTERNAL PyDOM%(typename)s_Type = {\n'
        '    PyVarObject_HEAD_INIT(NULL, 0)\n'
        '    "%(classname)s",                   /* tp_name */\n'
        '    sizeof(%(tp_basicsize)s),          /* tp_basicsize */\n'
        '    0,                                 /* tp_itemsize */\n'
        '    /* methods */\n'
        '    (destructor)%(tp_dealloc)s,        /* tp_dealloc */\n'
        '    (printfunc)0,                      /* tp_print */\n'
        '    (getattrfunc)%(tp_getattr)s,       /* tp_getattr */\n'
        '    (setattrfunc)%(tp_setattr)s,       /* tp_setattr */\n'
        '    %(tp_compare)s,           /* tp_compare */\n'
        '    (reprfunc)%(tp_repr)s,             /* tp_repr */\n'
        '    (PyNumberMethods*)%(tp_as_number)s,     /* tp_as_number */\n'
        '    (PySequenceMethods*)%(tp_as_sequence)s, /* tp_as_sequence */\n'
        '    (PyMappingMethods*)%(tp_as_mapping)s,   /* tp_as_mapping */\n'
        '    (hashfunc)%(tp_hash)s,             /* tp_hash */\n'
        '    (ternaryfunc)%(tp_call)s,          /* tp_call */\n'
        '    (reprfunc)%(tp_str)s,              /* tp_str */\n'
        '    (getattrofunc)%(tp_getattro)s,     /* tp_getattro */\n'
        '    (setattrofunc)%(tp_setattro)s,     /* tp_setattro */\n'
        '    (PyBufferProcs*)%(tp_as_buffer)s,  /* tp_as_buffer */\n'
        '    %(tp_flags)s,                      /* tp_flags */\n'
        '    %(tp_doc)s,                        /* Documentation string */\n'
        '    (traverseproc)%(tp_traverse)s,     /* tp_traverse */\n'
        '    (inquiry)%(tp_clear)s,             /* tp_clear */\n'
        '    (richcmpfunc)%(tp_richcompare)s,   /* tp_richcompare */\n'
        '    %(tp_weaklistoffset)s,             /* tp_weaklistoffset */\n'
        '    (getiterfunc)%(tp_iter)s,          /* tp_iter */\n'
        '    (iternextfunc)%(tp_iternext)s,     /* tp_iternext */\n'
        '    (struct PyMethodDef*)%(tp_methods)s, /* tp_methods */\n'
        '    (struct PyMemberDef*)0,              /* tp_members */\n'
        '    (struct PyGetSetDef*)%(tp_getset)s,  /* tp_getset */\n'
        '    NULL,                              /* tp_base */\n'
        '    NULL,                              /* tp_dict */\n'
        '    (descrgetfunc)%(tp_descr_get)s,    /* tp_descr_get */\n'
        '    (descrsetfunc)%(tp_descr_set)s,    /* tp_descr_set */\n'
        '    %(tp_dictoffset)s,                 /* tp_dictoffset */\n'
        '    (initproc)%(tp_init)s,             /* tp_init */\n'
        '    (allocfunc)%(tp_alloc)s,           /* tp_alloc */\n'
        '    (newfunc)%(tp_new)s,               /* tp_new */\n'
        '    (freefunc)%(tp_free)s,             /* tp_free */\n'
        '    (inquiry)%(tp_is_gc)s,              /* tp_is_gc */\n'
        '    0,                                 /* tp_bases */\n'
        '    0,                                 /* tp_mro */\n'
        '    0,                                 /* tp_cache */\n'
        '    0,                                 /* tp_subclasses */\n'
        '    0,                                 /* tp_weaklist */\n'
        '    0,                                 /* tp_del */\n'
        '    0                                  /* tp_version_tag */\n'
        '};\n\n'
        )

    slots_list = [
        'tp_getattr', 'tp_setattr', 'tp_getattro', 'tp_setattro',
        'tp_compare', 'tp_repr',
        'tp_as_number', 'tp_as_sequence', 'tp_as_mapping', 'tp_hash',
        'tp_call', 'tp_str', 'tp_as_buffer', 'tp_richcompare', 'tp_iter',
        'tp_iternext', 'tp_descr_get', 'tp_descr_set', 'tp_init',
        'tp_alloc', 'tp_new', 'tp_free', 'tp_is_gc',
        'tp_traverse', 'tp_clear', 'tp_dealloc', 'tp_flags', 'tp_doc'
        ]

    setter_tmpl = (
        '%(conditional_if)s'
        'static int\n'
        '%(funcname)s(PyObject *self, PyObject *args, void *closure)\n'
        '{\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    %(setreturn)s%(field)s%(arglist)s);\n'
        '%(codeafter)s\n'
        '    return 0;\n'
        '}\n'
        '%(conditional_endif)s\n'
        )

    getter_tmpl = (
        '%(conditional_if)s'
        'static PyObject *\n'
        '%(funcname)s(PyObject *self, void *closure)\n'
        '{\n'
        '%(varlist)s'
        '%(codebefore)s'
        '    ret = %(field)s%(farg)s;\n'
        '%(codeafter)s\n'
        '}\n'
        '%(conditional_endif)s\n'
        )

    dealloc_tmpl = (
        'void dealloc_%(classname)s(PyObject *self)\n'
        '{\n'
        '    PyDOMObject *obj = (PyDOMObject*)self;\n'
        '    WebCore::%(classname)s* cobj = core%(classname)s(obj);\n'
        '    WebKit::PythonObjectCache::forgetDOMObject(cobj);\n'
        '    cobj->deref();\n'
        '    self->ob_type->tp_free(self);\n'
        '}\n\n'
        )

    parseset_tmpl = (
        '    if (!PyArg_Parse(args,'
        '"%(typecodes)s:%(name)s"%(parselist)s))\n'
        '        return %(errorreturn)s;\n'
        )

    parse_tmpl = (
        '    if (!PyArg_ParseTupleAndKeywords(args, kwargs,'
        '"%(typecodes)s:%(name)s"%(parselist)s))\n'
        '        return %(errorreturn)s;\n'
        )

    deprecated_tmpl = (
        '    if (PyErr_Warn(PyExc_DeprecationWarning, '
        '"%(deprecationmsg)s") < 0)\n'
        '        return %(errorreturn)s;\n'
        )

    methdef_tmpl = (
        '    { "%(name)s", (PyCFunction)%(cname)s, %(flags)s,\n'
        '      %(docstring)s },\n'
        )

    noconstructor = (
        'static int\n'
        'pygobject_no_constructor(PyObject *self, PyObject *args, '
        'PyObject *kwargs)\n'
        '{\n'
        '    gchar buf[512];\n'
        '\n'
        '    g_snprintf(buf, sizeof(buf), "%s is an abstract widget", '
        'self->ob_type->tp_name);\n'
        '    PyErr_SetString(PyExc_NotImplementedError, buf);\n'
        '    return -1;\n'
        '}\n\n'
        )

    function_tmpl = (
        'static PyObject *\n'
        '_wrap_%(cname)s(PyObject *self%(extraparams)s)\n'
        '{\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    %(begin_allow_threads)s\n'
		'    %(setreturn)(s%(cname)s(%(arglist)s);\n'
        '    %(end_allow_threads)s\n'
        '%(codeafter)s\n'
        '}\n\n'
        )

    virtual_accessor_tmpl = (
        'static PyObject *\n'
        '_wrap_%(cname)s(PyObject *cls%(extraparams)s)\n'
        '{\n'
        '    gpointer klass;\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    klass = g_type_class_ref(pyg_type_from_object(cls));\n'
        '    if (%(class_cast_macro)s(klass)->%(virtual)s)\n'
        '        %(setreturn)s%(class_cast_macro)s(klass)->'
        '%(virtual)s(%(arglist)s);\n'
        '    else {\n'
        '        PyErr_SetString(PyExc_NotImplementedError, '
        '"virtual method %(name)s not implemented");\n'
        '        g_type_class_unref(klass);\n'
        '        return NULL;\n'
        '    }\n'
        '    g_type_class_unref(klass);\n'
        '%(codeafter)s\n'
        '}\n\n'
        )

    # template for method calls
    constructor_tmpl = None
    method_tmpl = None

    def __init__(self, parser, objinfo, overrides, fp=FileOutput(sys.stdout)):
        self.parser = parser
        self.objinfo = objinfo
        self.overrides = overrides
        self.fp = fp

    def get_lower_name(self):
        return string.lower(string.replace(self.objinfo.typecode,
                                           '_TYPE_', '_', 1))

    def get_field_accessor(self, fieldname):
        raise NotImplementedError

    def get_initial_class_substdict(self): return {}

    def get_initial_constructor_substdict(self, constructor):
        return { 'name': '%s.__init__' % self.objinfo.py_name,
                 'errorreturn': '-1' }

    def get_initial_method_substdict(self, method):
        substdict = { 'name': '%s.%s' % (self.objinfo.py_name, method.name) }
        if method.unblock_threads:
            substdict['begin_allow_threads'] = 'pyg_begin_allow_threads;'
            substdict['end_allow_threads'] = 'pyg_end_allow_threads;'
        else:
            substdict['begin_allow_threads'] = ''
            substdict['end_allow_threads'] = ''
        return substdict

    def write_class(self):
        if self.overrides.is_type_ignored(self.objinfo.c_name):
            return

        cond = get_conditional_substitutions(self.objinfo.orig_obj.attributes)

        self.fp.write(cond['conditional_if'])

        self.fp.write('\n/* ----------- %s ----------- */\n\n' %
                      self.objinfo.c_name)
        self.fp.write('namespace WebKit {\n')
        self.fp.write('using namespace WebCore;\n')
        substdict = self.get_initial_class_substdict()
        if not substdict.has_key('tp_flags'):
            substdict['tp_flags'] = self.write_flags()
        substdict['typename'] = self.objinfo.c_name
        if self.overrides.modulename:
            substdict['classname'] = '%s.%s' % (self.overrides.modulename,
                                           self.objinfo.name)
        else:
            substdict['classname'] = '%s.%s' % (self.prefix, self.objinfo.name)
        substdict['tp_doc'] = self.objinfo.docstring

        # Maybe this could be done in a nicer way, but I'll leave it as it is
        # for now: -- Johan
        if not self.overrides.slot_is_overriden('%s.tp_init' %
                                                self.objinfo.c_name):
            substdict['tp_init'] = self.write_constructor()
        substdict['tp_methods'] = self.write_methods()
        substdict['tp_getset'] = self.write_getsets()
        substdict['tp_dealloc'] = self.write_dealloc()
        substdict['tp_new'] = 'DOMObject_new'
        substdict['tp_iter'] = self.write_iter()
        substdict['tp_iternext'] = self.write_iternext()


        # handle slots ...
        for slot in self.slots_list:

            slotname = '%s.%s' % (self.objinfo.c_name, slot)
            slotfunc = '_wrap_%s_%s' % (self.get_lower_name(), slot)
            if slot[:6] == 'tp_as_':
                slotfunc = '&' + slotfunc
            if self.overrides.slot_is_overriden(slotname):
                data = self.overrides.slot_override(slotname)
                self.write_function(slotname, data)
                substdict[slot] = slotfunc
            else:
                if not substdict.has_key(slot):
                    substdict[slot] = '0'

        self.fp.write('} // namespace WebKit\n')

        self.fp.write('extern "C" {\n\n')
        self.fp.write(self.type_tmpl % substdict)
        self.fp.write('}; // extern "C"\n')

        self.write_virtuals()

        self.fp.write(cond['conditional_endif'])

        self.fp.write('\n')

    def find_function_ptypes(self, function_obj, handle_return=0):

        includes = set()
        for param in function_obj.params:
            includes.add(param.ptype)
        if handle_return:
            includes.add(function_obj.ret)
        return includes


    def write_flags(self):
        return 'Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE'

    def write_function_wrapper(self, function_obj, template,
                               handle_return=0, is_method=0, kwargs_needed=0,
                               substdict=None,
                               exception_needed=0):
        '''This function is the guts of all functions that generate
        wrappers for functions, methods and constructors.'''
        if not substdict: substdict = {}

        info = argtypes.WrapperInfo()

        substdict.setdefault('errorreturn', 'NULL')

        # for methods, we want the leading comma
        #if is_method:
            #info.arglist.append('')

        if function_obj.varargs:
            raise argtypes.ArgTypeNotFoundError("varargs functions not supported")

        for param in function_obj.params:
            if param.pdflt != None and '|' not in info.parsestr:
                info.add_parselist('|', [], [])
            handler = argtypes.matcher.get(param.ptype)
            handler.write_param(param.ptype, param.pname, param.pdflt,
                                param.pnull, info)

        if exception_needed:
            info.arglist.append("ec")
            info.codebefore.append("    WebCore::ExceptionCode ec = 0;\n")

        substdict['setreturn'] = ''
        if handle_return:
            if function_obj.ret not in ('none', None):
                if (self.objinfo.c_name == 'Node' and function_obj.c_name in
                    ['insertBefore', 'replaceChild',
                     'removeChild', 'appendChild']):
                    substdict['setreturn'] = 'bool ok = '
                    info.codeafter.append('    /* TODO: raise exception */\n')
                    info.codeafter.append('    if (!ok) {\n')
                    info.codeafter.append('        py_wk_exc(ec);\n')
                    info.codeafter.append('        return NULL;\n')
                    info.codeafter.append('    }\n')
                    res = function_obj.return_param[1] # XXX assumption!
                    info.codeafter.append('    Py_INCREF((PyObject*)%s);\n' % res)
                    info.codeafter.append('    return (PyObject*)%s;\n' % res)
                else:
                    substdict['setreturn'] = 'ret = '
                    if function_obj.return_param is None:
                        handler = argtypes.matcher.get(function_obj.ret)
                        handler.write_return(function_obj.ret,
                                             function_obj.caller_owns_return, info)
                    else:
                        handler = argtypes.matcher.get(function_obj.return_param[0])
                        handler.write_return(function_obj.return_param[0],
                                             function_obj.caller_owns_return, info)
            else:
                handler = argtypes.matcher.get(function_obj.ret)
                handler.write_return(function_obj.ret,
                                     function_obj.caller_owns_return, info)

        if function_obj.deprecated != None:
            deprecated = self.deprecated_tmpl % {
                'deprecationmsg': function_obj.deprecated,
                'errorreturn': substdict['errorreturn'] }
        else:
            deprecated = ''

        # if name isn't set, set it to function_obj.name
        substdict.setdefault('name', function_obj.name)

        if function_obj.unblock_threads:
            substdict['begin_allow_threads'] = 'pyg_begin_allow_threads;'
            substdict['end_allow_threads'] = 'pyg_end_allow_threads;'
        else:
            substdict['begin_allow_threads'] = ''
            substdict['end_allow_threads'] = ''

        if self.objinfo:
            substdict['typename'] = self.objinfo.c_name
        substdict.setdefault('cname',  function_obj.c_name)
        substdict['varlist'] = info.get_varlist()
        substdict['typecodes'] = info.parsestr
        substdict['parselist'] = info.get_parselist()
        substdict['arglist'] = info.get_arglist()
        substdict['codebefore'] = deprecated + (
            string.replace(info.get_codebefore(),
            'return NULL', 'return ' + substdict['errorreturn'])
            )
        substdict['codeafter'] = (
            string.replace(info.get_codeafter(),
                           'return NULL',
                           'return ' + substdict['errorreturn']))

        if info.parsestr or kwargs_needed:
            substdict['parseargs'] = self.parse_tmpl % substdict
            substdict['extraparams'] = ', PyObject *args, PyObject *kwargs'
            flags = 'METH_VARARGS|METH_KEYWORDS'

            # prepend the keyword list to the variable list
            substdict['varlist'] = info.get_kwlist() + substdict['varlist']
        else:
            substdict['parseargs'] = ''
            substdict['extraparams'] = ''
            flags = 'METH_NOARGS'

        return template % substdict, flags

    def write_constructor(self):
        
        pyinit_tmpl = \
"""
static int
%(classname)s_init(%(classname)s *self, PyObject *args, PyObject *kwds)
{
    if (PyDOM%(base)s_Type.tp_init((PyObject *)self, args, kwds) < 0)
        return -1;
    return 0;
}
"""

        classname = self.objinfo.name
        base = self.objinfo.parent
        if base == 'DOMObject':
            base = 'Object'
        code = pyinit_tmpl % dict(classname=classname, base=base)
        self.fp.write(code)
        return "WebKit::" + classname + "_init"

    def write_noconstructor(self):
        # this is a hack ...
        if not hasattr(self.overrides, 'no_constructor_written'):
            self.fp.write(self.noconstructor)
            self.overrides.no_constructor_written = 1
        initfunc = 'pygobject_no_constructor'
        return initfunc

    def write_default_constructor(self):
        return self.write_noconstructor()

    def get_methflags(self, funcname):
        if self.overrides.wants_kwargs(funcname):
            flags = 'METH_VARARGS|METH_KEYWORDS'
        elif self.overrides.wants_noargs(funcname):
            flags = 'METH_NOARGS'
        elif self.overrides.wants_onearg(funcname):
            flags = 'METH_O'
        else:
            flags = 'METH_VARARGS'
        if self.overrides.is_staticmethod(funcname):
            flags += '|METH_STATIC'
        elif self.overrides.is_classmethod(funcname):
            flags += '|METH_CLASS'
        return flags

    def write_function(self, funcname, data):
        lineno, filename = self.overrides.getstartline(funcname)
        self.fp.setline(lineno, filename)
        self.fp.write(data)
        self.fp.resetline()
        self.fp.write('\n\n')

    def _get_class_virtual_substdict(self, meth, cname, parent):
        substdict = self.get_initial_method_substdict(meth)
        substdict['virtual'] = meth.name
        substdict['cname'] = cname
        substdict['class_cast_macro'] = parent.typecode.replace(
            '_TYPE_', '_', 1) + "_CLASS"
        substdict['typecode'] = self.objinfo.typecode
        substdict['cast'] = string.replace(parent.typecode, '_TYPE_', '_', 1)
        return substdict

    def find_include_ptypes(self):
        includes = set()
        klass = self.objinfo.c_name
        # First, get methods from the defs files
        for meth in self.parser.find_methods(self.objinfo):
            method_name = meth.c_name
            if self.overrides.is_ignored(method_name):
                continue
            if self.overrides.is_overriden(method_name):
                continue
            includes.update(self.find_function_ptypes(meth, handle_return=1))
        return includes

    def write_methods(self):
        methods = []
        klass = self.objinfo.c_name
        # First, get methods from the defs files
        for meth in self.parser.find_methods(self.objinfo):
            method_name = meth.c_name
            if self.overrides.is_ignored(method_name):
                continue
            try:
                if self.overrides.is_overriden(method_name):
                    if not self.overrides.is_already_included(method_name):
                        data = self.overrides.override(method_name)
                        self.write_function(method_name, data)

                    methflags = self.get_methflags(method_name)
                else:
                    # write constructor from template ...
                    code, methflags = self.write_function_wrapper(meth,
                        self.method_tmpl, handle_return=1, is_method=1,
                        substdict=self.get_initial_method_substdict(meth),
                        exception_needed=meth.raises)
                    self.fp.write(code)
                methods.append(self.methdef_tmpl %
                               { 'name':  fixname(meth.name),
                                 'cname': 'WebKit::_wrap_%s_%s' % (klass, method_name),
                                 'flags': methflags,
                                 'docstring': meth.docstring })
                methods_coverage.declare_wrapped()
            except argtypes.ArgTypeError, ex:
                traceback.print_exc()
                sys.stderr.write('declaration of type needed %s.%s: %s\n'
                                % (klass, meth.name, ex))

        # Now try to see if there are any defined in the override
        for method_name in self.overrides.get_defines_for(klass):
            c_name = override.class2cname(klass, method_name)
            if self.overrides.is_already_included(method_name):
                continue

            try:
                data = self.overrides.define(klass, method_name)
                self.write_function(method_name, data)
                methflags = self.get_methflags(method_name)

                methods.append(self.methdef_tmpl %
                               { 'name':  method_name,
                                 'cname': '_wrap_' + c_name,
                                 'flags': methflags,
                                 'docstring': 'NULL' })
                methods_coverage.declare_wrapped()
            except argtypes.ArgTypeError, ex:
                methods_coverage.declare_not_wrapped()
                sys.stderr.write('Could not write method %s.%s: %s\n'
                                % (klass, method_name, str(ex)))

        # Add GObject virtual method accessors, for chaining to parent
        # virtuals from subclasses
        methods += self.write_virtual_accessors()

        if methods:
            self.fp.write('} // namespace WebKit\n')
            methoddefs = '_PyDOM%s_methods' % self.objinfo.c_name
            # write the PyMethodDef structure
            methods.append('    { NULL, NULL, 0, NULL }\n')
            self.fp.write('extern "C" {\n\n')
            self.fp.write('static const PyMethodDef %s[] = {\n' % methoddefs)
            self.fp.write(string.join(methods, ''))
            self.fp.write('};\n\n')
            self.fp.write('}; // extern "C"\n')
            self.fp.write('namespace WebKit {\n')
            self.fp.write('using namespace WebCore;\n')
        else:
            methoddefs = 'NULL'
        return methoddefs

    def write_iter(self):
        return "0"

    def write_iternext(self):
        return "0"

    def write_virtual_accessors(self):
        klass = self.objinfo.c_name
        methods = []
        for meth in self.parser.find_virtuals(self.objinfo):
            method_name = self.objinfo.c_name + "__do_" + meth.name
            if self.overrides.is_ignored(method_name):
                continue
            try:
                if self.overrides.is_overriden(method_name):
                    if not self.overrides.is_already_included(method_name):
                        data = self.overrides.override(method_name)
                        self.write_function(method_name, data)
                    methflags = self.get_methflags(method_name)
                else:
                    # temporarily add a 'self' parameter as first argument
                    meth.params.insert(0, definitions.Parameter(
                        ptype=(self.objinfo.c_name + '*'),
                        pname='self', pdflt=None, pnull=None))
                    try:
                        # write method from template ...
                        code, methflags = self.write_function_wrapper(
                            meth, self.virtual_accessor_tmpl,
                            handle_return=True, is_method=False,
                            substdict=self._get_class_virtual_substdict(
                            meth, method_name, self.objinfo))
                        self.fp.write(code)
                    finally:
                        del meth.params[0]
                methods.append(self.methdef_tmpl %
                               { 'name':  "do_" + fixname(meth.name),
                                 'cname': '_wrap_' + method_name,
                                 'flags': methflags + '|METH_CLASS',
                                 'docstring': 'NULL'})
                vaccessors_coverage.declare_wrapped()
            except argtypes.ArgTypeError, ex:
                vaccessors_coverage.declare_not_wrapped()
                sys.stderr.write(
                    'Could not write virtual accessor method %s.%s: %s\n'
                    % (klass, meth.name, str(ex)))
        return methods

    def write_virtuals(self):
        '''
        Write _wrap_FooBar__proxy_do_zbr() reverse wrapers for
        GObject virtuals
        '''
        klass = self.objinfo.c_name
        virtuals = []
        for meth in self.parser.find_virtuals(self.objinfo):
            method_name = self.objinfo.c_name + "__proxy_do_" + meth.name
            if self.overrides.is_ignored(method_name):
                continue
            try:
                if self.overrides.is_overriden(method_name):
                    if not self.overrides.is_already_included(method_name):
                        data = self.overrides.override(method_name)
                        self.write_function(method_name, data)
                else:
                    # write virtual proxy ...
                    ret, props = argtypes.matcher.get_reverse_ret(meth.ret)
                    wrapper = reversewrapper.ReverseWrapper(
                        '_wrap_' + method_name, is_static=True)
                    wrapper.set_return_type(ret(wrapper, **props))
                    wrapper.add_parameter(reversewrapper.PyDOMObjectMethodParam(
                        wrapper, "self", method_name="do_" + meth.name,
                        c_type=(klass + ' *')))
                    for param in meth.params:
                        handler, props = argtypes.matcher.get_reverse(
                            param.ptype)
                        props["direction"] = param.pdir
                        props["nullok"] = param.pnull
                        wrapper.add_parameter(handler(wrapper,
                                                      param.pname, **props))
                    buf = reversewrapper.MemoryCodeSink()
                    wrapper.generate(buf)
                    self.fp.write(buf.flush())
                virtuals.append((fixname(meth.name), '_wrap_' + method_name))
                vproxies_coverage.declare_wrapped()
            except argtypes.ArgTypeError, ex:
                vproxies_coverage.declare_not_wrapped()
                virtuals.append((fixname(meth.name), None))
                sys.stderr.write('Could not write virtual proxy %s.%s: %s\n'
                                % (klass, meth.name, str(ex)))
        if virtuals:
            # Write a 'pygtk class init' function for this object,
            # except when the object type is explicitly ignored (like
            # GtkPlug and GtkSocket on win32).
            if self.overrides.is_ignored(self.objinfo.typecode):
                return
            class_cast_macro = self.objinfo.typecode.replace(
                '_TYPE_', '_', 1) + "_CLASS"
            cast_macro = self.objinfo.typecode.replace('_TYPE_', '_', 1)
            funcname = "__%s_class_init" % klass
            self.objinfo.class_init_func = funcname
            have_implemented_virtuals = not not [True
                                                 for name, cname in virtuals
                                                     if cname is not None]
            self.fp.write(
            ('\nstatic int\n'
             '%(funcname)s(gpointer gclass, PyTypeObject *pyclass)\n'
             '{\n') % vars())

            if have_implemented_virtuals:
                self.fp.write('    PyObject *o;\n')
                self.fp.write(
                    '    %(klass)sClass *klass = '
                    '%(class_cast_macro)s(gclass);\n'
                    '    PyObject *gsignals = '
                    'PyDict_GetItemString(pyclass->tp_dict, "__gsignals__");\n'
                    % vars())

            for name, cname in virtuals:
                do_name = 'do_' + name
                if cname is None:
                    self.fp.write('\n    /* overriding %(do_name)s '
                                  'is currently not supported */\n' % vars())
                else:
                    self.fp.write('''
    o = PyObject_GetAttrString((PyObject *) pyclass, "%(do_name)s");
    if (o == NULL)
        PyErr_Clear();
    else {
        if (!PyObject_TypeCheck(o, &PyCFunction_Type)
            && !(gsignals && PyDict_GetItemString(gsignals, "%(name)s")))
            klass->%(name)s = %(cname)s;
        Py_DECREF(o);
    }
''' % vars())
            self.fp.write('    return 0;\n}\n')

    def write_dealloc(self):

        txt = self.dealloc_tmpl % {'classname': self.objinfo.c_name}
        self.fp.write(txt)

        return 'WebKit::dealloc_' + self.objinfo.c_name

    def write_getsets(self):
        lower_name = self.get_lower_name()
        getsets_name = lower_name + '_getsets'
        getterprefix = '_wrap_' + lower_name + '__get_'
        setterprefix = '_wrap_' + lower_name + '__set_'

        # no overrides for the whole function.  If no fields,
        # don't write a func
        if not self.objinfo.fields:
            return '0'
        getsets = []
        for ftype, cfname in self.objinfo.fields:
            fname = cfname.replace('.', '_')
            gettername = '0'
            settername = '0'
            
            attrname = self.objinfo.c_name + '.' + fname
            if self.overrides.attr_is_overriden(attrname):
                code = self.overrides.attr_override(attrname)
                self.write_function(attrname, code)
                if string.find(code, getterprefix + fname) >= 0:
                    gettername = getterprefix + fname
                if string.find(code, setterprefix + fname) >= 0:
                    settername = setterprefix + fname
            
            
            attribs = self.objinfo.attributes[fname]
            conditional = get_conditional_substitutions(attribs) 
            if gettername == '0':
                try:
                    funcname = getterprefix + fname
                    info = argtypes.WrapperInfo()
                    handler = argtypes.matcher.get(ftype)
                    # for attributes, we don't own the "return value"
                    handler.write_return(ftype, 0, info)
                    exception_needed = attribs.getter
                    if exception_needed:
                        field_args = "ec)"
                        info.codebefore.append("    WebCore::ExceptionCode ec = 0;\n")
                    else:
                        field_args = ")"
                    facc = self.get_field_accessor(cfname, ftype, attribs.attributes)

                    substdict = { 'funcname': funcname,
                                  'varlist': info.varlist,
                                  'field': facc,
                                  'farg': field_args,
                                  'codebefore': info.get_codebefore(),
                                  'codeafter': info.get_codeafter() }
                    substdict.update(conditional)

                    self.fp.write(self.getter_tmpl % substdict)

                    gettername = "WebKit::"+funcname
                except argtypes.ArgTypeError, ex:
                    sys.stderr.write(
                        "Could not write getter for %s.%s: %s\n"
                        % (self.objinfo.c_name, fname, str(ex)))
            
                    
            readonly = attribs.readonly
            if settername == '0' and not readonly:
                try:
                    funcname = setterprefix + fname
                    info = argtypes.WrapperInfo()
                    info.parselist = [''] # remove kwlist, for PyArgs_Parse
                    handler = argtypes.matcher.get(ftype)
                    hack = ftype in \
                        ['EventListener*', 'ScheduledActionBase*'] # XXX HACK!
                    handler.write_param(ftype, fname, None,
                                        hack, info)
                    exception_needed = attribs.setter
                    if exception_needed:
                        info.arglist.append("ec")
                        info.codebefore.append("    WebCore::ExceptionCode ec = 0;\n")

                    fset = self.get_field_setter(cfname, ftype, attribs.attributes)
                    substdict = { 'funcname': funcname,
                                    'varlist': info.get_varlist(),
                                    'field': fset,
                                    'codeafter': info.get_codeafter() }
                    substdict['varlist'] = substdict['varlist']
                    substdict.setdefault('errorreturn', '-1')
                    substdict.setdefault('name', funcname)
                    substdict['setreturn'] = ''
                    substdict['typecodes'] = info.parsestr
                    substdict['parselist'] = info.get_parselist()
                    substdict['arglist'] = info.get_arglist()
                    substdict['codebefore'] = (
                        string.replace(info.get_codebefore(),
                        'return NULL', 'return ' + substdict['errorreturn'])
                        )
                    substdict['codeafter'] = (
                        string.replace(info.get_codeafter(),
                                       'return NULL',
                                       'return ' + substdict['errorreturn']))

                    substdict['parseargs'] = self.parseset_tmpl % substdict
                    substdict.update(conditional)
                    
                    self.fp.write(self.setter_tmpl % substdict)
                    
                    settername = "WebKit::"+funcname
                except argtypes.ArgTypeError, ex:
                    traceback.print_exc()
                    sys.stderr.write(
                        "Could not write setter for %s.%s: %s\n"
                        % (self.objinfo.c_name, fname, str(ex)))
            if gettername != '0' or settername != '0':
                substdict = {}
                substdict['getter'] = gettername
                substdict['setter'] = settername
                substdict['name'] = fixname(fname)
                substdict.update(conditional)
                tmpl = (
                    '%(conditional_if)s'
                    '    {(char*)"%(name)s", (getter)%(getter)s, (setter)%(setter)s, 0, 0 },\n'
                    '%(conditional_endif)s')

                getsets.append(tmpl % substdict)

        if not getsets:
            return '0'
        self.fp.write('} // namespace WebKit\n')
        self.fp.write('extern "C" {\n\n')
        self.fp.write('static const PyGetSetDef %s[] = {\n' % getsets_name)
        for getset in getsets:
            self.fp.write(getset)
        self.fp.write('    { NULL, (getter)0, (setter)0, NULL, NULL },\n')
        self.fp.write('};\n\n')
        self.fp.write('}; // extern "C"\n')
        self.fp.write('namespace WebKit {\n')
        self.fp.write('using namespace WebCore;\n')
        self.fp.write('\n')

        return getsets_name

    def _write_get_symbol_names(self, writer, functions):
        self.fp.write("""static PyObject *
_wrap__get_symbol_names(PyObject *self)
{
    PyObject *pylist = PyList_New(0);

""")
        for obj, bases in writer.get_classes():
            self.fp.write('    PyList_Append(pylist, '
                          'PyUnicode_FromString("%s"));\n' % (obj.name))

        for name, cname, flags, docstring in functions:
            self.fp.write('    PyList_Append(pylist, '
                          'PyUnicode_FromString("%s"));\n' % (name))

        for enum in writer.get_enums():
            self.fp.write('    PyList_Append(pylist, '
                          'PyUnicode_FromString("%s"));\n' % (enum.name))
            for nick, value in enum.values:
                name = value[len(self.overrides.modulename)+1:]
                self.fp.write('    PyList_Append(pylist, '
                              'PyUnicode_FromString("%s"));\n' % (name))

        self.fp.write("    return pylist;\n}\n\n");

    def _write_get_symbol(self, writer, functions):
        self.fp.write("""static PyObject *
_wrap__get_symbol(PyObject *self, PyObject *args)
{
    PyObject *d;
    char *name;
    static PyObject *modulename = NULL;
    static PyObject *module = NULL;
    static char *strip_prefix = "%s";

    if (!PyArg_ParseTuple(args, "Os", &d, &name))
        return NULL;

    if (!modulename)
       modulename = PyUnicode_FromString("%s");

    if (!module)
       module = PyDict_GetItemString(d, "__module__");

""" % (self.overrides.modulename.upper() + '_',
       self.overrides.modulename))

        first = True
        # Classes / GObjects
        for obj, bases in writer.get_classes():
            if first:
                self.fp.write('    if (!strcmp(name, "%s")) {\n' % obj.name)
                first = False
            else:
                self.fp.write('    } else if (!strcmp(name, "%s")) {\n' % obj.name)
            self.fp.write(
                '       return (PyObject*)pygobject_lookup_class(%s);\n' %
                obj.typecode)
        self.fp.write('    }\n')

        # Functions
        for name, cname, flags, docstring in functions:
            self.fp.write('    else if (!strcmp(name, "%s")) {\n' % name)
            self.fp.write('        static PyMethodDef ml = { '
                          '"%s", (PyCFunction)%s, %s, "%s"};\n' % (
                name, cname, flags, docstring))
            self.fp.write('        return PyCFunction_NewEx(&ml, NULL, modulename);\n')
            self.fp.write('    }\n')

        # Enums
        def write_enum(enum, returnobj=False):
            if returnobj:
                ret = 'return '
            else:
                ret = ''
            if enum.deftype == 'enum':
                self.fp.write(
                    '        %spyg_enum_add(module, "%s", strip_prefix, %s);\n'
                    % (ret, enum.name, enum.typecode))
            else:
                self.fp.write(
                    '    %spyg_flags_add(module, "%s", strip_prefix, %s);\n'
                    % (ret, enum.name, enum.typecode))

        strip_len = len(self.overrides.modulename)+1 # GTK_
        for enum in writer.get_enums():
            # XXX: Implement without typecodes
            self.fp.write('    else if (!strcmp(name, "%s")) {\n' % enum.name)
            write_enum(enum, returnobj=True)
            self.fp.write('    }\n')

            for nick, value in enum.values:
                value = value[strip_len:]
                self.fp.write('    else if (!strcmp(name, "%s")) {\n' % value)
                write_enum(enum)
                self.fp.write('        return PyObject_GetAttrString(module, "%s");\n' %
                              value)
                self.fp.write('    }\n')

        self.fp.write('    return Py_None;\n}\n\n');

    def _write_function_bodies(self):
        functions = []
        # First, get methods from the defs files
        for func in self.parser.find_functions():
            funcname = func.c_name
            if self.overrides.is_ignored(funcname):
                continue
            try:
                if self.overrides.is_overriden(funcname):
                    data = self.overrides.override(funcname)
                    self.write_function(funcname, data)

                    methflags = self.get_methflags(funcname)
                else:
                    # write constructor from template ...
                    code, methflags = self.write_function_wrapper(func,
                        self.function_tmpl, handle_return=1, is_method=0)
                    self.fp.write(code)
                functions.append((func.name, '_wrap_' + funcname,
                                  methflags, func.docstring))
                functions_coverage.declare_wrapped()
            except argtypes.ArgTypeError, ex:
                functions_coverage.declare_not_wrapped()
                sys.stderr.write('Could not write function %s: %s\n'
                                 % (func.name, str(ex)))

        # Now try to see if there are any defined in the override
        for funcname in self.overrides.get_functions():
            try:
                data = self.overrides.function(funcname)
                self.write_function(funcname, data)
                methflags = self.get_methflags(funcname)
                functions.append((funcname, '_wrap_' + funcname,
                                  methflags, 'NULL'))
                functions_coverage.declare_wrapped()
            except argtypes.ArgTypeError, ex:
                functions_coverage.declare_not_wrapped()
                sys.stderr.write('Could not write function %s: %s\n'
                                 % (funcname, str(ex)))
        return functions

    def write_functions(self, writer, prefix):
        self.fp.write('\n/* ----------- functions ----------- */\n\n')
        functions = []
        func_infos = self._write_function_bodies()

        # If we have a dynamic namespace, write symbol and attribute getter
        if self.overrides.dynamicnamespace:
            self._write_get_symbol_names(writer, func_infos)
            self._write_get_symbol(writer, func_infos)
            for obj, bases in writer.get_classes():
                self.fp.write("""static PyTypeObject *
%s_register_type(const gchar *name, PyObject *unused)
{
    PyObject *m = PyImport_ImportModule("gtk");
    PyObject *d = PyModule_GetDict(m);
""" % obj.c_name)
                writer.write_class(obj, bases, indent=1)
                self.fp.write(
                    '    return (%s)PyDict_GetItemString(d, "%s");\n' % (
                    'PyTypeObject*', obj.name))
                self.fp.write("}\n")

            functions.append('    { "_get_symbol_names", '
                             '(PyCFunction)_wrap__get_symbol_names, '
                             'METH_NOARGS, NULL },\n')
            functions.append('    { "_get_symbol", '
                             '(PyCFunction)_wrap__get_symbol, '
                             'METH_VARARGS, NULL },\n')
        else:
            for name, cname, flags, docstring in func_infos:
                functions.append(self.methdef_tmpl % dict(name=name,
                                                          cname=cname,
                                                          flags=flags,
                                                          docstring=docstring))

        # write the PyMethodDef structure
        functions.append('    { NULL, NULL, 0, NULL }\n')

        #self.fp.write('const PyMethodDef ' + prefix + '_functions[] = {\n')
        #self.fp.write(string.join(functions, ''))
        #self.fp.write('};\n\n')

class GObjectWrapper(Wrapper):
    constructor_tmpl = (
        'static int\n'
        '_wrap_%(cname)s(PyDOMObject *self%(extraparams)s)\n'
        '{\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    self->obj = (GObject *)%(cname)s(%(arglist)s);\n'
        '%(codeafter)s\n'
        '    if (!self->obj) {\n'
        '        PyErr_SetString(PyExc_RuntimeError, '
        '"could not create %(typename)s object");\n'
        '        return -1;\n'
        '    }\n'
        '%(aftercreate)s'
        '    pygobject_register_wrapper((PyObject *)self);\n'
        '    return 0;\n'
        '}\n\n'
        )

    method_tmpl = (
        '%(conditional_if)s'
        'static PyObject *\n'
        '_wrap_%(typename)s_%(cname)s(PyDOMObject *self%(extraparams)s)\n'
        '{\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    %(begin_allow_threads)s\n'
        '    %(setreturn)s%(cast)s(self)->%(cname)s(%(arglist)s);\n'
        '    %(end_allow_threads)s\n'
        '%(codeafter)s\n'
        '}\n'
        '%(conditional_endif)s\n'
        )

    def __init__(self, parser, objinfo, overrides, fp=FileOutput(sys.stdout)):
        Wrapper.__init__(self, parser, objinfo, overrides, fp)
        if self.objinfo:
            self.castmacro = string.replace(self.objinfo.typecode,
                                            '_TYPE_', '_', 1)

    def is_iterator(self):
        o = self.objinfo.orig_obj
        if not o.attributes.attributes.has_key("HasIndexGetter"):
            return False

        return self.get_iter_method() != None

    def write_flags(self):
        if self.is_iterator():
            return Wrapper.write_flags(self) #+ " | Py_TPFLAGS_HAVE_ITER"

        return Wrapper.write_flags(self)

    def write_iter(self):
        if not self.is_iterator():
            return "0";
        
        tmpl = ( 
        'PyDOMObject* \n'
        '%(typename)s_iter(PyDOMObject* self)\n'
        '{\n'
        '   self->iter_index = 0;\n'
        '   self->iter_count = %(cast)s(self)->length();\n'
        '   Py_INCREF(self);\n'
        '   return self;\n'
        '}\n\n'
        )

        substdict = {}
        substdict['typename'] = self.objinfo.c_name
        substdict['cast'] = string.replace(self.objinfo.typecode, '_TYPE_', '_', 1)

        self.fp.write(tmpl % substdict)

        return "WebKit::%(typename)s_iter" % substdict

    def write_iternext(self):
        if not self.is_iterator():
            return "0";

        tmpl = ( 
        'PyObject* \n'
        '%(typename)s_iternext(PyDOMObject* self)\n'
        '{\n'
        '    unsigned long index = self->iter_index++;\n'
        '    if (index >= self->iter_count)\n'
        '    {\n'
        '        PyErr_SetNone(PyExc_StopIteration);\n'
        '        return NULL;\n'
        '    }\n\n'
        '    PyObject* args = Py_BuildValue("(k)", index);\n'
        '    PyObject* kwargs = PyDict_New();\n\n'
        '    return _wrap_%(typename)s_%(cname)s(self, args, kwargs);\n'
        '}\n\n'
        )
        
        m = self.get_iter_method()
        
        substdict = {}
        substdict['typename'] = self.objinfo.c_name
        substdict['cname'] = m.c_name
        
        self.fp.write(tmpl % substdict)

        return "WebKit::%(typename)s_iternext" % substdict

    def get_iter_method(self):
        for meth in self.parser.find_methods(self.objinfo):
            pp = meth.orig_method.params

            if len(pp) != 1:
                continue

            for att, val, loc in pp[0].attlist:
                if att == 'IsIndex':
                    return meth
        
        return None

    def get_initial_class_substdict(self):
        return { 'tp_basicsize'      : 'PyDOM%s' % self.objinfo.name,
                 'tp_weaklistoffset' : '0', 
                 'tp_dictoffset'     : '0'} 

    def attr_name_for_getter_setter(self, attr_name, attr_type):
        if attr_name == 'operator':
            return "_operator" # avoid c++ name-clash
        # TODO: SVG Animated type extension
        # if isSVGAnimatedType(attr_type): return "Animated"+attr_name
        return attr_name

    def content_attribute_name(self, iface, attr_name, attr_type, reflect):
        if reflect is None:
            return None
        reflect = reflect[0]
        if reflect is None:
            attr_name = self.attr_name_for_getter_setter(attr_name, attr_type)
        else:
            attr_name = reflect
            if isinstance(attr_name, list):
                attr_name = attr_name[0]
        # XXX TODO: detect interface, use SVGNames if appropriate.
        return "WebCore::%s::%sAttr" % (iface, attr_name)

    def get_field_accessor(self, attr_name, attr_type, attributes):
        castmacro = self.objinfo.typecode
        reflect = attributes.get('Reflect', None)
        fieldname = attr_name
        attr_name = self.content_attribute_name("HTMLNames", attr_name.lower(),
                                                 attr_type, reflect)
        if attr_name is None:
            fieldname = self.attr_name_for_getter_setter(fieldname, attr_type)
            fieldname = fieldname[0].lower() + fieldname[1:]
            fieldname = startreplace(fieldname, (
                            ("hTML", "html"), ("uRL", "url"), ("jS", "js"),
                            ("xML", "xml"), ("xSLT", "xslt"),
                            ("create", "isCreate"),
                            ("exclusive", "isExclusive")))
            return '%s((PyDOMObject*)(self))->%s(' % (castmacro, fieldname)

        if attributes.has_key("URL"):
            if attributes.has_key("NonEmpty"):
                functionName = "getNonEmptyURLAttribute"
            else:
                functionName = "getURLAttribute"
        elif attr_type == 'bool':
            functionName = "hasAttribute"
        elif attr_type == 'long':
            functionName = "getIntegralAttribute"
        elif attr_type == 'unsigned long':
            functionName = "getUnsignedIntegralAttribute"
        else:
            functionName = "getAttribute"

        return '%s((PyDOMObject*)(self))->%s(%s' % \
                (castmacro, functionName, attr_name)

    def get_field_setter(self, attr_name, attr_type, attributes):
        castmacro = self.objinfo.typecode
        reflect = attributes.get('Reflect', None)
        fieldname = attr_name
        attr_name = self.content_attribute_name("HTMLNames", attr_name.lower(),
                                                 attr_type, reflect)
        if attr_name is None:
            fieldname = self.attr_name_for_getter_setter(fieldname, attr_type)
            fieldname = fieldname[0].upper() + fieldname[1:]
            fieldname = startreplace(fieldname, (("Xml", "XML"),))
            return '%s((PyDOMObject*)(self))->set%s(' % (castmacro, fieldname)

        if attr_type == 'bool':
            functionName = "setBooleanAttribute"
        elif attr_type == 'long':
            functionName = "setIntegralAttribute"
        elif attr_type == 'unsigned long':
            functionName = "setUnsignedIntegralAttribute"
        else:
            functionName = "setAttribute"

        return '%s((PyDOMObject*)(self))->%s(%s, ' % \
                (castmacro, functionName, attr_name)

    def get_initial_constructor_substdict(self, constructor):
        substdict = Wrapper.get_initial_constructor_substdict(self,
                                                              constructor)
        if not constructor.caller_owns_return:
            substdict['aftercreate'] = "    g_object_ref(self->obj);\n"
        else:
            substdict['aftercreate'] = ''
        return substdict

    def get_initial_method_substdict(self, method):
        substdict = Wrapper.get_initial_method_substdict(self, method)
        substdict['cast'] = string.replace(self.objinfo.typecode,
                                           '_TYPE_', '_', 1)
        substdict.update(get_conditional_substitutions(method.orig_method))

        return substdict

    def write_default_constructor(self):
        try:
            parent = self.parser.find_object(self.objinfo.parent)
        except ValueError:
            parent = None
        if parent is not None:
            ## just like the constructor is inheritted, we should
            # inherit the new API compatibility flag
            self.objinfo.has_new_constructor_api = (
                parent.has_new_constructor_api)
        elif self.objinfo.parent == 'GObject':
            self.objinfo.has_new_constructor_api = True
        return '0'

    def write_property_based_constructor(self, constructor):
        self.objinfo.has_new_constructor_api = True
        out = self.fp
        print >> out, "static int"
        print >> out, '_wrap_%s(PyDOMObject *self, PyObject *args,' \
              ' PyObject *kwargs)\n{' % constructor.c_name
        if constructor.params:
            s = "    GType obj_type = pyg_type_from_object((PyObject *) self);"
            print >> out, s

        def py_str_list_to_c(arg):
            if arg:
                return "{" + ", ".join(
                    map(lambda s: '"' + s + '"', arg)) + ", NULL }"
            else:
                return "{ NULL }"

        classname = '%s.%s' % (self.overrides.modulename,
                               self.objinfo.name)

        if constructor.params:
            mandatory_arguments = [param for param in constructor.params
                                             if not param.optional]
            optional_arguments = [param for param in constructor.params
                                            if param.optional]
            arg_names = py_str_list_to_c(
            [param.argname
             for param in mandatory_arguments + optional_arguments])

            prop_names = py_str_list_to_c(
            [param.pname
             for param in mandatory_arguments + optional_arguments])

            print >> out, "    GParameter params[%i];" % \
                  len(constructor.params)
            print >> out, "    PyObject *parsed_args[%i] = {NULL, };" % \
                  len(constructor.params)
            print >> out, "    char *arg_names[] = %s;" % arg_names
            print >> out, "    char *prop_names[] = %s;" % prop_names
            print >> out, "    guint nparams, i;"
            print >> out
            if constructor.deprecated is not None:
                out.write(
                    '    if (PyErr_Warn(PyExc_DeprecationWarning, '
                    '"%s") < 0)\n' %
                    constructor.deprecated)
                print >> out, '        return -1;'
                print >> out
            out.write("    if (!PyArg_ParseTupleAndKeywords(args, kwargs, ")
            template = '"'
            if mandatory_arguments:
                template += "O"*len(mandatory_arguments)
            if optional_arguments:
                template += "|" + "O"*len(optional_arguments)
            template += ':%s.__init__"' % classname
            print >> out, template, ", arg_names",
            for i in range(len(constructor.params)):
                print >> out, ", &parsed_args[%i]" % i,

            out.write(
                "))\n"
                "        return -1;\n"
                "\n"
                "    memset(params, 0, sizeof(GParameter)*%i);\n"
                "    if (!pyg_parse_constructor_args(obj_type, arg_names,\n"
                "                                    prop_names, params, \n"
                "                                    &nparams, parsed_args))\n"
                "        return -1;\n"
                "    pygobject_constructv(self, nparams, params);\n"
                "    for (i = 0; i < nparams; ++i)\n"
                "        g_value_unset(&params[i].value);\n"
                % len(constructor.params))
        else:
            out.write(
                "    static char* kwlist[] = { NULL };\n"
                "\n")

            if constructor.deprecated is not None:
                out.write(
                    '    if (PyErr_Warn(PyExc_DeprecationWarning, "%s") < 0)\n'
                    '        return -1;\n'
                    '\n' % constructor.deprecated)

            out.write(
                '    if (!PyArg_ParseTupleAndKeywords(args, kwargs,\n'
                '                                     ":%s.__init__",\n'
                '                                     kwlist))\n'
                '        return -1;\n'
                '\n'
                '    pygobject_constructv(self, 0, NULL);\n' % classname)
        out.write(
            '    if (!self->obj) {\n'
            '        PyErr_SetString(\n'
            '            PyExc_RuntimeError, \n'
            '            "could not create %s object");\n'
            '        return -1;\n'
            '    }\n' % classname)

        if not constructor.caller_owns_return:
            print >> out, "    g_object_ref(self->obj);\n"

        out.write(
            '    return 0;\n'
            '}\n\n')

        return "_wrap_%s" % constructor.c_name


class GInterfaceWrapper(GObjectWrapper):
    virtual_accessor_tmpl = (
        'static PyObject *\n'
        '_wrap_%(cname)s(PyObject *cls%(extraparams)s)\n'
        '{\n'
        '    %(vtable)s *iface;\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    iface = g_type_interface_peek('
        'g_type_class_peek(pyg_type_from_object(cls)), %(typecode)s);\n'
        '    if (iface->%(virtual)s)\n'
        '        %(setreturn)siface->%(virtual)s(%(arglist)s);\n'
        '    else {\n'
        '        PyErr_SetString(PyExc_NotImplementedError, '
        '"interface method %(name)s not implemented");\n'
        '        return NULL;\n'
        '    }\n'
        '%(codeafter)s\n'
        '}\n\n'
        )

    def get_initial_class_substdict(self):
        return { 'tp_basicsize'      : 'PyObject',
                 'tp_weaklistoffset' : '0',
                 'tp_dictoffset'     : '0'}

    def write_constructor(self):
        # interfaces have no constructors ...
        return '0'
    def write_getsets(self):
        # interfaces have no fields ...
        return '0'

    def _get_class_virtual_substdict(self, meth, cname, parent):
        substdict = self.get_initial_method_substdict(meth)
        substdict['virtual'] = meth.name
        substdict['cname'] = cname
        substdict['typecode'] = self.objinfo.typecode
        substdict['vtable'] = self.objinfo.vtable
        return substdict

    def write_virtuals(self):
        ## Now write reverse method wrappers, which let python code
        ## implement interface methods.
        # First, get methods from the defs files
        klass = self.objinfo.c_name
        proxies = []
        for meth in self.parser.find_virtuals(self.objinfo):
            method_name = self.objinfo.c_name + "__proxy_do_" + meth.name
            if self.overrides.is_ignored(method_name):
                continue
            try:
                if self.overrides.is_overriden(method_name):
                    if not self.overrides.is_already_included(method_name):
                        data = self.overrides.override(method_name)
                        self.write_function(method_name, data)
                else:
                    # write proxy ...
                    ret, props = argtypes.matcher.get_reverse_ret(meth.ret)
                    wrapper = reversewrapper.ReverseWrapper(
                        '_wrap_' + method_name, is_static=True)
                    wrapper.set_return_type(ret(wrapper, **props))
                    wrapper.add_parameter(reversewrapper.PyDOMObjectMethodParam(
                        wrapper, "self", method_name="do_" + meth.name,
                        c_type=(klass + ' *')))
                    for param in meth.params:
                        handler, props = argtypes.matcher.get_reverse(
                            param.ptype)
                        props["direction"] = param.pdir
                        props["nullok"] = param.pnull
                        wrapper.add_parameter(
                            handler(wrapper, param.pname, **props))
                    buf = reversewrapper.MemoryCodeSink()
                    wrapper.generate(buf)
                    self.fp.write(buf.flush())
                proxies.append((fixname(meth.name), '_wrap_' + method_name))
                iproxies_coverage.declare_wrapped()
            except argtypes.ArgTypeError, ex:
                iproxies_coverage.declare_not_wrapped()
                proxies.append((fixname(meth.name), None))
                sys.stderr.write('Could not write interface proxy %s.%s: %s\n'
                                % (klass, meth.name, str(ex)))

        if not proxies or not [cname for name, cname in proxies if cname]:
            return

        ## Write an interface init function for this object
        funcname = "__%s__interface_init" % klass
        vtable = self.objinfo.vtable
        self.fp.write(
            '\nstatic void\n'
            '%(funcname)s(%(vtable)s *iface, PyTypeObject *pytype)\n'
            '{\n'
            '    %(vtable)s *parent_iface = '
            'g_type_interface_peek_parent(iface);\n'
            '    PyObject *py_method;\n'
            '\n'
            % vars())

        for name, cname in proxies:
            do_name = 'do_' + name
            if cname is None:
                continue

            self.fp.write((
                '    py_method = pytype? PyObject_GetAttrString('
                '(PyObject *) pytype, "%(do_name)s") : NULL;\n'
                '    if (py_method && !PyObject_TypeCheck(py_method, '
                '&PyCFunction_Type)) {\n'
                '        iface->%(name)s = %(cname)s;\n'
                '    } else {\n'
                '        PyErr_Clear();\n'
                '        if (parent_iface) {\n'
                '            iface->%(name)s = parent_iface->%(name)s;\n'
                '        }\n'
                '    Py_XDECREF(py_method);\n'
                '    }\n'
                ) % vars())
        self.fp.write('}\n\n')
        interface_info = "__%s__iinfo" % klass
        self.fp.write('''
static const GInterfaceInfo %s = {
    (GInterfaceInitFunc) %s,
    NULL,
    NULL
};
''' % (interface_info, funcname))
        self.objinfo.interface_info = interface_info

class GBoxedWrapper(Wrapper):
    constructor_tmpl = (
        'static int\n'
        '_wrap_%(cname)s(PyGBoxed *self%(extraparams)s)\n'
        '{\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    self->gtype = %(typecode)s;\n'
        '    self->free_on_dealloc = FALSE;\n'
        '    self->boxed = %(cname)s(%(arglist)s);\n'
        '%(codeafter)s\n'
        '    if (!self->boxed) {\n'
        '        PyErr_SetString(PyExc_RuntimeError, '
        '"could not create %(typename)s object");\n'
        '        return -1;\n'
        '    }\n'
        '    self->free_on_dealloc = TRUE;\n'
        '    return 0;\n'
        '}\n\n'
        )

    method_tmpl = (
        'static PyObject *\n'
        '_wrap_%(cname)s(PyObject *self%(extraparams)s)\n'
        '{\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    %(begin_allow_threads)s\n'
        '    %(setreturn)s%(cname)s(pyg_boxed_get(self, '
        '%(typename)s)%(arglist)s);\n'
        '    %(end_allow_threads)s\n'
        '%(codeafter)s\n'
        '}\n\n'
        )

    def get_initial_class_substdict(self):
        return { 'tp_basicsize'      : 'PyGBoxed',
                 'tp_weaklistoffset' : '0',
                 'tp_dictoffset'     : '0' }

    def get_field_accessor(self, fieldname):
        return 'pyg_boxed_get(self, %s)->%s' % (self.objinfo.c_name, fieldname)

    def get_initial_constructor_substdict(self, constructor):
        substdict = Wrapper.get_initial_constructor_substdict(
            self, constructor)
        substdict['typecode'] = self.objinfo.typecode
        return substdict

class GPointerWrapper(GBoxedWrapper):
    constructor_tmpl = (
        'static int\n'
        '_wrap_%(cname)s(PyGPointer *self%(extraparams)s)\n'
        '{\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    self->gtype = %(typecode)s;\n'
        '    self->pointer = %(cname)s(%(arglist)s);\n'
        '%(codeafter)s\n'
        '    if (!self->pointer) {\n'
        '        PyErr_SetString(PyExc_RuntimeError, '
        '"could not create %(typename)s object");\n'
        '        return -1;\n'
        '    }\n'
        '    return 0;\n'
        '}\n\n'
        )

    method_tmpl = (
        'static PyObject *\n'
        '_wrap_%(cname)s(PyObject *self%(extraparams)s)\n'
        '{\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    %(setreturn)s%(cname)s(pyg_pointer_get(self, '
        '%(typename)s)%(arglist)s);\n'
        '%(codeafter)s\n'
        '}\n\n'
        )

    def get_initial_class_substdict(self):
        return { 'tp_basicsize'      : 'PyGPointer',
                 'tp_weaklistoffset' : '0',
                 'tp_dictoffset'     : '0' }

    def get_field_accessor(self, fieldname):
        return 'pyg_pointer_get(self, %s)->%s' % (self.objinfo.c_name,
                                                  fieldname)

    def get_initial_constructor_substdict(self, constructor):
        substdict = Wrapper.get_initial_constructor_substdict(
            self, constructor)
        substdict['typecode'] = self.objinfo.typecode
        return substdict

class SourceWriter:

    # this is a bit odd / multi-purpose. inputs include Py_None,
    # or an already-created python-wrapped EventListener object,
    # or a callable function.  a callable function ends up being
    # stored inside the PythonEventListener
    wrapcore_eventlistener_tmpl = (
        'PyObject* toPython(WebCore::%(classname)s*);\n\n'
        'WebCore::%(classname)s *core%(classname)s(PyDOMObject* request)\n'
        '{\n'
        '    PyObject *obj = (PyObject*)request;\n'
        '    if (obj == Py_None) {\n'
        '        return NULL;\n'
        '    }\n'
        '    if (Py_TYPE((PyObject*)obj) == PtrPyDOMEventListener_Type) {\n'
        '        void *coreptr = ((PyDOMObject*)request)->ptr;\n'
        '        return static_cast<WebCore::%(classname)s*>(coreptr);\n'
        '    }\n'
        '    if (!PyCallable_Check(obj)) {\n'
        '        PyErr_SetString(PyExc_TypeError, "param must be callable");\n'
        '        return NULL;\n'
        '    }\n'
        '    return webkit_create_python_event_listener(obj);\n'
        #'    WebCore::%(classname)s *listener;\n'
        #'    listener = webkit_create_python_event_listener(obj);\n'
        #'    toPython(listener);\n'
        #'    return listener;\n'
        '}\n\n'
        )

    # this is a bit odd / multi-purpose. inputs include Py_None,
    # or an already-created python-wrapped ScheduledAction object,
    # or a callable function.  a callable function ends up being
    # stored inside the PythonEventListener
    wrapcore_scheduledaction_tmpl = (
        'PyObject* toPython(WebCore::%(classname)s*);\n\n'
        'WebCore::%(classname)s *core%(classname)s(PyDOMObject* request)\n'
        '{\n'
        '    PyObject *obj = (PyObject*)request;\n'
        '    if (obj == Py_None) {\n'
        '        return NULL;\n'
        '    }\n'
        '    if (Py_TYPE((PyObject*)obj) == PtrPyDOMScheduledAction_Type) {\n'
        '        void *coreptr = ((PyDOMObject*)request)->ptr;\n'
        '        return static_cast<WebCore::%(classname)s*>(coreptr);\n'
        '    }\n'
        '    if (!PyCallable_Check(obj)) {\n'
        '        PyErr_SetString(PyExc_TypeError, "param must be callable");\n'
        '        return NULL;\n'
        '    }\n'
        '    return webkit_create_python_scheduled_action(obj);\n'
        '}\n\n'
        )

    wrapcore_tmpl = (
        'WebCore::%(classname)s *core%(classname)s(PyDOMObject* request)\n'
        '{\n'
        '    void *coreptr = ((PyDOMObject*)request)->ptr;\n'
        '    return static_cast<WebCore::%(classname)s*>(coreptr);\n'
        '}\n\n'
        )

    wrapnode_tmpl = (
        'PyObject* pywrap%(classname)s(WebCore::%(classname)s* coreObject)\n'
        '{\n'
        '    void *coreptr = (static_cast<void*>(coreObject));\n'
        '    coreObject->ref();\n'
        '    return PyDOMObject_new(PtrPyDOM%(classname)s_Type, coreptr);\n'
        '}\n\n'
        )

    topython_tmpl = \
"""\
PyObject* toPython(WebCore::%(classname)s* obj)
{
    if (!obj)
        Py_RETURN_NONE;

    if (PyObject* ret = PythonObjectCache::getDOMObject(obj))
        return ret;

    return PythonObjectCache::putDOMObject(obj, WebKit::pywrap%(classname)s(obj));
}
"""
    
    topython_manual_tmpl = (
        'PyObject* toPython(WebCore::%(classname)s*);\n'
        )

    def __init__(self, parser, overrides, prefix, fp=FileOutput(sys.stdout)):
        self.parser = parser
        self.overrides = overrides
        self.prefix = prefix
        self.fp = fp

    def write(self, py_ssize_t_clean=False):
        argtypes.py_ssize_t_clean = py_ssize_t_clean

        self.write_headers(py_ssize_t_clean)
        self.include_types = self.get_class_include_types()
        self.write_imports()
        self.write_type_declarations()
        self.write_body()
        self.write_class_wrappers()
        self.write_classes()

        wrapper = Wrapper(self.parser, None, self.overrides, self.fp)
        wrapper.write_functions(self, self.prefix)

        if not self.overrides.dynamicnamespace:
            self.write_enums()
        self.fp.write('extern "C" {\n\n')
        self.write_extension_init()
        self.write_registers()
        self.fp.write("""

PyObject *toPythonFromDocumentPtr(gpointer ptr)
{
    WebCore::Document *doc = static_cast<WebCore::Document*>(ptr);
    return WebKit::toPython(doc);
}

PyObject *toPythonFromDOMWindowPtr(gpointer ptr)
{
    WebCore::DOMWindow *win = static_cast<WebCore::DOMWindow*>(ptr);
    return WebKit::toPython(win);
}

PyObject *toPythonFromXMLHttpRequestPtr(gpointer ptr)
{
    WebCore::XMLHttpRequest *xhr = static_cast<WebCore::XMLHttpRequest*>(ptr);
    return WebKit::toPython(xhr);
}

void webkit_init_pywebkit(PyObject *m, struct pyjoinapi *fns)
{
    fns->xhr = toPythonFromXMLHttpRequestPtr;
    fns->doc = toPythonFromDocumentPtr;
    fns->win = toPythonFromDOMWindowPtr;

    typedeclpywebkit();
    registerpywebkit(m);

    if (PyErr_Occurred ()) {
        PyErr_Print();
        Py_FatalError ("can't initialise module pywebkit.so");
    }
}
""")
        self.fp.write('}; // extern "C"\n')
        argtypes.py_ssize_t_clean = False

    def write_headers(self, py_ssize_t_clean):
        self.fp.write('/* -- THIS FILE IS GENERATED - DO NOT EDIT */')
        self.fp.write('/* -*- Mode: C; c-basic-offset: 4 -*- */\n\n')
        
        if py_ssize_t_clean:
            self.fp.write('#define PY_SSIZE_T_CLEAN\n')
        self.fp.write('#include <Python.h>\n')
        self.fp.write('#include "config.h"\n\n\n')
        self.fp.write('#include "HTMLNames.h"\n\n\n')
        self.fp.write('#include "KURL.h"\n\n\n')
        self.fp.write('#include "PlatformString.h"\n\n\n')
        self.fp.write('#include "PythonBinding.h"\n\n\n')
        self.fp.write('#include "pywebkit.h"\n\n\n')
        self.fp.write('#include <wtf/text/CString.h>\n\n\n')
        self.fp.write('#include <wtf/Forward.h>\n\n\n')
        self.fp.write("""\
char* cpUTF8(WTF::String const& s) { return strdup((s.utf8().data())); }
char* cpUTF8(WebCore::KURL const& s) { return strdup((s.string().utf8().data())); }
""")

        if py_ssize_t_clean:
            self.fp.write('''

#if PY_VERSION_HEX < 0x02050000
typedef int Py_ssize_t;
#define PY_SSIZE_T_MAX INT_MAX
#define PY_SSIZE_T_MIN INT_MIN
typedef inquiry lenfunc;
typedef intargfunc ssizeargfunc;
typedef intobjargproc ssizeobjargproc;
#endif

''')
        self.fp.write(self.overrides.get_headers())
        self.fp.resetline()
        self.fp.write('\n\n')

    def write_imports(self):
        self.fp.write('/* ---------- types from other modules ---------- */\n')
        for module, pyname, cname, importing_for in self.overrides.get_imports():
            if importing_for is None or is_registered_object(importing_for):
                self.fp.write('static PyTypeObject *_%s;\n' % cname)
                self.fp.write('#define %s (*_%s)\n' % (cname, cname))
        self.fp.write('\n\n')

    def write_class_wrappers(self):
        self.fp.write('/* ---------- class wrappers ---------- */\n')
        self.fp.write('namespace WebKit {\n')
        self.fp.write('using namespace WebCore;\n')
        self.fp.write('\n')
        
        for obj in self.parser.objects:
            cond = get_conditional_substitutions(obj.orig_obj.attributes)
            substdict = {'classname': obj.c_name}
            
            self.fp.write(cond['conditional_if'])
            
            if not self.overrides.is_type_ignored(obj.c_name):
                txt = self.wrapnode_tmpl % {'classname': obj.c_name}
                self.fp.write(txt)
                if obj.c_name == 'ScheduledActionBase':
                    tmpl = self.wrapcore_scheduledaction_tmpl 
                elif obj.c_name == 'EventListener':
                    tmpl = self.wrapcore_eventlistener_tmpl 
                else:
                    tmpl = self.wrapcore_tmpl

                
                self.fp.write(tmpl % substdict)
            
            if obj.c_name not in \
                    ["Node", "Document", "HTMLCollection", "SVGPathSeg",
                     "StyleSheet", "CSSRule", "CSSValue", "Object", "Event",
                     "Element", "Text", "EventTarget"]:
                tmpl = self.topython_tmpl
            else:
                tmpl = self.topython_manual_tmpl
            
            self.fp.write("#define PyDOM%s PyDOMObject\n" % obj.c_name)
            self.fp.write(tmpl % substdict)

            self.fp.write(cond['conditional_endif'])
            self.fp.write('\n')

        self.fp.write('} // namespace WebKit\n')
        self.fp.write('\n')

    def write_type_declarations(self):
        #todo use 'static' if used only in one file
        self.fp.write('/* ---------- includes ---------- */\n')
        for obj in self.parser.objects:
            if not self.overrides.is_type_ignored(obj.c_name):
                self.fp.write('#include "%s.h"\n' % obj.c_name)
        self.fp.write('\n')

        self.fp.write('/* ---------- forward type declarations ---------- */\n')
        self.fp.write('extern "C" {\n\n')

        for obj in self.parser.boxes:
            if not self.overrides.is_type_ignored(obj.c_name):
                cond = get_conditional_substitutions(obj.orig_obj.attributes)
                self.fp.write(cond['conditional_if'])
                self.fp.write('PyTypeObject *PtrPy' + obj.c_name + '_Type;\n')
                self.fp.write(cond['conditional_endif'])
        
        for obj in self.parser.objects:
            if not self.overrides.is_type_ignored(obj.c_name):
                cond = get_conditional_substitutions(obj.orig_obj.attributes)
                self.fp.write(cond['conditional_if'])
                self.fp.write('PyTypeObject *PtrPyDOM' + obj.c_name + '_Type;\n')
                self.fp.write(cond['conditional_endif'])
        
        for interface in self.parser.interfaces:
            if not self.overrides.is_type_ignored(interface.c_name):
                self.fp.write('PyTypeObject *PtrPy' + interface.c_name + '_Type;\n')
        
        self.fp.write('\n')
        self.fp.write('}; // extern "C"\n')

    def write_body(self):
        self.fp.write(self.overrides.get_body())
        self.fp.resetline()
        self.fp.write('\n\n')

    def _sort_parent_children(self, objects):
        objects = list(objects)
        modified = True
        while modified:
            modified = False
            parent_index = None
            child_index = None
            for i, obj in enumerate(objects):
                if obj.parent == 'GObject':
                    continue
                if obj.parent not in [info.c_name for info in objects[:i]]:
                    for j, info in enumerate(objects[i+1:]):
                        if info.c_name == obj.parent:
                            parent_index = i + 1 + j
                            child_index = i
                            break
                    else:
                        continue
                    break
            if child_index is not None and parent_index is not None:
                if child_index != parent_index:
                    objects.insert(child_index, objects.pop(parent_index))
                    modified = True
        return objects

    def get_class_include_types(self):
        ## Sort the objects, so that we generate code for the parent types
        ## before their children.
        objects = self._sort_parent_children(self.parser.objects)
        include_types = set()

        for klass, items in ((GBoxedWrapper, self.parser.boxes),
                             (GPointerWrapper, self.parser.pointers),
                             (GObjectWrapper, objects),
                             (GInterfaceWrapper, self.parser.interfaces)):
            for item in items:
                instance = klass(self.parser, item, self.overrides, self.fp)
                include_types.update(instance.find_include_ptypes())
        return include_types

    def write_classes(self):
        ## Sort the objects, so that we generate code for the parent types
        ## before their children.
        objects = self._sort_parent_children(self.parser.objects)
        include_types = set()

        for klass, items in ((GBoxedWrapper, self.parser.boxes),
                             (GPointerWrapper, self.parser.pointers),
                             (GObjectWrapper, objects),
                             (GInterfaceWrapper, self.parser.interfaces)):
            for item in items:
                instance = klass(self.parser, item, self.overrides, self.fp)
                include_types.update(instance.find_include_ptypes())
                instance.prefix = self.prefix
                instance.write_class()
                self.fp.write('\n')

    def get_enums(self):
        enums = []
        for enum in self.parser.enums:
            if self.overrides.is_type_ignored(enum.c_name):
                continue
            enums.append(enum)
        return enums

    def write_enums(self):
        if not self.parser.enums:
            return

        self.fp.write('\n/* ----------- enums and flags ----------- */\n\n')
        self.fp.write(
            'void\n' + self.prefix +
            '_add_constants(PyObject *module, const gchar *strip_prefix)\n{\n')

        self.fp.write(
            '#ifdef VERSION\n'
            '    PyModule_AddStringConstant(module, "__version__", VERSION);\n'
            '#endif\n')

        for enum in self.get_enums():
            if enum.typecode is None:
                for nick, value in enum.values:
                    self.fp.write(
                        '    PyModule_AddIntConstant(module, '
                        '(char *) pyg_constant_strip_prefix("%s", strip_prefix), %s);\n'
                        % (value, value))
            else:
                if enum.deftype == 'enum':
                    self.fp.write('  pyg_enum_add(module, "%s", strip_prefix, %s);\n'
                                  % (enum.name, enum.typecode))
                else:
                    self.fp.write('  pyg_flags_add(module, "%s", strip_prefix, %s);\n'
                                  % (enum.name, enum.typecode))

        self.fp.write('\n')
        self.fp.write('  if (PyErr_Occurred())\n')
        self.fp.write('    PyErr_Print();\n')
        self.fp.write('}\n\n')

    def write_object_imports(self, retval=''):
        imports = self.overrides.get_imports()[:]
        if not imports:
            return

        bymod = {}
        for module, pyname, cname, importing_for in imports:
            if importing_for is None or is_registered_object(importing_for):
                bymod.setdefault(module, []).append((pyname, cname))
        self.fp.write('    PyObject *module;\n\n')
        for module in bymod:
            self.fp.write(
                '    if ((module = PyImport_ImportModule("%s")) != NULL) {\n'
                % module)
            #self.fp.write(
            #    '        PyObject *moddict = PyModule_GetDict(module);\n\n')
            for pyname, cname in bymod[module]:
                #self.fp.write(
                #    '        _%s = (PyTypeObject *)PyDict_GetItemString('
                #    'moddict, "%s");\n' % (cname, pyname))
                self.fp.write(
                    '        _%s = (PyTypeObject *)PyObject_GetAttrString('
                    'module, "%s");\n' % (cname, pyname))
                self.fp.write('        if (_%s == NULL) {\n' % cname)
                self.fp.write('            PyErr_SetString(PyExc_ImportError,\n')
                self.fp.write('                "cannot import name %s from %s");\n'
                         % (pyname, module))
                self.fp.write('            return %s;\n' % retval)
                self.fp.write('        }\n')
            self.fp.write('    } else {\n')
            self.fp.write('        PyErr_SetString(PyExc_ImportError,\n')
            self.fp.write('            "could not import %s");\n' % module)
            self.fp.write('        return %s;\n' % retval)
            self.fp.write('    }\n')
        self.fp.write('\n')

    def write_extension_init(self):
        self.fp.write('/* initialise stuff extension classes */\n')
        self.fp.write('void typedecl%s(void)\n' % self.prefix)
        self.fp.write('{\n')
        self.fp.write('    if (PyType_Ready(&PyDOMObject_Type) < 0) return;\n')
        self.fp.write('\n')
        self.write_object_imports()
        for obj, bases in self.get_classes():
            self.write_class_base_link(obj, bases)
        self.fp.write('}\n\n')
        self.fp.write('void register%s(PyObject *m)\n' % self.prefix)
        self.fp.write('{\n')
        self.fp.write(self.overrides.get_init() + '\n')
        self.fp.resetline()

    def get_classes(self):
        objects = self.parser.objects[:]
        pos = 0
        while pos < len(objects):
            parent = objects[pos].parent
            for i in range(pos+1, len(objects)):
                if objects[i].c_name == parent:
                    objects.insert(i+1, objects[pos])
                    del objects[pos]
                    break
            else:
                pos = pos + 1

        retval = []
        for obj in objects:
            if self.overrides.is_type_ignored(obj.c_name):
                continue
            bases = []
            if obj.parent != None:
                bases.append(obj.parent)
            bases = bases + obj.implements
            retval.append((obj, bases))

        return retval

    def write_registers(self):
        for boxed in self.parser.boxes:
            if not self.overrides.is_type_ignored(boxed.c_name):
                self.fp.write('    pyg_register_boxed(d, "' + boxed.name +
                              '", ' + boxed.typecode +
                              ', &Py' + boxed.c_name +
                          '_Type);\n')
        for pointer in self.parser.pointers:
            if not self.overrides.is_type_ignored(pointer.c_name):
                self.fp.write('    pyg_register_pointer(d, "' + pointer.name +
                              '", ' + pointer.typecode +
                              ', &Py' + pointer.c_name + '_Type);\n')
        for interface in self.parser.interfaces:
            if not self.overrides.is_type_ignored(interface.c_name):
                self.fp.write('    pyg_register_interface(d, "'
                              + interface.name + '", '+ interface.typecode
                              + ', &Py' + interface.c_name + '_Type);\n')
                if interface.interface_info is not None:
                    self.fp.write('    pyg_register_interface_info(%s, &%s);\n' %
                                  (interface.typecode, interface.interface_info))

        if not self.overrides.dynamicnamespace:
            for obj, bases in self.get_classes():
                self.write_class(obj, bases)
        else:
            for obj, bases in self.get_classes():
                self.fp.write(
                    '    pyg_type_register_custom_callback("%s", '
                    '(PyGTypeRegistrationFunction)%s_register_type, d);\n' %
                    (obj.c_name, obj.c_name))

        self.fp.write('}\n')

    def _can_direct_ref(self, base):
        if not self.overrides.dynamicnamespace:
            return True
        if base == 'GObject':
            return True
        obj = get_object_by_name(base)
        if obj.module.lower() != self.overrides.modulename:
            return True
        return False

    def write_class_base_link(self, obj, bases, indent=1):
        indent_str = ' ' * (indent * 4)
        if not bases or bases[0] == 'DOMObject':
            bases_str = 'PyDOMObject_Type'
        else:
            bases_str = 'PyDOM%s_Type' % bases[0]

        self.fp.write("%sPtrPyDOM%s_Type = &PyDOM%s_Type;\n" % \
                    (indent_str, obj.c_name, obj.c_name))
        self.fp.write("%sPyDOM%s_Type.tp_base = &%s;\n" % \
                    (indent_str, obj.c_name, bases_str))
        self.fp.write("%sif (PyType_Ready(&PyDOM%s_Type) < 0) {\n" % \
                      (indent_str, obj.c_name))
        self.fp.write("%s    return;\n" % indent_str)
        self.fp.write("%s}\n" % indent_str)

    def write_class(self, obj, bases, indent=1):
        indent_str = ' ' * (indent * 4)
        if bases:
            bases_str = 'Py_BuildValue("(%s)"' % (len(bases) * 'O')

            for base in bases:
                if self._can_direct_ref(base):
                    bases_str += ', &PyDOM%s_Type' % base
                else:
                    baseobj = get_object_by_name(base)
                    bases_str += ', PyObject_GetAttrString(m, "%s")' % baseobj.name
            bases_str += ')'
        else:
            bases_str = 'NULL'

        self.fp.write('%(indent)sPy_INCREF(&PyDOM%(c_name)s_Type);\n'
                % dict(indent=indent_str, c_name=obj.c_name))
        self.fp.write(
                '%(indent)sPyModule_AddObject(m, "%(c_name)s", (PyObject*) &PyDOM%(c_name)s_Type);\n'
                % dict(indent=indent_str, c_name=obj.c_name,
                       py_name=self.prefix))

        if obj.class_init_func is not None:
            self.fp.write(
                indent_str + 'pyg_register_class_init(%s, %s);\n' %
                (obj.typecode, obj.class_init_func))

_objects = {}

def is_registered_object(c_name):
    return c_name in _objects

def get_object_by_name(c_name):
    global _objects
    return _objects[c_name]

def register_types(parser):
    global _objects
    for boxed in parser.boxes:
        argtypes.matcher.register_boxed(boxed.c_name, boxed.typecode)
        _objects[boxed.c_name] = boxed
    for pointer in parser.pointers:
        argtypes.matcher.register_pointer(pointer.c_name, pointer.typecode)
    for obj in parser.objects:
        argtypes.matcher.register_object(obj.c_name, obj.parent, obj.typecode)
        _objects[obj.c_name] = obj
    for iface in parser.interfaces:
        argtypes.matcher.register_object(iface.c_name, None, iface.typecode)
        _objects[iface.c_name] = iface
    for enum in parser.enums:
        if enum.deftype == 'flags':
            argtypes.matcher.register_flag(enum.c_name, enum.typecode)
        else:
            argtypes.matcher.register_enum(enum.c_name, enum.typecode)

def get_conditional_substitutions(member):
    ret = {"conditional_if": "", "conditional_endif": ""}
    
    cond = get_conditional_string(member)
    if cond is None:
        return ret

    ret['conditional_if'] = "#if {0}\n".format(cond)
    ret['conditional_endif'] = "#endif //{0}\n".format(cond)
        
    return ret

def get_conditional_string(member):
    cond = get_conditional(member)
    if cond is None:
        return None
    
    if cond.find('&') != -1:
        vals = cond.split('&')
        return "ENABLE({)}) && ENABLE({1})".format(vals[0], vals[1])
    elif cond.find('|') != -1:
        vals = cond.split('|')
        return "ENABLE({)}) || ENABLE({1})".format(vals[0], vals[1])
    
    return "ENABLE({0})".format(cond)

def get_conditional(member):
    if member.attributes.has_key('Conditional'):
        val = member.attributes['Conditional'][0]
        return val[0]

    return None

usage = 'usage: codegen.py [-o overridesfile] [-p prefix] defsfile'
def main(argv):
    o = override.Overrides()
    prefix = 'pygtk'
    outfilename = None
    errorfilename = None
    opts, args = getopt.getopt(argv[1:], "o:p:r:t:D:I:",
                        ["override=", "prefix=", "register=", "outfilename=",
                         "load-types=", "errorfilename=", "py_ssize_t-clean"])
    defines = {} # -Dkey[=val] options
    py_ssize_t_clean = False
    for opt, arg in opts:
        if opt in ('-o', '--override'):
            o = override.Overrides(arg)
        elif opt in ('-p', '--prefix'):
            prefix = arg
        elif opt in ('-r', '--register'):
            # Warning: user has to make sure all -D options appear before -r
            p = defsparser.DefsParser(arg, defines)
            p.startParsing()
            register_types(p)
            del p
        elif opt == '--outfilename':
            outfilename = arg
        elif opt == '--errorfilename':
            errorfilename = arg
        elif opt in ('-t', '--load-types'):
            globals = {}
            execfile(arg, globals)
        elif opt == '-D':
            nameval = arg.split('=')
            try:
                defines[nameval[0]] = nameval[1]
            except IndexError:
                defines[nameval[0]] = None
        elif opt == '-I':
            defsparser.include_path.insert(0, arg)
        elif opt == '--py_ssize_t-clean':
            py_ssize_t_clean = True
    if len(args) < 1:
        print >> sys.stderr, usage
        return 1
    if errorfilename:
        sys.stderr = open(errorfilename, "w")
    p = defsparser.DefsParser(args[0], defines)
    if not outfilename:
        outfilename = os.path.splitext(args[0])[0] + '.cpp'

    p.startParsing()

    register_types(p)
    sw = SourceWriter(p, o, prefix, FileOutput(sys.stdout, outfilename))
    sw.write(py_ssize_t_clean)

    functions_coverage.printstats()
    methods_coverage.printstats()
    vproxies_coverage.printstats()
    vaccessors_coverage.printstats()
    iproxies_coverage.printstats()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
