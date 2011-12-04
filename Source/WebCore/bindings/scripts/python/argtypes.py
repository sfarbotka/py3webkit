# -*- Mode: Python; py-indent-offset: 4 -*-
# Conversion for use in pywebkit Copyright (C) 2010 Free Software Foundation

import string
import keyword
import struct

py_ssize_t_clean = False

class ArgTypeError(Exception):
    pass

class ArgTypeNotFoundError(ArgTypeError):
    pass

class ArgTypeConfigurationError(ArgTypeError):
    pass


class VarList:
    """Nicely format a C variable list"""
    def __init__(self):
        self.vars = {}
    def add(self, ctype, name):
        if self.vars.has_key(ctype):
            self.vars[ctype] = self.vars[ctype] + (name,)
        else:
            self.vars[ctype] = (name,)
    def __str__(self):
        ret = []
        for type in self.vars.keys():
            ret.append('    ')
            ret.append(type)
            ret.append(' ')
            ret.append(string.join(self.vars[type], ', '))
            ret.append(';\n')
        if ret:
            ret.append('\n')
            return string.join(ret, '')
        return ''

class WrapperInfo:
    """A class that holds information about variable defs, code
    snippets, etcd for use in writing out the function/method
    wrapper."""
    def __init__(self):
        self.varlist = VarList()
        self.parsestr = ''
        self.parselist = ['', 'kwlist']
        self.codebefore = []
        self.codeafter = []
        self.arglist = []
        self.kwlist = []
    def get_parselist(self):
        return string.join(self.parselist, ', ')
    def get_codebefore(self):
        return string.join(self.codebefore, '')
    def get_codeafter(self):
        return string.join(self.codeafter, '')
    def get_arglist(self):
        return string.join(self.arglist, ', ')
    def get_varlist(self):
        return str(self.varlist)
    def get_kwlist(self):
        kwlist = map(lambda x: "(char*)"+x, self.kwlist)
        ret = '    static char *kwlist[] = { %s };\n' % \
              string.join(kwlist + [ 'NULL' ], ', ')
        if not self.get_varlist():
            ret = ret + '\n'
        return ret

    def add_parselist(self, codes, parseargs, keywords):
        self.parsestr = self.parsestr + codes
        for arg in parseargs:
            self.parselist.append(arg)
        for kw in keywords:
            if keyword.iskeyword(kw):
                kw = kw + '_'
            self.kwlist.append('"%s"' % kw)

class ArgType:
    def write_param(self, ptype, pname, pdflt, pnull, info):
        """Add code to the WrapperInfo instance to handle
        parameter."""
        raise RuntimeError, "write_param not implemented for %s" % \
              self.__class__.__name__
    def write_return(self, ptype, ownsreturn, info):
        """Adds a variable named ret of the return type to
        info.varlist, and add any required code to info.codeafter to
        convert the return value to a python object."""
        raise RuntimeError, "write_return not implemented for %s" % \
              self.__class__.__name__

class NoneArg(ArgType):
    def write_return(self, ptype, ownsreturn, info):
        info.codeafter.append('    Py_INCREF(Py_None);\n' +
                              '    return Py_None;')

class URLStringArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt != None:
            if pdflt != 'NULL': pdflt = '"' + pdflt + '"'
            info.varlist.add('char', '*' + pname + ' = ' + pdflt)
        else:
            info.varlist.add('char', '*' + pname)
        info.arglist.append("cvt_"+pname)
        # BIG UGLY HACK! yuk!
        info.codebefore.append('    WTF::String _cvt_%s = WTF::String::fromUTF8((const char*)%s);\n' % \
                            (pname, pname))
        info.codebefore.append('    WebCore::KURL cvt_%s = coreXMLHttpRequest(self)->scriptExecutionContext()->completeURL(_cvt_%s);\n' % \
                            (pname, pname))
        #info.codebefore.append('    WebCore::KURL cvt_%s;\n' % \
        #                    (pname))
        if pnull:
            info.add_parselist('z', ['&' + pname], [pname])
        else:
            info.add_parselist('s', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('WTF::String', 'ret')
        info.varlist.add('char', '*_ret')
        info.codeafter.append('    _ret = cpUTF8(ret);\n'
                              '    PyObject *py_ret = PyUnicode_FromString(_ret);\n'
                              '    free(_ret);\n'
                              '    return py_ret;')

class StringArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt != None:
            if pdflt != 'NULL': pdflt = '"' + pdflt + '"'
            info.varlist.add('char', '*' + pname + ' = ' + pdflt)
        else:
            info.varlist.add('char', '*' + pname)
        info.arglist.append("cvt_"+pname)
        info.codebefore.append('    WTF::String cvt_%s = WTF::String::fromUTF8((const char*)%s);\n' % \
                            (pname, pname))
        if pnull:
            info.add_parselist('z', ['&' + pname], [pname])
        else:
            info.add_parselist('s', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('WTF::String', 'ret')
        info.varlist.add('char', '*_ret')
        info.codeafter.append('    _ret = cpUTF8(ret);\n'
                              '    PyObject *py_ret = PyUnicode_FromString(_ret);\n'
                              '    free(_ret);\n'
                              '    return py_ret;')

class SerializedStringArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt != None:
            if pdflt != 'NULL': pdflt = '"' + pdflt + '"'
            info.varlist.add('char', '*' + pname + ' = ' + pdflt)
        else:
            info.varlist.add('char', '*' + pname)
        info.arglist.append("cvt_"+pname)
        info.codebefore.append('    WebCore::SerializedScriptValue *cvt_%s = WebCore::SerializedScriptValue::create(WTF::String::fromUTF8((const char*)%s));\n' % \
                            (pname, pname))
        if pnull:
            info.add_parselist('z', ['&' + pname], [pname])
        else:
            info.add_parselist('s', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('WebCore::SerializedScriptValue*', 'ret')
        info.codeafter.append('    PyObject *py_ret = PyUnicode_FromString(cpUTF8(ret->toString()));\n' +
                              '    return py_ret;')

class UCharArg(ArgType):
    # allows strings with embedded NULLs.
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('guchar', '*' + pname + ' = "' + pdflt + '"')
        else:
            info.varlist.add('guchar', '*' + pname)
        if py_ssize_t_clean:
            info.varlist.add('Py_ssize_t', pname + '_len')
        else:
            info.varlist.add('int', pname + '_len')
        info.arglist.append(pname)
        if pnull:
            info.add_parselist('z#', ['&' + pname, '&' + pname + '_len'],
                               [pname])
        else:
            info.add_parselist('s#', ['&' + pname, '&' + pname + '_len'],
                               [pname])

class CharArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('char', pname + " = '" + pdflt + "'")
        else:
            info.varlist.add('char', pname)
        info.arglist.append(pname)
        info.add_parselist('c', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('gchar', 'ret')
        info.codeafter.append('    return PyUnicode_FromStringAndSize(&ret, 1);')

class GUniCharArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt != None:
            if pdflt != 'NULL': pdflt = '"' + pdflt + '"'
            info.varlist.add('Py_UNICODE', '*' + pname + ' = ' + pdflt)
        else:
            info.varlist.add('Py_UNICODE', '*' + pname)
        info.arglist.append("cvt_"+pname)
        info.codebefore.append('    WTF::String cvt_%s = WTF::String((const UChar*)%s);\n' % \
                            (pname, pname))
        if pnull:
            info.add_parselist('z', ['&' + pname], [pname])
        else:
            info.add_parselist('z', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('WTF::String', 'ret')
        info.codeafter.append('    PyObject *py_ret = PyUnicode_FromWideChar((const wchar_t*)(ret.characters()), ret.length());\n' +
                              '    return py_ret;')

class GUniCharArg2(ArgType):
    ret_tmpl = ('#if !defined(Py_UNICODE_SIZE) || Py_UNICODE_SIZE == 2\n'
                '    if (ret > 0xffff) {\n'
                '        PyErr_SetString(PyExc_RuntimeError, "returned character can not be represented in 16-bit unicode");\n'
                '        return NULL;\n'
                '    }\n'
                '#endif\n'
                '    py_ret = (Py_UNICODE)ret;\n'
                '    return PyUnicode_FromUnicode(&py_ret, 1);\n')
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('gunichar', pname + " = '" + pdflt + "'")
        else:
            info.varlist.add('gunichar', pname)
        info.arglist.append(pname)
        info.add_parselist('O&', ['pyg_pyobj_to_unichar_conv', '&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('gunichar', 'ret')
        info.varlist.add('Py_UNICODE', 'py_ret')
        info.codeafter.append(self.ret_tmpl)


class CompareHowArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('int', pname + ' = ' + pdflt)
        else:
            info.varlist.add('int', pname)
        info.arglist.append("cvt_"+pname)
        info.codebefore.append('    WebCore::Range::CompareHow cvt_%s = static_cast<WebCore::Range::CompareHow>(%s);\n' % \
                            (pname, pname))
        info.add_parselist('i', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('int', 'ret')
        info.codeafter.append('    return PyLong_FromLong(ret);')

class IntArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('int', pname + ' = ' + pdflt)
        else:
            info.varlist.add('int', pname)
        info.arglist.append(pname)
        info.add_parselist('i', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('int', 'ret')
        info.codeafter.append('    return PyLong_FromLong(ret);')

class UIntArg(ArgType):
    dflt = ('    if (py_%(name)s) {\n'
            '        if (PyLong_Check(py_%(name)s))\n'
            '            %(name)s = PyLong_AsUnsignedLong(py_%(name)s);\n'
            '        else if (PyInt_Check(py_%(name)s))\n'
            '            %(name)s = PyInt_AsLong(py_%(name)s);\n'
            '        else\n'
            '            PyErr_SetString(PyExc_TypeError, "Parameter \'%(name)s\' must be an int or a long");\n'
            '        if (PyErr_Occurred())\n'
            '            return NULL;\n'
            '    }\n')
    before = ('    if (PyLong_Check(py_%(name)s))\n'
              '        %(name)s = PyLong_AsUnsignedLong(py_%(name)s);\n'
              '    else if (PyInt_Check(py_%(name)s))\n'
              '        %(name)s = PyInt_AsLong(py_%(name)s);\n'
              '    else\n'
              '        PyErr_SetString(PyExc_TypeError, "Parameter \'%(name)s\' must be an int or a long");\n'
              '    if (PyErr_Occurred())\n'
              '        return NULL;\n')
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if not pdflt:
            pdflt = '0';

        info.varlist.add(ptype, pname + ' = ' + pdflt)
        info.codebefore.append(self.dflt % {'name':pname})
        info.varlist.add('PyObject', "*py_" + pname + ' = NULL')
        info.arglist.append(pname)
        info.add_parselist('O', ['&py_' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add(ptype, 'ret')
        info.codeafter.append('    return PyLong_FromUnsignedLong(ret);')

class SizeArg(ArgType):

    if struct.calcsize('P') <= struct.calcsize('l'):
        llp64 = True
    else:
        llp64 = False

    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add(ptype, pname + ' = ' + pdflt)
        else:
            info.varlist.add(ptype, pname)
        info.arglist.append(pname)
        if self.llp64:
            info.add_parselist('k', ['&' + pname], [pname])
        else:
            info.add_parselist('K', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add(ptype, 'ret')
        if self.llp64:
            info.codeafter.append('    return PyLong_FromUnsignedLongLong(ret);\n')
        else:
            info.codeafter.append('    return PyLong_FromUnsignedLong(ret);\n')

class SSizeArg(ArgType):

    if struct.calcsize('P') <= struct.calcsize('l'):
        llp64 = True
    else:
        llp64 = False

    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add(ptype, pname + ' = ' + pdflt)
        else:
            info.varlist.add(ptype, pname)
        info.arglist.append(pname)
        if self.llp64:
            info.add_parselist('l', ['&' + pname], [pname])
        else:
            info.add_parselist('L', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add(ptype, 'ret')
        if self.llp64:
            info.codeafter.append('    return PyLong_FromLongLong(ret);\n')
        else:
            info.codeafter.append('    return PyLong_FromLong(ret);\n')

class LongArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add(ptype, pname + ' = ' + pdflt)
        else:
            info.varlist.add(ptype, pname)
        info.arglist.append(pname)
        info.add_parselist('l', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add(ptype, 'ret')
        info.codeafter.append('    return PyLong_FromLong(ret);\n')

class BoolArg(IntArg):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('int', pname + ' = ' + pdflt)
        else:
            info.varlist.add('int', pname)
        info.arglist.append("cvt_"+pname)
        info.codebefore.append('    bool cvt_%s = (bool)%s;\n' % \
                            (pname, pname))
        info.add_parselist('i', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('bool', 'ret')
        info.codeafter.append('    return PyBool_FromLong((long)ret);\n')

class TimeTArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('time_t', pname + ' = ' + pdflt)
        else:
            info.varlist.add('time_t', pname)
        info.arglist.append(pname)
        info.add_parselist('i', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('time_t', 'ret')
        info.codeafter.append('    return PyLong_FromLong(ret);')

class ULongArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('unsigned long', pname + ' = ' + pdflt)
        else:
            info.varlist.add('unsigned long', pname)
        info.arglist.append(pname)
        info.add_parselist('k', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add(ptype, 'ret')
        info.codeafter.append('    return PyLong_FromUnsignedLong(ret);\n')

class UInt32Arg(ULongArg):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        ULongArg.write_param(self, ptype, pname, pdflt, pnull, info)
        ## if sizeof(unsigned long) > sizeof(unsigned int), we need to
        ## check the value is within guint32 range
        if struct.calcsize('L') > struct.calcsize('I'):
            info.codebefore.append((
                '    if (%(pname)s > G_MAXUINT32) {\n'
                '        PyErr_SetString(PyExc_ValueError,\n'
                '                        "Value out of range in conversion of"\n'
                '                        " %(pname)s parameter to unsigned 32 bit integer");\n'
                '        return NULL;\n'
                '    }\n') % vars())

class Int64Arg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('long long', pname + ' = ' + pdflt)
        else:
            info.varlist.add('long long', pname)
        info.arglist.append(pname)
        info.add_parselist('L', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('long long', 'ret')
        info.codeafter.append('    return PyLong_FromLongLong(ret);')

class UInt64Arg(ArgType):
    dflt = '    if (py_%(name)s)\n' \
           '        %(name)s = PyLong_AsUnsignedLongLong(py_%(name)s);\n'
    before = '    %(name)s = PyLong_AsUnsignedLongLong(py_%(name)s);\n'
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('unsigned long long', pname + ' = ' + pdflt)
            info.codebefore.append(self.dflt % {'name':pname})
        else:
            info.varlist.add('unsigned long long', pname)
            info.codebefore.append(self.before % {'name':pname})
        info.varlist.add('PyObject', "*py_" + pname + ' = NULL')
        info.arglist.append(pname)
        info.add_parselist('O!', ['&PyLong_Type', '&py_' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('unsigned long long', 'ret')
        info.codeafter.append('    return PyLong_FromUnsignedLongLong(ret);')


class DoubleArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pdflt:
            info.varlist.add('double', pname + ' = ' + pdflt)
        else:
            info.varlist.add('double', pname)
        info.arglist.append(pname)
        info.add_parselist('d', ['&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('double', 'ret')
        info.codeafter.append('    return PyFloat_FromDouble(ret);')

class FileArg(ArgType):
    nulldflt = ('    if (py_%(name)s == Py_None)\n'
                '        %(name)s = NULL;\n'
                '    else if (py_%(name)s && PyFile_Check(py_%(name)s)\n'
                '        %s = PyFile_AsFile(py_%(name)s);\n'
                '    else if (py_%(name)s) {\n'
                '        PyErr_SetString(PyExc_TypeError, "%(name)s should be a file object or None");\n'
                '        return NULL;\n'
                '    }')
    null = ('    if (py_%(name)s && PyFile_Check(py_%(name)s)\n'
            '        %(name)s = PyFile_AsFile(py_%(name)s);\n'
            '    else if (py_%(name)s != Py_None) {\n'
            '        PyErr_SetString(PyExc_TypeError, "%(name)s should be a file object or None");\n'
            '        return NULL;\n'
            '    }\n')
    dflt = ('    if (py_%(name)s)\n'
            '        %(name)s = PyFile_AsFile(py_%(name)s);\n')
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pnull:
            if pdflt:
                info.varlist.add('FILE', '*' + pname + ' = ' + pdflt)
                info.varlist.add('PyObject', '*py_' + pname + ' = NULL')
                info.codebefore.append(self.nulldflt % {'name':pname})
            else:
                info.varlist.add('FILE', '*' + pname + ' = NULL')
                info.varlist.add('PyObject', '*py_' + pname)
                info.codebefore.append(self.null & {'name':pname})
            info.arglist.appned(pname)
            info.add_parselist('O', ['&py_' + pname], [pname])
        else:
            if pdflt:
                info.varlist.add('FILE', '*' + pname + ' = ' + pdflt)
                info.varlist.add('PyObject', '*py_' + pname + ' = NULL')
                info.codebefore.append(self.dflt % {'name':pname})
                info.arglist.append(pname)
            else:
                info.varlist.add('PyObject', '*' + pname)
                info.arglist.append('PyFile_AsFile(' + pname + ')')
            info.add_parselist('O!', ['&PyFile_Type', '&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add('FILE', '*ret')
        info.codeafter.append('    if (ret)\n' +
                              '        return PyFile_FromFile(ret, "", "", fclose);\n' +
                              '    Py_INCREF(Py_None);\n' +
                              '    return Py_None;')


class ObjectArg(ArgType):
    # should change these checks to more typesafe versions that check
    # a little further down in the class heirachy.
    nulldflt = ('    if ((PyObject *)py_%(name)s == Py_None)\n'
                '        %(name)s = NULL;\n'
                '    else if (py_%(name)s && pygobject_check(py_%(name)s, &Py%(type)s_Type))\n'
                '        %(name)s = %(cast)s(py_%(name)s->obj);\n'
                '    else if (py_%(name)s) {\n'
                '        PyErr_SetString(PyExc_TypeError, "%(name)s should be a %(type)s or None");\n'
                '        return NULL;\n'
                '    }\n')
    null = ('    if (py_%(name)s && pygobject_check(py_%(name)s, &Py%(type)s_Type))\n'
            '        %(name)s = %(cast)s(py_%(name)s->obj);\n'
            '    else if ((PyObject *)py_%(name)s != Py_None) {\n'
            '        PyErr_SetString(PyExc_TypeError, "%(name)s should be a %(type)s or None");\n'
            '        return NULL;\n'
            '    }\n')
    dflt = '    if (py_%(name)s)\n' \
           '        %(name)s = %(cast)s(py_%(name)s);\n'
    def __init__(self, objname, parent, typecode):
        self.objname = objname
        self.cast = typecode
        self.parent = parent
    def write_param(self, ptype, pname, pdflt, pnull, info):
        if pnull:
            if pdflt:
                info.varlist.add(self.objname, '*' + pname + ' = ' + pdflt)
                info.varlist.add('PyObject', '*py_' + pname + ' = NULL')
                info.codebefore.append(self.nulldflt % {'name':pname,
                                                        'cast':self.cast,
                                                        'type':self.objname})
            else:
                if ptype == 'ScheduledActionBase*':
                    info.varlist.add("OwnPtr<"+self.objname+">", pname)
                else:
                    info.varlist.add(self.objname, '*' + pname + ' = NULL')
                info.varlist.add('PyDOMObject', '*py_' + pname)
                info.codebefore.append(self.dflt % {'name':pname,
                                                    'cast':self.cast,
                                                    'type':self.objname})
            if ptype.endswith('*'):
                typename = ptype[:-1]
                try:
                    const, typename = typename.split('const-')
                except ValueError:
                    const = ''
                if typename != ptype and ptype != 'ScheduledActionBase*':
                    info.arglist.append('(%s *) %s' % (ptype[:-1], pname))
                else:
                    info.arglist.append(pname + '.release()')

            info.add_parselist('O', ['&py_' + pname], [pname])
        else:
            if pdflt:
                info.varlist.add(self.objname, '*' + pname + ' = ' + pdflt)
                info.varlist.add('PyDOMObject', '*py_' + pname + ' = NULL')
                info.codebefore.append(self.dflt % {'name':pname,
                                                    'cast':self.cast})
                info.arglist.append(pname)
                info.add_parselist('O!', ['PtrPyDOM%s_Type' % self.objname,
                                         '&py_' + pname], [pname])
            else:
                info.varlist.add('PyDOMObject', '*' + pname)
                info.arglist.append('%s(%s)' % (self.cast, pname))
                info.add_parselist('O!', ['PtrPyDOM%s_Type' % self.objname,
                                          '&' + pname], [pname])
    def write_return(self, ptype, ownsreturn, info):
        if ptype.endswith('*'):
            typename = ptype[:-1]
            try:
                const, typename = typename.split('const-')
            except ValueError:
                const = ''
        info.varlist.add("WTF::RefPtr<WebCore::%s>" % typename, 'ret')
        info.varlist.add("WebCore::%s*" % typename, '_ret')
        info.varlist.add('PyObject', '*py_ret')
        if ownsreturn:
            info.codeafter.append('    py_ret = pygobject_new((GObject *)ret);\n'
                                  '    if (ret != NULL)\n'
                                  '        g_object_unref(ret);\n'
                                  '    return py_ret;')
        else:
            info.codeafter.append('    _ret = WTF::getPtr(ret);\n') 
            info.codeafter.append('    py_ret = toPython(_ret);\n') 
            info.codeafter.append('    return py_ret;') 

class PyObjectArg(ArgType):
    def write_param(self, ptype, pname, pdflt, pnull, info):
        info.varlist.add('PyObject', '*' + pname)
        info.add_parselist('O', ['&' + pname], [pname])
        info.arglist.append(pname)
    def write_return(self, ptype, ownsreturn, info):
        info.varlist.add("PyObject", "*ret")
        if ownsreturn:
            info.codeafter.append('    if (ret) {\n'
                                  '       return ret;\n'
                                  '    }\n'
                                  '    Py_INCREF(Py_None);\n'
                                  '    return Py_None;')
        else:
            info.codeafter.append('    if (!ret) ret = Py_None;\n'
                                  '    Py_INCREF(ret);\n'
                                  '    return ret;')


class ArgMatcher:
    def __init__(self):
        self.argtypes = {}

    def register(self, ptype, handler, overwrite=False):
        if not overwrite and ptype in self.argtypes:
            return
        self.argtypes[ptype] = handler

    def register_object(self, ptype, parent, typecode):
        oa = ObjectArg(ptype, parent, typecode)
        self.register(ptype, oa)  # in case I forget the * in the .defs
        self.register(ptype+'*', oa)
        self.register('const '+ptype+'*', oa)

    def get(self, ptype):
        try:
            return self.argtypes[ptype]
        except KeyError:
            print(self.argtypes['EventListener'])
            raise ArgTypeNotFoundError(ptype)

    def object_is_a(self, otype, parent):
        if otype == None: return 0
        if otype == parent: return 1
        if not self.argtypes.has_key(otype): return 0
        return self.object_is_a(self.get(otype).parent, parent)

matcher = ArgMatcher()

arg = NoneArg()
matcher.register(None, arg)
matcher.register('none', arg)

arg = URLStringArg()
matcher.register('kurl', arg)

arg = StringArg()
matcher.register('char*', arg)
matcher.register('const char*', arg)
matcher.register('char const*', arg)
matcher.register('string', arg)
matcher.register('static_string', arg)

arg = SerializedStringArg()
matcher.register('SerializedScriptValue', arg)

arg = UCharArg()
matcher.register('unsigned char*', arg)

arg = CharArg()
matcher.register('char', arg)

arg = GUniCharArg()
matcher.register('DOMString', arg)
matcher.register('wchar_t*', arg)

arg = IntArg()
matcher.register('int', arg)
matcher.register('short', arg)
matcher.register('unsigned short', arg)

arg = CompareHowArg()
matcher.register('CompareHow', arg)

arg = LongArg()
matcher.register('long', arg)

arg = BoolArg()
matcher.register('bool', arg)

arg = TimeTArg()
matcher.register('time_t', arg)

arg = ULongArg()
matcher.register('unsigned long', arg)

arg = Int64Arg()
matcher.register('long long', arg)

arg = UInt64Arg()
matcher.register('unsigned long long', arg)

arg = DoubleArg()
matcher.register('double', arg)
matcher.register('float', arg)

arg = FileArg()
matcher.register('FILE*', arg)

del arg

# enums, flags, objects

matcher.register('PyObject*', PyObjectArg())
matcher.register('ScheduledActionBase*', ObjectArg("ScheduledActionBase", "DOMObject", "coreScheduledActionBase"))
