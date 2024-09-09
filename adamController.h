
/*   adamController.h

  arduino/c++ library for control of generic Advantech Data Aquisition Modules (ADAM-xxxx) 

  Imogen Heard
    21/12/23


*/

#pragma once

#ifndef adamController_h
#define adamController_h

//#include <string.h>  // moved recently is needed?
#include <Ethernet.h>
#include <ArduinoRS485.h>  // ArduinoModbus depends on the ArduinoRS485 library
#include <ArduinoModbus.h>
#include <utility/w5100.h>  // added to try & solve timeout issue

#if (ARDUINO >= 100)
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#define DEBUG_MODBUS false
#define DEBUG_ADAM false // debug ADAM functions within library
#define PRINT_RAW_DATA false
#define PRINT_SCALED_DATA false
#define DEBUG_ANALOG_AS_DIGITAL false

// define type for analog inputs/output (this changes the format of the data returned from analog inputs,[ DAC value (0-65525), voltage, current]
// CHANGE THIS TO ENUM
//#define DAC_OUTPUT 0
//#define VOLTAGE_OUTPUT 1
//#define CURRENT_OUTPUT 2
typedef enum {
  DAC_OUTPUT,
  VOLTAGE_OUTPUT,
  CURRENT_OUTPUT,
  TEMP_OUTPUT
} analogDataType;


class adamController {

private:
  EthernetClient ethClient;
  IPAddress serverIP;
  ModbusTCPClient modbusTCP;

public:


  bool moduleActive = true;

  // Constructor

  adamController(EthernetClient _client, IPAddress _server, analogDataType _analogType = DAC_OUTPUT, const char _moduleID[32] = { "ADAM-xxxx" })
    : ethClient(_client),
      serverIP(_server),
      modbusTCP(ethClient),
      analogType(_analogType) {
    strcpy(moduleName, _moduleID);
  }

  // Constants

  const int d_out[8] = { 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17 };
  const int d_in[8] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07 };
  const int a_out[6] = { 0xA, 0xB, 0xC, 0xD, 0xE, 0xF };  // first 2 values true for adam6024, untested for other models
  const int a_in[8] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07 };

  // Analog Data Structure
  struct dataArray {
    uint16_t i_data[8];        // Always holds the direct ADC value read from data aquisition module
    float f_data[8];           // holds the calculated voltage or current value, or a copy of the ADC as a float
    uint32_t timeStamp_mS[8];  // holds the time data was sampled in mS from time of power up
  } d_array;

  // Digital Data Structures
  uint8_t g_DO_State = 0b00000000;
  uint8_t g_DI_State = 0b00000000;
  uint8_t g_AIasDI_State = 0b00000000;  // Holding Variable for analog as digital inputs

  // Methods

  void begin();

  bool check_modbus_connect();

  int16_t set_coil(int coilNum, bool coilState = false);
  int16_t set_coils(uint8_t coilStates = 0b00000000);
  int16_t read_coil(uint8_t outputNum);
  int16_t read_coils();


  int16_t read_digital_input(uint8_t inputNum);
  int16_t read_digital_inputs(uint8_t numInputs = 0x08);

  int16_t read_analog_input(uint8_t inputNum);
  dataArray read_analog_inputs(uint8_t numInputs = 0x06);

  int16_t write_holding_register(uint16_t base, uint16_t outputVal);

  int16_t set_DAC_analog_output(int outputNum = 0xA, uint16_t outputVal = 0); // output is 10bit so 4095 is max val
  int16_t set_mA_analog_output(int outputNum = 0xA, float outputVal = 0);
  

  float adc_to_voltage(uint16_t _adcvalue);
  float adc_to_current(uint16_t _acdvalue);
  float adc_to_temperature(uint16_t _adcvalue);

  uint16_t current_4_20mA_to_dac(float _mA_value);

  uint8_t analogAsDigital(float dataArray[8]);  // Method to convert 8 analog values into a digital output

  // Define limits for fuzzy logic (values between these will be ignored and current state will be preserved)
#define FUZZY_LOGIC_HIGH 7.0
#define FUZZY_LOGIC_LOW 3.0


  void printBin(uint8_t binaryVal);

  bool report_modbus_status();

  // Variables
  char moduleName[32] = { "ADAM-xxxxA" };
  bool modbusConnected = false;



  uint8_t bitmask[8] = {
    0b00000001,
    0b00000010,
    0b00000100,
    0b00001000,
    0b00010000,
    0b00100000,
    0b01000000,
    0b10000000
  };
  // Inverse of previous bitmask
  uint8_t not_bitmask[8] = {
    0b11111110,
    0b11111101,
    0b11111011,
    0b11110111,
    0b11101111,
    0b11011111,
    0b10111111,
    0b01111111
  };


  char dataTypeName[4][15] = {
    "DAC_OUTPUT",
    "VOLTAGE_OUTPUT",
    "CURRENT_OUTPUT",
    "TEMP_OUTPUT"
  };

private:
  analogDataType analogType = DAC_OUTPUT;
  char leadingZeros[9][9] = { "", "0", "00", "000", "0000", "00000", "000000", "0000000", "00000000" };
};


#endif
