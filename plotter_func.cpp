/*
 * plotter_func.cpp
 *
 *  Created on: Jun 20, 2019
 *      Author: verena
 */

#include "plotter_func.h"
#include "setup.h"

/************************************FUNCTIONS************************************/
//plotter functions: move, reset, line, diagnal
void plotter_move(unsigned int move)
{
	cs = 0;     //pull SPi low to initiate communication

    //SPI adressing
	led2.write(1);
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

void plotter_diagnal(int x_steps, int x_dir, int y_steps, int y_dir){

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



