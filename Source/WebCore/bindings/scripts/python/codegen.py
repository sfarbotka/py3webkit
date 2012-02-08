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
import warnings

def startreplace(fieldname, opts):
    for (opt, replace) in opts:
        if fieldname.startswith(opt):
            return replace+fieldname[3:]
    return fieldname
    
def fixname(name):
    if keyword.iskeyword(name):
        return name + '_'
    return name

_objects = {}

def is_registered_object(c_name):
    return c_name in _objects

def get_object_by_name(c_name):
    global _objects
    return _objects[c_name]

def register_types(parser):
    global _objects
    for obj in parser.objects:
        argtypes.matcher.register_object(obj.c_name, obj.parent, obj.typecode)
        _objects[obj.c_name] = obj

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
        return "ENABLE({}) && ENABLE({})".format(vals[0], vals[1])
    elif cond.find('|') != -1:
        vals = cond.split('|')
        return "ENABLE({}) || ENABLE({})".format(vals[0], vals[1])

    return "ENABLE({0})".format(cond)

def get_conditional(member):
    if member.attributes.has_key('Conditional'):
        val = member.attributes['Conditional'][0]
        return val[0]

    return None


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

    method_not_implemented_tmpl = (
        'static PyObject*\n'
        '%(funcname)s(PyDOMObject *self, PyObject *args, PyObject *kwargs)\n'
        '{\n'
        '    // TODO Implement method\n'
        '    PyErr_SetString(PyExc_NotImplementedError, \n'
        '            "Custom method %(klass)s.%(method)s is not implemented yet");\n'
        '    return NULL;\n'
        '}\n\n'
        )
    # template for method calls
    method_tmpl = None

    def __init__(self, parser, objinfo, fp=FileOutput(sys.stdout)):
        self.parser = parser
        self.objinfo = objinfo
        self.fp = fp
        self._implemented_custom_methods = []

    def get_lower_name(self):
        return string.lower(string.replace(self.objinfo.typecode,
                                           '_TYPE_', '_', 1))

    def get_field_accessor(self, fieldname):
        raise NotImplementedError

    def get_initial_class_substdict(self):
        return {}

    def get_initial_method_substdict(self, method):
        substdict = { 'name': '%s.%s' % (self.objinfo.py_name, method.name) }
        return substdict

    def write_class(self):
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
        substdict['classname'] = '%s.%s' % (self.prefix, self.objinfo.name)
        substdict['tp_doc'] = self.objinfo.docstring
        substdict['tp_init'] = self.write_constructor()
        substdict['tp_methods'] = self.write_methods()
        substdict['tp_getset'] = self.write_getsets()
        substdict['tp_dealloc'] = self.write_dealloc()
        substdict['tp_new'] = 'DOMObject_new'
        substdict['tp_iter'] = self.write_iter()
        substdict['tp_iternext'] = self.write_iternext()
        substdict['tp_as_sequence'] = self.write_sequence()


        # handle slots ...
        for slot in self.slots_list:

            slotname = '%s.%s' % (self.objinfo.c_name, slot)
            slotfunc = '_wrap_%s_%s' % (self.get_lower_name(), slot)
            if slot[:6] == 'tp_as_':
                slotfunc = '&' + slotfunc
            if not substdict.has_key(slot):
                substdict[slot] = '0'

        self.fp.write('} // namespace WebKit\n')

        self.fp.write('extern "C" {\n\n')
        self.fp.write(self.type_tmpl % substdict)
        self.fp.write('}; // extern "C"\n')

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

    def get_methflags(self, funcname):
        return 'METH_VARARGS|METH_CLASS'

    def write_function(self, funcname, data):
        self.fp.write(data)
        self.fp.write('\n\n')

    def find_include_ptypes(self):
        includes = set()
        klass = self.objinfo.c_name
        # First, get methods from the defs files
        for meth in self.parser.find_methods(self.objinfo):
            method_name = meth.c_name
            includes.update(self.find_function_ptypes(meth, handle_return=1))
        return includes

    def write_methods(self):
        methods = []
        klass = self.objinfo.c_name
        # First, get methods from the defs files
        for meth in self.parser.find_methods(self.objinfo):
            method_name = meth.c_name

            if method_name in self._implemented_custom_methods:
                continue

            if meth.requires_custom_implementation:
                self._implemented_custom_methods.append(method_name)

                methflags = 'METH_VARARGS|METH_KEYWORDS'

                if meth.implemented:
                    funcname = '_wrap_%s_%s' % (klass, method_name)
                    code = 'PyObject* _wrap_%s_%s(PyDOMObject *self, PyObject *args, PyObject *kwargs);\n\n' % (
                            klass, method_name)
                    self.fp.write(code)

                else:
                    substdict = {}
                    substdict['funcname'] = '_wrap_%s_%s' % (klass, method_name)
                    substdict['klass'] = klass
                    substdict['method'] = method_name

                    self.fp.write(self.method_not_implemented_tmpl % substdict)
            else:
                try:
                    # write constructor from template ...
                    code, methflags = self.write_function_wrapper(meth,
                        self.method_tmpl, handle_return=1, is_method=1,
                        substdict=self.get_initial_method_substdict(meth),
                        exception_needed=meth.raises)
                    self.fp.write(code)

                except argtypes.ArgTypeError, ex:
                    traceback.print_exc()
                    sys.stderr.write('declaration of type needed %s.%s: %s\n'
                                    % (klass, meth.name, ex))
                    continue

            methods.append(self.methdef_tmpl %
                           { 'name':  fixname(meth.name),
                             'cname': 'WebKit::_wrap_%s_%s' % (klass, method_name),
                             'flags': methflags,
                             'docstring': meth.docstring })


        if methods:
            self.fp.write('} // namespace WebKit\n\n')
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

    def write_sequence(self):
        return "0"

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


