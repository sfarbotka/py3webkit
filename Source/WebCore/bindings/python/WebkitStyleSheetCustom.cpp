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
 * with JSStyleSheetCustom.cpp.  any additions to JSStyleSheetCustom.cpp
 * will also require the EXACT same additions, here.
 *
 * FIXME: there should have been no need to duplicate the functionality behind
 * JSDOMBinding.cpp and call it PythonBinding.cpp in the first place, and
 * there should be no need for this file; the functionality should be
 * merged into common code, as it does exactly the same thing.
 */

#include <Python.h>

#include "config.h"

#include "CString.h"
#include "CSSStyleSheet.h"
#include "PythonBinding.h"

namespace WebKit {

using namespace WebCore;

PyObject* pywrapCSSStyleSheet(CSSStyleSheet*);
PyObject* pywrapStyleSheet(StyleSheet*);

PyObject* toPython(StyleSheet* styleSheet)
{
    if (!styleSheet)
        Py_RETURN_NONE;

    PyObject* pobj = PythonObjectCache::getDOMObject(styleSheet);
    if (pobj)
        return pobj;

    PyObject* ret;
    if (styleSheet->isCSSStyleSheet())
        ret = pywrapCSSStyleSheet(static_cast<CSSStyleSheet*>(styleSheet));
    else
        ret = pywrapStyleSheet(styleSheet);

    return PythonObjectCache::putDOMObject(styleSheet, ret);
}

} // namespace WebKit

