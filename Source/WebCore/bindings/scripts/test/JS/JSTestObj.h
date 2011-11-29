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

#ifndef JSTestObj_h
#define JSTestObj_h

#include "JSDOMBinding.h"
#include "TestObj.h"
#include <runtime/JSGlobalObject.h>
#include <runtime/JSObject.h>
#include <runtime/ObjectPrototype.h>

namespace WebCore {

class JSTestObj : public JSDOMWrapper {
public:
    typedef JSDOMWrapper Base;
    static JSTestObj* create(JSC::Structure* structure, JSDOMGlobalObject* globalObject, PassRefPtr<TestObj> impl)
    {
        JSTestObj* ptr = new (JSC::allocateCell<JSTestObj>(globalObject->globalData().heap)) JSTestObj(structure, globalObject, impl);
        ptr->finishCreation(globalObject->globalData());
        return ptr;
    }

    static JSC::JSObject* createPrototype(JSC::ExecState*, JSC::JSGlobalObject*);
    static bool getOwnPropertySlot(JSC::JSCell*, JSC::ExecState*, const JSC::Identifier& propertyName, JSC::PropertySlot&);
    static bool getOwnPropertyDescriptor(JSC::JSObject*, JSC::ExecState*, const JSC::Identifier& propertyName, JSC::PropertyDescriptor&);
    static void put(JSC::JSCell*, JSC::ExecState*, const JSC::Identifier& propertyName, JSC::JSValue, JSC::PutPropertySlot&);
    static const JSC::ClassInfo s_info;

    static JSC::Structure* createStructure(JSC::JSGlobalData& globalData, JSC::JSGlobalObject* globalObject, JSC::JSValue prototype)
    {
        return JSC::Structure::create(globalData, globalObject, prototype, JSC::TypeInfo(JSC::ObjectType, StructureFlags), &s_info);
    }

    static JSC::JSValue getConstructor(JSC::ExecState*, JSC::JSGlobalObject*);
    JSC::WriteBarrier<JSC::Unknown> m_cachedAttribute1;
    JSC::WriteBarrier<JSC::Unknown> m_cachedAttribute2;
    static void visitChildren(JSCell*, JSC::SlotVisitor&);


    // Custom attributes
    JSC::JSValue customAttr(JSC::ExecState*) const;
    void setCustomAttr(JSC::ExecState*, JSC::JSValue);

    // Custom functions
    JSC::JSValue customMethod(JSC::ExecState*);
    JSC::JSValue customMethodWithArgs(JSC::ExecState*);
    TestObj* impl() const { return m_impl; }
    void releaseImpl() { m_impl->deref(); m_impl = 0; }

private:
    TestObj* m_impl;
protected:
    JSTestObj(JSC::Structure*, JSDOMGlobalObject*, PassRefPtr<TestObj>);
    void finishCreation(JSC::JSGlobalData&);
    static const unsigned StructureFlags = JSC::OverridesGetOwnPropertySlot | JSC::OverridesVisitChildren | Base::StructureFlags;
};

class JSTestObjOwner : public JSC::WeakHandleOwner {
    virtual bool isReachableFromOpaqueRoots(JSC::Handle<JSC::Unknown>, void* context, JSC::SlotVisitor&);
    virtual void finalize(JSC::Handle<JSC::Unknown>, void* context);
};

inline JSC::WeakHandleOwner* wrapperOwner(DOMWrapperWorld*, TestObj*)
{
    DEFINE_STATIC_LOCAL(JSTestObjOwner, jsTestObjOwner, ());
    return &jsTestObjOwner;
}

inline void* wrapperContext(DOMWrapperWorld* world, TestObj*)
{
    return world;
}

JSC::JSValue toJS(JSC::ExecState*, JSDOMGlobalObject*, TestObj*);
TestObj* toTestObj(JSC::JSValue);

class JSTestObjPrototype : public JSC::JSNonFinalObject {
public:
    typedef JSC::JSNonFinalObject Base;
    static JSC::JSObject* self(JSC::ExecState*, JSC::JSGlobalObject*);
    static JSTestObjPrototype* create(JSC::JSGlobalData& globalData, JSC::JSGlobalObject* globalObject, JSC::Structure* structure)
    {
        JSTestObjPrototype* ptr = new (JSC::allocateCell<JSTestObjPrototype>(globalData.heap)) JSTestObjPrototype(globalData, globalObject, structure);
        ptr->finishCreation(globalData);
        return ptr;
    }

    static const JSC::ClassInfo s_info;
    static bool getOwnPropertySlot(JSC::JSCell*, JSC::ExecState*, const JSC::Identifier&, JSC::PropertySlot&);
    static bool getOwnPropertyDescriptor(JSC::JSObject*, JSC::ExecState*, const JSC::Identifier&, JSC::PropertyDescriptor&);
    static JSC::Structure* createStructure(JSC::JSGlobalData& globalData, JSC::JSGlobalObject* globalObject, JSC::JSValue prototype)
    {
        return JSC::Structure::create(globalData, globalObject, prototype, JSC::TypeInfo(JSC::ObjectType, StructureFlags), &s_info);
    }

private:
    JSTestObjPrototype(JSC::JSGlobalData& globalData, JSC::JSGlobalObject*, JSC::Structure* structure) : JSC::JSNonFinalObject(globalData, structure) { }
protected:
    static const unsigned StructureFlags = JSC::OverridesGetOwnPropertySlot | JSC::OverridesVisitChildren | Base::StructureFlags;
};

class JSTestObjConstructor : public DOMConstructorObject {
private:
    JSTestObjConstructor(JSC::Structure*, JSDOMGlobalObject*);
    void finishCreation(JSC::ExecState*, JSDOMGlobalObject*);

public:
    typedef DOMConstructorObject Base;
    static JSTestObjConstructor* create(JSC::ExecState* exec, JSC::Structure* structure, JSDOMGlobalObject* globalObject)
    {
        JSTestObjConstructor* ptr = new (JSC::allocateCell<JSTestObjConstructor>(*exec->heap())) JSTestObjConstructor(structure, globalObject);
        ptr->finishCreation(exec, globalObject);
        return ptr;
    }

