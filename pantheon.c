#include <stdio.h>
#include <stdlib.h>
#include <regex.h>

int IP = 0;
int URL = 0;
void commandDescription(){
	printf("");
}
int main(int argc, char *argv[]){
	if(argc < 2){
		printf("Not enough arguements where provided\n");
		commandDescription();
		printf("EX: pantheon [] <IP or URL>\n");
		return 0;
	}
	
	regex_t reegex;
	int value;
	value = regcomp(&reegex, "(http|https):\\/\\/(www.)?",0);
	value = regexec(&reegex,argv[1],0,NULL,0);
	if(value == 0){
		printf("successfull");
	}
	else if(value == REG_NOMATCH){
		printf("Pattern not found");
	}
	else{
		printf("an error occurred.\n");
	}
	return 0;
}
