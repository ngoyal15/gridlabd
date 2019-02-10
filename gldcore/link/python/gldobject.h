
#include <pthread.h>
#include "gridlabd.h"
#include <Python.h>
#include "cmdarg.h"
#include "load.h"
#include "exec.h"
#include "save.h"

typedef struct {
    PyObject_HEAD
    OBJECT *obj;
} GldObject;

#define GldObject_Check(v) (Py_TYPE(v) == &GldObject_Type)

#ifdef __cplusplus
extern "C" {
#endif

int GldObject_addtype(PyObject *module);

#ifdef __cplusplus
}
#endif
