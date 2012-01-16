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
 * with JSHTMLCollectionCustom.cpp.  any additions to
 * JSHTMLCollectionCustom.cpp will also require the EXACT same additions, here.
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

#include "Node.h"
#include "StaticNodeList.h"

#include "HTMLCollection.h"
#include "HTMLOptionsCollection.h"
#include "HTMLAllCollection.h"

#if ENABLE(MICRODATA)
#include "HTMLPropertiesCollection.h"
#endif

#include <wtf/Vector.h>
#include <wtf/text/CString.h>

#include "PyDOMObject.h"



namespace WebKit {

using namespace WebCore;

HTMLCollection *coreHTMLCollection(PyDOMObject*);
PyObject* toPython(WebCore::Node* obj);
PyObject* toPython(WebCore::NodeList* obj);

PyObject* pywrapHTMLCollection(HTMLCollection*);
PyObject* pywrapHTMLOptionsCollection(HTMLOptionsCollection*);
PyObject* pywrapHTMLAllCollection(HTMLAllCollection*);
#if ENABLE(MICRODATA)
PyObject* pywrapHTMLPropertiesCollection(HTMLPropertiesCollection*);
#endif

static PyObject* getNamedItems(PyDOMObject* self, PyObject* obj)
{
    Vector<RefPtr<Node> > namedItems;
    PyObject* uobj;
    PyObject* sobj;
    char* name;

    uobj = PyObject_Str(obj);
    if (!uobj)
        return NULL;

    sobj = PyUnicode_AsUTF8String(uobj);
    Py_DECREF(uobj);
    if (!sobj)
        return NULL;

    name = PyBytes_AsString(sobj);
    Py_DECREF(sobj);
    if (!name)
        return NULL;


    WTF::String cvt_name = WTF::String::fromUTF8((const char*)name);
    coreHTMLCollection(self)->namedItems(cvt_name, namedItems);

    if (namedItems.isEmpty())
    {
        Py_INCREF(Py_None);
        return Py_None;
    }

    if (namedItems.size() == 1)
        return toPython(namedItems[0].get());

    return toPython(StaticNodeList::adopt(namedItems).get());
}

PyObject * _wrap_HTMLCollection_item(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"index", NULL };
    PyObject* oindex;
    unsigned long index;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"k:pywebkit.HTMLCollection.item", kwlist, &index))
        return NULL;

    WebCore::Node* ret = coreHTMLCollection(self)->item(index);
    return toPython(ret);
}


PyObject* _wrap_HTMLCollection_namedItem(PyDOMObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { (char*)"name", NULL };
    PyObject* name;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"O:pywebkit.HTMLAllCollection.namedItem", kwlist, &name))
        return NULL;

    return getNamedItems(self, name);
}

PyObject* toPython(HTMLCollection* collection)
{
    if (!collection)
        Py_RETURN_NONE;

    PyObject* pobj = PythonObjectCache::getDOMObject(collection);

    if (pobj)
        return pobj;

    PyObject* ret;
    switch (collection->type()) {
        case SelectOptions:
            ret = pywrapHTMLOptionsCollection(static_cast<HTMLOptionsCollection*>(collection));
            break;
        case DocAll:
            ret = pywrapHTMLAllCollection(static_cast<HTMLAllCollection*>(collection));
            break;
#if ENABLE(MICRODATA)
        case ItemProperties:
            ret = pywrapHTMLPropertiesCollection(static_cast<HTMLPropertiesCollection*>(collection));
            break;
#endif
        default:
            ret = pywrapHTMLCollection(static_cast<HTMLCollection*>(collection));
            break;
    }

    return PythonObjectCache::putDOMObject(collection, ret);
}


} // namespace WebKit

