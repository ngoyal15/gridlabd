/** $Id: assert.cpp 4738 2014-07-03 00:55:39Z dchassin $

   General purpose assert objects

 **/

#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <math.h>
#include <complex.h>
#include <time.h>

#include "interface.h"

EXPORT_CREATE(interface);
EXPORT_INIT(interface);
EXPORT_PRECOMMIT(interface);
EXPORT_SYNC(interface);
EXPORT_COMMIT(interface);
EXPORT_FINALIZE(interface);
EXPORT_LOADMETHOD(interface,on_init);
EXPORT_LOADMETHOD(interface,on_precommit);
EXPORT_LOADMETHOD(interface,on_presync);
EXPORT_LOADMETHOD(interface,on_sync);
EXPORT_LOADMETHOD(interface,on_postsync);
EXPORT_LOADMETHOD(interface,on_commit);
EXPORT_LOADMETHOD(interface,on_finalize);

CLASS *interface::oclass = NULL;
interface *interface::defaults = NULL;

interface::interface(MODULE *module)
{
	if (oclass==NULL)
	{
		// register to receive notice for first top down. bottom up, and second top down synchronizations
		oclass = gld_class::create(module,"interface",sizeof(interface),PC_PRETOPDOWN|PC_BOTTOMUP|PC_POSTTOPDOWN|PC_AUTOLOCK|PC_OBSERVER);
		if (oclass==NULL)
			throw "unable to register class interface";
		else
			oclass->trl = TRL_PROVEN;

		defaults = this;
		if (gl_publish_variable(oclass,
			PT_int32,"interval",get_interval_offset(),PT_DESCRIPTION,"interval at which interface is activated",
			NULL)<1){
				char msg[256];
				sprintf(msg, "unable to publish properties in %s",__FILE__);
				throw msg;
		}
		gl_publish_loadmethod(oclass,"on_init",loadmethod_interface_on_init);
		gl_publish_loadmethod(oclass,"on_precommit",loadmethod_interface_on_precommit);
		gl_publish_loadmethod(oclass,"on_presync",loadmethod_interface_on_presync);
		gl_publish_loadmethod(oclass,"on_sync",loadmethod_interface_on_sync);
		gl_publish_loadmethod(oclass,"on_postsync",loadmethod_interface_on_postsync);
		gl_publish_loadmethod(oclass,"on_commit",loadmethod_interface_on_commit);
		gl_publish_loadmethod(oclass,"on_finalize",loadmethod_interface_on_finalize);
		memset(this,0,sizeof(interface));
	}
}

int interface::create(void) 
{
	memcpy(this,defaults,sizeof(*this));
	return SUCCESS;
}

int interface::init(OBJECT *parent)
{
	if ( parent == NULL )
		exception("parent of '%s' is not specified", get_name());

	return run_handler(&init_handler) ? SUCCESS : FAILED;
}

TIMESTAMP interface::precommit(TIMESTAMP t1)
{
	return run_handler(&precommit_handler,t1) ? interval*(t1/interval+1) : TS_ZERO;
}

TIMESTAMP interface::presync(TIMESTAMP t1)
{
	return run_handler(&presync_handler,t1) ? interval*(t1/interval+1) : TS_ZERO;
}

TIMESTAMP interface::sync(TIMESTAMP t1)
{
	return run_handler(&sync_handler,t1) ? interval*(t1/interval+1) : TS_ZERO;
}

TIMESTAMP interface::postsync(TIMESTAMP t1)
{
	return run_handler(&postsync_handler,t1) ? interval*(t1/interval+1) : TS_ZERO;
}

TIMESTAMP interface::commit(TIMESTAMP t1, TIMESTAMP t2)
{
	return run_handler(&commit_handler,t1) ? interval*(t1/interval+1) : TS_ZERO;
}

int interface::finalize(void)
{
	return run_handler(&finalize_handler) ? SUCCESS : FAILED;
}

int interface::set_handler(EVENTHANDLER *handler, char *specification)
{
	strcpy(handler->specification,specification);
	handler->enable = true;
	handler->interval = interval;
	handler->next = NULL;
	gl_verbose("%s setting handler for '%s' (enabled, interval=%d)",get_name(),handler->specification,handler->interval);
	return SUCCESS;
}

int interface::run_handler(EVENTHANDLER *handler,TIMESTAMP t)
{
	// TODO
	//system("/usr/bin/python run_thermostat.py air_temperature 12.3 heating_setpoint 15.0 cooling_setpoint 20.0 thermostat_deadband 1.0");
	EVENTHANDLER *item;
	for ( item = handler ; item != NULL ; item = item->next )
	{
		if ( item->enable && t%item->interval==0 )
		{
			char env[1024];
			sprintf(env,"%d",t);
			setenv("TIMESTAMP",env,1);
			gld_clock dt(t);
			dt.to_string(env,sizeof(env));
			setenv("DATETIME",env,1);
			int rc = system(item->specification);
			if ( rc != 0 )
			{
				gl_error("interface::run_handler(spec='%s') return code %d",item->specification,rc);
				return FAILED;
			}
		}
	}
	return SUCCESS;
}

int interface::on_init(char *value)
{
	return set_handler(&init_handler, value);
}

int interface::on_precommit(char *value)
{
	return set_handler(&precommit_handler, value);
}

int interface::on_presync(char *value)
{
	return set_handler(&presync_handler, value);
}

int interface::on_sync(char *value)
{
	return set_handler(&sync_handler, value);
}

int interface::on_postsync(char *value)
{
	return set_handler(&postsync_handler, value);
}

int interface::on_commit(char *value)
{
	return set_handler(&commit_handler, value);
}

int interface::on_finalize(char *value)
{
	return set_handler(&finalize_handler, value);
}

