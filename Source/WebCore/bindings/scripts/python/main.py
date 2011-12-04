
import sys
import os
import subprocess

from xpidl import IDLParser, Attribute, CDATA, Method, Interface
import codegen
import override


tmap = {
    "float": "float",
    "CompareHow": "CompareHow",
    "double": "double",
    "boolean": "bool",
    "char": "char",
    "long": "long",
    "short": "short",
    "uchar": "uchar",
    "unsigned": "unsigned",
    "any": "SerializedScriptValue",
    "TimeoutHandler": "ScheduledActionBase*",
    "int": "int",
    "unsigned int": "unsigned int",
    "unsigned long": "unsigned long",
    "unsigned long long": "unsigned long long",
    "unsigned short": "unsigned short",
    "void": "none",
    #"EventTarget": "Node*",
    "DOMString": "char*"
}

def typeMap(ptype):
    global tmap
    if tmap.has_key(ptype):
        return tmap[ptype]
    return "%s*" % ptype


def should_exclude_attribute(iname, aname):
    if iname == 'DOMWindow' and aname in ['event', 'postMessage', 'crypto', 'console', 'PeerConnection', 'location']:
        return True
    if iname == 'Event' and aname == 'timeStamp':
        return True
    if iname == 'HTMLInputElement' and aname in ['valueAsDate', 'files']:
        return True
    if iname == 'ImageData' and aname == 'data':
        return True
    if iname == 'XMLHttpRequest' and aname == 'response':
        return True
    if iname == 'XMLHttpRequestProgressEvent' and aname in ['position', 'totalSize']:
        return True
    if iname == 'Navigator' and aname in ['plugins', 'mimeTypes']:
        return True
    if iname == 'MediaQueryList' and aname in ['addListener', 'removeListener']:
        return True
    if iname == 'Location' and aname in ['href', 'protocol', 'host', 'hostname', 'port', 'pathname', 'search', 'hash']:
        return True
    if iname == 'Document' and aname in ['webkitVisibilityState', 'webkitHidden']:
        return True
    if iname == 'HTMLMediaElement' and aname in ['webkitAudioDecodedByteCount', 'webkitVideoDecodedByteCount']:
        return True
    if iname == 'HTMLBodyElement' and aname == 'onorientationchange':
        return True
    if iname == 'HTMLFrameSetElement' and aname == 'onorientationchange':
        return True
    if iname == 'HTMLVideoElement' and aname in ['webkitDroppedFrameCount', 'webkitDecodedFrameCount']:
        return True

    return False


def should_exclude_method(iname, mname):
    if iname == 'History' and mname in ['pushState', 'replaceState']:
        return True
    if iname == 'EventListener' and mname == 'handleEvent':
        return True
    if iname == 'DOMWindow' and mname == 'open':
        return True
    if iname == 'HTMLMediaElement' and mname in ['pause', 'play', 'load']:
        return True
    if iname == 'HTMLVideoElement' and mname in ['webkitEnterFullScreen', 'webkitEnterFullscreen']:
        return True
    if iname == 'Location' and mname in ['replace', 'assign', 'reload']:
        return True
    if iname == 'KeyboardEvent' and mname == 'initKeyboardEvent':
        return True
    if iname == 'DedicatedWorkerContext' and mname == 'postMessage':
        return True

    return False


class Parameter(object):
    def __init__(self, ptype, pname, pdflt, pnull, pdir=None):
        self.ptype = ptype
        self.pname = pname
        self.pdflt = pdflt
        self.pnull = pnull
        self.pdir = pdir

    def __len__(self): return 4
    def __getitem__(self, i):
        return (self.ptype, self.pname, self.pdflt, self.pnull)[i]


class ReturnType(str):
    def __new__(cls, *args, **kwds):
        return str.__new__(cls, *args[:1])
    def __init__(self, type_name, optional=False):
        str.__init__(self)
        self.optional = optional


class Definition(object):
    docstring = "NULL"

    def py_name(self):
        return '%s.%s' % (self.module, self.name)

    py_name = property(py_name)

    def __init__(self, *args):
        raise RuntimeError, "this is an abstract class"

    def write_defs(self, fp=sys.stdout):
        raise RuntimeError, "this is an abstract class"

    def guess_return_value_ownership(self):
        "return 1 if caller owns return value"
        if getattr(self, 'is_constructor_of', False):
            self.caller_owns_return = True
        elif self.ret in ('char*', 'string'):
            self.caller_owns_return = True
        else:
            self.caller_owns_return = False


class ObjectDef(Definition):
    def __init__(self, name, module=None, parent=None, c_name=None, typecode=None, fields=None):
        self.name = name
        self.module = module
        self.parent = parent
        self.c_name = c_name
        self.typecode = typecode
        self.fields = fields
        self.implements = []
        self.class_init_func = None
        self.has_new_constructor_api = False

    def write_defs(self, fp=sys.stdout):
        fp.write('(define-object ' + self.name + '\n')
        if self.module:
            fp.write('  (in-module "' + self.module + '")\n')
        if self.parent != (None, None):
            fp.write('  (parent "' + self.parent + '")\n')
        if self.c_name:
            fp.write('  (c-name "' + self.c_name + '")\n')
        if self.typecode:
            fp.write('  (gtype-id "' + self.typecode + '")\n')
        if self.fields:
            fp.write('  (fields\n')
            for (ftype, fname) in self.fields:
                fp.write('    \'("' + ftype + '" "' + fname + '")\n')
            fp.write('  )\n')
        fp.write(')\n\n')


