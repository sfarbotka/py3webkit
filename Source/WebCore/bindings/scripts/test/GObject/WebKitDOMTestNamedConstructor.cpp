/*
    This file is part of the WebKit open source project.
    This file has been generated by generate-bindings.pl. DO NOT MODIFY!

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Library General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Library General Public License for more details.

    You should have received a copy of the GNU Library General Public License
    along with this library; see the file COPYING.LIB.  If not, write to
    the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
    Boston, MA 02110-1301, USA.
*/

#include <glib-object.h>
#include "config.h"

#include <wtf/GetPtr.h>
#include <wtf/RefPtr.h>
#include "DOMObjectCache.h"
#include "ExceptionCode.h"
#include "JSMainThreadExecState.h"
#include "TestNamedConstructor.h"
#include "WebKitDOMBinding.h"
#include "gobject/ConvertToUTF8String.h"
#include "webkit/WebKitDOMTestNamedConstructor.h"
#include "webkit/WebKitDOMTestNamedConstructorPrivate.h"
#include "webkitdefines.h"
#include "webkitglobalsprivate.h"
#include "webkitmarshal.h"

namespace WebKit {
    
WebKitDOMTestNamedConstructor* kit(WebCore::TestNamedConstructor* obj)
{
    g_return_val_if_fail(obj, 0);

    if (gpointer ret = DOMObjectCache::get(obj))
        return static_cast<WebKitDOMTestNamedConstructor*>(ret);

    return static_cast<WebKitDOMTestNamedConstructor*>(DOMObjectCache::put(obj, WebKit::wrapTestNamedConstructor(obj)));
}
    
} // namespace WebKit //


G_DEFINE_TYPE(WebKitDOMTestNamedConstructor, webkit_dom_test_named_constructor, WEBKIT_TYPE_DOM_OBJECT)

namespace WebKit {

WebCore::TestNamedConstructor* core(WebKitDOMTestNamedConstructor* request)
{
    g_return_val_if_fail(request, 0);

    WebCore::TestNamedConstructor* coreObject = static_cast<WebCore::TestNamedConstructor*>(WEBKIT_DOM_OBJECT(request)->coreObject);
    g_return_val_if_fail(coreObject, 0);

    return coreObject;
}

} // namespace WebKit
enum {
    PROP_0,
};


static void webkit_dom_test_named_constructor_finalize(GObject* object)
{
    WebKitDOMObject* dom_object = WEBKIT_DOM_OBJECT(object);
    
    if (dom_object->coreObject) {
        WebCore::TestNamedConstructor* coreObject = static_cast<WebCore::TestNamedConstructor *>(dom_object->coreObject);

        WebKit::DOMObjectCache::forget(coreObject);
        coreObject->deref();

        dom_object->coreObject = NULL;
    }

    G_OBJECT_CLASS(webkit_dom_test_named_constructor_parent_class)->finalize(object);
}

static void webkit_dom_test_named_constructor_set_property(GObject* object, guint prop_id, const GValue* value, GParamSpec* pspec)
{
    WebCore::JSMainThreadNullState state;
    switch (prop_id) {
    default:
        G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
        break;
    }
}


static void webkit_dom_test_named_constructor_get_property(GObject* object, guint prop_id, GValue* value, GParamSpec* pspec)
{
    WebCore::JSMainThreadNullState state;
    switch (prop_id) {
    default:
        G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
        break;
    }
}


static void webkit_dom_test_named_constructor_constructed(GObject* object)
{

    if (G_OBJECT_CLASS(webkit_dom_test_named_constructor_parent_class)->constructed)
        G_OBJECT_CLASS(webkit_dom_test_named_constructor_parent_class)->constructed(object);
}

static void webkit_dom_test_named_constructor_class_init(WebKitDOMTestNamedConstructorClass* requestClass)
{
    GObjectClass *gobjectClass = G_OBJECT_CLASS(requestClass);
    gobjectClass->finalize = webkit_dom_test_named_constructor_finalize;
    gobjectClass->set_property = webkit_dom_test_named_constructor_set_property;
    gobjectClass->get_property = webkit_dom_test_named_constructor_get_property;
    gobjectClass->constructed = webkit_dom_test_named_constructor_constructed;



}

static void webkit_dom_test_named_constructor_init(WebKitDOMTestNamedConstructor* request)
{
}

namespace WebKit {
WebKitDOMTestNamedConstructor* wrapTestNamedConstructor(WebCore::TestNamedConstructor* coreObject)
{
    g_return_val_if_fail(coreObject, 0);

    /* We call ref() rather than using a C++ smart pointer because we can't store a C++ object
     * in a C-allocated GObject structure.  See the finalize() code for the
     * matching deref().
     */
    coreObject->ref();

    return  WEBKIT_DOM_TEST_NAMED_CONSTRUCTOR(g_object_new(WEBKIT_TYPE_DOM_TEST_NAMED_CONSTRUCTOR,
                                               "core-object", coreObject, NULL));
}
} // namespace WebKit
