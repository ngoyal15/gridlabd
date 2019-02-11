/* GldObject is the base class used to define new classes in the gridlabd python module */

#include "GldObject.h"
#include "gridlabd.h"

// base type static allocation
static PyTypeObject GldObject_Type;
static CLASS *python_object_class = NULL;

// type init
void GldObject_typeinit(void)
{
	python_object_class = class_register(NULL,"python_object",sizeof(GldObject_Type),PC_AUTOLOCK);
	if ( python_object_class == NULL )
		THROW("unable to register python_object class in gridlabd");
}

// module add type
int GldObject_addtype(PyObject *module)
{
	if ( python_object_class == NULL )
		GldObject_typeinit();
    if ( PyType_Ready(&GldObject_Type) )
        return -1;
    if ( PyModule_AddObject(module,"GldObject",&GldObject_Type))
        return -1;
    return 0;
}

// type methods
static void GldObject_name(GldObject *self, char *buffer, size_t size)
{
	if ( self->obj ) 
	{
		if ( self->obj->name )
		{
			snprintf(buffer,size,"%s",self->obj->name);
		}
		else
		{
			snprintf(buffer,size,"<%s:%d>",self->obj->oclass->name,self->obj->id);
		}
	}
}

static PyObject *GldObject_exception(GldObject *self, PyObject *args)
{
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
    char *text;
    if ( PyArg_ParseTuple(args,"s",&text) )
	    THROW("%s%s",objname,text);
    return NULL;
}

static PyObject *GldObject_error(GldObject *self, PyObject *args)
{
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
    char *text;
    if ( ! PyArg_ParseTuple(args,"s",&text) )
        return NULL;
    return PyLong_FromLong(output_error("%s.%s",objname,text));
}

static PyObject *GldObject_output(GldObject *self, PyObject *args)
{
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
    char *text;
    if ( ! PyArg_ParseTuple(args,"s",&text) )
        return NULL;
    return PyLong_FromLong(output_message("%s.%s",objname,text));
}

static PyObject *GldObject_warning(GldObject *self, PyObject *args)
{
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
    char *text;
    if ( ! PyArg_ParseTuple(args,"s",&text) )
        return NULL;
    return PyLong_FromLong(output_warning("%s.%s",objname,text));
}

static PyObject *GldObject_debug(GldObject *self, PyObject *args)
{
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
    char *text;
    if ( ! PyArg_ParseTuple(args,"s",&text) )
        return NULL;
    return PyLong_FromLong(output_debug("%s.%s",objname,text));
}

static PyObject *GldObject_get_name(GldObject *self, PyObject *args)
{
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
    return Py_BuildValue("s",objname);
}

static PyObject *GldObject_get_class(GldObject *self, PyObject *args)
{
    // TODO
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *GldObject_get_id(GldObject *self, PyObject *args)
{
    // TODO
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef GldObject_tp_methods[] = {
	// output streams
    {"exception",   GldObject_exception,    METH_VARARGS, PyDoc_STR("Raise an exception")},
    {"error",       GldObject_error,        METH_VARARGS, PyDoc_STR("Output an object error message")},
    {"warning",     GldObject_warning,      METH_VARARGS, PyDoc_STR("Output an object warning message")},
    {"output",      GldObject_output,       METH_VARARGS, PyDoc_STR("Output an object message")},
    {"debug",       GldObject_debug,        METH_VARARGS, PyDoc_STR("Output an object debug message")},
    // header access
    {"get_name",    GldObject_get_name,     METH_VARARGS, PyDoc_STR("Get object name")},
    {"get_class",   GldObject_get_class,    METH_VARARGS, PyDoc_STR("Get object class")},
    {"get_id",      GldObject_get_id,       METH_VARARGS, PyDoc_STR("Get object id")},
    // property access
    {NULL, NULL} /* sentinel */
};

// type functions
static PyObject *GldObject_tp_new(GldObject *arg)
{
    GldObject *self = PyObject_New(GldObject, &GldObject_Type);
    if (self == NULL)
        return NULL;
    self->oclass = python_object_class;
    self->obj = object_create_single(self->oclass);
    return (PyObject*)self;
}

static int GldObject_tp_init(GldObject *self, PyObject *args, PyObject *kwargs)
{
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
	output_error("%s.init(...): not implemented",objname);
    return 0;
}

static void GldObject_tp_dealloc(GldObject *self)
{
    PyObject_Del(self);
}

static PyObject *GldObject_tp_repr(GldObject *self)
{
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
    return Py_BuildValue("s",objname);
}

static PyObject *GldObject_tp_getattro(GldObject *self, const char *name)
{
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
	output_error("%s.getattro(name='%s'): not implemented",objname,name);
    return PyObject_GenericGetAttr((PyObject *)self, name);
}

static int GldObject_tp_setattro(GldObject *self, const char *name, PyObject *v)
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
	char objname[64] = "<GldObject:NULL>";
	GldObject_name(self,objname,sizeof(objname));
    output_error("%s.setattr(name='%s'): not implemented",objname,name);
    Py_INCREF(Py_None);
    return Py_None;
}

static int GldObject_tp_is_gc(GldObject *self)
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
    "gridlabd.GldObject",       		/*tp_name*/
    sizeof(GldObject),          		/*tp_basicsize*/
    0,                          		/*tp_itemsize*/
    /* methods */
    GldObject_tp_dealloc,    	        /*tp_dealloc*/
    0,                          		/*tp_print*/
    0,               					/*tp_getattr*/
    0,   	        					/*tp_setattr*/
    0,                          		/*tp_reserved*/
    GldObject_tp_repr,                  /*tp_repr*/
    0,                          		/*tp_as_number*/
    0,                          		/*tp_as_sequence*/
    0,                          		/*tp_as_mapping*/
    0,                          		/*tp_hash*/
    0,                          		/*tp_call*/
    0,                          		/*tp_str*/
    GldObject_tp_getattro,	            /*tp_getattro*/
    GldObject_tp_setattro,      		/*tp_setattro*/
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
