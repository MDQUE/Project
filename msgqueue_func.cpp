/*
 * msgqueue_func.cpp
 *
 *  Created on: Jun 20, 2019
 *      Author: verena
 */

#include "mbed.h"
#include "rtos.h"
#include <stdlib.h>
#include <string>
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <cmath>
#include <queue>
#include "setup.h"
#include <pthread.h>
#include "msgqueue_func.h"


//MESSAGE QUES

//QUEUE_FUNCTIONS
void msgtransmitter(string gcode_line);

		pthread_mutex_lock(&msgmutex);
		msgq.push(gcode_line); // push message onto the queue
		pthread_mutex_unlock(&msgmutex);
} // msgtransmitter()

string msgreceiver(){
	long qsize;
	string msg;

	while(true){
		if(msgq.empty()){
		//usleep(10000); // sleep 0.01 sec before trying again		//waiting?
		continue;
		}

		// we end up here because there was something in the msg queue
		pthread_mutex_lock(&msgmutex);
		msg = msgq.front(); // get next message in queue
		msgq.pop(); // remove it from the queue
		pthread_mutex_unlock(&msgmutex);
	}
	return msg;
} // msgreceiver()



