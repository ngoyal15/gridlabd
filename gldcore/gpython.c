// python.c
// Copyright (C) 2018 Stanford University

#include "config.h"
#include "gridlabd.h"
#include "python.h"

#ifdef HAVE_PYTHON

#include <Python.h>

typedef enum {PS_INIT, PS_READY, PS_ERROR} PYTHONSTATUS;
static PYTHONSTATUS python_status = PS_INIT;

static PyObject *SpamError;

static PyObject *python_gridlabd(PyObject *self, PyObject *args)
{
    char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return Py_BuildValue("i", sts);

}
static PyMethodDef SpamMethods[] = {
    {"gridlabd",  python_gridlabd, METH_VARARGS},
    {NULL,      NULL}        /* Sentinel */
};

static bool python_init(void)
{
    PyObject *m, *d;

	output_verbose("initializing python interface");

    m = Py_InitModule("spam", SpamMethods);
    d = PyModule_GetDict(m);
    SpamError = PyErr_NewException("spam.error", NULL, NULL);
    PyDict_SetItemString(d, "error", SpamError);

	python_status = PS_READY;
	return python_status == PS_READY;
}

STATUS python_import(char *filename)
{
	output_verbose("importing python code from %s...",filename);
	if ( ! python_init() )
		return FAILED;
	return SUCCESS;
}

#else // !HAVE_PYTHON

STATUS python_import(char *filename)
{
	output_error("python_import(filename='%s') python interface not available in the build",filename);
	return FAILED;
}

#endif // !HAVE_PYTHON

