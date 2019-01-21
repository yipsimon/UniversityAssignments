#include "p30f6014A.h"
#include "stdio.h"
#include "string.h"

#include "a_d/e_prox.h"

#include "uart/e_uart_char.h"
#include "motor_led/e_init_port.h"
#include "motor_led/e_epuck_ports.h"
#include "motor_led/advance_one_timer/e_motors.h"
#include "motor_led/advance_one_timer/e_agenda.h"

#include "camera/fast_2_timer/e_poxxxx.h"
#include "motor_led/advance_one_timer/e_led.h"

#include "imageCapture.h"
#include "findRed.h"
#include "followGreen.h"
#include "rectangle.h"
#include "goalTest.h"
#include "approachRed.h"
#include "approachBlue.h"
#include "behaviours.h"

int flash0(void) {
	long i;
	int led0 = 0;
	e_init_port();
	LED0 = led0 = led0 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	LED0 = led0 = led0 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	return 0;
}

int flash1(void) {
	long i;
	int led1 = 0;
	e_init_port();
	LED1 = led1 = led1 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	LED1 = led1 = led1 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	return 0;
}

int flash2(void) {
	long i;
	int led2 = 0;
	e_init_port();
	LED2 = led2 = led2 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	LED2 = led2 = led2 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	return 0;
}

int flash3(void) {
	long i;
	int led3 = 0;
	e_init_port();
	LED3 = led3 = led3 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	LED3 = led3 = led3 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	return 0;
}

int flash4(void) {
	long i;
	int led4 = 0;
	e_init_port();
	LED4 = led4 = led4 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	LED4 = led4 = led4 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	return 0;
}

int flash5(void) {
	long i;
	int led5 = 0;
	e_init_port();
	LED5 = led5 = led5 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	LED5 = led5 = led5 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	return 0;
}

int flash6(void) {
	long i;
	int led6 = 0;
	e_init_port();
	LED6 = led6 = led6 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	LED6 = led6 = led6 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	return 0;
}

int flash7(void) {
	long i;
	int led7 = 0;
	e_init_port();
	LED7 = led7 = led7 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	LED7 = led7 = led7 ^ 1;
	for (i = 0; i < 500000; i++) {
		asm("nop");
	}
	return 0;
}


int flashClose(void) {
	int value0, value1, value2, value3, value4, value5, value6, value7;
	e_init_port();
	e_init_prox();
	//long counter = 0;
	while (1) {
		value0 = e_get_prox(0);
		value1 = e_get_prox(1);
		value2 = e_get_prox(2);
		value3 = e_get_prox(3);
		value4 = e_get_prox(4);
		value5 = e_get_prox(5);
		value6 = e_get_prox(6);
		value7 = e_get_prox(7);
		if (value0 > value1 && value0 > value2 && value0 > value3 && value0 > value4 && value0 > value5 && value0 > value6 && value0 > value7) {	//LED0 on if an obstacle is detected by proxy0
			flash0();
		}
		else if (value1 > value0 && value1 > value2 && value1 > value3 && value1 > value4 && value1 > value5 && value1 > value6 && value1 > value7) {	//LED0 on if an obstacle is detected by proxy0
			flash1();
		}
		else if (value2 > value0 && value2 > value1 && value2 > value3 && value2 > value4 && value2 > value5 && value2 > value6 && value2 > value7) {	//LED0 on if an obstacle is detected by proxy0
			flash2();
		}
		else if (value3 > value0 && value3 > value1 && value3 > value2 && value3 > value4 && value3 > value5 && value3 > value6 && value3 > value7) {	//LED0 on if an obstacle is detected by proxy0
			flash3();
		}
		else if (value4 > value0 && value4 > value1 && value4 > value2 && value4 > value3 && value4 > value5 && value4 > value6 && value4 > value7) {	//LED0 on if an obstacle is detected by proxy0
			flash5();
		}
		else if (value5 > value0 && value5 > value1 && value5 > value2 && value5 > value3 && value5 > value4 && value5 > value6 && value5 > value7) {	//LED0 on if an obstacle is detected by proxy0
			flash6();
		}
		else if (value6 > value0 && value6 > value1 && value6 > value2 && value6 > value3 && value6 > value4 && value6 > value5 && value6 > value7) {	//LED0 on if an obstacle is detected by proxy0
			flash7();
		}
		else if (value7 > value0 && value7 > value1 && value7 > value2 && value7 > value3 && value7 > value4 && value7 > value5 && value7 > value6) {	//LED0 on if an obstacle is detected by proxy0
			flash0();
		}
		else {
			flash4();
		}

	}

	return 0;
}

