
#include <stdlib.h>
#include <stdio.h>
#include <wiringPi.h>

#define PULSE_LENGTH 189

/* protocol (times pulse length) : 
 * 0 : 1 high, 3 low
 * 1 : 3 high, 1 low
 */  

char *num2char(unsigned int num)
{
	char *code_table;
	int i;

	code_table = malloc(32 * sizeof(char));

	if (code_table == NULL) {
		printf("malloc error\n");
		return NULL;
	}

	printf("original value : %d \n", num);

	for (i = 31; i >= 0 ; i--){
		code_table[i] = num & 1;
		num = num >> 1;
	}

	printf("binary value : ");
	for (i = 0; i < 32 ; i++)
		printf("%d", code_table[i]);
	printf("\n");

	return code_table;
}

void send_code(char *code_table)
{
	int i;

	/* set level low before sending code */

	digitalWrite(DEFAULT_PIN, LOW);
	delayMicroseconds(500);

	for (i = 31; i >= 0 ; i--) {
		if (code_table[i] == 1) {			
			digitalWrite(DEFAULT_PIN, HIGH);
			delayMicroseconds(PULSE_LENGTH * 3);
			digitalWrite(DEFAULT_PIN, HIGH);
			delayMicroseconds(PULSE_LENGTH * 1);
		} else {
			digitalWrite(DEFAULT_PIN, HIGH);
			delayMicroseconds(PULSE_LENGTH * 1);
			digitalWrite(DEFAULT_PIN, HIGH);
			delayMicroseconds(PULSE_LENGTH * 3);
		}
	}
}

void main(int argc, char *argv[])
{
	char *table;
	int gpio = DEFAULT_PIN;

	if (wiringPiSetup () == -1) {
		return -1;
	}
	pinMode(DEFAULT_PIN, OUTPUT);

	/* conversion to char table */
	table = num2char(256703);
	send_code(table);
}
