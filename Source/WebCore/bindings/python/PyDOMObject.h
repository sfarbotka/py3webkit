#ifndef PyDOMObject_h
#define PyDOMObject_h

typedef struct
{
    PyObject_HEAD
    void* ptr;
    unsigned long iter_index;
    unsigned long iter_count;
} PyDOMObject;

extern PyTypeObject PyDOMObject_Type;

PyObject* DOMObject_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
PyObject* DOMObject_getptr(PyDOMObject *self, PyObject *);
PyObject* DOMObject_setptr(PyDOMObject *self, PyObject *args, PyObject *kwargs);

PyObject* PyDOMObject_new(PyTypeObject *type, void *ptr);

#endif //PyDOMObject_h
