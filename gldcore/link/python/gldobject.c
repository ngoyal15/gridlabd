/* GldObject is the base class used to define new classes in the gridlabd python module */

#include "Python.h"

static PyObject *ErrorObject;

typedef struct {
    PyObject_HEAD
    OBJECT header;
} GldObject;

static PyTypeObject Gld_Type;

#define GldObject_Check(v)      (Py_TYPE(v) == &Gld_Type)

static GldObject *
newGldObject(PyObject *arg)
{
    GldObject *self = PyObject_New(GldObject, &Gld_Type);
    if (self == NULL)
        return NULL;
    self->obj = NULL;
    return self;
}

/* Gld methods */

static void
Gld_dealloc(GldObject *self)
{
    PyObject_Del(self);
}

static PyObject *
Gld_getname(GldObject *self, PyObject *args)
{
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef Gld_methods[] = {
    {"demo",            (PyCFunction)Gld_demo,  METH_VARARGS,
        PyDoc_STR("demo() -> None")},
    {NULL,              NULL}           /* sentinel */
};

static PyObject *
Gld_getattro(GldObject *self, PyObject *name)
{
    if (self->x_attr != NULL) {
        PyObject *v = PyDict_GetItem(self->x_attr, name);
        if (v != NULL) {
            Py_INCREF(v);
            return v;
        }
    }
    return PyObject_GenericGetAttr((PyObject *)self, name);
}

static int
Gld_setattr(GldObject *self, const char *name, PyObject *v)
{
    if (self->x_attr == NULL) {
        self->x_attr = PyDict_New();
        if (self->x_attr == NULL)
            return -1;
    }
    if (v == NULL) {
        int rv = PyDict_DelItemString(self->x_attr, name);
        if (rv < 0)
            PyErr_SetString(PyExc_AttributeError,
                "delete non-existing Gld attribute");
        return rv;
    }
    else
        return PyDict_SetItemString(self->x_attr, name, v);
}

static PyTypeObject Gld_Type = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "gridlabd.GldObject",       /*tp_name*/
    sizeof(GldObject),          /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    /* methods */
    (destructor)Gld_dealloc,    /*tp_dealloc*/
    0,                          /*tp_print*/
    (getattrfunc)0,             /*tp_getattr*/
    (setattrfunc)Gld_setattr,   /*tp_setattr*/
    0,                          /*tp_reserved*/
    0,                          /*tp_repr*/
    0,                          /*tp_as_number*/
    0,                          /*tp_as_sequence*/
    0,                          /*tp_as_mapping*/
    0,                          /*tp_hash*/
    0,                          /*tp_call*/
    0,                          /*tp_str*/
    (getattrofunc)Gld_getattro, /*tp_getattro*/
    0,                          /*tp_setattro*/
    0,                          /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,         /*tp_flags*/
    0,                          /*tp_doc*/
    0,                          /*tp_traverse*/
    0,                          /*tp_clear*/
    0,                          /*tp_richcompare*/
    0,                          /*tp_weaklistoffset*/
    0,                          /*tp_iter*/
    0,                          /*tp_iternext*/
    Gld_methods,                /*tp_methods*/
    0,                          /*tp_members*/
    0,                          /*tp_getset*/
    0,                          /*tp_base*/
    0,                          /*tp_dict*/
    0,                          /*tp_descr_get*/
    0,                          /*tp_descr_set*/
    0,                          /*tp_dictoffset*/
    0,                          /*tp_init*/
    0,                          /*tp_alloc*/
    0,                          /*tp_new*/
    0,                          /*tp_free*/
    0,                          /*tp_is_gc*/
};
/* --------------------------------------------------------------------- */

/* Function of two integers returning integer */

// PyDoc_STRVAR(xx_foo_doc,
// "foo(i,j)\n\
// \n\
// Return the sum of i and j.");

// static PyObject *
// xx_foo(PyObject *self, PyObject *args)
// {
//     long i, j;
//     long res;
//     if (!PyArg_ParseTuple(args, "ll:foo", &i, &j))
//         return NULL;
//     res = i+j; /* XXX Do something here */
//     return PyLong_FromLong(res);
// }


/* Function of no arguments returning new Gld object */

static PyObject *
gldobject_new(PyObject *self, PyObject *args)
{
    GldObject *rv;

    if (!PyArg_ParseTuple(args, ":new"))
        return NULL;
    rv = newGldObject(args);
    if (rv == NULL)
        return NULL;
    return (PyObject *)rv;
}

/* Example with subtle bug from extensions manual ("Thin Ice"). */

static PyObject *
gldobject_bug(PyObject *self, PyObject *args)
{
    PyObject *list, *item;

    if (!PyArg_ParseTuple(args, "O:bug", &list))
        return NULL;

    item = PyList_GetItem(list, 0);
    /* Py_INCREF(item); */
    PyList_SetItem(list, 1, PyLong_FromLong(0L));
    PyObject_Print(item, stdout, 0);
    printf("\n");
    /* Py_DECREF(item); */

    Py_INCREF(Py_None);
    return Py_None;
}

/* Test bad format character */

static PyObject *
gldobject_roj(PyObject *self, PyObject *args)
{
    PyObject *a;
    long b;
    if (!PyArg_ParseTuple(args, "O#:roj", &a, &b))
        return NULL;
    Py_INCREF(Py_None);
    return Py_None;
}


