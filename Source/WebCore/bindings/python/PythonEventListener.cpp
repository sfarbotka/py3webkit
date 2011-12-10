#include <Python.h>
#include "config.h"
#include "PythonBinding.h"
#include "PythonEventListener.h"

PyObject *WebKit::toPython(WebCore::Event *);

WebCore::EventListener*
webkit_create_python_event_listener(PyObject *callback)
{
    printf("create PythonEventListener\n");
    RefPtr<PythonEventListener> listener;
    listener = PythonEventListener::create(callback);
    listener->ref();
    return listener.get();
}

void webkit_delete_python_event_listener(WebCore::EventListener *l)
{
    printf("deref PythonEventListener\n");
    l->deref();
}


PassRefPtr<PythonEventListener> PythonEventListener::create(PyObject* callback)
{
   return adoptRef(new PythonEventListener(callback));
}

PythonEventListener::PythonEventListener(PyObject *callback)
  : WebCore::EventListener(WebCore::EventListener::PythonEventListenerType)
  , m_callback(callback)
{
    printf("PythonEventListener(%p) = %p\n", callback, this);
    if (callback)
        Py_INCREF(callback);
}

PythonEventListener::~PythonEventListener()
{
    printf("~PythonEventListener() = %p\n", this);
    if (m_callback)
        Py_DECREF(m_callback);
}



const PythonEventListener* PythonEventListener::cast(const EventListener* listener)
{
    return listener->type() == PythonEventListenerType
        ? static_cast<const PythonEventListener*>(listener)
        : 0;
}

void PythonEventListener::handleEvent(WebCore::ScriptExecutionContext*,
                                      WebCore::Event* event)
{
    printf("PythonEventListener::handleEvent() = %p\n", this);
    PyObject* pev = WebKit::toPython(event);
    PyObject* arglist = Py_BuildValue((char*)"(O)", pev);
    PyGILState_STATE __py_state;
    __py_state = PyGILState_Ensure();
    PyObject* result = PyObject_CallObject(m_callback, arglist);
    PyGILState_Release(__py_state);
    Py_DECREF(arglist);
    Py_DECREF(pev);
    if (result == NULL)
    {
        fprintf(stderr, "Exception occurred while handling event\n");
        __py_state = PyGILState_Ensure();
        PyErr_Print();
        PyGILState_Release(__py_state);
        return;
    }
    /* Here maybe use the result */
    Py_DECREF(result);
    return;
}


bool PythonEventListener::operator==(const EventListener& listener)
{
    const PythonEventListener* pyEventListener;
    pyEventListener = PythonEventListener::cast(&listener);
    if (pyEventListener)
        return m_callback == pyEventListener->m_callback;

    return false;
}
