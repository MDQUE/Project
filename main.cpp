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

int main(void){

	osStatus status;

	pwm_signal.period_ms(20); //define PWM period in ms
	pwm_signal.write(1.0);  //default duty cicle

	spi_init();
	Endstops.clear(0x7fffffff);
	thread_control_mutex.lock();

	
	//endstop_up.rise(Endstop1_reached);
	//endstop_up.fall(Endstop1_left);
	//endstop_down.rise(Endstop2_reached);
	//endstop_down.fall(Endstop2_left);
	//endstop_right.rise(Endstop3_reached);
	//endstop_right.fall(Endstop3_left);
	//endstop_left.rise(Endstop4_reached);
	//endstop_left.fall(Endstop4_left);
	

	uart.printf("Main start\n");

	Move_enable();

	Thread_com.start(com_Thread);
	Thread_int.start(int_Thread);
	
	//Message_handout.start(Message_handout_thread);
	thread_control_mutex.unlock();

	while(1){

	
	}
	return 0;
}

//endstop Handling
void Endstop1_reached(void){
	Endstops.set(0x1);
}

void Endstop1_left(void){
	Endstops.clear(0x1);
}

//down
void Endstop2_reached(void){
	Endstops.set(0x2);
}

void Endstop2_left(void){
	Endstops.clear(0x2);
}

//right
void Endstop3_reached(void){
	Endstops.set(0x3);
}

void Endstop3_left(void){
	Endstops.clear(0x3);
}

//left
void Endstop4_reached(void){
	Endstops.set(0x4);
}

void Endstop4_left(void){
	Endstops.clear(0x4);
}

//enable flag?
void Move_enable(void){
	Endstops.set(0x10);
}
void Move_disable(void){
	Endstops.clear(0x10);
}
void int_enable(void){
	Endstops.set(0x20);
}
void int_disable(void){
	Endstops.clear(0x20);
}
/************************************PLOTTER-FUNCTIONS************************************/
//plotter functions:check_endstops, move, single_move, reset, line, diagnal

void check_endstops(){
	//check endstopX = up and set flag accordingly
	uint32_t endstops_set = Endstops.get();

	//check endstop1 = up
	if(endstop_up.read() != 1){
		if((endstops_set & 0x00000001) != 0x00000001){
			Endstop1_reached();
		}
	} else {
		if((endstops_set & 0x00000001) == 0x00000001){
			Endstop1_left();
		}
	}
	//endstop down
	if(endstop_up.read() == 1){
		if((endstops_set & 0x00000002) != 0x00000002){
			Endstop2_reached();
		}
	} else {
		if((endstops_set & 0x00000002) == 0x00000002){
			Endstop2_left();
		}
	}
	//endstop left
	if(endstop_up.read() == 1){
		if((endstops_set & 0x00000004) != 0x00000004){
			Endstop1_reached();
		}
	} else {
		if((endstops_set & 0x00000004) == 0x00000004){
			Endstop1_left();
		}
	}
	//endstop right
	if(endstop_up.read() == 1){
		if((endstops_set & 0x00000008) != 0x00000008){
			Endstop1_reached();
		}
	} else {
		if((endstops_set & 0x00000008) == 0x00000008){
			Endstop1_left();
		}
	}
	wait_us(20);

}
void plotter_move(char direction){

	uint32_t endstop_flags = Endstops.get();

	//check if an endpoint is active and set flags accordingly before making a step
	//check_endstops();

	//if move is enabled
	if((0x10 & endstop_flags) == 0x10){

		//up 0x02 endstop 1
		if( ((direction & 0x02) == 0x02) /*&& ((0x00000001 & endstop_flags) == 0x01)*/ ){
			plotter_single_move(0x02);
		}

		//down 0x03 endstop 2
		if( ((direction & 0x03) == 0x03) /*&& ((0x00000002 & endstop_flags) == 0x02)*/ ){
			plotter_single_move(0x03);
		}

		//left 0x08 endstop 4
		if( ((direction & 0x08) == 0x08)/* && ((0x00000004 & endstop_flags) == 0x04) */){
			plotter_single_move(0x08);
		}

		//right 0x0C endstop 3
		if( ((direction & 0x0C) == 0x0C) /*&& ((0x00000008 & endstop_flags) == 0x08)*/){
			plotter_single_move(0x0C);
		}

	}
		
}
void plotter_single_move(char direction){

	//uart.printf("plotter-single-move dir: %d\n", direction);

	cs = 0;     //pull SPi low to initiate communication

    //SPI adressing
	//led2.write(1); 4
	spi.write(0x40); //device optcode  //bit0 -> 0 write/1 read             //0100 0000
	spi.write(0x09); //adress of register (GPIO port register 0x09)         //0000 1001
	spi.write(direction); //data to write to register                       //0000 0000

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
	uint32_t endstop_flags = Endstops.get();


	while( (0x00000002 & endstop_flags) != 0x2){
		plotter_single_move(down);
	}
	while( (0x00000004 & endstop_flags) != 0x4){
		plotter_single_move(left);
	}
}

