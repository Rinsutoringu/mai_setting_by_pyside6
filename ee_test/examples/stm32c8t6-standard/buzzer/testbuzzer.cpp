//
// Created by Chord on 25-6-14.
//

#include "stm32f1xx_hal.h"
#include "gpio.h"
#include "main.h"
#include "cmsis_os.h"
#include "stm32f1xx_it.h"
#include "testbuzzer.h"
#include "tim.h"


Buzzer buzzer(BUZZER_PIN_GPIO_Port, BUZZER_PIN_Pin, &htim3, TIM_CHANNEL_1);

void RTOS_Threads_Init(void) {
	buzzer.init();
	
	while (1)
	{
		buzzer.start_buzzer();
		osDelay(500);
		buzzer.stop_buzzer();
		osDelay(500);
	}

}