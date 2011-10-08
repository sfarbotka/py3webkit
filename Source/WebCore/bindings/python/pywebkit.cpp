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
static PyObject* pywebkit_module = NULL;


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
	
	return pywebkit_api_fns.doc(ptr);
}

static PyMethodDef pywebkit_methods[] = 
{
	{"test", (PyCFunction)pywebkit_test, METH_NOARGS, PyDoc_STR("test method")},
	{"GetDomDocument", (PyCFunction)pywebkit_get_dom_document, METH_VARARGS, PyDoc_STR("Get DOMDocument object")},
	{"GetDomWindow", (PyCFunction)pywebkit_get_dom_window, METH_VARARGS, PyDoc_STR("Get DOMWindow object")},
	//{"GetXmlHttpRequest", (PyCFunction)pywebkit_get_xml_http_request, METH_VARARGS, PyDoc_STR("Get XMLHTTPRequest object")},
	{NULL, NULL, 0, NULL}
};

void pywebkit_init()
{
	printf("Initializing module pywebkit...\n");
	PyObject* mod = Py_InitModule("pywebkit", pywebkit_methods);

	webkit_init_pywebkit(mod, &pywebkit_api_fns);

	pywebkit_module = PyImport_ImportModule("pywebkit");

	printf("Module is initialized\n");

	Py_DECREF(mod);
}

