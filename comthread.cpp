/*
 * comthread.cpp
 *
 *  Created on: Jun 20, 2019
 *      Author: verena
 */
#include <pthread.h>
#include "comthread.h"
#include "msgqueue_func.h"

//COMMUNICATION THREAD
void com_Thread(){
    char char_rec;
    int counter1 = 0;
    int direction = 0x00;
	std::string message;

	while(1){
    //check if a char has been received
		if(uart.readable()){
			char_rec = uart.getc();
			//uart.printf("%c", char_rec);

			if((char_rec == '#') || (counter1 > 49)){
				counter1 = 0;

			} else if (char_rec == '$'){
				uart.printf("%s", message.c_str());
				msgtransmitter(message);
				message = "";
				counter1 = 0;

			} else {
				if(wasd_enabled){
					switch(char_rec){
					case 'w':
						direction = up;
						break;
					case 'a':
						direction = left;
						break;
					case 's':
						direction = down;
						break;
					case 'd':
						direction = right;
						break;
					}
					plotter_line(WASD_STEPS, direction);
				}
				message += char_rec;
				//uart.printf("%c\n", char_rec);
				counter1++;
			}
		}
	}
}
//COMMUNICATION THREAD END






