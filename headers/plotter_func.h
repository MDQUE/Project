/*
 * plotter_func.h
 *
 *  Created on: Jun 20, 2019
 *      Author: verena
 */

#ifndef PLOTTER_FUNC_H
#define PLOTTER_FUNC_H

#include "mbed.h"
#include "rtos.h"
#include <stdlib.h>
#include <string>
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <cmath>
#include <queue>
#include "setup.h"
#include <pthread.h>
#include "msgqueue_func.h"


void plotter_move(unsigned int move);
void plotter_reset();
void plotter_line(int steps, int direction);
void plotter_diagnal(int x_steps, int x_dir, int y_steps, int y_dir)

#endif
