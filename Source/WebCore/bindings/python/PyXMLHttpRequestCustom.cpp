
#include "Python.h"
#include "config.h"

#include "XMLHttpRequest.h"
#include "ArrayBuffer.h"
#include "Blob.h"
#include "DOMFormData.h"
#include "Document.h"


struct PyDOMObject;


extern "C" PyTypeObject PyDOMDocument_Type;
extern "C" PyTypeObject PyDOMDOMFormData_Type;
extern "C" PyTypeObject PyDOMBlob_Type;

void py_wk_exc(WebCore::ExceptionCode &ec);

namespace WebKit {

WebCore::XMLHttpRequest* coreXMLHttpRequest(PyDOMObject* request);
WebCore::Document* coreDocument(PyDOMObject*);
WebCore::DOMFormData* coreDOMFormData(PyDOMObject*);
WebCore::Blob* coreBlob(PyDOMObject*);



PyObject * _wrap_XMLHttpRequest_send(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"data", NULL };
    PyDOMObject *data = NULL;
    WebCore::ExceptionCode ec = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"|O:pywebkit.XMLHttpRequest.send", kwlist, &data))
        return NULL;

    if (!data)
        coreXMLHttpRequest(self)->send(ec);
    else if (PyObject_TypeCheck(data, &PyDOMDocument_Type))
        coreXMLHttpRequest(self)->send(coreDocument(data), ec);
    else if (PyObject_TypeCheck(data, &PyDOMDOMFormData_Type))
        coreXMLHttpRequest(self)->send(coreDOMFormData(data), ec);
    else if (PyObject_TypeCheck(data, &PyDOMDocument_Type))
        coreXMLHttpRequest(self)->send(coreDocument(data), ec);
    else if (PyObject_TypeCheck(data, &PyDOMBlob_Type))
        coreXMLHttpRequest(self)->send(coreBlob(data), ec);
    // TODO ArrayBuffer, convert obj to string in 'else' case
    else
    {
        PyErr_SetString(PyExc_NotImplementedError, "Possibly not fully implemented custom method XMLHttlRequest.send");
        return NULL;
    }

    if (ec)
    {
        py_wk_exc(ec);
        return NULL;
    }

    Py_INCREF(Py_None);
    return Py_None;
}

} // namespace WebKit
