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
 * with JSElementCustom.cpp.  any additions to JSElementCustom.cpp will also
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
#include "Node.h"

struct PyDOMObject;


extern "C" PyTypeObject PyDOMNode_Type;
extern "C" PyTypeObject *PtrPyDOMNode_Type;

void py_wk_exc(WebCore::ExceptionCode &ec);

namespace WebKit {

WebCore::Node* coreNode(PyDOMObject*);


PyObject * _wrap_Node_appendChild(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"newChild", NULL };
    PyDOMObject *child = NULL;
    WebCore::ExceptionCode ec = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"O!:pywebkit.Node.appendChild", kwlist, PtrPyDOMNode_Type, &child))
        return NULL;

    bool ok = coreNode(self)->appendChild(coreNode(child), ec, true);
    if (ec)
    {
        py_wk_exc(ec);
        return NULL;
    }
    
    if (ok)
    {
        Py_INCREF(child);
        return (PyObject*)child;
    }
    
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject * _wrap_Node_removeChild(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"oldChild", NULL };
    PyDOMObject *child = NULL;
    WebCore::ExceptionCode ec = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"O!:pywebkit.Node.appendChild", kwlist, PtrPyDOMNode_Type, &child))
        return NULL;

    bool ok = coreNode(self)->removeChild(coreNode(child), ec);
    if (ec)
    {
        py_wk_exc(ec);
        return NULL;
    }
    
    if (ok)
    {
        Py_INCREF(child);
        return (PyObject*)child;
    }
    
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject * _wrap_Node_replaceChild(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"newChild", (char*)"oldChild", NULL };
    PyDOMObject *nchild = NULL;
    PyDOMObject *ochild = NULL;
    WebCore::ExceptionCode ec = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"O!O!:pywebkit.Node.appendChild", kwlist, PtrPyDOMNode_Type, &nchild, PtrPyDOMNode_Type, &ochild))
        return NULL;

    bool ok = coreNode(self)->replaceChild(coreNode(nchild), coreNode(ochild), ec, true);
    if (ec)
    {
        py_wk_exc(ec);
        return NULL;
    }
    
    if (ok)
    {
        Py_INCREF(ochild);
        return (PyObject*)ochild;
    }
    
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject * _wrap_Node_insertBefore(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"newChild", (char*)"refChild", NULL };
    PyDOMObject *nchild = NULL;
    PyDOMObject *rchild = NULL;
    WebCore::ExceptionCode ec = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"O!O!:pywebkit.Node.appendChild", kwlist, PtrPyDOMNode_Type, &nchild, PtrPyDOMNode_Type, &rchild))
        return NULL;

    bool ok = coreNode(self)->insertBefore(coreNode(nchild), coreNode(rchild), ec, true);
    if (ec)
    {
        py_wk_exc(ec);
        return NULL;
    }
    
    if (ok)
    {
        Py_INCREF(rchild);
        return (PyObject*)rchild;
    }
    
    Py_INCREF(Py_None);
    return Py_None;
}



} // namespace WebKit

