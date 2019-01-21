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

char bbuffer[160];
int bnumbuffer[80];
long bisRedVisable;
int bvalue0;

//custom cam picture load
void bgetImage() {
	e_poxxxx_launch_capture((char *)bbuffer);
	while (!e_poxxxx_is_img_ready()) {};
}
// Image processing removes useless information
void bImage() {

	long i;
	int green, blue, vis;
	for (i = 0; i<80; i++) {
		//RGB turned into an integer value for comparison
		blue = ((bbuffer[2 * i + 1] & 0x1F) << 3);
		green = (((bbuffer[2 * i] & 0x07) << 5) | ((bbuffer[2 * i + 1] & 0xE0) >> 3));
		//blue = ((rbuffer[2*i+1] & 0x1F) << 3); we don't need blue for looking for red.
		if (blue > green + 20) { // green will be less then blue when blue is strong.
			bnumbuffer[i] = 1;
			vis++;
		}
		else {
			bnumbuffer[i] = 0;
		}
		//If red is visable then risRedVisable turns to true
		if (vis>0) {
			bisRedVisable = 1;
		}
		else {
			bisRedVisable = 0;
		}
	}
}

//Decide which way to turn based on the number of true pixels.
int bturnDirection() {
	int sumL = 0;
	int sumR = 0;
	int i;
	for (i = 0; i<40; i++) {
		sumL += bnumbuffer[i];
		sumR += bnumbuffer[i + 40];
	}
	if (sumL<sumR) {
		return 1;
	}
	else {
		return 0;
	}
}
//Function to deal with turning.
void bturn(void) {
	if (bturnDirection()) {
		e_set_speed_left(500);
		e_set_speed_right(-500);
	}
	else {
		e_set_speed_left(-500);
		e_set_speed_right(500);
	}
}
void bforward(void) {
	e_set_speed_left(350);
	e_set_speed_right(350);
}

int bstop(void) {
	e_destroy_agenda(bturn);

	e_set_speed_left(0); //go forward on full speed
	e_set_speed_right(0);

	return 0;
}
int b_start_anotherfunction(void) {

	e_set_led(0, 1);
	e_init_prox();

	while (1) {

		//printf("%d/n", e_get_prox(0));
		//printf("%d/n", e_get_prox(7));

		if (e_get_prox(0) > 200 && e_get_prox(7) > 200) {

			e_destroy_agenda(bforward);
			e_set_speed_left(0);
			e_set_speed_right(0);
			break;

		}
		else {
			e_set_led(1, 1);
			e_set_led(7, 1);
			e_activate_agenda(bforward, 200);


		}
	}

	e_activate_agenda(flow_led, 200);
	return 0;

}
//Main function of follower
int approachBlue(void) {
	//basic set up for the camera and 
	e_poxxxx_init_cam();
	e_poxxxx_config_cam(0, (ARRAY_HEIGHT - 4) / 2, 640, 4, 8, 4, RGB_565_MODE);
	e_poxxxx_write_cam_registers();

	e_start_agendas_processing();
	int centreValue;
	int counter = 0;

	while (1) {
		bgetImage();
		bImage();
		e_led_clear();

		//Take a section of the center, this means if there is an error with one it won't effect it as a whole.
		centreValue = bnumbuffer[38] + bnumbuffer[39] + bnumbuffer[40] + bnumbuffer[41] + bnumbuffer[42] + bnumbuffer[43]; // removes stray 
		if (centreValue > 3) { //If red is in the middle then it will go forward 
			e_destroy_agenda(bturn);
			e_set_speed_left(0);
			e_set_speed_right(0);
			e_set_led(0, 1);

			counter = counter + 1;
			e_set_led(counter, 1);

			long i;
			for (i = 0; i < 200000; i++) {
				asm("nop");

			}

		}
		else if (bisRedVisable == 1) {//If red isn't in the center but is visable then picks a direction to turn to face it
			e_activate_agenda(bturn, 650);
			e_set_led(1, 1);
			counter = 0;
		}
		else {// if red isn't visible and no true values it will turn left
			e_destroy_agenda(bturn);
			e_set_speed_left(0);
			e_set_speed_right(0);
			e_set_led(2, 1);
		}
		if (counter == 7) {
			break;
		}

	}

	b_start_anotherfunction();
	return 0;
}
