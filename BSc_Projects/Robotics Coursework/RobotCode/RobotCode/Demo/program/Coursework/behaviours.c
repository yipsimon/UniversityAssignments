#include "motor_led/e_init_port.h"
#include "motor_led/e_epuck_ports.h"
#include "motor_led/advance_one_timer/e_motors.h"
#include "motor_led/advance_one_timer/e_agenda.h"
#include "motor_led/advance_one_timer/e_led.h"

#include "a_d/advance_ad_scan/e_ad_conv2.h"
#include "a_d/advance_ad_scan/e_prox2.h"
#include "a_d/e_ad_conv.h"
#include "a_d/e_prox.h"

#define PROXSCALING_FOLLOW 20
#define PROXSCALING_SHOCK 4
#define BASICSPEED 550


#define LEFT_FOLLOW			0		// behaviors IDs	
#define RIGHT_FOLLOW		1 

#define NB_SENSORS          8		// number of sensors
#define BIAS_SPEED      	350		// robot bias speed
#define SENSOR_THRESHOLD	300		// discount sensor noise below threshold
#define MAXSPEED 			800		// maximum robot speed


int follow_sensorzero[8];
int follow_weightleft[8] = {-10,-10,-5,0,0,5,10,10};
int follow_weightright[8] = {10,10,5,0,0,-5,-10,-10};

int followgetSelectorValue() {
	return SELECTOR0 + 2*SELECTOR1 + 4*SELECTOR2 + 8*SELECTOR3;
}

void wait(long num) {
	long i;
	for(i=0;i<num;i++);
}


/*! \breif Read the sensors proxymities
 * \param sensorTable Where the value must be stocked
 */
void followGetSensorValues(int *sensorTable) {
	unsigned int i;
	for (i=0; i < NB_SENSORS; i++) {
		sensorTable[i] = e_get_calibrated_prox2(i); //e_get_prox(i) - follow_sensorzero[i];
	}		
}

/*! \brief Set robot speed */
void followsetSpeed(int LeftSpeed, int RightSpeed) {
	if (LeftSpeed < -MAXSPEED) {LeftSpeed = -MAXSPEED;}
	if (LeftSpeed >  MAXSPEED) {LeftSpeed =  MAXSPEED;}
	if (RightSpeed < -MAXSPEED) {RightSpeed = -MAXSPEED;}
	if (RightSpeed >  MAXSPEED) {RightSpeed =  MAXSPEED;}
	e_set_speed_left(LeftSpeed);
	e_set_speed_right(RightSpeed); 
}

/*! \brief The "main" function of the program */
void curious() {
	int leftwheel, rightwheel;		// motor speed left and right
	int distances[NB_SENSORS];		// array keeping the distance sensor readings
	int i;							// FOR-loop counters
	int gostraight;
	int loopcount;
	unsigned char selector_change;
	 
	e_init_port();
	e_init_ad_scan(ALL_ADC);
	e_init_motors();
	e_start_agendas_processing();

	//follow_sensor_calibrate();	
	
	e_activate_agenda(left_led, 2500);
	e_activate_agenda(right_led, 2500);
	e_pause_agenda(left_led);
	e_pause_agenda(right_led);
	
	e_calibrate_ir2();
	loopcount=0;
	selector_change = !(followgetSelectorValue() & 0x0001);

	while (1) {
		followGetSensorValues(distances); // read sensor values

		gostraight=0;
		if ((followgetSelectorValue() & 0x0001) == RIGHT_FOLLOW) {
			if(selector_change == LEFT_FOLLOW) {
				selector_change = RIGHT_FOLLOW;
				e_led_clear();
				e_pause_agenda(left_led);
				e_restart_agenda(right_led);
			}  
			for (i=0; i<8; i++) {
				if (distances[i]>50) {break;}
			}
			if (i==8) {
				gostraight=1;
			} else {
				follow_weightleft[0]=-10;
				follow_weightleft[7]=-10;
				follow_weightright[0]=10;
				follow_weightright[7]=10;
				if (distances[2]>300) {
					distances[1]-=200;
					distances[2]-=600;
					distances[3]-=100;
				}
			}
		} else {
			if(selector_change == RIGHT_FOLLOW) {
				selector_change = LEFT_FOLLOW;
				e_led_clear();
				e_pause_agenda(right_led);
				e_restart_agenda(left_led);
			}
			for (i=0; i<8; i++) {
				if (distances[i]>50) {break;}
			}
			if (i==8) {
				gostraight=1;
			} else {
				follow_weightleft[0]=10;
				follow_weightleft[7]=10;
				follow_weightright[0]=-10;
				follow_weightright[7]=-10;
				if (distances[5]>300) {
					distances[4]-=100;
					distances[5]-=600;
					distances[6]-=200;
				}
			}
		}

		leftwheel=BIAS_SPEED;
		rightwheel=BIAS_SPEED;
		if (gostraight==0) {
			for (i=0; i<8; i++) {
				leftwheel+=follow_weightleft[i]*(distances[i]>>4);
				rightwheel+=follow_weightright[i]*(distances[i]>>4);
			}
		}

		// set robot speed
		followsetSpeed(leftwheel, rightwheel);

		wait(15000);
	}	
}






