#include <Python.h>
#include "config.h"
#include "PyScheduledAction.h"
#include "PythonBinding.h"

PyTypeObject *PtrPyPyScheduledAction_Type;

PassOwnPtr<WebCore::PyScheduledAction> WebCore::PyScheduledAction::create(PyObject* callback)
{
    return adoptPtr(new PyScheduledAction(callback));
}

WebCore::PyScheduledAction::PyScheduledAction(PyObject *callback)
    : m_callback(callback)
{
    printf("PyScheduledAction() = %p\n", this);
    if (callback)
        Py_INCREF(callback);
}

WebCore::PyScheduledAction::~PyScheduledAction()
{
    printf("~PyScheduledAction() = %p\n", this);
    if (m_callback)
        Py_DECREF(m_callback);
}

void WebCore::PyScheduledAction::execute(ScriptExecutionContext* context)
{
    printf("PyScheduledAction::execute() = %p\n", this);
    if (context->isDocument())
        execute(static_cast<Document*>(context));
#if 0 // ENABLE(WORKERS)
    else {
        ASSERT(context->isWorkerContext());
        execute(static_cast<WorkerContext*>(context));
    }
#else
    ASSERT(context->isDocument());
#endif
}

void WebCore::PyScheduledAction::execute(Document* document)
{
    RefPtr<Frame> frame = document->frame();
    PyObject* arglist = Py_BuildValue((char*)"()");

    if (!frame || !frame->script()->canExecuteScripts(AboutToExecuteScript))
        return;

    // XXX Hack frame->script()->setProcessingTimerCallback(true);
    PyGILState_STATE __py_state;
    __py_state = PyGILState_Ensure();
    PyObject* result = PyObject_CallObject(m_callback, arglist);
    PyGILState_Release(__py_state);
    // XXX Hack frame->script()->setProcessingTimerCallback(false);

    Py_DECREF(arglist);

    if (result == NULL)
    {
        fprintf(stderr, "Exception occurred while executing scheduled action\n");
        __py_state = PyGILState_Ensure();
        PyErr_Print();
        PyGILState_Release(__py_state);
        return;
    }
    /* Here maybe use the result */
    Py_DECREF(result);
    return;

}




PassOwnPtr<WebCore::ScheduledActionBase> WebKit::corePyScheduledAction(PyDOMObject* request)
{
    PyObject *obj = (PyObject*)request;
    if (obj == Py_None) {
        return nullptr;
    }
    if (Py_TYPE((PyObject*)obj) == PtrPyPyScheduledAction_Type) {
        void *coreptr = ((PyDOMObject*)request)->ptr;
        return adoptPtr(static_cast<WebCore::ScheduledActionBase*>(coreptr));
    }
    if (!PyCallable_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "param must be callable");
        return nullptr;
    }

    printf("create PyScheduledAction\n");
    OwnPtr<WebCore::ScheduledActionBase> sa = WebCore::PyScheduledAction::create(obj);
    return sa.release();
}

int PyScheduledAction_init(WebCore::ScheduledActionBase *self, PyObject *args, PyObject *kwargs)
{
    if (PyDOMObject_Type.tp_init((PyObject *)self, args, kwargs) < 0)
        return -1;
    return 0;
}

void dealloc_PyScheduledAction(PyObject *self)
{
    printf("dealloc_PyScheduledAction\n");
    PyDOMObject *obj = (PyDOMObject*)self;
    void *coreptr = obj->ptr;
    WebKit::PythonObjectCache::forgetDOMObject(coreptr);
    self->ob_type->tp_free(self);
}

PyObject* WebKit::pywrapPyScheduledAction(WebCore::ScheduledActionBase* coreObject)
{
    void *coreptr = (static_cast<void*>(coreObject));
    //coreObject->ref();
    return PyDOMObject_new(PtrPyPyScheduledAction_Type, coreptr);
}

PyObject* WebKit::toPython(WebCore::ScheduledActionBase* obj)
{
    if (!obj)
        Py_RETURN_NONE;

    if (PyObject* ret = WebKit::PythonObjectCache::getDOMObject(obj))
        return ret;

    return WebKit::PythonObjectCache::putDOMObject(obj, WebKit::pywrapPyScheduledAction(obj));
}




PyTypeObject G_GNUC_INTERNAL PyPyScheduledAction_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "pywebkit.ScheduledAction",                   /* tp_name */
    sizeof(PyPyScheduledAction),          /* tp_basicsize */
    0,                                 /* tp_itemsize */
    /* methods */
    (destructor)dealloc_PyScheduledAction,        /* tp_dealloc */
    (printfunc)0,                      /* tp_print */
    (getattrfunc)0,       /* tp_getattr */
    (setattrfunc)0,       /* tp_setattr */
    0,           /* tp_compare */
    (reprfunc)0,             /* tp_repr */
    (PyNumberMethods*)0,     /* tp_as_number */
    (PySequenceMethods*)0, /* tp_as_sequence */
    (PyMappingMethods*)0,   /* tp_as_mapping */
    (hashfunc)0,             /* tp_hash */
    (ternaryfunc)0,          /* tp_call */
    (reprfunc)0,              /* tp_str */
    (getattrofunc)0,     /* tp_getattro */
    (setattrofunc)0,     /* tp_setattro */
    (PyBufferProcs*)0,  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                      /* tp_flags */
    NULL,                        /* Documentation string */
    (traverseproc)0,     /* tp_traverse */
    (inquiry)0,             /* tp_clear */
    (richcmpfunc)0,   /* tp_richcompare */
    0,             /* tp_weaklistoffset */
    (getiterfunc)0,          /* tp_iter */
    (iternextfunc)0,     /* tp_iternext */
    (struct PyMethodDef*)NULL, /* tp_methods */
    (struct PyMemberDef*)0,              /* tp_members */
    (struct PyGetSetDef*)0,  /* tp_getset */
    NULL,                              /* tp_base */
    NULL,                              /* tp_dict */
    (descrgetfunc)0,    /* tp_descr_get */
    (descrsetfunc)0,    /* tp_descr_set */
    0,                 /* tp_dictoffset */
    (initproc)PyScheduledAction_init,             /* tp_init */
    (allocfunc)0,           /* tp_alloc */
    (newfunc)DOMObject_new,               /* tp_new */
    (freefunc)0,             /* tp_free */
    (inquiry)0,              /* tp_is_gc */
    0,                                 /* tp_bases */
    0,                                 /* tp_mro */
    0,                                 /* tp_cache */
    0,                                 /* tp_subclasses */
    0,                                 /* tp_weaklist */
    0,                                 /* tp_del */
    0                                  /* tp_version_tag */
};
