//G-Code Interpreter made by Dominique v1.0

#include "ginterpret.h"

namespace gci{
//Default constructor
interpret::interpret(){}

//Overloaded Constructor
void interpret::translate(std::string CodeLine){
	int Instruction_counter = 0;
  std::istringstream ss(CodeLine); 

  // Traverse through all words 
  while(ss) { 
      // Read a word 
      std::string word; 
      ss >> word; 

      // Print the read word 
      if (word.length() >= 2)
	      Instruction_counter += Analyze(word);
  }; 
  if (Instruction_counter >> 0){
	  if (Movement_type == 1){
		  Calculate_Line(MoveX,MoveY);
		  MoveX = 0;
		  MoveY = 0;
	  }
  }
}

//destructor
interpret::~interpret(){}


void interpret::_initdraw(float X1, float Y1, float X2, float Y2, float RX1, float RY1, float RES)
	{
		Drawlimit_X1 = X1;
		Drawlimit_Y1 = Y1;
		Drawlimit_X2 = X2;
		Drawlimit_Y2 = Y2;
		Ref_point_RX1 = RX1;
		Ref_point_RY1 = RY1;
		Move_RES = RES;
		Last_Pos_X = RX1;
		Last_Pos_Y = RY1;
	}

unsigned int interpret::Calculate_Line(float MovementX, float MovementY){
	bool movex = false;
	bool movey = false;
	bool PP_Flag = false;
	bool is_negativeX = false;
	bool is_negativeY = false;
	unsigned int stepsx = 0;
	unsigned int stepsy = 0;
	int recursion = 0;
	if (MovementX < 0.0){
		is_negativeX = true;
		MovementX = fabs(MovementX);
	}
	if (MovementY < 0){
		is_negativeY = true;
		MovementY = fabs(MovementY);
	}
	if (MovementX == 0)
	{
		movey = true;
		if (MovementY >= (float)200){
			recursion = 1;
			stepsy = (unsigned int) (MovementY / Move_RES)/2;
		}
		else{
			stepsy = (unsigned int) (MovementY / Move_RES);
		}
	}
	else if (MovementY == 0)
	{
		movex = true;
		if (MovementX >= (float)200){
			recursion = 1;
			stepsx = (unsigned int) (MovementX / Move_RES)/2;
		}
		else{
			stepsx = (unsigned int) (MovementX / Move_RES);
		}
	}
	else
	{
		movey = true;
		movex = true;
		if (MovementX == MovementY){
			if (MovementX >= (float)200){
					recursion = 1;
					stepsx = (unsigned int) (MovementX / Move_RES)/2;
					stepsy = stepsx;
			}
			stepsx = (unsigned int) (MovementX / Move_RES);
			stepsy = stepsx;
		}
		else{
			PP_Flag= true;
			if (MovementX >= (float)200 || MovementY >= (float)200){
					recursion = 1;
					stepsx = (unsigned int) (MovementX / Move_RES)/2;
					stepsy = (unsigned int) (MovementY / Move_RES)/2;
			}
			else{
				stepsx = (unsigned int) (MovementX / Move_RES);
				stepsy = (unsigned int) (MovementY / Move_RES);
			}
		}
	}
	gcode NewInstruction(movex, movey, stepsx, stepsy, true);
	NewInstruction.set_Line_Number(Actual_Line_Number);
	if (recursion >> 0){
		NewInstruction.set_Recursion(recursion);
	}
	if (PP_Flag == true){
		NewInstruction.set_Pp_flag();
	}
	if (is_negativeX == true){
		NewInstruction.set_dirX_Orientation(true);
	}
	if (is_negativeY == true){
		NewInstruction.set_dirY_Orientation(true);
	}
	MyInstructions.push_back(NewInstruction);
	return 1;
}

void interpret::set_Resolution(float resolution){
	Move_RES = resolution;
}

void interpret::Next_Instruction(){
	MyInstructions.erase(MyInstructions.begin());
}


int interpret::Analyze(std::string word){
	int Return_val = 0;
	std::cout << word << std::endl;
	char a = *word.begin();
	std::string num = word.substr (1,1 - word.length());
	switch (a)
	{
		case'N': 	{int Num= std::stoi(num, nullptr);
		Actual_Line_Number = Num;
#if DEBUG
							std::cout << "Line Number:" <<  Num << std::endl;
#endif
							break;}
		case'G':{
				int Num= std::stoi(num, nullptr);
				switch (Num){
					case 0:
						Movement_type = 0;
#if DEBUG
						std::cout << " linear interpolation (fast movement)" << std::endl;
#endif
					case 1:
						Movement_type = 1;
#if DEBUG
						std::cout << "linear interpolation" << std::endl;
#endif
						break;
					case 2:
						Movement_type = 2;
#if DEBUG
						std::cout << "circular interpolation CW" << std::endl;
#endif
						break;
					case 3:
						Movement_type = 3;
#if DEBUG
						std::cout << "circular interpolation CCW" << std::endl;
#endif
						break;
					case 90:
						Absolute_Coordinates = 1;
#if DEBUG
						std::cout << "Absolute Coordinates set" << std::endl;
#endif
						break;
					case 91:
						Absolute_Coordinates = 0;
#if DEBUG
						std::cout << "Realtive Coordinates set" << std::endl;
#endif
						break;
					default:
#if DEBUG
						std::cout << "Unknown Command" << std::endl;
#endif
						break;
				}
				break;
				}
		case 'X':{
			float Num = stof(num);
			MoveX = Num;
#if DEBUG
			std::cout << "go in X dir: " << Num << " mm" << std::endl;
#endif
			Return_val =  1;
			break;
		}
		case 'Y':{
			float Num = stof(num);
			MoveY = Num;
#if DEBUG
			std::cout << "go in Y dir: " << Num << " mm" << std::endl;
#endif
			Return_val =  1;
			break;
		}
		case 'R':{
			float Num = stof(num);
			Radius = Num;
#if DEBUG
			std::cout << "radius of sphere" << Num << " mm" << std::endl;
#endif
			break;
		}
		case 'Z':{
			int Num= std::stoi(num, nullptr);
#if DEBUG
			std::cout << "Pen position" << Num << " mm" << std::endl;
#endif
			Return_val =  1;
			break;
		}
		
	}
	return Return_val;
}
}
