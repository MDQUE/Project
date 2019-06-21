// Object made by MDQUE
#ifndef GCODE_H
#define GCODE_H

#include "mbed.h"
#include "rtos.h"

namespace gci{

class gcode {

public:

// ############################### Constructor / Destructor ########################################
		//Default Constructor
		gcode();

		//Overload Constructor
		gcode(bool, bool, unsigned int, unsigned int, bool);
				//par1: X orientation Enabled
				//par2: Y Orientation Enabled
				//par3: Steps on X Axis
				//par4: Steps on Y Axis
				//par5: End of Instruction

		//Destructor
		~gcode();
				//No static variables -> no explicite  work

// ########################################## Accesors #######################################

		//returs True if movement on X Axis
		bool get_dirX_Active();
		
		//returns True if movement on Y Axis
		bool get_dirY_Active();
		
		//Returns how many times the Instructions should be executed
		unsigned int get_Recursion();
		
		//Returns True if its the last Instruction of a Sentence (Enables line by line Execution)
		bool get_EoL();
		
		//Returns the Orientation of the movement on X Axis
		bool get_dirX_Orientation();
		
		//Returns the Orientation of the movement on Y Axis
		bool get_dirY_Orientation();
		
		//returns Number of steps to Execute on Y Axis
		unsigned int get_StepsY();
		
		//returns Number of steps to Execute on X Axis
		unsigned int get_StepsX();
		
		//Returns the post_processing Flag
		bool get_Pp_flag();
		
		//Returns the Pen Position (0 ~ Up ; 1 ~ Down)
		bool get_Pen_Position();
		
		int get_Line_Number();
		
// ######################################### Mutators #########################################
		
		//Sets how many times the instructions should be executed
		void set_Recursion(unsigned int);
		
		//Sets Orientation of the Movement on X Axis
		void set_dirX_Orientation(bool);
		
		//Sets Orientation of the Movent on Y Axis
		void set_dirY_Orientation(bool);
		
		//Sets the post_processing Flag
		void set_Pp_flag();
		
		//Sets the Pen Position
		void Move_Pen_down(bool);
		
		//Sets the Line Number
		void set_Line_Number(int);
		
private:
		bool dirX;
		bool dirX_Negative = false;
		bool dirY;
		bool dirY_Negative = false;
		unsigned int StepsX;
		unsigned int StepsY;
		bool Pen_down = false;
		unsigned int Recursion = 0;
		bool Post_process_flag = false;
		bool End_of_Line;
		int Line_Number;

};
}

#endif
