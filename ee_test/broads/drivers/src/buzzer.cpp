//
// Created by Chord on 25-6-13.
//

#include "../include/testbuzzer.h"



Buzzer::Buzzer(GPIO_TypeDef* buzzer_port, uint16_t buzzer_pin, TIM_HandleTypeDef* buzzer_tim, uint32_t buzzerchannel):
	buzzer_port_(buzzer_port),
	buzzer_pin_(buzzer_pin),
	buzzer_tim_(buzzer_tim),
	sConfigOC_{0},
	buzzer_channel_(buzzerchannel)
	{}

// 初始化蜂鸣器设备
void Buzzer::init()
{
	GPIO_InitTypeDef buzzer_gpio;
	buzzer_gpio.Pin = buzzer_pin_;
	buzzer_gpio.Mode = GPIO_MODE_AF_PP;
	buzzer_gpio.Speed = GPIO_SPEED_FREQ_MEDIUM;
	buzzer_gpio.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(buzzer_port_, &buzzer_gpio);

	__HAL_RCC_TIM3_CLK_ENABLE();
	__HAL_RCC_GPIOB_CLK_ENABLE();
	// 计算公式: 频率 = TIM_CLK / ((PSC+1)*(ARR+1))
	// 例如: 36MHz / ((899+1)*(19+1)) = 2kHz

	buzzer_tim_->Instance = TIM3;
	buzzer_tim_->Init.Prescaler = 899;   // 预分频器
	buzzer_tim_->Init.CounterMode = TIM_COUNTERMODE_UP;
	buzzer_tim_->Init.Period = 19;       // 自动重装载值
	buzzer_tim_->Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
	buzzer_tim_->Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
	HAL_TIM_PWM_Init(buzzer_tim_);

	// 配置PWM通道
	sConfigOC_.OCMode = TIM_OCMODE_PWM1;
	sConfigOC_.Pulse = 10; // 占空比50%，Pulse=Period/2
	sConfigOC_.OCPolarity = TIM_OCPOLARITY_LOW;
	sConfigOC_.OCFastMode = TIM_OCFAST_DISABLE;
	HAL_TIM_PWM_ConfigChannel(buzzer_tim_, &sConfigOC_, buzzer_channel_);
}

// 启动蜂鸣器
void Buzzer::start_buzzer()
{
	HAL_TIM_PWM_Start(buzzer_tim_, buzzer_channel_);
}

// 停止蜂鸣器
void Buzzer::stop_buzzer()
{
	HAL_TIM_PWM_Stop(buzzer_tim_, buzzer_channel_);
}

// 配置蜂鸣器频率
void Buzzer::set_frequency(uint32_t frequency)
{
	// 以36MHz时钟为例，目标频率 = 36MHz / ((PSC+1)*(ARR+1))
	// 这里简单设PSC=71，则计数频率500kHz，ARR = (500000/frequency)-1
	uint32_t psc = 71;
	uint32_t arr = 500000 / frequency - 1;

	buzzer_tim_->Init.Prescaler = psc;
	buzzer_tim_->Init.Period = arr;
	HAL_TIM_PWM_Init(buzzer_tim_);

	sConfigOC_.Pulse = (arr + 1) / 2; // 50%占空比
	HAL_TIM_PWM_ConfigChannel(buzzer_tim_, &sConfigOC_, buzzer_channel_);
}

void Buzzer::delay(uint32_t delay)
{
	osDelay(delay);
}

// 设置频率，启动输出，运行指定时间后关闭pwm输出
void Buzzer::play(uint16_t time, uint16_t frequency)
{
	set_frequency(frequency);
	start_buzzer();
	delay(time);
	stop_buzzer();
}
