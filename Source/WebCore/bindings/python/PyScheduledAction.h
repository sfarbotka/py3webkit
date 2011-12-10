#ifndef PySheduledAction_h
#define PySheduledAction_h


#include "Frame.h"
#include "ScheduledActionBase.h"
#include "PyDOMObject.h"


namespace WebCore
{

    class PyScheduledAction : public ScheduledActionBase
    {
    public:
        static PassOwnPtr<PyScheduledAction> create(PyObject* callback);

        void execute(WebCore::ScriptExecutionContext*);
        virtual ~PyScheduledAction();

    private:
        PyObject *m_callback;
        PyScheduledAction(PyObject *callback);

        void execute(Document*);
    };

}; // namespace WebCore


extern PyTypeObject *PtrPyPyScheduledAction_Type;

namespace WebKit
{

PassOwnPtr<WebCore::ScheduledActionBase> corePyScheduledAction(PyDOMObject* request);
PyObject* pywrapPyScheduledAction(WebCore::ScheduledActionBase* coreObject);
PyObject* toPython(WebCore::ScheduledActionBase*);
#define PyPyScheduledAction PyDOMObject


}; // namespace WebKit


extern "C" {


int PyScheduledAction_init(WebCore::ScheduledActionBase *self, PyObject *args, PyObject *kwargs);

void dealloc_PyScheduledAction(PyObject *self);

extern PyTypeObject G_GNUC_INTERNAL PyPyScheduledAction_Type;

}; // extern "C"

#endif // PySheduledAction_h
