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
 * with JSDocumentCustom.cpp.  any additions to JSDocumentCustom.cpp
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
#include "PythonBinding.h"
#include "Document.h"
#include "HTMLDocument.h"

#if ENABLE(SVG)
#ifdef __TODO_BUG_20586__ /* XXX TODO - see #20586 */
#include "SVGDocument.h"
#endif
#endif

namespace WebKit {

using namespace WebCore;

PyObject* pywrapHTMLDocument(HTMLDocument*);
PyObject* pywrapDocument(Document*);

#if ENABLE(SVG)
#ifdef __TODO_BUG_20586__ /* XXX TODO - see #20586 */
PyObject* pywrapSVGDocument(SVGDocument*);
#endif
#endif

PyObject* toPython(Document* doc)
{
    if (!doc)
        Py_RETURN_NONE;

    PyObject* pobj = PythonObjectCache::getDOMObject(doc);
    if (pobj)
        return pobj;

    PyObject* ret;

    if (doc->isHTMLDocument())
        ret = pywrapHTMLDocument(static_cast<HTMLDocument*>(doc));
#if ENABLE(SVG)
    else if (doc->isSVGDocument())
    {
        return NULL; /* XXX TODO - see #20586 */
#ifdef __TODO_BUG_20586__ /* XXX TODO - see #20586 */
        ret = pywrapSVGDocument(static_cast<SVGDocument*>(doc));
#endif
    }
#endif
    else
        ret = pywrapDocument(doc);

    return PythonObjectCache::putDOMObject(doc, ret);
}


} // namespace WebKit

