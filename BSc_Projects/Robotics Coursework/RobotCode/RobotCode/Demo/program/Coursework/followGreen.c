#include "motor_led/e_init_port.h"
#include "motor_led/e_epuck_ports.h"
#include "motor_led/advance_one_timer/e_motors.h"
#include "motor_led/advance_one_timer/e_agenda.h"
#include "uart/e_uart_char.h"
#include "camera/fast_2_timer/e_poxxxx.h"
#include "motor_led/advance_one_timer/e_led.h"
#include "codec/e_sound.h"
#include "stdio.h"
#include "string.h"
#include "stdlib.h"

#include "./findRed.h"

char gbuffer[160];
int gnumbuffer[80];
long isGreenVisable;


//custom cam picture load
void ggetImage(){
	e_poxxxx_launch_capture((char *)gbuffer);
    while(!e_poxxxx_is_img_ready()){};
}
// Image processing removes useless information
void gImage(){	
	long i;
	int green, red, vis;
	for(i=0; i<80; i++){
		//RGB turned into an integer value for comparison
		red = (gbuffer[2*i] & 0xF8);
		green = (((gbuffer[2*i] & 0x07) << 5) | ((gbuffer[2*i+1] & 0xE0) >> 3));
		//blue = ((gfbwbuffer[2*i+1] & 0x1F) << 3); we don't need blue for looking for green.
		if(green > red + 50){ //Green is usually much higher then red due the the extra bit place in RGB565
			gnumbuffer[i] = 1;
			vis +=1;
		}else{
			gnumbuffer[i] = 0;
		}
		//If Green is visable then isRedVisable turns to true
		if(vis>0){
			isGreenVisable = 1;
		}else{
			isGreenVisable = 0;
		}
	}	
}

//Decide which way to turn based on the number of true pixels.
int gturnDirection(){
	int sumL = 0;
	int sumR = 0;
	int i;
	for(i=0;i<40;i++){
		sumL += gnumbuffer[i];
		sumR += gnumbuffer[i+40];
	}
	if(sumL<sumR){ 
		return 1;
	}else{
		return 0;
	}
}


//Function to deal with turning.
void gturn(void) {
	if(gturnDirection()){
		e_set_speed_left (500);
		e_set_speed_right(-500);
	}else{
		e_set_speed_left (-500);
		e_set_speed_right(500);
	}
	//playall();
	//e_close_sound();
}

void stop1 (void){
		e_set_speed_left (0);
		e_set_speed_right(0);
}


void forward(void){
	e_init_prox();
	if(e_get_prox(0) > 230 || e_get_prox(7) > 230 ){
		e_set_speed_left (0);
		e_set_speed_right(0);
	}	
	else{
		e_destroy_agenda(stop1);
		e_set_speed_left (500);
		e_set_speed_right(500);
	}
}

void gturn2(void) {
	e_init_prox();
	if (gturnDirection() == 0){
		e_set_speed_left (-600);
		e_set_speed_right(600);
	}else{ // if(gturnDirection() == 1)
		e_set_speed_left (600);
		e_set_speed_right(-600);
	}

}

void playsound(void);
void playsound(void){
	e_play_sound(0, 2112);
	long i; 
	for (i = 0; i < 300000; i++) {asm("nop");}
}

int e_start_follow(void){
	//basic set up for the camera and 
	e_poxxxx_init_cam();
	e_poxxxx_config_cam(0,(ARRAY_HEIGHT - 4)/2,640,4,8,4,RGB_565_MODE);
	e_poxxxx_write_cam_registers(); 
	e_end_agendas_processing();
	e_start_agendas_processing();
	int centreValue;
	int counter = 0;
	int robotfind = 0;
 	e_init_sound();
	e_init_prox();

	while(1){
		ggetImage();
		gImage();
		e_led_clear();
		
		e_destroy_agenda(gturn2);

		if(counter == 7 && robotfind == 0){
			robotfind = 1;			
			counter = 0;
		}
		if(counter == 7 && robotfind == 1){
			break;
		}
		//Take a section of the center, this means if there is an error with one it won't effect it as a whole.
		centreValue = gnumbuffer[36] + gnumbuffer[37] + gnumbuffer[38] + gnumbuffer[39] + gnumbuffer[40] + gnumbuffer[41] + gnumbuffer[42] + gnumbuffer[43] + gnumbuffer[44] + gnumbuffer[45]; // removes stray 
		if(centreValue > 2){ //If green is in the middle then it will go forward 
			//e_destroy_agenda(playsound);
			e_destroy_agenda(stop1);
			e_destroy_agenda(gturn2);
				if(robotfind == 0){
					e_destroy_agenda(flow_led);
					e_activate_agenda(stop1, 600);
					counter = counter + 1;
					e_set_led(counter,1);
					long i;
					for (i = 0; i < 100000; i++) {asm("nop");}
					//continue;
				}
				else{
					e_set_led(0,1);
					if(e_get_prox(0) > 220 && e_get_prox(7) > 220 ){
						e_activate_agenda(stop1, 600);
						counter = counter + 1;
						e_set_led(counter,1);
						long j;
						for (j = 0; j < 900000; j++) {asm("nop");}
						}	
					else{
						e_destroy_agenda(stop1);
						e_set_speed_left (800);
						e_set_speed_right(800);
						counter = 0;
					}
				
				}
		}
		else{ 
			e_destroy_agenda(stop1);

			if(robotfind == 0){
				//e_set_front_led(1);
				e_set_body_led(1);
				//e_activate_agenda(playsound,10000);
				counter = 0;		
			}
			else{
				e_activate_agenda(gturn2,500);
				e_set_led(1,1);
				e_set_led(7,1);
				//counter = 0;
			}
		}

	}
	
	finish();
	return 0;		
}

void finish(void);

void finish(void){
	while(1){
		e_activate_agenda(flow_led, 500);
		e_play_sound(2116, 1760);
		long i; 
		for (i = 0; i < 500000; i++) {asm("nop");}
	}
}
