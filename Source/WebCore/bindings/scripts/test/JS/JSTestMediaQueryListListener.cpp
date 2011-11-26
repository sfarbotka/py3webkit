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

#include "config.h"
#include "JSTestMediaQueryListListener.h"

#include "ExceptionCode.h"
#include "JSDOMBinding.h"
#include "MediaQueryListListener.h"
#include "TestMediaQueryListListener.h"
#include <runtime/Error.h>
#include <wtf/GetPtr.h>

using namespace JSC;

namespace WebCore {

ASSERT_CLASS_FITS_IN_CELL(JSTestMediaQueryListListener);

/* Hash table */
#if ENABLE(JIT)
#define THUNK_GENERATOR(generator) , generator
#else
#define THUNK_GENERATOR(generator)
#endif
#if ENABLE(DFG_JIT)
#define INTRINSIC(intrinsic) , intrinsic
#else
#define INTRINSIC(intrinsic)
#endif

static const HashTableValue JSTestMediaQueryListListenerTableValues[] =
{
    { "constructor", DontEnum | ReadOnly, (intptr_t)static_cast<PropertySlot::GetValueFunc>(jsTestMediaQueryListListenerConstructor), (intptr_t)0 THUNK_GENERATOR(0) INTRINSIC(DFG::NoIntrinsic) },
    { 0, 0, 0, 0 THUNK_GENERATOR(0) INTRINSIC(DFG::NoIntrinsic) }
};

#undef THUNK_GENERATOR
static const HashTable JSTestMediaQueryListListenerTable = { 2, 1, JSTestMediaQueryListListenerTableValues, 0 };
/* Hash table for constructor */
#if ENABLE(JIT)
#define THUNK_GENERATOR(generator) , generator
#else
#define THUNK_GENERATOR(generator)
#endif
#if ENABLE(DFG_JIT)
#define INTRINSIC(intrinsic) , intrinsic
#else
#define INTRINSIC(intrinsic)
#endif

static const HashTableValue JSTestMediaQueryListListenerConstructorTableValues[] =
{
    { 0, 0, 0, 0 THUNK_GENERATOR(0) INTRINSIC(DFG::NoIntrinsic) }
};

#undef THUNK_GENERATOR
static const HashTable JSTestMediaQueryListListenerConstructorTable = { 1, 0, JSTestMediaQueryListListenerConstructorTableValues, 0 };
const ClassInfo JSTestMediaQueryListListenerConstructor::s_info = { "TestMediaQueryListListenerConstructor", &DOMConstructorObject::s_info, &JSTestMediaQueryListListenerConstructorTable, 0, CREATE_METHOD_TABLE(JSTestMediaQueryListListenerConstructor) };

JSTestMediaQueryListListenerConstructor::JSTestMediaQueryListListenerConstructor(Structure* structure, JSDOMGlobalObject* globalObject)
    : DOMConstructorObject(structure, globalObject)
{
}

void JSTestMediaQueryListListenerConstructor::finishCreation(ExecState* exec, JSDOMGlobalObject* globalObject)
{
    Base::finishCreation(exec->globalData());
    ASSERT(inherits(&s_info));
    putDirect(exec->globalData(), exec->propertyNames().prototype, JSTestMediaQueryListListenerPrototype::self(exec, globalObject), DontDelete | ReadOnly);
}

bool JSTestMediaQueryListListenerConstructor::getOwnPropertySlot(JSCell* cell, ExecState* exec, const Identifier& propertyName, PropertySlot& slot)
{
    return getStaticValueSlot<JSTestMediaQueryListListenerConstructor, JSDOMWrapper>(exec, &JSTestMediaQueryListListenerConstructorTable, static_cast<JSTestMediaQueryListListenerConstructor*>(cell), propertyName, slot);
}

bool JSTestMediaQueryListListenerConstructor::getOwnPropertyDescriptor(JSObject* object, ExecState* exec, const Identifier& propertyName, PropertyDescriptor& descriptor)
{
    return getStaticValueDescriptor<JSTestMediaQueryListListenerConstructor, JSDOMWrapper>(exec, &JSTestMediaQueryListListenerConstructorTable, static_cast<JSTestMediaQueryListListenerConstructor*>(object), propertyName, descriptor);
}

/* Hash table for prototype */
#if ENABLE(JIT)
#define THUNK_GENERATOR(generator) , generator
#else
#define THUNK_GENERATOR(generator)
#endif
#if ENABLE(DFG_JIT)
#define INTRINSIC(intrinsic) , intrinsic
#else
#define INTRINSIC(intrinsic)
#endif

static const HashTableValue JSTestMediaQueryListListenerPrototypeTableValues[] =
{
    { "method", DontDelete | Function, (intptr_t)static_cast<NativeFunction>(jsTestMediaQueryListListenerPrototypeFunctionMethod), (intptr_t)1 THUNK_GENERATOR(0) INTRINSIC(DFG::NoIntrinsic) },
    { 0, 0, 0, 0 THUNK_GENERATOR(0) INTRINSIC(DFG::NoIntrinsic) }
};

#undef THUNK_GENERATOR
static const HashTable JSTestMediaQueryListListenerPrototypeTable = { 2, 1, JSTestMediaQueryListListenerPrototypeTableValues, 0 };
const ClassInfo JSTestMediaQueryListListenerPrototype::s_info = { "TestMediaQueryListListenerPrototype", &JSC::JSNonFinalObject::s_info, &JSTestMediaQueryListListenerPrototypeTable, 0, CREATE_METHOD_TABLE(JSTestMediaQueryListListenerPrototype) };

JSObject* JSTestMediaQueryListListenerPrototype::self(ExecState* exec, JSGlobalObject* globalObject)
{
    return getDOMPrototype<JSTestMediaQueryListListener>(exec, globalObject);
}

bool JSTestMediaQueryListListenerPrototype::getOwnPropertySlot(JSCell* cell, ExecState* exec, const Identifier& propertyName, PropertySlot& slot)
{
    JSTestMediaQueryListListenerPrototype* thisObject = jsCast<JSTestMediaQueryListListenerPrototype*>(cell);
    return getStaticFunctionSlot<JSObject>(exec, &JSTestMediaQueryListListenerPrototypeTable, thisObject, propertyName, slot);
}

bool JSTestMediaQueryListListenerPrototype::getOwnPropertyDescriptor(JSObject* object, ExecState* exec, const Identifier& propertyName, PropertyDescriptor& descriptor)
{
    JSTestMediaQueryListListenerPrototype* thisObject = jsCast<JSTestMediaQueryListListenerPrototype*>(object);
    return getStaticFunctionDescriptor<JSObject>(exec, &JSTestMediaQueryListListenerPrototypeTable, thisObject, propertyName, descriptor);
}

const ClassInfo JSTestMediaQueryListListener::s_info = { "TestMediaQueryListListener", &JSDOMWrapper::s_info, &JSTestMediaQueryListListenerTable, 0 , CREATE_METHOD_TABLE(JSTestMediaQueryListListener) };

JSTestMediaQueryListListener::JSTestMediaQueryListListener(Structure* structure, JSDOMGlobalObject* globalObject, PassRefPtr<TestMediaQueryListListener> impl)
    : JSDOMWrapper(structure, globalObject)
    , m_impl(impl.leakRef())
{
}

void JSTestMediaQueryListListener::finishCreation(JSGlobalData& globalData)
{
    Base::finishCreation(globalData);
    ASSERT(inherits(&s_info));
}

JSObject* JSTestMediaQueryListListener::createPrototype(ExecState* exec, JSGlobalObject* globalObject)
{
    return JSTestMediaQueryListListenerPrototype::create(exec->globalData(), globalObject, JSTestMediaQueryListListenerPrototype::createStructure(globalObject->globalData(), globalObject, globalObject->objectPrototype()));
}

bool JSTestMediaQueryListListener::getOwnPropertySlot(JSCell* cell, ExecState* exec, const Identifier& propertyName, PropertySlot& slot)
{
    JSTestMediaQueryListListener* thisObject = jsCast<JSTestMediaQueryListListener*>(cell);
    ASSERT_GC_OBJECT_INHERITS(thisObject, &s_info);
    return getStaticValueSlot<JSTestMediaQueryListListener, Base>(exec, &JSTestMediaQueryListListenerTable, thisObject, propertyName, slot);
}

bool JSTestMediaQueryListListener::getOwnPropertyDescriptor(JSObject* object, ExecState* exec, const Identifier& propertyName, PropertyDescriptor& descriptor)
{
    JSTestMediaQueryListListener* thisObject = jsCast<JSTestMediaQueryListListener*>(object);
    ASSERT_GC_OBJECT_INHERITS(thisObject, &s_info);
    return getStaticValueDescriptor<JSTestMediaQueryListListener, Base>(exec, &JSTestMediaQueryListListenerTable, thisObject, propertyName, descriptor);
}

JSValue jsTestMediaQueryListListenerConstructor(ExecState* exec, JSValue slotBase, const Identifier&)
{
    JSTestMediaQueryListListener* domObject = static_cast<JSTestMediaQueryListListener*>(asObject(slotBase));
    return JSTestMediaQueryListListener::getConstructor(exec, domObject->globalObject());
}

JSValue JSTestMediaQueryListListener::getConstructor(ExecState* exec, JSGlobalObject* globalObject)
{
    return getDOMConstructor<JSTestMediaQueryListListenerConstructor>(exec, static_cast<JSDOMGlobalObject*>(globalObject));
}

EncodedJSValue JSC_HOST_CALL jsTestMediaQueryListListenerPrototypeFunctionMethod(ExecState* exec)
{
    JSValue thisValue = exec->hostThisValue();
    if (!thisValue.inherits(&JSTestMediaQueryListListener::s_info))
        return throwVMTypeError(exec);
    JSTestMediaQueryListListener* castedThis = static_cast<JSTestMediaQueryListListener*>(asObject(thisValue));
    ASSERT_GC_OBJECT_INHERITS(castedThis, &JSTestMediaQueryListListener::s_info);
    TestMediaQueryListListener* imp = static_cast<TestMediaQueryListListener*>(castedThis->impl());
    if (exec->argumentCount() < 1)
        return throwVMError(exec, createTypeError(exec, "Not enough arguments"));
    RefPtr<MediaQueryListListener> listener(MediaQueryListListener::create(ScriptValue(exec->globalData(), MAYBE_MISSING_PARAMETER(exec, 0, MissingIsUndefined))));
    if (exec->hadException())
        return JSValue::encode(jsUndefined());
    imp->method(listener);
    return JSValue::encode(jsUndefined());
}

static inline bool isObservable(JSTestMediaQueryListListener* jsTestMediaQueryListListener)
{
    if (jsTestMediaQueryListListener->hasCustomProperties())
        return true;
    return false;
}

bool JSTestMediaQueryListListenerOwner::isReachableFromOpaqueRoots(JSC::Handle<JSC::Unknown> handle, void*, SlotVisitor& visitor)
{
    JSTestMediaQueryListListener* jsTestMediaQueryListListener = static_cast<JSTestMediaQueryListListener*>(handle.get().asCell());
    if (!isObservable(jsTestMediaQueryListListener))
        return false;
    UNUSED_PARAM(visitor);
    return false;
}

void JSTestMediaQueryListListenerOwner::finalize(JSC::Handle<JSC::Unknown> handle, void* context)
{
    JSTestMediaQueryListListener* jsTestMediaQueryListListener = static_cast<JSTestMediaQueryListListener*>(handle.get().asCell());
    DOMWrapperWorld* world = static_cast<DOMWrapperWorld*>(context);
    uncacheWrapper(world, jsTestMediaQueryListListener->impl(), jsTestMediaQueryListListener);
    jsTestMediaQueryListListener->releaseImpl();
}

JSC::JSValue toJS(JSC::ExecState* exec, JSDOMGlobalObject* globalObject, TestMediaQueryListListener* impl)
{
    return wrap<JSTestMediaQueryListListener>(exec, globalObject, impl);
}

TestMediaQueryListListener* toTestMediaQueryListListener(JSC::JSValue value)
{
    return value.inherits(&JSTestMediaQueryListListener::s_info) ? static_cast<JSTestMediaQueryListListener*>(asObject(value))->impl() : 0;
}

}
