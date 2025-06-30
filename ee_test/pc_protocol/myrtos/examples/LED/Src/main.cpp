//
// Created by Chord on 25-6-11.
//

#include "stm32f1xx_hal.h"
#include "gpio.h"
#include "main.h"

#include <cstdio>

#include "cmsis_os.h"
#include "stm32f1xx_it.h"
#include "blueled.h"
#include "redled.h"



#ifdef __cplusplus
extern "C" {
#endif

void RTOS_Threads_Init(void) {
	//    extimuTaskHandle = osThreadNew(extimuTask, nullptr, &extimuTaskAttribute);
	// 分别启动每个任务
	BlueLedTaskHandle = osThreadNew(BlueLedTask, nullptr, &BlueLedTaskAttribute);
	RedLedTaskHandle = osThreadNew(RedLedTask, nullptr, &RedLedTaskAttribute);
}

#ifdef __cplusplus
}
#endif