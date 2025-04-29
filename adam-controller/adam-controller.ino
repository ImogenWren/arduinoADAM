/*  adam-controller: example

Imogen Heard
16/07/2024

This example isnt a complete solution as every ADAM module has a little figuring out to do. 
For Full implementations see projects based off this library.

This sketch is designed to test the Analog Output for ADAM6024 Universal IO modules

*/
#include "adamController.h"


// Hardware Options
#define ETHERNET_SHIELD 'B'  // Select from 'A', 'B' or 'C' (Only applies to practable.io hardware - for your own hardware change byte mac[] in globals.h to match your ethernet shield)


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

IPAddress adam6024_ip(192, 168, 1, 114);  // update with the IP Address of your Modbus server (the remote IO controller)

adamController adam6024(ethClient, adam6024_ip, VOLTAGE_OUTPUT, "ADAM-6024-UIO");

void adams_begin() {

  Serial.println("Adam Test Library");
  adam6024.begin();
  Serial.println("Testing Here");
  adam6024.set_coils(0b00000000);
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





void setup() {
  Serial.begin(115200);
  Serial.println("\n");
  ethernet_begin();
  adams_begin();
  adam6024.set_coil(1, true);
  Serial.println("\n Adam Test Analog OP");
  adam6024.set_mA_analog_output(0, 4);
  delay(2000);
  adam6024.set_mA_analog_output(0, 8);
  delay(3000);
  adam6024.set_mA_analog_output(0, 15);
   delay(3000);
  adam6024.set_mA_analog_output(0, 20);
     delay(3000);
  adam6024.set_mA_analog_output(0, 0);
}

void loop() {
  // adam6024.set_analog_output(0, 0x8888);
}
