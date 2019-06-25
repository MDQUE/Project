#ifndef GINTERPRET_H
#define GINTERPRET_H

//G-Code Interpreter made by Dominique v1.0

//#include <stdint.h>
#include <cmath>
#include <string>
#include <cstdlib>
#include <sstream>
#include "gcode.h"
#include <vector>
#include <cstring>
#include <iostream>
#include "mbed.h"
#include "rtos.h"



namespace gci
{
	
class interpret{

public:
// ################################## Constructor / Destructor #################################
		
		//Default Constructor
		interpret();
		
		//Overloaded Constructor
		void translate(std::string CodeLine);
		
		//destructor
		~interpret();
		
// ################################## Mutator Functions #########################################
		
		//Initalize drawing Area
		//	X1,X2,Y1,Y2 - Limits of the drawable Area measured from the lokal minimum (0,0)
		//	RX1,RY1      - place of the Reference Point measured from X1,Y1
		//	RES         - size of 1 Step of the Steppermotor
		void _initdraw(float X1 = 30, float Y1 = 30, float X2 = 260, float Y2 = 230, float RX1 =180, 
									 float RY1 =180, float RES = 0);
		
		// Set the Steplength of 1 Step
		void set_Resolution(float resolution);
		
		// Erase last instruction on the Object - Vector
		void Next_Instruction();
		
		std::vector<gcode> MyInstructions;
		 
		
		
		// ################################## Accessor Functions #########################################
		
private:
		// Analyse the given "sentence" of G-Code
		int Analyze(std::string word);
		
		// Calculate line in G1 mode, save results in MyInstructions
		unsigned int Calculate_Line(float MovementX, float MovementY);
		
		
		 float Drawlimit_X1;
		 float Drawlimit_Y1;
		 float Drawlimit_X2;
		 float Drawlimit_Y2;
		 float Ref_point_RX1;
		 float Ref_point_RY1;
		 float Move_RES;
		 bool Absolute_Coordinates = 1;
		 int Travel_Speed = 30;
		
		// Measured From Reference Point
		 float Last_Pos_X;
		 float Last_Pos_Y;
		 
		 int Actual_Line_Number;
		 bool Program_End = 0;
		 float MoveX = 0;
		 float MoveY = 0;
		 float Radius;
		 int Movement_type = 1;
		
		

};
}

#endif