void plotter_line(int steps, char direction){

	for(int i = 0; i < steps; i++){
		plotter_move(direction); 	//direction is: 0x03 | 0x04 | 0x08 | 0x0C
	}
}

void plotter_diagnal (int x_steps, char x_dir, int y_steps, char y_dir){
	int last_steps = 0;
	int total_steps = 0;
	int actual_steps = 0;
	int th;
	int bound;
	char main_dir;
	char second_dir;

	uart.printf("in diagnal function\n");

	//check main direction ( x >?< y)
	if(x_steps > y_steps){
		th = x_steps / y_steps;
		bound = y_steps;
		main_dir = x_dir;
		second_dir = y_dir;
	} else {
		th = x_steps / y_steps;
		bound = x_steps;
		main_dir = y_dir;
		second_dir = x_dir;
	}

	uart.printf("parameters: x: %c  y: %c stepsx: %d stepsy %d\n", x_dir, y_dir, x_steps, y_steps);
	for (int i = 1; i <= bound; i++){
		total_steps = (int)ceil(i * th);
		actual_steps = total_steps - last_steps;
		last_steps = total_steps;

		//draw the line with actual steps
		for(int i = 0; i < actual_steps; i++){
			plotter_single_move(main_dir);
		}
		plotter_single_move(second_dir);
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



//INTERPRETER THREAD
void int_Thread(){

	std::string incoming_msg = "";
	bool msgq_empty;
	osEvent in_message;

	uint32_t current_position_X = 0;
	uint32_t current_position_Y = 0;
	int direction_factorX = 1;
	int direction_factorY = 1;

	char directionX = 0x00;
	char directionY = 0x00;
	int stepsX = 0;
	int stepsY = 0;

	int instruction_number = 0;


	uart.printf("INT-THREAD\n");
	//uint32_t wait_any(uint32_t flags = 0, uint32_t timeout = osWaitForever, bool clear = true);
	//Endstops.wait_any(0x20);
/*
	while(1){
		msgq_empty = com_msgqueue.empty();
		if(!msgq_empty){
			led1.write(!led1);
			in_message = com_msgqueue.get();
			//incoming_msg = in_message.value;
			//uart.printf("int_thread: %s\n", in_message.value);
		}
	}
*/	
		thread_control_mutex.lock();
		uart.printf("int got lock\n");
	//get line from msgq and pop it
	//string newline = msgreceiver();

	// Create "Code" Object
		gci::interpret Code;

	// Set The resolution
		Code.set_Resolution(0.023);

	// Translate a Line of Instruction
		Code.translate("G01 X100");
		Code.translate("G01 Y100");
		Code.translate("G01 X100");

		uart.printf("int translated\n");
		uart.printf("int gives lock back\n");
		thread_control_mutex.unlock();
	
	while(1){
		thread_control_mutex.lock();
		uart.printf("int got lock\n");

	// Get Some info;
	//std::cout << Code.MyInstructions[0].get_StepsX() << std::endl;

	//DRAW THE OBJECT
		//get gocde obect pointer
		if(Code.MyInstructions.empty()){
			uart.printf("no element in instructions\n");
			uart.printf("int gives lock back\n");
			thread_control_mutex.unlock();
		} else {
			while(!Code.MyInstructions.empty()){
				uart.printf("int sets parameters\n");

				uart.printf("x: %d, y: %d\n", Code.MyInstructions[0].get_dirX_Active(), Code.MyInstructions[0].get_dirY_Active());
				uart.printf("x: %d, y: %d\n", Code.MyInstructions[0].get_dirX_Orientation(), Code.MyInstructions[0].get_dirY_Orientation());
				
			
				//set direction
				if (Code.MyInstructions[0].get_dirX_Active()){
					//x direction set

					//has stepsX steps
					stepsX = Code.MyInstructions[0].get_StepsX();

					if(Code.MyInstructions[0].get_dirX_Orientation()){
						//direction is left
						directionX = 0x08;
						direction_factorX = 1;

					} else {
						//direction is right
						directionX = 0x0C;
						direction_factorX = -1;
					}
				}
				if (Code.MyInstructions[0].get_dirY_Active()){
					//y direction is set

					//has stepsY steps
					stepsY = Code.MyInstructions[0].get_StepsY();

					if(Code.MyInstructions[0].get_dirY_Orientation()){
						//direction is down
						directionY = 0x03;
						direction_factorY = -1;
					} else {
						//direction is up
						directionY = 0x02;
						direction_factorY = 1;
					}
				}

				//pen up or down?
				if(Code.MyInstructions[0].get_Pen_Position()){
					//moove pen down if pen is up
				} else {
					//moove pen up if pen is down
				}

				uart.printf("int draws instruction\n");
	
				//draw line
				if((Code.MyInstructions[0].get_dirY_Active()) && (Code.MyInstructions[0].get_dirX_Active()) ){
					//plotter_diagnal (int x_steps, int x_dir, int y_steps, int y_dir)
						uart.printf("Its a diagnal!\n");
						uart.printf("parameters: x: %d  y: %d stepsx: %d stepsy %d\n", directionX, directionY, stepsX,stepsY);
						plotter_diagnal(stepsX, directionX, stepsY, directionY);

				} else {
					if(Code.MyInstructions[0].get_dirX_Active()){
						uart.printf("Its a x-line! steps: %d dir: %d\n", stepsX, directionX);
						for(int i = 0; i < stepsX; i++){
							//uart.printf(" i: %d\n");
							plotter_move(0x0C);
						}
						uart.printf("done drawing x-line\n");
					}
					if(Code.MyInstructions[0].get_dirX_Active()){
						for(int i = 0; i < stepsY; i++){
							uart.printf("Its a y-line!\n");
							plotter_single_move(directionY);
						}
					}
				}
	
				current_position_X += stepsX * direction_factorX;	//in steps or in mm?
				current_position_Y += stepsY * direction_factorY;

				stepsX = 0;
				stepsY = 0;
				directionX = 0x00;
				directionY = 0x00;

				uart.printf("int pops instruction\n");
				Code.Next_Instruction();

				//report done
			}
				uart.printf("int finished drawing\n");
				uart.printf("int gives lock back\n");
				thread_control_mutex.unlock();
		}
	}
}



//COMMUNICATION THREAD
void com_Thread(){
  char char_rec;
//    int counter1 = 0;
//    int direction = 0x00;
	std::string message = "";
	std::string last_msg = "";
//	std::string *pMsg = &message;
//	char msg_array[6] = '\0';

	uart.printf("COM-THREAD\n");
	while(1){	
		//lock mutex, no other thread can interrupt
		thread_control_mutex.lock();
		uart.printf("com got lock\n");
		if(uart.readable()){
			char_rec = uart.getc();
			if (char_rec == '$'){
				while (1){
					if(uart.readable()){
					char_rec = uart.getc();
					message += char_rec;
					}
					if (char_rec == '#'){
						uart.printf("%s\n", message.c_str());
						uart.printf("1:ACK");
						last_msg = message;
						msgpointer *dudewtf = mpool.alloc();
						dudewtf->msg_pointer = &last_msg;
						msg_queue.put(dudewtf);
						message = "";
						break;
					}
				}
			}
					
		}
		//if msg handling is done, unlock mutex
		uart.printf("com giving lock back\n");
		int_enable();
		thread_control_mutex.unlock();
	}
}
//COMMUNICATION THREAD END


//Message Handout Thread (1 hot)
//		Prefix 1: message to Interpreter
//		Prefix 2: message to plotter
//		Prefix 3: message to booth
void Message_handout_thread(void){
	while (1){
	osEvent evt = msg_queue.get();
        if (evt.status == osEventMessage) {
            msgpointer *msg = (msgpointer*)evt.value.p;
            std::string *chars = msg->msg_pointer;
            mpool.free(msg);
        }
	}
	
}

/*! EOF */
