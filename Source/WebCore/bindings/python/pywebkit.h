#include <Python.h>

typedef PyObject* (*ToPythonFn) (gpointer);

struct pyjoinapi {
    ToPythonFn xhr;
    ToPythonFn win;
    ToPythonFn doc;
};


void pywebkit_init();

