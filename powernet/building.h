// powernet/building.h
// Copyright (C) 2016, Stanford University
// Author: dchassin@slac.stanford.edu

#ifndef _BUILDING_H
#define _BUILDING_H

#include "powernet.h"

DECL_METHOD(building,connect);

typedef struct s_enduseload {
	OBJECT *obj;
	enum {PC_NONE=0, PC_ONE=1, PC_TWO=2, PC_BOTH=3} circuit;
	double Zf; // constant impedance fraction (pu)
	double If; // constant current fraction (pu)
	double Pf; // constant power fraction (pu)
	double Mf; // motor power fraction (pu)
	double Ef; // electronic power fraction (pu)
	double Lw; // total load (kW)
	double F; // power factor
	double Qh; // heat gain to indoor space (kW)
} ENDUSELOAD;

class building : public gld_object {
public:
	GL_ATOMIC(object,weather); // weather
	GL_ATOMIC(double_array,x); // internal state of building
	GL_ATOMIC(double_array,u); // control input to building
	GL_ATOMIC(double_array,A); // continuous-time state transition matrix of building
	GL_ATOMIC(double_array,Bu); // control input matrix of building
	GL_ATOMIC(double_array,Bw); // weather input matrix of building
	GL_ATOMIC(double_array,y); // output vector of building
	GL_ATOMIC(double_array,C); // output measurement matrix of building
	GL_ATOMIC(double_array,D); // feed-forward control matrix of building
	GL_METHOD(building,connect);
private:
	std::list<ENDUSELOAD*> loads;
	ENDUSELOAD *add_load(OBJECT *obj, bool is220=false); // the output y of the load will be mapped to u
	gld_property Tout;
	gld_property sell;
public:
	/* required implementations */
	building(MODULE *module);
	int create(void);
	int init(OBJECT *parent);
	TIMESTAMP presync(TIMESTAMP t1);
	TIMESTAMP sync(TIMESTAMP t1);
	TIMESTAMP postsync(TIMESTAMP t1);
	TIMESTAMP commit(TIMESTAMP t1, TIMESTAMP t2);

public:
	static CLASS *oclass;
	static building *defaults;
};

#endif // _BUILDING_H
