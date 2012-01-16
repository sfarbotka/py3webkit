
#include <Python.h>
#include "config.h"

#include "HTMLAllCollection.h"
#include "Node.h"
#include "StaticNodeList.h"
#include <wtf/Vector.h>
#include <wtf/text/CString.h>

#include "PyDOMObject.h"

namespace WebKit {
using namespace WebCore;

HTMLAllCollection *coreHTMLAllCollection(PyDOMObject*);
PyObject* toPython(WebCore::Node* obj);
PyObject* toPython(WebCore::NodeList* obj);


static PyObject* getNamedItems(PyDOMObject* self, PyObject* obj)
{
    Vector<RefPtr<Node> > namedItems;
    PyObject* uobj;
    PyObject* sobj;
    char* name;

    uobj = PyObject_Str(obj);
    if (!uobj)
        return NULL;

    sobj = PyUnicode_AsUTF8String(uobj);
    Py_DECREF(uobj);
    if (!sobj)
        return NULL;

    name = PyBytes_AsString(sobj);
    Py_DECREF(sobj);
    if (!name)
        return NULL;


    WTF::String cvt_name = WTF::String::fromUTF8((const char*)name);
    coreHTMLAllCollection(self)->namedItems(cvt_name, namedItems);

    if (namedItems.isEmpty())
    {
        Py_INCREF(Py_None);
        return Py_None;
    }

    if (namedItems.size() == 1)
        return toPython(namedItems[0].get());

    return toPython(StaticNodeList::adopt(namedItems).get());
}


PyObject * _wrap_HTMLAllCollection_item(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"index", NULL };
    PyObject* oindex;
    unsigned long index;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"k:pywebkit.HTMLAllCollection.item", kwlist, &index))
        return NULL;

    WebCore::Node* ret = coreHTMLAllCollection(self)->item(index);
    return toPython(ret);
}


PyObject* _wrap_HTMLAllCollection_namedItem(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"name", NULL };
    PyObject* name;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"O:pywebkit.HTMLAllCollection.namedItem", kwlist, &name))
        return NULL;

    return getNamedItems(self, name);
}




} // namespace WebKit
