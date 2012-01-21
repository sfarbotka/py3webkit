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

#include "Python.h"
#include "config.h"

#include <wtf/text/CString.h>
#include "DOMFormData.h"
#include "Blob.h"

struct PyDOMObject;


extern "C" PyTypeObject PyDOMDOMFormData_Type;
extern "C" PyTypeObject PyDOMBlob_Type;

namespace WebKit {

WebCore::DOMFormData* coreDOMFormData(PyDOMObject*);
WebCore::Blob* coreBlob(PyDOMObject*);



PyObject * _wrap_DOMFormData_append(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"name", (char*)"value", (char*)"filename", NULL };
    char *name = NULL;
    PyDOMObject *value = NULL;
    char *filename = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"|sOs:pywebkit.DOMFormData.append", kwlist, &name, &value, &filename))
        return NULL;

    if (name && value)
    {
        WTF::String cvt_name = WTF::String::fromUTF8((const char*)name);
        if (PyObject_TypeCheck(value, &PyDOMBlob_Type))
        {
            WTF::String cvt_fname = WTF::String::fromUTF8(name ? (const char*)name : "");
            coreDOMFormData(self)->append(cvt_name, coreBlob(value), cvt_fname);
        }
        else
        {
            PyObject* ss = PyObject_Str((PyObject*)value);
            PyObject* s = PyUnicode_AsUTF8String(ss);

            WTF::String cvt_value = WTF::String::fromUTF8(PyBytes_AsString(s));

            coreDOMFormData(self)->append(cvt_name, cvt_value);

            Py_DECREF(s);
            Py_DECREF(ss);
        }
    }

    Py_INCREF(Py_None);
    return Py_None;
}

} // namespace WebKit
