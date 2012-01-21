/*
 *  Copyright (C) 1999-2001 Harri Porten (porten@kde.org)
 *  Copyright (C) 2004, 2005, 2006, 2007, 2008 Apple Inc. All rights reserved.
 *  Copyright (C) 2007 Samuel Weinig <sam@webkit.org>
 *  Copyright (C) 2008 Martin Soto <soto@freedesktop.org>
 *  Copyright (C) 2010 Free Software Foundation
 *
 *  This library is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU Lesser General Public
 *  License as published by the Free Software Foundation; either
 *  version 2 of the License, or (at your option) any later version.
 *
 *  This library is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public
 *  License along with this library; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

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
