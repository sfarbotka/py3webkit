typedef PyObject* (*ToPythonFn) (gpointer);

struct pyjoinapi {
    ToPythonFn xhr;
    ToPythonFn win;
    ToPythonFn doc;
};

