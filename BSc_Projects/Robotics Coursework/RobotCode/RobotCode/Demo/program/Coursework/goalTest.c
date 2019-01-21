#include "p30f6014A.h"
#include "stdio.h"
#include "string.h"

#include "motor_led/e_init_port.h"
#include "motor_led/e_epuck_ports.h"
#include "motor_led/advance_one_timer/e_motors.h"
#include "motor_led/advance_one_timer/e_agenda.h"
#include "a_d/e_prox.h"

#include "./goalTest.h"

int flashSpecific(long pos) {
	long position;
	position = pos;
	long i;
	int led0 = 0;
	int led1 = 0;
	int led2 = 0;
	int led3 = 0;
	int led4 = 0;
	int led5 = 0;
	int led6 = 0;
	int led7 = 0;
	e_init_port();

	switch (position) {
	case 0:
		LED0 = led0 = led0 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED0 = led0 = led0 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 1:
		LED1 = led1 = led1 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED1 = led1 = led1 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 2:
		LED2 = led2 = led2 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED2 = led2 = led2 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 3:
		LED3 = led3 = led3 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED3 = led3 = led3 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 4:
		LED4 = led4 = led4 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED4 = led4 = led4 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 5:
		LED5 = led5 = led5 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED5 = led5 = led5 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 6:
		LED6 = led6 = led6 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED6 = led6 = led6 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 7:
		LED7 = led7 = led7 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED7 = led7 = led7 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 8:
		break;
	}

	return 0;
}

void lTurn(void) {
	e_set_speed_left(-500);
	e_set_speed_right(500);
}

void rTurn(void) {
	e_set_speed_left(500);
	e_set_speed_right(-500);
}

int spinLeft(long spin90) { //90 degrees

	e_activate_agenda(lTurn, 1000);

	long i; //go
	for (i = 0; i < spin90; i++) { //was 650000
		asm("nop");
	}

	e_destroy_agenda(lTurn);

	return 0;
}

int spinRight(long spin90) { //90 degrees

	e_activate_agenda(rTurn, 1000);

	long i; //go
	for (i = 0; i < spin90; i++) { //was 650000
		asm("nop");
	}

	e_destroy_agenda(rTurn);

	return 0;
}

int goForward(void) {
	e_destroy_agenda(lTurn);
	e_destroy_agenda(rTurn);

	e_set_speed_left(500); //go forward on full speed
	e_set_speed_right(500);

	return 0;
}

int stop(void) {
	e_destroy_agenda(lTurn);
	e_destroy_agenda(rTurn);

	e_set_speed_left(0); //go forward on full speed
	e_set_speed_right(0);

	return 0;
}


