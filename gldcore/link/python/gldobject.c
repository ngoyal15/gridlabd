/* GldObject is the base class used to define new classes in the gridlabd python module */

#include "GldObject.h"

// base type static allocation
static PyTypeObject GldObject_Type;

// module add type
int GldObject_addtype(PyObject *module)
{
    if ( PyType_Ready(&GldObject_Type) )
        return -1;
    if ( PyModule_AddObject(module,"GldObject",&GldObject_Type))
        return -1;
    return 0;
}

// type methods
static PyObject *GldObject_exception(PyObject *self, PyObject *args)
{
    char *text;
    if ( ! PyArg_ParseTuple(args,"s",&text) )
        return NULL;
    THROW("%s",text);
    Py_UNREACHABLE();
}

static PyObject *GldObject_error(PyObject *self, PyObject *args)
{
    char *text;
    if ( ! PyArg_ParseTuple(args,"s",&text) )
        return NULL;
    return PyLong_FromLong(output_error("%s",text));
}

static PyObject *GldObject_output(PyObject *self, PyObject *args)
{
    char *text;
    if ( ! PyArg_ParseTuple(args,"s",&text) )
        return NULL;
    return PyLong_FromLong(output_message("%s",text));
}

static PyObject *GldObject_warning(PyObject *self, PyObject *args)
{
    char *text;
    if ( ! PyArg_ParseTuple(args,"s",&text) )
        return NULL;
    return PyLong_FromLong(output_warning("%s",text));
}

static PyObject *GldObject_debug(PyObject *self, PyObject *args)
{
    char *text;
    if ( ! PyArg_ParseTuple(args,"s",&text) )
        return NULL;
    return PyLong_FromLong(output_debug("%s",text));
}

static PyObject *GldObject_get_name(PyObject *self, PyObject *args)
{
    // TODO
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *GldObject_get_class(PyObject *self, PyObject *args)
{
    // TODO
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *GldObject_get_id(PyObject *self, PyObject *args)
{
    // TODO
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef GldObject_tp_methods[] = {
	// output streams
    {"exception", (PyCFunction)GldObject_exception, METH_VARARGS, PyDoc_STR("Raise an exception")},
    {"error", (PyCFunction)GldObject_error, METH_VARARGS, PyDoc_STR("Output an object error message")},
    {"warning", (PyCFunction)GldObject_warning, METH_VARARGS, PyDoc_STR("Output an object warning message")},
    {"output", (PyCFunction)GldObject_output, METH_VARARGS, PyDoc_STR("Output an object message")},
    {"debug", (PyCFunction)GldObject_debug, METH_VARARGS, PyDoc_STR("Output an object debug message")},
    // header access
    {"get_name", (PyCFunction)GldObject_get_name, METH_VARARGS, PyDoc_STR("Get object name")},
    {"get_class", (PyCFunction)GldObject_get_class, METH_VARARGS, PyDoc_STR("Get object class")},
    {"get_id", (PyCFunction)GldObject_get_id, METH_VARARGS, PyDoc_STR("Get object id")},
    // property access
    {NULL, NULL} /* sentinel */
};

// type functions
static PyObject *GldObject_tp_new(PyObject *arg)
{
    GldObject *self = PyObject_New(GldObject, &GldObject_Type);
    if (self == NULL)
        return NULL;
    // TODO
    self->obj = NULL;
    return (PyObject*)self;
}

static int GldObject_tp_init(PyObject *self, PyObject *args, PyObject *kwargs)
{
    // TODO
    return 0;
}

static void GldObject_tp_dealloc(GldObject *self)
{
    PyObject_Del(self);
}

static PyObject *GldObject_tp_repr(GldObject *self)
{
    if ( self->obj )
    {
        char buffer[1024];
        snprintf(buffer,sizeof(buffer),"<%s:%d>",self->obj->oclass->name,self->obj->id);
        return Py_BuildValue("s",buffer);
    }
    else
    {
        char buffer[1024];
        snprintf(buffer,sizeof(buffer),"<unlinked GldObject at 0x%08x>",self);
        return Py_BuildValue("s",buffer);
    }
}

static PyObject *GldObject_tp_getattro(PyObject *self, PyObject *name)
{
    // TODO
    // if (self->x_attr != NULL) {
    //     PyObject *v = PyDict_GetItem(self->x_attr, name);
    //     if (v != NULL) {
    //         Py_INCREF(v);
    //         return v;
    //     }
    // }
    return PyObject_GenericGetAttr((PyObject *)self, name);
}

static int GldObject_tp_setattr(GldObject *self, const char *name, PyObject *v)
{
    // TODO
    // if (self->x_attr == NULL) {
    //     self->x_attr = PyDict_New();
    //     if (self->x_attr == NULL)
    //         return -1;
    // }
    // if (v == NULL) {
    //     int rv = PyDict_DelItemString(self->x_attr, name);
    //     if (rv < 0)
    //         PyErr_SetString(PyExc_AttributeError,
    //             "delete non-existing Gld attribute");
    //     return rv;
    // }
    // else
    //     return PyDict_SetItemString(self->x_attr, name, v);
    Py_INCREF(Py_None);
    return Py_None;
}

static int GldObject_tp_is_gc(PyObject *self)
{
    return 0;
}

PyObject *GldObject_tp_alloc(PyTypeObject *self, Py_ssize_t nitems)
{
    // TODO
    return (PyObject*) malloc(sizeof(GldObject_Type)*nitems);
}

// module type definition
static PyTypeObject GldObject_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "GldObject",       		            /*tp_name*/
    sizeof(GldObject),          		/*tp_basicsize*/
    0,                          		/*tp_itemsize*/
    /* methods */
    GldObject_tp_dealloc,    	        /*tp_dealloc*/
    0,                          		/*tp_print*/
    0,             		                /*tp_getattr*/
    GldObject_tp_setattr,   	        /*tp_setattr*/
    0,                          		/*tp_reserved*/
    GldObject_tp_repr,                  /*tp_repr*/
    0,                          		/*tp_as_number*/
    0,                          		/*tp_as_sequence*/
    0,                          		/*tp_as_mapping*/
    0,                          		/*tp_hash*/
    0,                          		/*tp_call*/
    0,                          		/*tp_str*/
    GldObject_tp_getattro,	            /*tp_getattro*/
    0,                          		/*tp_setattro*/
    0,                          		/*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE, /*tp_flags*/
    0,                          		/*tp_doc*/
    0,                          		/*tp_traverse*/
    0,                          		/*tp_clear*/
    0,                          		/*tp_richcompare*/
    0,                          		/*tp_weaklistoffset*/
    0,                          		/*tp_iter*/
    0,                          		/*tp_iternext*/
    GldObject_tp_methods,               /*tp_methods*/
    0,                          		/*tp_members*/
    0,                          		/*tp_getset*/
    0,                          		/*tp_base*/
    0,                          		/*tp_dict*/
    0,                          		/*tp_descr_get*/
    0,                          		/*tp_descr_set*/
    0,                          		/*tp_dictoffset*/
    GldObject_tp_init,                  /*tp_init*/
    GldObject_tp_alloc,                 /*tp_alloc*/
    GldObject_tp_new,                   /*tp_new*/
    0,                          		/*tp_free*/
    GldObject_tp_is_gc,                 /*tp_is_gc*/
};
