#ifndef SETUP_H
#define SETUP_H

#include "mbed.h"
#include "rtos.h"
#include <stdlib.h>
#include <string>
#include <cstring>
#include <iostream>
#include <cmath>
#include <queue>

//own includes
#include <gcode.h>
#include <ginterpret.h>

//#include <comthread.h>


//#include <Stepper.h>
/************************************************/
#define DEBUG 0
#define BUF_SIZE 40
#define RUN 1
#define SPEED 200	//speed of the plotter
#define WASD_STEPS	1000	//set steps for wasd-control
#define MSQSIZE 10

#define right	0x0C
#define left	0x08
#define down	0x03
#define up	    0x02
/******************************************************************** init pins**************************************** */

//Create a PwmOut connected to the specified pin
//mbed_os - drivers PwmOut
PwmOut pwm_signal(P1_3);   // CCU4 P1.3    //CCU8 P0.3

//create class object SPI
//initialise mosi, miso, clk, cs
//mbed os - drivers - spi.h
SPI spi(P0_5, P0_4, P0_11);     //mosi, miso, sclk
DigitalOut cs(P1_2);    		//IO_cs

//init serial
//mbed os - drivers - serial.h
Serial uart(P0_1, P0_0,9600);   //rdx, tdx, baudrate

//targets/TARGET_Infineon/TARGET_XMC4XXX/TARGET_XMC4500/PinNames.h
DigitalIn button1(SW1);		//P1_14
DigitalIn button2(SW2);		//P1_15
DigitalOut led1(LED1);      //P1_1
DigitalOut led2(LED2);      //P1_0

//endstops
DigitalIn endstop_up(P1_15);      //endstop 1
DigitalIn endstop_down(P1_13);    //endstop 2
DigitalIn endstop_right(P1_12);   //endstop 3
DigitalIn endstop_left(P1_14);    //endstop 4

//msgqueue
Queue <string, MSQSIZE>  com_msgqueue;

//function declarations;

void spi_init(void);
void endstop_counter(void);
void sendmsg(string msg);
void int_Thread();
void com_Thread();
void plotter_reset();
void plotter_move(unsigned int move);
void plotter_line(int steps, int direction);
void plotter_diagnal(int x_steps, int x_dir, int y_steps, int y_dir);


//variables
int counter = 0;
bool wasd_enabled = true;	//set if wasd-control is enabled

#endif
