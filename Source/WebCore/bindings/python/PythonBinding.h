/*
 *  Copyright (C) 1999-2001 Harri Porten (porten@kde.org)
 *  Copyright (C) 2003, 2004, 2005, 2006, 2008 Apple Inc. All rights reserved.
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

#ifndef PythonDOMBinding_h
#define PythonDOMBinding_h

#include <Python.h>

#include "CString.h"
#include "CSSRule.h"
#include "CSSValue.h"
#include "Element.h"
#include "Event.h"
#include "EventTarget.h"
#include "HTMLCollection.h"
#include "Node.h"
#include "StyleSheet.h"
#include "Text.h"
#include <wtf/Noncopyable.h>

namespace WebCore {

    class Document;
    class Event;
    class Frame;
    class Node;

#if ENABLE(SVG)
    class SVGElement;
#endif
} // namespace WebCore

namespace WebKit {
    PyObject* toPython(WebCore::CSSRule*);
    PyObject* toPython(WebCore::CSSValue*);
    PyObject* toPython(WebCore::Document*);
    PyObject* toPython(WebCore::Element*);
    PyObject* toPython(WebCore::Event*);
    PyObject* toPython(WebCore::EventTarget*);
    PyObject* toPython(WebCore::HTMLCollection*);
    PyObject* toPython(WebCore::Node*);
    PyObject* toPython(WebCore::StyleSheet*);
    PyObject* toPython(WebCore::Text*);

    class PythonObjectCache {
    public:
        static PyObject* getDOMObject(void *);
        static PyObject* putDOMObject(void *, PyObject*);
        static void forgetDOMObject(void *);
    };
} // namespace WebKit

#endif // PythonDOMBinding_h
