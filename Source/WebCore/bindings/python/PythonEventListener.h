#ifndef PythonEventListener_h
#define PythonEventListener_h

#include "EventListener.h"



class PythonEventListener : public WebCore::EventListener
{
public:
    static PassRefPtr<PythonEventListener> create(PyObject* callback);

    virtual void handleEvent(WebCore::ScriptExecutionContext*, WebCore::Event*);
    virtual bool operator==(const EventListener& other);
    static const PythonEventListener* cast(const EventListener* listener);

private:
    PythonEventListener(PyObject *callback);
    ~PythonEventListener();

    PyObject *m_callback;
};


extern "C"
{

WebCore::EventListener* webkit_create_python_event_listener(PyObject *callback);
void webkit_delete_python_event_listener(WebCore::EventListener *l);

} //extern "C"




#endif //PythonEventListener_h
