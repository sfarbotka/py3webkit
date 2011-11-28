#include "Python.h"
#include "config.h"

#include <wtf/text/CString.h>
#include "DOMFormData.h"
#include "Blob.h"

struct PyDOMObject;


extern "C" PyTypeObject PyDOMDOMFormData_Type;
extern "C" PyTypeObject PyDOMBlob_Type;

namespace WebKit {

WebCore::DOMFormData* coreDOMFormData(PyDOMObject*);
WebCore::Blob* coreBlob(PyDOMObject*);



PyObject * _wrap_DOMFormData_append(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"name", (char*)"value", (char*)"filename", NULL };
    char *name = NULL;
    PyDOMObject *value = NULL;
    char *filename = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"|sOs:pywebkit.DOMFormData.append", kwlist, &name, &value, &filename))
        return NULL;

    if (name && value)
    {
        WTF::String cvt_name = WTF::String::fromUTF8((const char*)name);
        if (PyObject_TypeCheck(value, &PyDOMBlob_Type))
        {
            WTF::String cvt_fname = WTF::String::fromUTF8(name ? (const char*)name : "");
            coreDOMFormData(self)->append(cvt_name, coreBlob(value), cvt_fname);
        }
        else
        {
            PyObject* ss = PyObject_Str((PyObject*)value);
            PyObject* s = PyUnicode_AsUTF8String(ss);

            WTF::String cvt_value = WTF::String::fromUTF8(PyBytes_AsString(s));

            coreDOMFormData(self)->append(cvt_name, cvt_value);

            Py_DECREF(s);
            Py_DECREF(ss);
        }
    }

    Py_INCREF(Py_None);
    return Py_None;
}

} // namespace WebKit
