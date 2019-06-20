/* mbed Example Program
 * Copyright (c) 2006-2014 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/******************comments
*/
/******************************************************************* Includes */
#include "mbed.h"
#include "rtos.h"
#include <string>
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <cmath>
#include <queue>
#include "setup.h"
#include <pthread.h>
#include "msgqueue_func.h"
#include "comthread.h"


//THREADS
Thread *thread_int;


//MESSAGE QUES
pthread_mutex_t msgmutex = PTHREAD_MUTEX_INITIALIZER;
queue<string> msgq_com_int;

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
		//sleep(10000); // sleep 0.01 sec before trying again
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



//spi init
void spi_init(void)
{
	cs.write(1);
	spi.format(8, 0);
	spi.frequency(10000000); //10MHz

	cs = 0;
	spi.write(0x40);    // 0100 0000
	spi.write(0x00);    // 0000 0000
	spi.write(0xF0);    // 1111 0000    //why???
	cs = 1;
}

//check endstops function?
//for endstops thread which constantly watches endstop acivation?
//to check how many steps from one endstop to the next!
void endstop_counter(void)
{
	int buffer = right;

	while(1)
	{

		if (!endstop_down && !endstop_right)
		{
			//device.printf("counter is: %d\n", counter);
			counter = 0;
			buffer = up;
			//move servo -> pen up
			//pwm_signal_1_3.write(0.95); //0.92
			//pwm_signal_0_3.write(0.9);
			//Thread::wait(10);
			//pwm_signal_1_3.write(1.0);

		}

	  	else if (!endstop_up && !endstop_left)
		{
			//device.printf("counter is: %d\n", counter);
			counter=0;
			buffer = down;

		}
		else if (!endstop_down && !endstop_left)
		{
			//device.printf("counter is: %d\n", counter);
			counter=0;
			buffer = right;
			//move servo -> pen up
			//pwm_signal_0_3.write(0.9);
			//pwm_signal_1_3.write(0.9); //0.8
			//Thread::wait(10);
			//pwm_signal_1_3.write(1.0);
		}
		else if (!endstop_right && !endstop_up)
		{
			//device.printf("counter is: %d\n", counter);
			counter=0;
			buffer = left;
		}
		else if (!endstop_down) // unten
		{

			buffer = right;
		}

		else if (!endstop_up) //oben
		{

			buffer = left;

		}
		else if (!endstop_left) //oben links
		{

			buffer = down;
		}
		else if (!endstop_right) //oben rechts
		{

			buffer = up;
		}
		plotter_move(buffer);
		counter++;
		uart.printf("counter is: %d\n", counter);

	}
	//device.printf("counter is: %d\n", counter);
}

/*Thread Endstops end*/


void sendmsg(string msg){
		uart.printf("%s\n", msg);
}



//INTERPRETER THREAD
void int_Thread(){

	while(1){


	//get line from msgq and pop it
	string newline = msgreceiver();

	// Create "Code" Object
	gci::interpret Code;

	// Set The resolution
	Code.set_Resolution(0.023);

	// Translate a Line of Instruction
	Code.translate(newline);

	// Get Some info;
	//std::cout << Code.MyInstructions[0].get_StepsX() << std::endl;
	]
}


int main(void){

	osStatus status;

	pwm_signal.period_ms(20); //define PWM period in ms
	pwm_signal.write(1.0);  //default duty cicle

	spi_init();


	uart.printf("Main-Start\n");

	//start com_Thread and check if it worked
	status = thread_com->start(com_Thread);
	if (status != osOK)
	{
		error("ERROR: Thread buttons: Failed!");
	}


	while(1){
		//nothing
	}

}
/*! EOF */
