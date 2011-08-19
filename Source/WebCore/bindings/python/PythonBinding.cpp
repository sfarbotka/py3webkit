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

/* 
 * FIXME: there should have been no need to duplicate the functionality behind
 * JSDOMBinding.cpp and call it PythonBinding.cpp in the first place.
 * There should be no need for this file; the functionality should be
 * merged into common code, as it does exactly the same thing.
 *
 * however, it is being added near-verbatim-cut-paste because a) that is
 * easier b) it's exactly what the objective-c bindings do
 *
 */

// gcc 3.x can't handle including the HashMap pointer specialization
// in this file
#if defined __GNUC__ && !defined __GLIBCXX__ // less than gcc 3.4
#define HASH_MAP_PTR_SPEC_WORKAROUND 1
#endif

#include <Python.h>

#include "config.h"

#include "CString.h"
#include "PythonBinding.h"
#include "Attr.h"
#include "CDATASection.h"
#include "Comment.h"
#include "Document.h"
#include "DocumentType.h"
#include "DocumentFragment.h"
#include "PythonHTMLElementWrapperFactory.h"
#include "Element.h"
#include "Entity.h"
#include "EntityReference.h"
#include "Node.h"
#include "Notation.h"
#include "ProcessingInstruction.h"
#include "Text.h"
#include "HTMLElement.h"

namespace WebKit {

using namespace WebCore;

typedef HashMap<void*, PyObject*> DOMObjectMap;

static DOMObjectMap& domObjects()
{
    static DOMObjectMap staticDOMObjects;
    return staticDOMObjects;
}

PyObject* PythonObjectCache::getDOMObject(void* objectHandle)
{
    PyObject* ret = domObjects().get(objectHandle);
    if (ret)
    {
        /* when getting a python DOM object: if it exists, always always
           the ref count will need to be increased.
         */
        Py_INCREF(ret);
    }
    return ret;
}

PyObject* PythonObjectCache::putDOMObject(void* objectHandle, PyObject* pywrapper)
{
    /* put is only used on new items.  therefore we do not do a
       Py_INCREF because new PyObjects always get created with an
       initial refcount of 1
     */
    domObjects().set(objectHandle, pywrapper);
    return pywrapper;
}

void PythonObjectCache::forgetDOMObject(void* objectHandle)
{
    PyObject* ret = domObjects().take(objectHandle);
}

static PyObject* createWrapper(Node* node);

PyObject* toPythonNewlyCreated(Node* node)
{
    if (!node)
        Py_RETURN_NONE;

    return createWrapper(node);
}

PyObject* toPython(Node* node)
{
    if (!node)
    {
        Py_INCREF(Py_None);
        return Py_None;
    }

    PyObject* ret = PythonObjectCache::getDOMObject(node);
    if (ret)
        return ret;

    return createWrapper(node);
}

extern PyObject* pywrapElement(Element*);
extern PyObject* pywrapText(Text*);
extern PyObject* pywrapCDATASection(CDATASection*);
extern PyObject* pywrapAttr(Attr*);
extern PyObject* pywrapEntity(Entity*);
extern PyObject* pywrapProcessingInstruction(ProcessingInstruction*);
extern PyObject* pywrapComment(Comment*);
extern PyObject* pywrapDocumentType(DocumentType*);
extern PyObject* pywrapNotation(Notation*);
extern PyObject* pywrapDocumentFragment(DocumentFragment*);
extern PyObject* pywrapEntityReference(EntityReference*);
extern PyObject* pywrapNode(Node*);

static ALWAYS_INLINE PyObject* createWrapper(Node* node)
{
    ASSERT(node);
    ASSERT(!ScriptInterpreter::getDOMObject(node));

    PyObject* ret = NULL;

    switch (node->nodeType()) {
        case Node::ELEMENT_NODE:
            if (node->isHTMLElement())
                ret = createPythonHTMLElementWrapper(
                                        static_cast<HTMLElement*>(node));
#if ENABLE(SVG)
            else if (node->isSVGElement())
                return NULL; /* XXX TODO - see #20586 */
#ifdef __TODO_BUG_20586__ /* XXX TODO - see #20586 */
                ret = createPythonSVGElementWrapper(
                                        static_cast<SVGElement*>(node));
#endif
#endif
            else
                ret = pywrapElement(static_cast<Element*>(node));
            break;
        case Node::ATTRIBUTE_NODE:
            ret = pywrapAttr(static_cast<Attr*>(node));
            break;
        case Node::TEXT_NODE:
            ret = pywrapText(static_cast<Text*>(node));
            break;
        case Node::CDATA_SECTION_NODE:
            ret = pywrapCDATASection(static_cast<CDATASection*>(node));
            break;
        case Node::ENTITY_NODE:
            ret = pywrapEntity(static_cast<Entity*>(node));
            break;
        case Node::PROCESSING_INSTRUCTION_NODE:
            ret = pywrapProcessingInstruction(
                                    static_cast<ProcessingInstruction*>(node));
            break;
        case Node::COMMENT_NODE:
            ret = pywrapComment(static_cast<Comment*>(node));
            break;
        case Node::DOCUMENT_NODE:
            // we don't want to cache the document itself in
            // the per-document dictionary
            return toPython(static_cast<Document*>(node));
        case Node::DOCUMENT_TYPE_NODE:
            ret = pywrapDocumentType(static_cast<DocumentType*>(node));
            break;
        case Node::NOTATION_NODE:
            ret = pywrapNotation(static_cast<Notation*>(node));
            break;
        case Node::DOCUMENT_FRAGMENT_NODE:
            ret = pywrapDocumentFragment(static_cast<DocumentFragment*>(node));
            break;
        case Node::ENTITY_REFERENCE_NODE:
            ret = pywrapEntityReference(static_cast<EntityReference*>(node));
            break;
        default:
            ret = pywrapNode(node);
    }

    return PythonObjectCache::putDOMObject(node, ret);
}


} // namespace WebKit

