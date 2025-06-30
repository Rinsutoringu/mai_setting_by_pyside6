//
// Created by Chord on 25-6-13.
//
#include "stm32f1xx_hal.h"
#include "gpio.h"
#include "main.h"
#include "cmsis_os.h"
#include "stm32f1xx_it.h"

void RTOS_Threads_Init(void) {
	//    extimuTaskHandle = osThreadNew(extimuTask, nullptr, &extimuTaskAttribute);
	// 分别启动每个任务
}