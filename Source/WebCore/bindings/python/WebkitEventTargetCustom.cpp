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

/* PLEASE NOTE: this file needs to be kept up-to-date in EXACT accordance
 * with JSCustomEvent.cpp.  any additions to JSCustomEvent.cpp will also
 * require the EXACT same additions, here.
 *
 * FIXME: there should have been no need to duplicate the functionality behind
 * JSDOMBinding.cpp and call it PythonBinding.cpp in the first place, and
 * there should be no need for this file; the functionality should be
 * merged into common code, as it does exactly the same thing.
 */

#include <Python.h>

#include "config.h"

#include "CString.h"
#include "PythonBinding.h"
#include "XMLHttpRequest.h"
#include "XMLHttpRequestUpload.h"

#if ENABLE(OFFLINE_WEB_APPLICATIONS)
#include "DOMApplicationCache.h"
#endif

namespace WebKit {

using namespace WebCore;

/* derived sources auto-generated */
PyObject* toPython(XMLHttpRequestUpload* obj);

PyObject* toPython(EventTarget* target)
{
    if (!target)
        Py_RETURN_NONE;

#ifdef __TODO_BUG_20586__ /* TODO - see #20586 */
#if ENABLE(SVG)
    // SVGElementInstance supports both toSVGElementInstance and
    // toNode since so much mouse handling code depends on toNode
    // returning a valid node.
    SVGElementInstance* instance = target->toSVGElementInstance();
    if (instance)
        return toPython(exec, instance);
#endif
#endif

    Node* node = target->toNode();
    if (node)
        return toPython(node);

    if (XMLHttpRequest* xhr = target->toXMLHttpRequest())
        // XMLHttpRequest is always created via Python, so we don't need
        // to use cacheDOMObject() here.
        return PythonObjectCache::getDOMObject(xhr);

    if (XMLHttpRequestUpload* upload = target->toXMLHttpRequestUpload())
        return toPython(upload);

#if ENABLE(OFFLINE_WEB_APPLICATIONS)
    if (DOMApplicationCache* cache = target->toDOMApplicationCache())
        // DOMApplicationCache is always created via Python, so we don't
        // need to use cacheDOMObject() here.
        return PythonObjectCache::getDOMObject(cache);
#endif

    ASSERT_NOT_REACHED();
    Py_RETURN_NONE;
}

} // namespace WebKit