    static bool getOwnPropertySlot(JSC::JSCell*, JSC::ExecState*, const JSC::Identifier&, JSC::PropertySlot&);
    static bool getOwnPropertyDescriptor(JSC::JSObject*, JSC::ExecState*, const JSC::Identifier&, JSC::PropertyDescriptor&);
    static const JSC::ClassInfo s_info;
    static JSC::Structure* createStructure(JSC::JSGlobalData& globalData, JSC::JSGlobalObject* globalObject, JSC::JSValue prototype)
    {
        return JSC::Structure::create(globalData, globalObject, prototype, JSC::TypeInfo(JSC::ObjectType, StructureFlags), &s_info);
    }
protected:
    static const unsigned StructureFlags = JSC::OverridesGetOwnPropertySlot | JSC::ImplementsHasInstance | DOMConstructorObject::StructureFlags;
    static JSC::EncodedJSValue JSC_HOST_CALL constructJSTestObj(JSC::ExecState*);
    static JSC::ConstructType getConstructData(JSC::JSCell*, JSC::ConstructData&);
};

// Functions

JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionVoidMethod(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionVoidMethodWithArgs(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionIntMethod(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionIntMethodWithArgs(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionObjMethod(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionObjMethodWithArgs(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionMethodThatRequiresAllArgsAndThrows(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionSerializedValue(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionIdbKey(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionOptionsObject(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionMethodWithException(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionCustomMethod(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionCustomMethodWithArgs(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionCustomArgsAndException(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionAddEventListener(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionRemoveEventListener(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithDynamicFrame(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithDynamicFrameAndArg(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithDynamicFrameAndOptionalArg(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithDynamicFrameAndUserGesture(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithDynamicFrameAndUserGestureASAD(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithScriptStateVoid(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithScriptStateObj(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithScriptStateVoidException(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithScriptStateObjException(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionWithScriptExecutionContext(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionMethodWithOptionalArg(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionMethodWithNonOptionalArgAndOptionalArg(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionMethodWithNonOptionalArgAndTwoOptionalArgs(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionMethodWithCallbackArg(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionMethodWithNonCallbackArgAndCallbackArg(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionMethodWithCallbackAndOptionalArg(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionConditionalMethod1(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionConditionalMethod2(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionConditionalMethod3(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjPrototypeFunctionOverloadedMethod(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjConstructorFunctionClassMethod(JSC::ExecState*);
JSC::EncodedJSValue JSC_HOST_CALL jsTestObjConstructorFunctionClassMethodWithOptional(JSC::ExecState*);
// Attributes

JSC::JSValue jsTestObjReadOnlyIntAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjReadOnlyStringAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjReadOnlyTestObjAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjShortAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjShortAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjUnsignedShortAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjUnsignedShortAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjIntAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjIntAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjLongLongAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjLongLongAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjUnsignedLongLongAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjUnsignedLongLongAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjStringAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjStringAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjTestObjAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjTestObjAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjXMLObjAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjXMLObjAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjCreate(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjCreate(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedStringAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedStringAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedIntegralAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedIntegralAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedUnsignedIntegralAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedUnsignedIntegralAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedBooleanAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedBooleanAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedURLAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedURLAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedNonEmptyURLAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedNonEmptyURLAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedStringAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedStringAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedCustomIntegralAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedCustomIntegralAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedCustomBooleanAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedCustomBooleanAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedCustomURLAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedCustomURLAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjReflectedCustomNonEmptyURLAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjReflectedCustomNonEmptyURLAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjAttrWithGetterException(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjAttrWithGetterException(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjAttrWithSetterException(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjAttrWithSetterException(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjStringAttrWithGetterException(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjStringAttrWithGetterException(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjStringAttrWithSetterException(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjStringAttrWithSetterException(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjCustomAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjCustomAttr(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjScriptStringAttr(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjConditionalAttr1(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjConditionalAttr1(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjConditionalAttr2(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjConditionalAttr2(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjConditionalAttr3(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjConditionalAttr3(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjConditionalAttr4Constructor(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjConditionalAttr4Constructor(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjConditionalAttr5Constructor(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjConditionalAttr5Constructor(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjConditionalAttr6Constructor(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjConditionalAttr6Constructor(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjCachedAttribute1(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCachedAttribute2(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjDescription(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjId(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
void setJSTestObjId(JSC::ExecState*, JSC::JSObject*, JSC::JSValue);
JSC::JSValue jsTestObjHash(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjConstructor(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
// Constants

#if ENABLE(Condition1)
JSC::JSValue jsTestObjCONDITIONAL_CONST(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
#endif
JSC::JSValue jsTestObjCONST_VALUE_0(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_1(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_2(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_4(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_8(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_9(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_10(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_11(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_12(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_13(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_VALUE_14(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);
JSC::JSValue jsTestObjCONST_JAVASCRIPT(JSC::ExecState*, JSC::JSValue, const JSC::Identifier&);

} // namespace WebCore

#endif
