#include "gcode.h"

namespace gci{

gcode::gcode(){}
	
gcode::gcode(bool X = false, bool Y = false, unsigned int Stepsx = 0, unsigned int Stepsy = 0, 
             bool End = true){
	dirX = X;
	dirY = Y;
	StepsX = Stepsx;
	StepsY = Stepsy;
	End_of_Line = End;
}

gcode::~gcode(){}

bool gcode::get_dirX_Active(){
	return dirX;
}

bool gcode::get_dirY_Active(){
	return dirY;
}

void gcode::set_dirX_Orientation(bool isNegative){
	dirX_Negative = isNegative;
}

bool gcode::get_dirX_Orientation(){
	return dirX_Negative;
}

void gcode::set_dirY_Orientation(bool isNegative){
	dirY_Negative = isNegative;
}

bool gcode::get_dirY_Orientation(){
	return dirY_Negative;
}

unsigned int gcode::get_StepsX(){
	return (unsigned int) StepsX;
}

unsigned int gcode::get_StepsY(){
	return (unsigned int) StepsY;
}

void gcode::set_Recursion(unsigned int num){
	Recursion = (unsigned int)num;
}

unsigned int gcode::get_Recursion(){
	return Recursion;
}

bool gcode::get_EoL(){
	return End_of_Line;
}

void gcode::set_Pp_flag(){
	Post_process_flag = true;
}

bool gcode::get_Pp_flag(){
	return Post_process_flag;
}

int gcode::get_Line_Number(){
	return Line_Number;
}

void gcode::set_Line_Number(int Number){
	Line_Number = Number;
}

bool gcode::get_Pen_Position(){
	return Pen_down;
}






}