int goalTest(long correct90, long correctGoalDistance, long correctSensor) {

	e_start_agendas_processing();


	e_init_motors();
	e_init_port();
	e_init_prox();

	int led0 = 0;
	int led1 = 0;
	int led2 = 0;
	int led3 = 0;
	int led4 = 0;
	int led5 = 0;
	int led6 = 0;
	int led7 = 0;

	long distanceRemaining;
	distanceRemaining = correctGoalDistance;

	long horizontalDisplacement;
	horizontalDisplacement = 0;

	long goalDirection;
	goalDirection = 0;

	long percentagePoint;
	percentagePoint = (correctGoalDistance / 100);

	long pulseLength1;
	pulseLength1 = (percentagePoint * 5);

	long pulseLength2;
	pulseLength2 = 1500000;

	int ping0;
	int ping1;
	int ping2;
	int ping3;

	long a;

	int clear;
	clear = 0;

	while (distanceRemaining > 0) {
		ping0 = e_get_prox(0);
		ping1 = e_get_prox(2);
		ping2 = e_get_prox(3);
		ping3 = e_get_prox(5);
		if (e_get_prox(0) < 220 || e_get_prox(7) < 220) {


			goForward();
			for (a = 0; a < pulseLength1; a++) {
				asm("nop");
			}
			distanceRemaining = distanceRemaining - pulseLength1;
		}
		else {//some obstacle
			stop();
			for (a = 0; a < pulseLength1; a++) {
				asm("nop");
			}
			spinRight(correct90);
			if (e_get_prox(7) > 220) {//avoid left---------------------
				spinLeft(correct90);
				spinLeft(correct90);

				goForward();
				for (a = 0; a < (pulseLength2); a++) {
					asm("nop");
				}
				stop();
				for (a = 0; a < pulseLength1; a++) {
					asm("nop");
				}
				spinRight(correct90);

				if (e_get_prox(0) > 220 || e_get_prox(7) > 220) {//further along too
					spinLeft(correct90); //to left
					goForward();
					for (a = 0; a < (pulseLength2); a++) {
						asm("nop");
					}
					stop();
					for (a = 0; a < pulseLength1; a++) {
						asm("nop");
					}
					spinRight(correct90);//to forward

					goForward();
					for (a = 0; a < (pulseLength1 * 2); a++) {
						asm("nop");
					}
					distanceRemaining = distanceRemaining - (pulseLength1 * 2);
					stop();
					for (a = 0; a < pulseLength1; a++) {
						asm("nop");
					}
					if (e_get_prox(0) > 220 || e_get_prox(7) > 220) {//part way along avoid
						spinLeft(correct90);
						goForward();
						for (a = 0; a < (pulseLength2); a++) {
							asm("nop");
						}
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinRight(correct90);
						goForward();
						for (a = 0; a < (pulseLength1 * 2); a++) {
							asm("nop");
						}
						distanceRemaining = distanceRemaining - (pulseLength1 * 2);
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinRight(correct90);
						goForward();
						for (a = 0; a < (pulseLength2); a++) {
							asm("nop");
						}
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}

					}
					else {
						goForward();
						for (a = 0; a < (pulseLength1 * 2); a++) {
							asm("nop");
						}
						distanceRemaining = distanceRemaining - (pulseLength1 * 2);
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinRight(correct90);
					}


					goForward();
					for (a = 0; a < (pulseLength2); a++) {
						asm("nop");
					}
					stop();
					for (a = 0; a < pulseLength1; a++) {
						asm("nop");
					}

				}//end further elong too
				else {
					goForward();
					for (a = 0; a < (pulseLength1 * 2); a++) {
						asm("nop");
					}
					distanceRemaining = distanceRemaining - (pulseLength1 * 2);
					stop();
					for (a = 0; a < pulseLength1; a++) {
						asm("nop");
					}
					if (e_get_prox(0) > 220 || e_get_prox(7) > 220) {//part way along avoid
						spinLeft(correct90);
						goForward();
						for (a = 0; a < (pulseLength2); a++) {
							asm("nop");
						}
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinRight(correct90);
						goForward();
						for (a = 0; a < (pulseLength1 * 2); a++) {
							asm("nop");
						}
						distanceRemaining = distanceRemaining - (pulseLength1 * 2);
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinRight(correct90);
						goForward();
						for (a = 0; a < (pulseLength2); a++) {
							asm("nop");
						}
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}

					}
					else {
						goForward();
						for (a = 0; a < (pulseLength1 * 2); a++) {
							asm("nop");
						}
						distanceRemaining = distanceRemaining - (pulseLength1 * 2);
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinRight(correct90);
					}
				}

				goForward();
				for (a = 0; a < (pulseLength2); a++) {
					asm("nop");
				}
				stop();
				for (a = 0; a < pulseLength1; a++) {
					asm("nop");
				}
				spinLeft(correct90);
			}//end avoid left---------------------------

			else {//avoid right--------------------------------------
				goForward();
				for (a = 0; a < (pulseLength2); a++) {
					asm("nop");
				}
				stop();
				for (a = 0; a < pulseLength1; a++) {
					asm("nop");
				}
				spinLeft(correct90);



				if (e_get_prox(0) > 220 || e_get_prox(7) > 220) {//further along too
					spinRight(correct90); //to left
					goForward();
					for (a = 0; a < (pulseLength2); a++) {
						asm("nop");
					}
					stop();
					for (a = 0; a < pulseLength1; a++) {
						asm("nop");
					}
					spinLeft(correct90);//to forward

					goForward();
					for (a = 0; a < (pulseLength1 * 2); a++) {
						asm("nop");
					}
					distanceRemaining = distanceRemaining - (pulseLength1 * 2);
					stop();
					for (a = 0; a < pulseLength1; a++) {
						asm("nop");
					}
					if (e_get_prox(0) > 220 || e_get_prox(7) > 220) {//part way along avoid
						spinRight(correct90);
						goForward();
						for (a = 0; a < (pulseLength2); a++) {
							asm("nop");
						}
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinLeft(correct90);
						goForward();
						for (a = 0; a < (pulseLength1 * 2); a++) {
							asm("nop");
						}
						distanceRemaining = distanceRemaining - (pulseLength1 * 2);
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinLeft(correct90);
						goForward();
						for (a = 0; a < (pulseLength2); a++) {
							asm("nop");
						}
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}

					}
					else {
						goForward();
						for (a = 0; a < (pulseLength1 * 2); a++) {
							asm("nop");
						}
						distanceRemaining = distanceRemaining - (pulseLength1 * 2);
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinLeft(correct90);
					}


					goForward();
					for (a = 0; a < (pulseLength2); a++) {
						asm("nop");
					}
					stop();
					for (a = 0; a < pulseLength1; a++) {
						asm("nop");
					}

				}//end further elong too
				else {
					goForward();
					for (a = 0; a < (pulseLength1 * 2); a++) {
						asm("nop");
					}
					distanceRemaining = distanceRemaining - (pulseLength1 * 2);
					stop();
					for (a = 0; a < pulseLength1; a++) {
						asm("nop");
					}
					if (e_get_prox(0) > 220 || e_get_prox(7) > 220) {//part way along avoid
						spinRight(correct90);
						goForward();
						for (a = 0; a < (pulseLength2); a++) {
							asm("nop");
						}
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinLeft(correct90);
						goForward();
						for (a = 0; a < (pulseLength1 * 2); a++) {
							asm("nop");
						}
						distanceRemaining = distanceRemaining - (pulseLength1 * 2);
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinLeft(correct90);
						goForward();
						for (a = 0; a < (pulseLength2); a++) {
							asm("nop");
						}
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}

					}
					else {
						goForward();
						for (a = 0; a < (pulseLength1 * 2); a++) {
							asm("nop");
						}
						distanceRemaining = distanceRemaining - (pulseLength1 * 2);
						stop();
						for (a = 0; a < pulseLength1; a++) {
							asm("nop");
						}
						spinLeft(correct90);
					}
				}

				goForward();
				for (a = 0; a < (pulseLength2); a++) {
					asm("nop");
				}
				stop();
				for (a = 0; a < pulseLength1; a++) {
					asm("nop");
				}
				spinRight(correct90);
			}//end avoid right------------------------
		}//end obstacle forward
	}

	stop();
	flashSpecific(4);
	flashSpecific(1);
	flashSpecific(4);
	flashSpecific(1);
	flashSpecific(4);

	return 0;
}