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

#ifndef PyDOMObject_h
#define PyDOMObject_h

typedef struct
{
    PyObject_HEAD
    void* ptr;
    unsigned long iter_index;
    unsigned long iter_count;
} PyDOMObject;

extern PyTypeObject PyDOMObject_Type;

PyObject* DOMObject_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
PyObject* DOMObject_getptr(PyDOMObject *self, PyObject *);
PyObject* DOMObject_setptr(PyDOMObject *self, PyObject *args, PyObject *kwargs);

PyObject* PyDOMObject_new(PyTypeObject *type, void *ptr);

#endif //PyDOMObject_h