int i, s, m;
long potential[2];
int speed[2];
long ProxSensOffBuf[8];
int ui_lin = 0;

int factor_array[2][8] =
	{{-10,-30,15,0,0,-15,30,10},
	{10,30,-15,0,0,15,-30,-10}};

int matrix_prox[2][8] =
	{{8,4,2,0,0,-4,-8,-16},
	{-16,-8,-4,0,0,2,4,8}};

void shock_neuron(void)
{
	for (m = 0; m < 2; m++)
	{
		potential[m] = 0;
		for (s = 0; s < 8; s++)
			potential[m] += (matrix_prox[m][s]*e_get_calibrated_prox2(s)); // get values from proximity sensors
        speed[m] = (potential[m]/PROXSCALING_SHOCK + BASICSPEED);
	}

	if((speed[1] < 50 && speed[1] > -50)
		&& (speed[0] < 50 && speed[0] > -50)) {
		speed[1] = speed[1] * 20;
		speed[0] = speed[0] * 20;
	}

	if (speed[1] > 1000)
		speed[1] = 1000;
	else if (speed[1] < -1000 )
		speed[1] = -1000;

	if (speed[0] > 1000)
		speed[0] = 1000;
	else if (speed[0] < -1000 )
		speed[0] = -1000;

	e_set_speed_left(speed[1]);
	e_set_speed_right(speed[0]);
}

int lin_speed_calc(int distance, int gain)
{
	int consigne = 100;
	float h = 0.05;
	int ti = 3;
	int ecart = consigne-distance;
	int lin_speed;

	ui_lin = ui_lin + h * ecart / ti;
	lin_speed = (ecart + ui_lin) * gain;

	if(lin_speed >= 1000)
	{
		ui_lin = 999/gain - ecart;
		if(ui_lin > 60)			
			ui_lin = 60.0;
		lin_speed = 999;
	}
	else if(lin_speed <= -1000)
	{
		ui_lin = -999/gain + ecart;
		if(ui_lin < -10)		
			ui_lin = -10.0;
		lin_speed = -999;
	}
	return lin_speed;
}

int angle_speed_calc(int pos, int gain)
{
	int consigne = 0;
	int angle_speed = 0;
	int ecart = consigne - pos;

	angle_speed = ecart*gain;

	if(angle_speed >= 1000)
		angle_speed = 999;
	else if(angle_speed <= -1000)
		angle_speed = -999;

	return angle_speed;
}

void follow_neuron(void)
{
	int lin_speed = lin_speed_calc((e_get_calibrated_prox2(7)+e_get_calibrated_prox2(0))/2, 6);
	int angle_speed = angle_speed_calc((e_get_calibrated_prox2(0)+e_get_calibrated_prox2(1)) -
										(e_get_calibrated_prox2(7)+e_get_calibrated_prox2(6)), 4);

	e_set_speed_left (lin_speed - angle_speed);
	e_set_speed_right(lin_speed + angle_speed);
}

