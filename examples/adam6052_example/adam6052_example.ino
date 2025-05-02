/*  adam-controller: example

Imogen Heard
30/04/2025

This example isnt a complete solution as every ADAM module has a little figuring out to do (though this library version is now very useable and covers most bases)
For Full implementations see projects based off this library.

This sketch is designed to test the Digital and PULSE outputs for ADAM6052 8DI8DO modules
This example shows:
- PULSE output on DO_0 and DO_1
- DO on DO_2 and DO_3

Note: In order to use the PULSE settings (pulse high and pulse low registers), the output must be set to PULSE mode using the ADAM.NET utility. This will prevent the output from being used 
as a typical DO output, and you must use the stop_pulse(uint16_t outputNum); method to stop this output (note, the stop_pulse() function will trigger one additional pulse before stopping due to limitations in the
MODBUS command set)

*/
#include "adamController.h"


// Hardware Options
#define ETHERNET_SHIELD 'C'  // Select from 'A', 'B' or 'C' (Only applies to practable.io hardware - for your own hardware change byte mac[] in globals.h to match your ethernet shield)


#if ETHERNET_SHIELD == 'A'
#pragma Ethernet Shield A Selected
byte mac[] = { 0xA8, 0X61, 0x0A, 0xAE, 0xE1, 0x48 };  // FOR SHIELD A
#elif ETHERNET_SHIELD == 'B'
#pragma Ethernet Shield B Selected
byte mac[] = { 0xA8, 0X61, 0x0A, 0xAE, 0xF3, 0x23 };  // FOR SHIELD B
#elif ETHERNET_SHIELD == 'C'
#pragma Ethernet Shield C Selected
byte mac[] = { 0xA8, 0X61, 0x0A, 0xAF, 0x14, 0x67 };  // FOR SHIELD B

#else
#error "VALID MAC ADDRESS NOT FOUND"
#endif



IPAddress ip(192, 168, 1, 100);  //Define the ip address for the client (local modbus controller) (the device this firmware is running on)

// Create an Ethernet Client
EthernetClient ethClient;

IPAddress adam6052_ip(192, 168, 1, 111);  // update with the IP Address of your Modbus server (the remote IO controller)

adamController adam6052(ethClient, adam6052_ip, VOLTAGE_OUTPUT, "ADAM-6052-8DI8DO");


void adams_begin() {
  Serial.println("Adam Test Library");
  adam6052.begin();
  Serial.println("Testing adam6052");
  //adam6052.set_coils(0b00000000);   // Using binary for easy reading of each output state
  adam6052.set_coils(0xFF);  // Use Hex because it makes you look cool
  //adam6052.set_coils(255);          // use decimal to keep them guessing
  delay(1000);
}


void ethernet_begin() {
  // start the Ethernet connection and the server:
  Ethernet.begin(mac, ip);
  // Check for Ethernet hardware present
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println(F("{\"error\":\"Arduino: Ethernet shield not found. Can't run without hardware\"}"));

    // while (true) {
    delay(1);  // do nothing, no point running without Ethernet hardware - wrong because this way will send error report as per usual
    //  }
  }
  delay(500);
  if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println(F("{\"error\":\"Arduino: Ethernet cable not connected.\"}"));
  }
}



int16_t counter_one = 49;
int16_t counter_two = 1;  //(2E16/2)-1;

void setup() {
  Serial.begin(115200);
  Serial.println("\n");
  ethernet_begin();
  adams_begin();
  //adam6052.write_holding_register(ABSOLUTE_PULSE, 0);  // Non abstracted method writing to holding registers directly. Trigger a continuous pulse to start
  adam6052.set_pulse_frequency(200);   // pulse frequency is global using this library. If use case exists for different frequencies this could be modified after
  adam6052.set_pulse_duty(0x00, 0.3);  //(output, duty)
  adam6052.set_pulse_percent(0x01, 100);
  adam6052.start_pulse_output(1);
  adam6052.start_pulse_output(0);
}


float duty = 0.1;
int16_t percent = 100;
bool coilstate = false;

void loop() {
  percent -= 5;
  duty = duty + 0.1;
  counter_one += -5;
  counter_two += 5;
  coilstate = !coilstate;
  Serial.print("low: ");
  Serial.print(adam6052.read_holding_register(CH0_PULSE_LOW_ADDR));
  Serial.print(", high: ");
  Serial.print(adam6052.read_holding_register(CH0_PULSE_HIGH_ADDR));
  //adam6052.write_holding_register(PULSE_LOW_ADDR, counter_one);
  //adam6052.write_holding_register(PULSE_HIGH_ADDR, counter_two);
  Serial.print(" Percent: ");
  Serial.println(percent);
  adam6052.set_pulse_percent(0, percent);
  adam6052.set_pulse_duty(1, duty);
  adam6052.set_coil(2, coilstate);
  delay(1000);

  while (counter_one == 0) {
    //adam6052.set_coils(0b00000000);
    adam6052.write_holding_register(ALL_DO_ADDR, 0);  // Alternative way of setting all outputs  (except pulse)
                                                      //adam6052.write_holding_register(PULSE_LOW_ADDR, 100);
                                                      //adam6052.write_holding_register(ABSOLUTE_PULSE, 1);  // this seems like the best way to "cheat" and stop the pulse output
                                                      //adam6052.write_holding_register(PULSE_HIGH_ADDR, 0);
    adam6052.stop_pulse_output(0);
    adam6052.stop_pulse_output(1);
    delay(2000);
    adam6052.set_coils(0xFF);
    counter_one = -1;
  }
  if (counter_one <= 0) counter_one = 50;
  if (counter_two >= 50) counter_two = 0;
  if (duty >= 1.0) duty = 0.0;
  if (percent <= 0) percent = 100;
  if (percent > 100) percent = 0;
}
