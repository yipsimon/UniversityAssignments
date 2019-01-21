#include "motor_led/e_init_port.h"
#include "motor_led/e_epuck_ports.h"
#include "motor_led/advance_one_timer/e_motors.h"
#include "motor_led/advance_one_timer/e_agenda.h"
#include "uart/e_uart_char.h"
#include "camera/fast_2_timer/e_poxxxx.h"
#include "motor_led/advance_one_timer/e_led.h"

#include "a_d/e_prox.h"

#include "stdio.h"
#include "string.h"
#include "stdlib.h"

#include "./findRed.h"

char rbuffer[160];
int rnumbuffer[80];
long risRedVisable;
int rvalue0;

int getdistance(){
	e_init_port();
	e_init_prox();

	rvalue0 = e_get_prox(0);

	return 0;

}

//custom cam picture load
void rgetImage() {
	e_poxxxx_launch_capture((char *)rbuffer);
	while (!e_poxxxx_is_img_ready()) {};
}
// Image processing removes useless information
void rImage() {

	long i;
	int green, red, vis;
	for (i = 0; i<80; i++) {
		//RGB turned into an integer value for comparison
		red = (rbuffer[2 * i] & 0xF8);
		green = (((rbuffer[2 * i] & 0x07) << 5) | ((rbuffer[2 * i + 1] & 0xE0) >> 3));
		//blue = ((rbuffer[2*i+1] & 0x1F) << 3); we don't need blue for looking for red.
		if (red > green + 20) { // green will be less then red when red is strong.
			rnumbuffer[i] = 1;
			vis++;
		}
		else {
			rnumbuffer[i] = 0;
		}
		//If red is visable then risRedVisable turns to true
		if (vis>0) {
			risRedVisable = 1;
		}
		else {
			risRedVisable = 0;
		}
	}
}

//Decide which way to turn based on the number of true pixels.
int rturnDirection() {
	int sumL = 0;
	int sumR = 0;
	int i;
	for (i = 0; i<40; i++) {
		sumL += rnumbuffer[i];
		sumR += rnumbuffer[i + 40];
	}
	if (sumL<sumR) {
		return 1;
	}
	else {
		return 0;
	}
}
//Function to deal with turning.
void rturn(void) {
	//if (rturnDirection()) {
		e_set_speed_left(500);
		e_set_speed_right(-500);
	//}
	//else {
		e_set_speed_left(-500);
		e_set_speed_right(500);
	//}
}
void rforward(void) {
	e_set_speed_left(350);
	e_set_speed_right(350);
}

int rstop(void) {
	e_destroy_agenda(rturn);

	e_set_speed_left(0); //go forward on full speed
	e_set_speed_right(0);

	return 0;
}
int e_start_anotherfunction(void) {

	e_init_prox();

	while (1) {

		if (e_get_prox(0) > 2000 || e_get_prox(7) > 2000) {

			e_destroy_agenda(rforward);
			e_set_speed_left(0);
			e_set_speed_right(0);
			break;

		}
		else {
			e_set_led(1, 1);
			e_set_led(7, 1);
			e_activate_agenda(rforward, 200);
		}
	}

	e_activate_agenda(flow_led, 200);
	return 0;

}
//Main function of follower
int approachRed(void) {
	//basic set up for the camera and 
	e_poxxxx_init_cam();
	e_poxxxx_config_cam(0, (ARRAY_HEIGHT - 4) / 2, 640, 4, 8, 4, RGB_565_MODE);
	e_poxxxx_write_cam_registers();

	e_start_agendas_processing();
	int centreValue;
	int counter = 0;

	while (1) {
		rgetImage();
		rImage();
		e_led_clear();

			//Take a section of the center, this means if there is an error with one it won't effect it as a whole.
			centreValue = rnumbuffer[38] + rnumbuffer[39] + rnumbuffer[40] + rnumbuffer[41] + rnumbuffer[42] + rnumbuffer[43]; // removes stray 
			if (centreValue > 3) { //If red is in the middle then it will go forward 
				e_destroy_agenda(rturn);
				e_set_speed_left(0);
				e_set_speed_right(0);
				e_set_led(0, 1);

				counter = counter + 1;
				e_set_led(counter, 1);

				long i;
				for (i = 0; i < 400000; i++) {
					asm("nop");

				}

			}
			else if (risRedVisable == 1) {//If red isn't in the center but is visable then picks a direction to turn to face it
				e_activate_agenda(rturn, 650);
				e_set_led(1, 1);
				counter = 0;
			}
			else {// if red isn't visible and no true values it will turn left
				e_destroy_agenda(rturn);
				e_set_speed_left(-500);
				e_set_speed_right(500);
			}
			if (counter == 7) {
				break;
			}

		}

	e_start_anotherfunction();
	return 0;
	}
