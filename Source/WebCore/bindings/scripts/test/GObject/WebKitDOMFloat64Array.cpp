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
#include "Float64Array.h"
#include "Int32Array.h"
#include "JSMainThreadExecState.h"
#include "WebKitDOMBinding.h"
#include "gobject/ConvertToUTF8String.h"
#include "webkit/WebKitDOMFloat32Array.h"
#include "webkit/WebKitDOMFloat32ArrayPrivate.h"
#include "webkit/WebKitDOMFloat64Array.h"
#include "webkit/WebKitDOMFloat64ArrayPrivate.h"
#include "webkit/WebKitDOMInt32Array.h"
#include "webkit/WebKitDOMInt32ArrayPrivate.h"
#include "webkitdefines.h"
#include "webkitglobalsprivate.h"
#include "webkitmarshal.h"

namespace WebKit {
    
WebKitDOMFloat64Array* kit(WebCore::Float64Array* obj)
{
    g_return_val_if_fail(obj, 0);

    if (gpointer ret = DOMObjectCache::get(obj))
        return static_cast<WebKitDOMFloat64Array*>(ret);

    return static_cast<WebKitDOMFloat64Array*>(DOMObjectCache::put(obj, WebKit::wrapFloat64Array(obj)));
}
    
} // namespace WebKit //

WebKitDOMInt32Array*
webkit_dom_float64array_foo(WebKitDOMFloat64Array* self, WebKitDOMFloat32Array* array)
{
    g_return_val_if_fail(self, 0);
    WebCore::JSMainThreadNullState state;
    WebCore::Float64Array * item = WebKit::core(self);
    g_return_val_if_fail(array, 0);
    WebCore::Float32Array * converted_array = NULL;
    if (array != NULL) {
        converted_array = WebKit::core(array);
        g_return_val_if_fail(converted_array, 0);
    }
    PassRefPtr<WebCore::Int32Array> g_res = WTF::getPtr(item->foo(converted_array));
    WebKitDOMInt32Array* res = WebKit::kit(g_res.get());
    return res;
}


G_DEFINE_TYPE(WebKitDOMFloat64Array, webkit_dom_float64array, WEBKIT_TYPE_DOM_ARRAY_BUFFER_VIEW)

namespace WebKit {

WebCore::Float64Array* core(WebKitDOMFloat64Array* request)
{
    g_return_val_if_fail(request, 0);

    WebCore::Float64Array* coreObject = static_cast<WebCore::Float64Array*>(WEBKIT_DOM_OBJECT(request)->coreObject);
    g_return_val_if_fail(coreObject, 0);

    return coreObject;
}

} // namespace WebKit
enum {
    PROP_0,
};


static void webkit_dom_float64array_finalize(GObject* object)
{
    WebKitDOMObject* dom_object = WEBKIT_DOM_OBJECT(object);
    
    if (dom_object->coreObject) {
        WebCore::Float64Array* coreObject = static_cast<WebCore::Float64Array *>(dom_object->coreObject);

        WebKit::DOMObjectCache::forget(coreObject);
        coreObject->deref();

        dom_object->coreObject = NULL;
    }

    G_OBJECT_CLASS(webkit_dom_float64array_parent_class)->finalize(object);
}

static void webkit_dom_float64array_set_property(GObject* object, guint prop_id, const GValue* value, GParamSpec* pspec)
{
    WebCore::JSMainThreadNullState state;
    switch (prop_id) {
    default:
        G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
        break;
    }
}


static void webkit_dom_float64array_get_property(GObject* object, guint prop_id, GValue* value, GParamSpec* pspec)
{
    WebCore::JSMainThreadNullState state;
    switch (prop_id) {
    default:
        G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
        break;
    }
}


static void webkit_dom_float64array_constructed(GObject* object)
{

    if (G_OBJECT_CLASS(webkit_dom_float64array_parent_class)->constructed)
        G_OBJECT_CLASS(webkit_dom_float64array_parent_class)->constructed(object);
}

static void webkit_dom_float64array_class_init(WebKitDOMFloat64ArrayClass* requestClass)
{
    GObjectClass *gobjectClass = G_OBJECT_CLASS(requestClass);
    gobjectClass->finalize = webkit_dom_float64array_finalize;
    gobjectClass->set_property = webkit_dom_float64array_set_property;
    gobjectClass->get_property = webkit_dom_float64array_get_property;
    gobjectClass->constructed = webkit_dom_float64array_constructed;



}

static void webkit_dom_float64array_init(WebKitDOMFloat64Array* request)
{
}

namespace WebKit {
WebKitDOMFloat64Array* wrapFloat64Array(WebCore::Float64Array* coreObject)
{
    g_return_val_if_fail(coreObject, 0);

    /* We call ref() rather than using a C++ smart pointer because we can't store a C++ object
     * in a C-allocated GObject structure.  See the finalize() code for the
     * matching deref().
     */
    coreObject->ref();

    return  WEBKIT_DOM_FLOAT64ARRAY(g_object_new(WEBKIT_TYPE_DOM_FLOAT64ARRAY,
                                               "core-object", coreObject, NULL));
}
} // namespace WebKit
