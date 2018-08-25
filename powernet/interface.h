/** $Id: assert.h 4738 2014-07-03 00:55:39Z dchassin $

 General purpose interface objects

 **/

#ifndef _INTERFACE_H
#define _INTERFACE_H

#include "gridlabd.h"

typedef struct s_eventhandler {
	char specification[1024];
	int interval;
	bool enable;
	struct s_eventhandler *next;
} EVENTHANDLER;

class interface : public gld_object {
public:
	GL_ATOMIC(int32,interval);

public:
	/* required implementations */
	interface(MODULE *module);
	int create(void);
	int init(OBJECT *parent);
	TIMESTAMP precommit(TIMESTAMP t1);
	TIMESTAMP presync(TIMESTAMP t1);
	TIMESTAMP sync(TIMESTAMP t1);
	TIMESTAMP postsync(TIMESTAMP t1);
	TIMESTAMP commit(TIMESTAMP t1, TIMESTAMP t2);
	int finalize(void);

public:
	/* method implementations */
	int on_init(char *value);
	int on_precommit(char *value);
	int on_presync(char *value);
	int on_sync(char *value);
	int on_postsync(char *value);
	int on_commit(char *value);
	int on_finalize(char *value);

private: /* event handler data */
	EVENTHANDLER *handlers;

private: /* event handler functions */
	int run_handler(EVENTHANDLER *handler,TIMESTAMP t=TS_NEVER);
	int set_handler(EVENTHANDLER *handler, char *specification);
	EVENTHANDLER init_handler;
	EVENTHANDLER precommit_handler;
	EVENTHANDLER presync_handler;
	EVENTHANDLER sync_handler;
	EVENTHANDLER postsync_handler;
	EVENTHANDLER commit_handler;
	EVENTHANDLER finalize_handler;

public:
	static CLASS *oclass;
	static interface *defaults;
};

#endif // _INTERFACE_H
