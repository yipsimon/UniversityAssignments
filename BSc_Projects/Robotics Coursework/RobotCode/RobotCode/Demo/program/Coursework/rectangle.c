#include "motor_led/e_init_port.h"
#include "motor_led/e_epuck_ports.h"
#include "a_d/e_prox.h"

#include "p30f6014A.h"
#include "stdio.h"
#include "string.h"

#include "./rectangle.h"

void aforward(void) {
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

void aturn(void) {
	e_set_speed_left(500);
	e_set_speed_right(-500);
}

void aspin(void) {

	e_activate_agenda(aturn, 650);
	long i; //go
	for (i = 0; i < 639000; i++) {
		asm("nop");
	}
}


int rectangle() {

	while (1) {

		e_start_agendas_processing();

		aspin();
		e_destroy_agenda(aturn);
		aforward();
		aspin();
		e_destroy_agenda(aturn);
		aforward();
		aspin();
		e_destroy_agenda(aturn);
		aforward();
		aspin();
		e_destroy_agenda(aturn);
		aforward();
	}

	return 0;
}