int flashBuildup(long pos) {
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
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 2:
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 3:
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 4:
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		LED4 = led4 = led4 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		LED4 = led4 = led4 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 5:
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		LED4 = led4 = led4 ^ 1;
		LED5 = led5 = led5 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		LED4 = led4 = led4 ^ 1;
		LED5 = led5 = led5 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 6:
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		LED4 = led4 = led4 ^ 1;
		LED5 = led5 = led5 ^ 1;
		LED6 = led6 = led6 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		LED4 = led4 = led4 ^ 1;
		LED5 = led5 = led5 ^ 1;
		LED6 = led6 = led6 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		break;
	case 7:
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		LED4 = led4 = led4 ^ 1;
		LED5 = led5 = led5 ^ 1;
		LED6 = led6 = led6 ^ 1;
		LED7 = led7 = led7 ^ 1;
		for (i = 0; i < 500000; i++) {
			asm("nop");
		}
		LED0 = led0 = led0 ^ 1;
		LED1 = led1 = led1 ^ 1;
		LED2 = led2 = led2 ^ 1;
		LED3 = led3 = led3 ^ 1;
		LED4 = led4 = led4 ^ 1;
		LED5 = led5 = led5 ^ 1;
		LED6 = led6 = led6 ^ 1;
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

/*! \brief The "main" function of fear */
void fear(void)
{	
	e_init_port();
	e_init_motors();
	e_init_ad_scan(ALL_ADC);
	
	e_calibrate_ir2();

	e_activate_agenda(flow_led, 900);
	e_activate_agenda(shock_neuron, 650);
	e_start_agendas_processing();
	while(1);
}

void love(void)
{
	e_init_port();
	e_init_motors();
	e_init_ad_scan(ALL_ADC);
	
	e_calibrate_ir2();

	e_activate_agenda(k2000_led, 2500);
	e_activate_agenda(follow_neuron, 650);
	e_start_agendas_processing();
	while(1);
}

int spinLeft1(long spin90) { //90 degrees
	e_init_motors();
	e_set_speed_left(-1000); //go forward on half speed
	e_set_speed_right(1000); //go backward on half speed
	long i;
	for (i = 0; i < spin90; i++) { //was 650000
		asm("nop");
	}
	e_set_speed_left(0); //stop
	e_set_speed_right(0);


	/*long j;
	for (j = 0; j < 650000; j++) {
	asm("nop");
	}*/


	return 0;
}

int aggression() {
	e_init_motors();
	e_init_port();
	e_init_prox();
	long a;
	int clear;
	clear = 0;
	while (clear == 0) {
		e_set_speed_left(400); //slow speed
		e_set_speed_right(400);

		for (a = 0; a < 10000; a++) {  // change number for slow walk
			asm("nop");
		}			
		int jab;
		jab = 0;
		while (jab < 9){
		
			if (e_get_prox(0) > 300) {
				e_set_speed_left(1000);
				e_set_speed_right(1000);

				for (a = 0; a < 50000; a++) { //number controls length of aggression
					asm("nop");
				}
				e_set_speed_left(0);
				e_set_speed_right(0);

				for (a = 0; a < 50000; a++) { //number controls length of aggression
					asm("nop");
				}
			
				e_set_speed_left(-800);
				e_set_speed_right(-800);

				for (a = 0; a < 50000; a++) { //number controls length of aggression
					asm("nop");
				}

				e_set_speed_left(0);
				e_set_speed_right(0);

				for (a = 0; a < 50000; a++) { //number controls length of aggression
					asm("nop");
				}

				if (jab == 8){
					flashBuildup(7);
					e_set_speed_left(1000);
					e_set_speed_right(1000);

					for (a = 0; a < 1000000; a++) { //number controls length of aggression
						asm("nop");
					}
					e_set_speed_left(0);
					e_set_speed_right(0);

					for (a = 0; a < 1000000; a++) { //number controls length of aggression
						asm("nop");
					}

				
					jab = 10; 
					spinLeft1(700000);
				}
				flashBuildup(jab); //flashes front led
				jab = jab+1;
				
			}
			else {
				jab = 10;
			}
			
		}
		
	}
}