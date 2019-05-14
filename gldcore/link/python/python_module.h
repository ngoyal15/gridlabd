// gldcore/link/python/python.h
// Copyright (C) 2019, Regents of the Leland Stanford Jr. University
// David P. Chassin
// SLAC National Accelerator Laboratory

#ifndef _PYTHON_H
#define _PYTHON_H

#include "Python.h"

MODULE *python_module_load(char const*, int, char**);
int python_event(struct s_object_list*, char const*, long long*);

#endif
