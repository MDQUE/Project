#include "setup.h"

//Eventflags Controlin Enstop hit scenarios
//	If a bounderi is rached, flag is set, direction should be temporarely blocked

void Endstop1_reached(void){
	Endstops.set(0x1);
}

void Endstop1_left(void){
	Endstops.clear(0x1);
}

void Endstop2_reached(void){
	Endstops.set(0x2);
}

void Endstop2_left(void){
	Endstops.clear(0x2);
}

void Endstop3_reached(void){
	Endstops.set(0x4);
}

void Endstop3_left(void){
	Endstops.clear(0x4);
}

void Endstop4_reached(void){
	Endstops.set(0x8);
}

void Endstop4_left(void){
	Endstops.clear(0x8);
}