class MethodDef(Definition):
    def __init__(self, name, of_object, c_name, rettype, params):
        self.name = name
        self.ret = rettype
        self.caller_owns_return = None
        self.unblock_threads = None
        self.c_name = c_name
        self.typecode = None
        self.of_object = of_object
        self.params = params if isinstance(params, list) else []
        self.varargs = 0
        self.deprecated = None

        if self.ret is not None:
            self.guess_return_value_ownership()

    def write_defs(self, fp=sys.stdout):
        params = ''
        for pi, p in enumerate(self.params):
            if pi != 0:
                params += ', '
            params += "{} {}".format(p.ptype, p.pname)

        ret = str(self.ret) + ' ' if self.ret not in ('none', None) else ''
        s = "{}{}::{}({})\n".format(ret, self.of_object, self.c_name, params)
        fp.write(s)


class IDLDefsParser:
    def __init__(self):
        self.objects = []
        self.functions = []
        self.c_name = {}     # hash of c names of functions
        self.methods = {}    # hash of methods of particular objects
        self.parser = IDLParser()

    def add_object(self, odef):
        self.objects.append(odef)
        self.c_name[odef.c_name] = odef

    def add_method(self, mdef):
        self.functions.append(mdef)
        self.c_name[mdef.c_name] = mdef

    def write_defs(self, fp=sys.stdout):
        for obj in self.objects:
            obj.write_defs(fp)
        for func in self.functions:
            func.write_defs(fp)

    def find_object(self, c_name):
        for obj in self.objects:
            if obj.c_name == c_name:
                return obj
        else:
            raise ValueError('object %r not found' % c_name)

    def find_methods(self, obj):
        objname = obj.c_name
        return filter(lambda func, on=objname: isinstance(func, MethodDef) and
                      func.of_object == on, self.functions)

    def startParsing(self, input, modulename, filename):
        p = self.parser #IDLParser()
        x = p.parse(input, filename)
        for obj in x.productions:
            if isinstance(obj, Interface):
                fields = []
                attsd = {}
                for m in obj.members:
                    if not isinstance(m, Attribute):
                        continue
                    # HACKS!

                    if should_exclude_attribute(obj.name, m.name):
                        continue


                    if m.attributes.has_key("Replaceable"):
                        m.readonly = True

                    fields.append((typeMap(m.type), m.name))
                    attsd[m.name] = m

                typecode = 'core' + obj.name
                parent = obj.base[0] if obj.base else 'DOMObject'

                odef = ObjectDef(obj.name, modulename, parent, obj.nativename, typecode, fields)
                odef.attributes = attsd
                odef.orig_obj = obj
                self.add_object(odef)

            for m in obj.members:
                if isinstance(m, CDATA):
                    continue
                if isinstance(m, Method):

                    if should_exclude_method(obj.name, m.name):
                        continue

                    if obj.name == 'DOMWindow' and m.name in ['setTimeout', 'setInterval']:
                        # XXX HACK! custom exception
                        m.raises = 'DOMException'


                    params = []
                    return_param = None
                    for p in m.params:
                        rt = p.attributes.has_key("Return")
                        if p.name == 'url' and obj.name == 'XMLHttpRequest' and m.name == 'open':
                            # HACK! XMLHTTPRequest.open url is WebCore::KURL
                            p = Parameter('kurl', p.name, None, 0, None)
                        else:
                            if p.type in ['EventListener', 'TimeoutHandler']:
                                p = Parameter(typeMap(p.type), p.name, None, 1, None)
                            else:
                                p = Parameter(typeMap(p.type), p.name, None, 0, None)
                        params.append(p)
                        if rt:
                            return_param = p

                    rettype = ReturnType(typeMap(m.type), False)

                    mdef = MethodDef(m.name, obj.name, m.name, rettype, params)
                    mdef.attributes = m.attributes
                    mdef.raises = m.raises
                    mdef.return_param = return_param
                    mdef.orig_method = m
                    self.add_method(mdef)

        # debug output
        #self.write_defs()



if __name__ == '__main__':
    modname = "pywebkit"
    p = IDLDefsParser()
    o = override.Overrides(sys.argv[1])
    output_fname = sys.argv[2]
    cwd = os.path.abspath(os.getcwd())
    files = open(sys.argv[3])
    files_prefix = sys.argv[4]
    for fname in files.readlines():
        f = fname.strip()
        if len(f) == 0:
            continue

        f = os.path.join(files_prefix, f)
        print "Parsing %s" % f
        (pth, fn) = os.path.split(f)
        (fn, ext) = os.path.splitext(fn)

        cmd = 'cpp -DLANGUAGE_PYTHON=1 %s' % f.replace(" ", "\ ")
        proc = subprocess.Popen(cmd,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=True,
                           cwd=cwd,
                           )
        stdout_value, stderr_value = proc.communicate('')

        p.startParsing(stdout_value, modname, filename=f)
        codegen.register_types(p)
    fo = codegen.FileOutput(open(output_fname, "w"))
    sw = codegen.SourceWriter(p, o, modname, fo)
    sw.write()
    fo.close()
