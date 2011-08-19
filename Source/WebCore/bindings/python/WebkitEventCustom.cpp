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
 * with JSEventCustom.cpp.  any additions to JSEventCustom.cpp will also
 * require the EXACT same additions, here.
 *
 * FIXME: there should have been no need to duplicate the functionality behind
 * JSDOMBinding.cpp and call it PythonBinding.cpp in the first place, and
 * there should be no need for this file; the functionality should be
 * merged into common code, as it does exactly the same thing.
 */

#include <Python.h>

#include "config.h"

#include "PythonBinding.h"

#include "CString.h"
#include "Event.h"
#include "KeyboardEvent.h"
#include "MessageEvent.h"
#include "MouseEvent.h"
#include "MutationEvent.h"
#include "OverflowEvent.h"
#include "ProgressEvent.h"
#include "TextEvent.h"
#include "UIEvent.h"
#include "WebKitAnimationEvent.h"
#include "WebKitTransitionEvent.h"
#include "WheelEvent.h"
#include "XMLHttpRequestProgressEvent.h"

#if ENABLE(DOM_STORAGE)
#include "StorageEvent.h"
#endif

#if ENABLE(SVG)
#ifdef __TODO_BUG_20586__ /* TODO - see #20586 */
#include "SVGZoomEvent.h"
#endif
#endif

namespace WebKit {

using namespace WebCore;

#if ENABLE(SVG)
#ifdef __TODO_BUG_20586__ /* TODO - see #20586 */
PyObject* pywrapSVGZoomEvent(SVGZoomEvent*);
#endif
#endif

PyObject* pywrapEvent(Event*);
PyObject* pywrapKeyboardEvent(KeyboardEvent*);
PyObject* pywrapTextEvent(TextEvent*);
PyObject* pywrapMouseEvent(MouseEvent*);
PyObject* pywrapWheelEvent(WheelEvent*);
PyObject* pywrapUIEvent(UIEvent*);
PyObject* pywrapMutationEvent(MutationEvent*);
PyObject* pywrapOverflowEvent(OverflowEvent*);
PyObject* pywrapMessageEvent(MessageEvent*);
PyObject* pywrapXMLHttpRequestProgressEvent(XMLHttpRequestProgressEvent*);
PyObject* pywrapProgressEvent(ProgressEvent*);
PyObject* pywrapStorageEvent(StorageEvent*);
PyObject* pywrapWebKitAnimationEvent(WebKitAnimationEvent*);
PyObject* pywrapWebKitTransitionEvent(WebKitTransitionEvent*);

PyObject* toPython(Event* event)
{
    if (!event)
        Py_RETURN_NONE;

    PyObject* pobj = PythonObjectCache::getDOMObject(event);
    if (pobj)
        return pobj;

    PyObject* ret;
    if (event->isUIEvent()) {
        if (event->isKeyboardEvent())
            ret = pywrapKeyboardEvent(static_cast<KeyboardEvent*>(event));
        else if (event->isTextEvent())
            ret = pywrapTextEvent(static_cast<TextEvent*>(event));
        else if (event->isMouseEvent())
            ret = pywrapMouseEvent(static_cast<MouseEvent*>(event));
        else if (event->isWheelEvent())
            ret = pywrapWheelEvent(static_cast<WheelEvent*>(event));
#if ENABLE(SVG)
        else if (event->isSVGZoomEvent())
        {
            return NULL; /* TODO - see #20586 */
#ifdef __TODO_BUG_20586__ /* TODO - see #20586 */
            ret = pywrapSVGZoomEvent(static_cast<SVGZoomEvent*>(event), 0);
#endif
        }
#endif
        else
            ret = pywrapUIEvent(static_cast<UIEvent*>(event));
    } else if (event->isMutationEvent())
        ret = pywrapMutationEvent(static_cast<MutationEvent*>(event));
    else if (event->isOverflowEvent())
        ret = pywrapOverflowEvent(static_cast<OverflowEvent*>(event));
    else if (event->isMessageEvent())
        ret = pywrapMessageEvent(static_cast<MessageEvent*>(event));
    else if (event->isProgressEvent()) {
        if (event->isXMLHttpRequestProgressEvent())
            ret = pywrapXMLHttpRequestProgressEvent(static_cast<XMLHttpRequestProgressEvent*>(event));
        else
            ret = pywrapProgressEvent(static_cast<ProgressEvent*>(event));
    }
#if ENABLE(DOM_STORAGE)
    else if (event->isStorageEvent())
        ret = pywrapStorageEvent(static_cast<StorageEvent*>(event));
#endif
    else if (event->isWebKitAnimationEvent())
        ret = pywrapWebKitAnimationEvent(static_cast<WebKitAnimationEvent*>(event));
    else if (event->isWebKitTransitionEvent())
        ret = pywrapWebKitTransitionEvent(static_cast<WebKitTransitionEvent*>(event));
    else
        ret = pywrapEvent(event);

    return PythonObjectCache::putDOMObject(event, ret);
}

} // namespace WebKit