void uTurn(void) {
	e_set_speed_left(-500);
	e_set_speed_right(500);
}

void push(void) {
	e_destroy_agenda(uTurn);

	e_set_speed_left(500);
	e_set_speed_right(500);

	long i; //go
	for (i = 0; i < 5000000; i++) { //was 650000
		asm("nop");
	}

	e_set_speed_left(0);
	e_set_speed_right(0);
}

void turn180(long spin90) {

		e_destroy_agenda(uTurn);

		e_activate_agenda(uTurn, 1000);

		long i; //go
		for (i = 0; i < spin90; i++) { //was 650000
			asm("nop");
		}

		e_destroy_agenda(uTurn);

		return 0;
}
void mstop() {
	e_destroy_agenda(uTurn);

	e_set_speed_left(0);
	e_set_speed_right(0);
}

void tstop() {
	e_destroy_agenda(uTurn);

		mstop();

		long i; //go
		for (i = 0; i < 6000000; i++) { //was 650000
			asm("nop");
		}

		return 0;
}

/*int spinRight(void) { //90 degrees
	e_set_speed_left(500); //go forward on half speed
	e_set_speed_right(-500); //go backward on half speed
	long i;
	for (i = 0; i < 639000; i++) { //was 650000
		asm("nop");
	}
	e_set_speed_left(0); //stop
	e_set_speed_right(0);


	long j;
	for (j = 0; j < 639000; j++) {
		asm("nop");
	}


	return 0;
}

void forwardPulse(void) {

	long time = 500000;
	e_init_motors();
	e_set_speed_left(500); //go forward on full speed
	e_set_speed_right(500); //go backward on full speed

	long i; //go
	for (i = 0; i < time; i++) {
		asm("nop");
	}

	e_set_speed_left(0); //stop
	e_set_speed_right(0);

	long j; //pause
	for (j = 0; j < 500000; j++) {
		asm("nop");
	}

}

int rectangle() {
	spinRight();
	forwardPulse(2000000);
	spinRight();
	forwardPulse(2000000);
	spinRight();
	forwardPulse(2000000);
	spinRight();
	forwardPulse(2000000);

	return 0;
}*/

int getselector() {
	return SELECTOR0 + 2*SELECTOR1 + 4*SELECTOR2 + 8*SELECTOR3;
}

int main() {
	int selector;

	long spin90;
	long spin180;
	long correctGoalDistance;
	long correctSensor;

	spin90 = 757800; //At speed 1000
	spin180 = 1400000;
	correctGoalDistance = 8200000; //8000000 1000 1m
	correctSensor = 250;


//init
	e_init_port();
	e_init_uart1(); 
	e_init_motors();

	e_start_agendas_processing();

	selector=getselector();
	
	if (selector==0) {
		love();
	} else if (selector==1) {
		fear();
	} else if (selector==2) {
		curious();
	} else if (selector==3) {
		aggression();
	} else if (selector==4) {
		goalTest(spin90, correctGoalDistance, correctSensor);
	} else if (selector==5) {
		push();
		goalTest(spin90, correctGoalDistance, correctSensor);
		approachRed();		
		turn180(spin90);
		turn180(spin90-60000);
		tstop();
		goalTest(spin90, correctGoalDistance+280000, correctSensor);
		approachBlue();
		push();
		turn180(spin90);
		turn180(spin90);
	} else if (selector==6){
		e_start_follow();
	} else if (selector==7){
		approachBlue();
	} else if (selector==8){
		approachRed();
		turn180(spin180);
		tstop();
		goalTest(spin90, correctGoalDistance+1000000, correctSensor);
		approachBlue();
		push();
		turn180(spin90);
		turn180(spin90);
	} else if (selector==9){
		turn180(spin90);
	}
	
	while(1);
}

