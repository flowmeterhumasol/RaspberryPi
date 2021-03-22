        


void setup() {
// put your setup code here, to run once:
Serial.begin(9600);

}

void loop() {
// put your main code here, to run repeatedly:
//data that is being Sent
uint16_t liters= 25;
uint8_t from= 2; 
char data[20];
   sprintf(data,"%u:%u",from,liters);  //format two ints into character array
   Serial.println(data);
delay(2000);
}
