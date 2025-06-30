//
// Created by Chord on 25-6-11.
//

#include "redled.h"

osThreadId_t RedLedTaskHandle = nullptr;

const osThreadAttr_t RedLedTaskAttribute = {.name = "RedLedTask",
                                            .attr_bits = osThreadDetached,
                                            .cb_mem = nullptr,
                                            .cb_size = 0,
                                            .stack_mem = nullptr,
                                            .stack_size = 128 * 4,
                                            .priority = (osPriority_t)osPriorityBelowNormal,
                                            .tz_module = 0,
                                            .reserved = 0};
void RedLedTask(void *argument)
{
    UNUSED(argument);
    while (1)
    {
        HAL_GPIO_TogglePin(RED_LED_GPIO_Port, RED_LED_Pin);
        osDelay(600);
    }
}

