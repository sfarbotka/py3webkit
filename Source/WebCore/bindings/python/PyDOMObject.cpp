#include <Python.h>
#include "config.h"
#include "PyDOMObject.h"



PyObject* DOMObject_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyDOMObject *self;

    self = (PyDOMObject *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->ptr = NULL;
    }

    return (PyObject *)self;
}

PyObject* DOMObject_getptr(PyDOMObject *self, PyObject *)
{
    return PyLong_FromLong((long)self->ptr);
}

PyObject * DOMObject_setptr(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"ptr", NULL };
    long ptr;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"l:shoddy.DOMObject.setptr",
                                     kwlist, &ptr))
        return NULL;

    self->ptr = (void*)ptr;
    Py_INCREF(Py_None);
    return Py_None;
}


PyMethodDef DOMObject_methods[] = {
    {"setptr", (PyCFunction)DOMObject_setptr, METH_VARARGS|METH_KEYWORDS,
     PyDoc_STR("set pointer")},
    {"getptr", (PyCFunction)DOMObject_getptr, METH_NOARGS,
     PyDoc_STR("get pointer")},
    {NULL,	NULL, 0, NULL},
};

PyObject* PyDOMObject_new(PyTypeObject *type, void *ptr)
{
    PyDOMObject *v;
    v = (PyDOMObject *)type->tp_alloc(type, 0);
    v->ptr = ptr;
    return (PyObject *) v;
}

PyTypeObject PyDOMObject_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pywebkit.DOMObject",    /* tp_name */
    sizeof(PyDOMObject),     /* tp_basicsize */
    0,                       /* tp_itemsize */
    0,                       /* tp_dealloc */
    0,                       /* tp_print */
    0,                       /* tp_getattr */
    0,                       /* tp_setattr */
    0,                       /* tp_compare */
    0,                       /* tp_repr */
    0,                       /* tp_as_number */
    0,                       /* tp_as_sequence */
    0,                       /* tp_as_mapping */
    0,                       /* tp_hash */
    0,                       /* tp_call */
    0,                       /* tp_str */
    0,                       /* tp_getattro */
    0,                       /* tp_setattro */
    0,                       /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
      Py_TPFLAGS_BASETYPE,   /* tp_flags */
    0,                       /* tp_doc */
    0,                       /* tp_traverse */
    0,                       /* tp_clear */
    0,                       /* tp_richcompare */
    0,                       /* tp_weaklistoffset */
    0,                       /* tp_iter */
    0,                       /* tp_iternext */
    DOMObject_methods,          /* tp_methods */
    0,                       /* tp_members */
    0,                       /* tp_getset */
    0,                       /* tp_base */
    0,                       /* tp_dict */
    0,                       /* tp_descr_get */
    0,                       /* tp_descr_set */
    0,                       /* tp_dictoffset */
    0,                       /* tp_init */
    0,                       /* tp_alloc */
    DOMObject_new,           /* tp_new */
    0,                       /* tp_free */
    0,                       /* tp_is_gc */
    0,                                 /* tp_bases */
    0,                                 /* tp_mro */
    0,                                 /* tp_cache */
    0,                                 /* tp_subclasses */
    0,                                 /* tp_weaklist */
    0,                                 /* tp_del */
    0                                  /* tp_version_tag */

};
