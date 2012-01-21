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
