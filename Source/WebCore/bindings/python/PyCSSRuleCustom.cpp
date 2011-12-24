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
 * with JSCSSRuleCustom.cpp.  any additions to JSCSSRuleCustom.cpp will also
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
#include "CSSRule.h"
#include "CSSCharsetRule.h"
#include "CSSFontFaceRule.h"
#include "CSSImportRule.h"
#include "CSSMediaRule.h"
#include "CSSPageRule.h"
#include "CSSStyleRule.h"
#include "PythonBinding.h"

namespace WebKit {

using namespace WebCore;

extern PyObject* pywrapCSSStyleRule(CSSStyleRule*);
extern PyObject* pywrapCSSMediaRule(CSSMediaRule*);
extern PyObject* pywrapCSSFontFaceRule(CSSFontFaceRule*);
extern PyObject* pywrapCSSPageRule(CSSPageRule*);
extern PyObject* pywrapCSSImportRule(CSSImportRule*);
extern PyObject* pywrapCSSCharsetRule(CSSCharsetRule*);
extern PyObject* pywrapCSSRule(CSSRule*);

PyObject* toPython(CSSRule* rule)
{
    if (!rule)
        Py_RETURN_NONE;

    PyObject* pobj = PythonObjectCache::getDOMObject(rule);

    if (pobj)
        return pobj;

    PyObject* ret;
    switch (rule->type()) {
        case CSSRule::STYLE_RULE:
            ret = pywrapCSSStyleRule(static_cast<CSSStyleRule*>(rule));
            break;
        case CSSRule::MEDIA_RULE:
            ret = pywrapCSSMediaRule(static_cast<CSSMediaRule*>(rule));
            break;
        case CSSRule::FONT_FACE_RULE:
            ret = pywrapCSSFontFaceRule(static_cast<CSSFontFaceRule*>(rule));
            break;
        case CSSRule::PAGE_RULE:
            ret = pywrapCSSPageRule(static_cast<CSSPageRule*>(rule));
            break;
        case CSSRule::IMPORT_RULE:
            ret = pywrapCSSImportRule(static_cast<CSSImportRule*>(rule));
            break;
        case CSSRule::CHARSET_RULE:
            ret = pywrapCSSCharsetRule(static_cast<CSSCharsetRule*>(rule));
            break;
        default:
            ret = pywrapCSSRule(rule);
            break;
    }

    return PythonObjectCache::putDOMObject(rule, ret);
}

} // namespace WebKit