class ObjectWrapper(Wrapper):
    method_tmpl = (
        '%(conditional_if)s'
        'static PyObject *\n'
        '_wrap_%(typename)s_%(cname)s(PyDOMObject *self%(extraparams)s)\n'
        '{\n'
        '%(varlist)s'
        '%(parseargs)s'
        '%(codebefore)s'
        '    %(setreturn)s%(cast)s(self)->%(cname)s(%(arglist)s);\n'
        '%(codeafter)s\n'
        '}\n'
        '%(conditional_endif)s\n'
        )

    def __init__(self, parser, objinfo, fp=FileOutput(sys.stdout)):
        Wrapper.__init__(self, parser, objinfo, fp)
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

    def write_sequence(self):
        if not self.is_iterator():
            return "0"

        lower_name = self.get_lower_name()
        sequence_name = lower_name + '_sequence'

        lenfname = self.write_sequence_len()
        getitemfname = self.write_sequence_getitem()

        len_name = 'WebKit::' + lenfname
        getitem_name = 'WebKit::' + getitemfname


        tmpl = (
        'extern "C"\n'
        '{\n'
        'static PySequenceMethods %(sequence_name)s =\n'
        '{\n'
        '    (lenfunc)%(len_name)s,\n'
        '    (binaryfunc)0,\n'
        '    (ssizeargfunc)0,\n'
        '    (ssizeargfunc)%(getitem_name)s,\n'
        '    (void*)0,\n'
        '    (ssizeobjargproc)0,\n'
        '    (void*)0,\n'
        '    (objobjproc)0,\n'
        '    (binaryfunc)0,\n'
        '    (ssizeargfunc)0\n'
        '};\n'
        '}; // extern "C"\n\n'
        )

        substdict = {}
        substdict['sequence_name'] = sequence_name
        substdict['len_name'] = len_name
        substdict['getitem_name'] = getitem_name

        self.fp.write('} // namespace WebKit\n\n')
        self.fp.write(tmpl % substdict)
        self.fp.write('namespace WebKit {\n')
        self.fp.write('using namespace WebCore;\n')

        return '&' + sequence_name

    def write_sequence_len(self):
        lower_name = self.get_lower_name()
        fname = '_sequence_' + lower_name + '__len'

        tmpl = (
        'static Py_ssize_t\n'
        '%(fname)s(PyDOMObject* self)\n'
        '{\n'
        '    unsigned long len = %(cast)s(self)->length();\n'
        '    return (Py_ssize_t)len;\n'
        '}\n\n'
        )

        substdict = {}
        substdict['fname'] = fname
        substdict['cast'] = string.replace(self.objinfo.typecode, '_TYPE_', '_', 1)

        self.fp.write(tmpl % substdict)

        return fname

    def write_sequence_getitem(self):
        lower_name = self.get_lower_name()
        fname = '_sequence_' + lower_name + '__getitem'

        tmpl = (
        'static PyObject* \n'
        '%(fname)s(PyDOMObject* self, Py_ssize_t index)\n'
        '{\n'
        '    unsigned long len = %(cast)s(self)->length();\n'
        '    if ((index < 0) || ((unsigned long)index >= len))\n'
        '    {\n'
        '        PyErr_SetString(PyExc_IndexError, "Index out of range");\n'
        '        return NULL;\n'
        '    }\n\n'
        '    PyObject* args = Py_BuildValue("(k)", index);\n'
        '    PyObject* kwargs = PyDict_New();\n\n'
        '    PyObject* ret = _wrap_%(typename)s_%(cname)s(self, args, kwargs);\n\n'
        '    Py_DECREF(args);\n'
        '    Py_DECREF(kwargs);\n\n'
        '    return ret;\n'
        '}\n\n'
        )

        m = self.get_iter_method()

        substdict = {}
        substdict['typename'] = self.objinfo.c_name
        substdict['cname'] = m.c_name
        substdict['fname'] = fname
        substdict['cast'] = string.replace(self.objinfo.typecode, '_TYPE_', '_', 1)

        self.fp.write(tmpl % substdict)

        return fname

    def write_iter(self):
        if not self.is_iterator():
            return "0"
        
        tmpl = ( 
        'static PyObject* \n'
        '%(typename)s_iter(PyDOMObject* self)\n'
        '{\n'
        '   self->iter_index = 0;\n'
        '   self->iter_count = %(cast)s(self)->length();\n'
        '   Py_INCREF(self);\n'
        '   return (PyObject*)self;\n'
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
        'static PyObject* \n'
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
        '    PyObject* ret = _wrap_%(typename)s_%(cname)s(self, args, kwargs);\n\n'
        '    Py_DECREF(args);\n'
        '    Py_DECREF(kwargs);\n\n'
        '    return ret;\n'
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

        for meth in self.parser.find_methods(self.objinfo):
            if meth.name != 'item':
                continue

            if meth.requires_custom_implementation:
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

    def get_initial_method_substdict(self, method):
        substdict = Wrapper.get_initial_method_substdict(self, method)
        substdict['cast'] = string.replace(self.objinfo.typecode,
                                           '_TYPE_', '_', 1)
        substdict.update(get_conditional_substitutions(method.orig_method))

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

    def __init__(self, parser, prefix, fp=FileOutput(sys.stdout)):
        self.parser = parser
        self.prefix = prefix
        self.fp = fp

    def write(self, py_ssize_t_clean=False):
        argtypes.py_ssize_t_clean = py_ssize_t_clean

        self.write_headers(py_ssize_t_clean)
        self.include_types = self.get_class_include_types()
        self.write_type_declarations()
        self.write_body()
        self.write_class_wrappers()
        self.write_classes()

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
        self.fp.write('#include <Python.h>\n\n')
        self.fp.write('#include "config.h"\n\n')
        self.fp.write('#include <wtf/text/CString.h>\n')
        self.fp.write('#include <wtf/Forward.h>\n\n')
        self.fp.write('#include "HTMLNames.h"\n')
        self.fp.write('#include "KURL.h"\n')
        self.fp.write('#include "PlatformString.h"\n\n')
        self.fp.write('#include "PythonBinding.h"\n')
        self.fp.write('#include "pywebkit.h"\n')
        self.fp.write('#include "PyDOMObject.h"\n')
        self.fp.write('#include "PyScheduledAction.h"\n')
        self.fp.write('#include "PythonEventListener.h"\n\n\n')
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
            self.fp.write('#include "%s.h"\n' % obj.c_name)
        self.fp.write('\n')

        self.fp.write('/* ---------- forward type declarations ---------- */\n')
        self.fp.write('extern "C" {\n\n')

        for obj in self.parser.objects:
            cond = get_conditional_substitutions(obj.orig_obj.attributes)
            self.fp.write(cond['conditional_if'])
            self.fp.write('PyTypeObject *PtrPyDOM' + obj.c_name + '_Type;\n')
            self.fp.write(cond['conditional_endif'])
        
        self.fp.write('\n')
        self.fp.write('}; // extern "C"\n')

    def write_body(self):
        self.fp.write('\n')
        self.fp.write('void py_wk_exc(WebCore::ExceptionCode &ec)\n')
        self.fp.write('{\n')
        self.fp.write('    WebCore::ExceptionCodeDescription ecdesc(ec);\n')
        self.fp.write('    PyErr_SetString(PyExc_Exception, ecdesc.name);\n')
        self.fp.write('}\n\n')

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

        for obj in objects:
            instance = ObjectWrapper(self.parser, obj, self.fp)
            include_types.update(instance.find_include_ptypes())
        return include_types

    def write_classes(self):
        ## Sort the objects, so that we generate code for the parent types
        ## before their children.
        objects = self._sort_parent_children(self.parser.objects)
        include_types = set()

        for obj in objects:
            instance = ObjectWrapper(self.parser, obj, self.fp)
            include_types.update(instance.find_include_ptypes())
            instance.prefix = self.prefix
            instance.write_class()
            self.fp.write('\n')

    def write_extension_init(self):
        self.fp.write('/* initialise stuff extension classes */\n')
        self.fp.write('void typedecl%s(void)\n' % self.prefix)
        self.fp.write('{\n')
        self.fp.write('    if (PyType_Ready(&PyDOMObject_Type) < 0) return;\n')
        self.fp.write('\n')
        for obj, bases in self.get_classes():
            cond = get_conditional_substitutions(obj.orig_obj.attributes)
            self.fp.write(cond['conditional_if'])
            self.write_class_base_link(obj, bases)
            self.fp.write(cond['conditional_endif'])
        self.fp.write('}\n\n')
        self.fp.write('void register%s(PyObject *m)\n' % self.prefix)
        self.fp.write('{\n')
        self.fp.write('    Py_INCREF(&PyDOMObject_Type);\n')
        self.fp.write('    PyModule_AddObject(m, "DOMObject", (PyObject *) &PyDOMObject_Type);\n')
        self.fp.write('\n')
        self.fp.write('    PtrPyPyScheduledAction_Type = &PyPyScheduledAction_Type;\n')
        self.fp.write('    PyPyScheduledAction_Type.tp_base = &PyDOMObject_Type;\n')
        self.fp.write('    if (PyType_Ready(&PyPyScheduledAction_Type) < 0)\n')
        self.fp.write('        return;\n')
        self.fp.write('\n')
        self.fp.write('    Py_INCREF(&PyPyScheduledAction_Type);\n')
        self.fp.write('    PyModule_AddObject(m, "ScheduledAction", (PyObject*) &PyPyScheduledAction_Type);\n')
        self.fp.write('\n')

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
            bases = []
            if obj.parent != None:
                bases.append(obj.parent)
            bases = bases + obj.implements
            retval.append((obj, bases))

        return retval

    def write_registers(self):
        for obj, bases in self.get_classes():
            self.write_class(obj, bases)
        self.fp.write('}\n')

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
                bases_str += ', &PyDOM%s_Type' % base
            bases_str += ')'
        else:
            bases_str = 'NULL'

        cond = get_conditional_substitutions(obj.orig_obj.attributes)
        self.fp.write(cond['conditional_if'])
        self.fp.write('%(indent)sPy_INCREF(&PyDOM%(c_name)s_Type);\n'
                % dict(indent=indent_str, c_name=obj.c_name))
        self.fp.write(
                '%(indent)sPyModule_AddObject(m, "%(c_name)s", (PyObject*) &PyDOM%(c_name)s_Type);\n'
                % dict(indent=indent_str, c_name=obj.c_name,
                       py_name=self.prefix))
        self.fp.write(cond['conditional_endif'])



