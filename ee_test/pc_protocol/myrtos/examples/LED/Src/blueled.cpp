//
// Created by Chord on 25-6-11.
//


#include "blueled.h"

osThreadId_t BlueLedTaskHandle = nullptr;

const osThreadAttr_t BlueLedTaskAttribute = {.name = "BlueLedTask",
                                            .attr_bits = osThreadDetached,
                                            .cb_mem = nullptr,
                                            .cb_size = 0,
                                            .stack_mem = nullptr,
                                            .stack_size = 128 * 4,
                                            .priority = (osPriority_t)osPriorityBelowNormal,
                                            .tz_module = 0,
                                            .reserved = 0};

void BlueLedTask(void *argument)
{
    UNUSED(argument);
    while (1)
    {
        HAL_GPIO_TogglePin(BLUE_LED_GPIO_Port, BLUE_LED_Pin);
        osDelay(1000);
    }
}

