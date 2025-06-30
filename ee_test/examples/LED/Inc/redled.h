//
// Created by Chord on 25-6-12.
//
#include "stm32f1xx_hal.h"
#include "gpio.h"
#include "main.h"
#include "cmsis_os.h"
#include "stm32f1xx_it.h"

#pragma once

extern osThreadId_t RedLedTaskHandle;

extern const osThreadAttr_t RedLedTaskAttribute;

void RedLedTask(void* argument);