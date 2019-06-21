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
 * distributed under the License is distributed on an "AS IS" BASIS,s
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/******************comments
*/
/******************************************************************* Includes */
#include "setup.h"

/************************************PLOTTER-FUNCTIONS************************************/
//plotter functions: move, reset, line, diagnal
void plotter_move(unsigned int move){
	cs = 0;     //pull SPi low to initiate communication

    //SPI adressing
	//led2.write(1);
	spi.write(0x40); //device optcode  //bit0 -> 0 write/1 read             //0100 0000
	spi.write(0x09); //adress of register (GPIO port register 0x09)         //0000 1001
	spi.write(move); //data to write to register                            //0000 0000

	cs = 1;     	//set SPI bus high for no communication
	wait_us(SPEED);	//speed of the plotter
	cs = 0;    		 //pull SPI low to initiate comm

    //after step, reset GPIO register
	spi.write(0x40);
	spi.write(0x09);
	spi.write(0x00);

	cs = 1;     //set SPI high for no communication
}

void plotter_reset(){
    //reset plotter to 0,0 (left,down)
    //move to left position

	//is 0 or 1 endstop active???

    while(!endstop_down){
        plotter_move(left);
    }
    //move to down position
    while(!endstop_left){
        plotter_move(down);
    }
}

void plotter_line(int steps, int direction){

	for(int i = 0; i < steps; i++){
		plotter_move(direction); 	//direction is: 0x03 | 0x04 | 0x08 | 0x0C
	}
}

void plotter_diagnal (int x_steps, int x_dir, int y_steps, int y_dir){
	int last_steps = 0;
	int total_steps = 0;
	int actual_steps = 0;
	int th;
	int bound;

	if(x_steps > y_steps){
		th = x_steps / y_steps;
		bound = y_steps;
	} else {
		th = x_steps / y_steps;
		bound = x_steps;
	}

	for (int i = 1; i <= bound; i++){
		total_steps = (int)ceil(i * th);
		actual_steps = total_steps - last_steps;
		last_steps = total_steps;
	}
}


//spi init
void spi_init(void){
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
void endstop_counter(void){
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
		//uart.write("counter is: %d\n", counter);

	}
	//device.printf("counter is: %d\n", counter);
}

/*Thread Endstops end*/


//THREADS
Thread Thread_com;
Thread Thread_int;

//INTERPRETER THREAD
void int_Thread(){

	std::string incoming_msg = "";
	bool msgq_empty;
	osEvent in_message;

	//uart.printf("COM-THREAD\n");

	while(1){
		msgq_empty = com_msgqueue.empty();
		if(!msgq_empty){
			led1.write(0);
			in_message = com_msgqueue.get();
			//incoming_msg = in_message.value;
			//uart.printf("int_thread: %s\n", in_message.value);
		}
	}
	
	/*
	while(1){


	//get line from msgq and pop it
	//string newline = msgreceiver();

	// Create "Code" Object
	gci::interpret Code;

	// Set The resolution
	Code.set_Resolution(0.023);

	// Translate a Line of Instruction
	Code.translate("N110");

	// Get Some info;
	//std::cout << Code.MyInstructions[0].get_StepsX() << std::endl;
	}
	*/
}

//COMMUNICATION THREAD
void com_Thread(){
    unsigned char char_rec;
    int counter1 = 0;
    int direction = 0x00;
	std::string message;
	std::string *pMsg = &message;
	char msg_array[6] = '\0';

	//uart.printf("COM-THREAD\n");
	while(1){	
		if(uart.readable()){
			char_rec = uart.getc();
			//uart.putc(char_rec);
			msg_array[counter1] = char_rec;
			for(int i = 0; i < 6; i++){
				uart.putc(msg_array[i]);
			}
			//uart.putc(counter1);
			//uart.printf("counter: %d\n", counter1);
			counter1++;
		}
		if(counter1 >= 5)
			counter1 = 0;
	}
}
//COMMUNICATION THREAD END



int main(void){

	osStatus status;

	pwm_signal.period_ms(20); //define PWM period in ms
	pwm_signal.write(1.0);  //default duty cicle

	spi_init();

	//uart.write("Main-Start\n");
	
	/*
	//start com_Thread and check if it worked
	status = Thread_com->start(com_Thread);
	if (status != osOK)
	{
		error("ERROR: Thread buttons: Failed!");
	}
	*/
	Thread_com.start(com_Thread);


	while(1){
		led1 = !led1;
	}
	return 0;
}
/*! EOF */
