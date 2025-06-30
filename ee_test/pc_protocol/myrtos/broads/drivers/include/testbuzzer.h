//
// Created by Chord on 25-6-13.
//

#pragma once

#include "cmsis_os2.h"
#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_gpio.h"

class Buzzer {
public:
	Buzzer(GPIO_TypeDef* buzzer_port, uint16_t buzzer_pin,TIM_HandleTypeDef* buzzer_tim, uint32_t buzzerchannel);
	void init();
	void play(uint16_t time, uint16_t frequency);
	void delay(uint32_t delay);
	void set_frequency(uint32_t frequency);
	void start_buzzer();
	void stop_buzzer();
private:
	GPIO_TypeDef* buzzer_port_;
	uint16_t buzzer_pin_;
	uint32_t buzzer_frequency_;
	TIM_HandleTypeDef* buzzer_tim_;
	TIM_OC_InitTypeDef sConfigOC_;
	uint32_t buzzer_channel_;

};



