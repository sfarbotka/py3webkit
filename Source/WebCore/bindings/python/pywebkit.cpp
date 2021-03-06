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

#include <Python.h>

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <stdio.h>
#include "pywebkit.h"

extern "C" void webkit_init_pywebkit(PyObject* module, pyjoinapi *api_fns);
extern "C" void* webkit_web_frame_get_dom_document(void* webView);
extern "C" void* webkit_web_frame_get_dom_window(void* webView);
extern "C" void* webkit_web_frame_get_xml_http_request(void* webView);
extern "C" void* webkit_web_view_get_main_frame(void* webView);

static pyjoinapi pywebkit_api_fns;


static void* pywebkit_get_webview(PyObject* args)
{
	PyObject* obj = NULL;
	if (!PyArg_ParseTuple(args, "O", &obj))
		return NULL;
	
	PyObject* result = PyObject_CallMethod(obj, "get_native_ptr", NULL);
	if (!result)
		return NULL;

	void* ret = (void*)PyLong_AsLong(result);
	Py_DECREF(result);

	return ret;
}


static PyObject* pywebkit_test(PyObject* self, PyObject* unused)
{
	printf("Hello from pywebkit_test!!!\n");
	
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* pywebkit_get_dom_document(PyObject* self, PyObject* args)
{
	void* webview = pywebkit_get_webview(args);
	if (!webview)
		return NULL;

	void* frame = webkit_web_view_get_main_frame(webview);
	gpointer ptr = webkit_web_frame_get_dom_document(frame);
	
	return pywebkit_api_fns.doc(ptr);
}

/*static PyObject* pywebkit_get_xml_http_request(PyObject* self, PyObject* args)
{
	void* webview = pywebkit_get_webview(args);
	if (!webview)
		return NULL;

	void* frame = webkit_web_view_get_main_frame(webview);
	gpointer ptr = webkit_web_frame_get_xml_http_request(frame);
	
	return pywebkit_api_fns.xhr(ptr);
}*/

static PyObject* pywebkit_get_dom_window(PyObject* self, PyObject* args)
{
	void* webview = pywebkit_get_webview(args);
	if (!webview)
		return NULL;

	void* frame = webkit_web_view_get_main_frame(webview);
	gpointer ptr = webkit_web_frame_get_dom_window(frame);
	
	return pywebkit_api_fns.win(ptr);
}

static PyMethodDef pywebkit_methods[] = 
{
	{"test", (PyCFunction)pywebkit_test, METH_NOARGS, PyDoc_STR("test method")},
	{"GetDomDocument", (PyCFunction)pywebkit_get_dom_document, METH_VARARGS, PyDoc_STR("Get DOMDocument object")},
	{"GetDomWindow", (PyCFunction)pywebkit_get_dom_window, METH_VARARGS, PyDoc_STR("Get DOMWindow object")},
	//{"GetXmlHttpRequest", (PyCFunction)pywebkit_get_xml_http_request, METH_VARARGS, PyDoc_STR("Get XMLHTTPRequest object")},
	{NULL, NULL, 0, NULL}
};

static PyModuleDef pywebkit_module = 
{
	PyModuleDef_HEAD_INIT,
	"pywebkit", 
	NULL, 
	-1, 
	pywebkit_methods, 
	NULL, 
	NULL, 
	NULL, 
	NULL
};

PyObject* pywebkit_module_init()
{
	printf("Initializing module pywebkit...\n");

	PyObject* mod = PyModule_Create(&pywebkit_module);
	if (!mod)
	{
		printf("Unable to initalize module pywebkit!!!\n");
		return NULL;
	}

	webkit_init_pywebkit(mod, &pywebkit_api_fns);

	printf("Module is initialized\n");

	return mod;
}

void pywebkit_init()
{
	PyObject* mod = pywebkit_module_init();
	if (!mod)
		return;

	PyObject* mdict = PyImport_GetModuleDict();
	PyDict_SetItemString(mdict, "pywebkit", mod);
}


