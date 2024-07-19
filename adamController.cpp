/*  adamController.cpp

  arduino/c++ library for control of generic Advantech Data Aquisition Modules (ADAM-xxxx) 

  Imogen Heard
    21/12/23


*/

/*  Anatomy of a ModBus Message


  0x  (in hex)
message prefix
  01  station address
  0F  function code   (01, 02, 03, 04,05, 06, 08, 0f, 10 )
  00  end of prefix
message contents
  10  coil/register address High Byte
  17  coil/register address low byte
  0A  ??
  02  ??
  CD  ??
  01  ??

ASCII Commands
$aaM  = $01M


*/


#include "adamController.h"






void adamController::begin() {
  modbusTCP.begin(serverIP, 502);
  W5100.setRetransmissionTime(0x03E8);  // seems to work with all of these and the include for the w5100 library in header file
  W5100.setRetransmissionCount(1);
  modbusTCP.setTimeout(1000);  // doesnt seem to be working
  ethClient.setConnectionTimeout(1000);
  adamController::check_modbus_connect();
}



bool adamController::check_modbus_connect() {
#if DEBUG_MODBUS == true
  Serial.print("DEBUG_MODBUS: ");
  Serial.println(moduleName);
#endif
  if (!modbusTCP.connected()) {

#if DEBUG_MODBUS == true
    // client not connected, start the Modbus TCP client
    Serial.print("DEBUG_MODBUS: ");
    Serial.println(moduleName);
    Serial.println(F(": modbus not connected. Attempting to connect to Modbus TCP server"));
#endif

    modbusConnected = false;
    if (!modbusTCP.begin(serverIP, 502)) {
#if DEBUG_MODBUS == true
      Serial.print("DEBUG_MODBUS: ");
      Serial.println(moduleName);
      Serial.print(F(": Modbus TCP Client failed to connect!"));
      Serial.println(F("\"}"));  //JSON error message footer
#endif
    } else {
      modbusConnected = true;
#if DEBUG_MODBUS == true
      Serial.print(moduleName);
      Serial.println(F(": Modbus TCP Client connected"));
#endif
    }
  } else {
    modbusConnected = true;
  }
  return modbusConnected;
}





int16_t adamController::set_coil(int coilNum, bool coilState) {
  uint8_t state;
  if (coilState) {
    state = 0x01;
  } else {
    state = 0x00;
  }

  char buffer[64];

  if ((coilNum >= 0) && (coilNum < 8)) {
    if (!modbusTCP.coilWrite(d_out[coilNum], state)) {
      sprintf(buffer, "{\"error\":\"%s: Failed to set coil: %i ( %#0x ) to %i. %s\"}", moduleName, coilNum, d_out[coilNum], coilState, modbusTCP.lastError());
      coilState = -1;
      // Serial.println(modbusTCP.lastError());
    } else {
      sprintf(buffer, "{\"status\":\"%s: Set Coil: %i ( %#0x ) to %i\"}", moduleName, coilNum, d_out[coilNum], coilState);
    }
  } else {
    sprintf(buffer, "{\"error\":\"%s: Unable to set Coil %i - out of range :(\"}", moduleName, coilNum);
    coilState = -1;
  }
#if DEBUG_ADAM == true
  Serial.print("DEBUG_ADAM: ");
  Serial.println(buffer);
#endif
  return coilState;
}



int16_t adamController::set_coils(uint8_t coilStates) {
  int16_t response;
  response = modbusTCP.beginTransmission(COILS, 0x10, 0x08);  // type, address (any val) , nb (no bytes to be sent)

  for (int i = 0; i < 8; i++) {
    response = modbusTCP.write(coilStates & bitmask[i]);  // Fun bitmasking operation
  }
  response = modbusTCP.endTransmission();

  char binString[9];
  itoa(coilStates, binString, 2);  //trying some magic to make sprinf work to print status in columns
  int zeroPadding = int(8 - strlen(binString));
  char buffer[64];

  if (response == 1) {
    sprintf(buffer, "{\"status\":\"%s: Set Coils:   %s%s \"}", moduleName, leadingZeros[zeroPadding], binString);
  } else {
    sprintf(buffer, "{\"error\":\"%s: Unable to Set Coils to: %s%s \"}", moduleName, leadingZeros[zeroPadding], binString);
    coilStates = -1;
  }
  // g_DO_State = coilStates;
//  Serial.println(response);
#if DEBUG_ADAM == true
  Serial.print("DEBUG_ADAM: ");
  Serial.println(buffer);
#endif
  return coilStates;
}



int16_t adamController::read_coil(uint8_t outputNum) {
  char buffer[64];
  int16_t outState = -1;
  if (outputNum < 8) {
    outState = modbusTCP.coilRead(d_out[outputNum]);
    if (outState == -1) {
      sprintf(buffer, "{\"error\":\" %s: Error Code %i: Unable to Read Output Status %i :(\"} ", moduleName, outState, outputNum);
    } else {
      sprintf(buffer, "{\"status\":\" %s: Output %i Status: %i\"} ", moduleName, outputNum, outState);
    }
  } else {
    sprintf(buffer, "{\"error\":\" %s: Unable to Read Output Status %i - out of range :(\"} ", moduleName, outputNum);
    outState = -1;
  }
#if DEBUG_ADAM == true
  Serial.print("DEBUG_ADAM: ");
  Serial.println(buffer);
#endif
  return outState;
}



int16_t adamController::read_coils() {
  int response = modbusTCP.requestFrom(COILS, d_out[0], 0x08);
  int numReadings = modbusTCP.available();  // Is this line even needed? requestFrom returns number of readings
  int readBuffer[numReadings];
  int coilStates = 0;
  char buffer[64];
  if (response > 0) {
    for (int i = 0; i < numReadings; i++) {
      readBuffer[i] = modbusTCP.read();                    // this array fill in reverse?
      coilStates = coilStates + readBuffer[i] * (1 << i);  // This calculates the total value of all the coils so it can be displayed in binary
    }

    char binString[9];
    itoa(coilStates, binString, 2);  //trying some magic to make sprinf work to print status in columns
    int zeroPadding = int(8 - strlen(binString));

    sprintf(buffer, "{\"status\":\"%s: Read Coils:  %s%s \"} ", moduleName, leadingZeros[zeroPadding], binString);
  } else {
    sprintf(buffer, "{\"error\":\"%s: ERROR: Unable to read coil status \"}", moduleName);
  }
  g_DO_State = coilStates;
#if DEBUG_ADAM == true
  Serial.print("DEBUG_ADAM: ");
  Serial.println(buffer);
#endif
  return coilStates;
}





int16_t adamController::read_digital_input(uint8_t inputNum) {
  char buffer[64];
  int16_t inputState = -1;
  if (inputNum < 8) {
    inputState = modbusTCP.discreteInputRead(inputNum);
    if (inputState == -1) {
      sprintf(buffer, "{\"error\":\"%s: Error Code %i: Unable to Read Input %i :(\"}", moduleName, inputState, inputNum);
    } else {
      sprintf(buffer, "{\"status\":\"%s: Input %i Status: %i\"}", moduleName, inputNum, inputState);
    }
  } else {
    sprintf(buffer, "{\"error\":\"%s: Unable to Read Input %i - out of range :(\"}", moduleName, inputNum);
    inputState = -1;
  }
#if DEBUG_ADAM == true
  Serial.println(buffer);
#endif
  return inputState;
}



int16_t adamController::read_digital_inputs(uint8_t numInputs) {
  int response = modbusTCP.requestFrom(DISCRETE_INPUTS, d_in[0], numInputs);
  int numReadings = modbusTCP.available();  // Is this line even needed? requestFrom returns number of readings
  int readBuffer[numReadings];
  int inputStates = 0;
  char buffer[64];
  if (response > 0) {
    for (int i = 0; i < numReadings; i++) {
      readBuffer[i] = modbusTCP.read();                      // this array fill in reverse?
      inputStates = inputStates + readBuffer[i] * (1 << i);  // This calculates the total value of all the coils so it can be displayed in binary
    }
    char binString[9];
    itoa(inputStates, binString, 2);  //trying some magic to make sprinf work to print status in columns
    int zeroPadding = int(8 - strlen(binString));

    sprintf(buffer, "{\"status\":\" %s: Read Digital Inputs: %s%s\"}", moduleName, leadingZeros[zeroPadding], binString);
  } else {
    sprintf(buffer, "{\"error\":\" %s: ERROR: Unable to read input status\"}", moduleName);
    inputStates = 0;  // used to be set to -1 but was unsigned so not sensible
  }
  g_DI_State = inputStates;
  // Serial.println(buffer);  // TODO MOVED THIS BECAUSE NOT PRINTING WAHH
#if DEBUG_ADAM == true
  Serial.print(F("DEBUG_ADAM: "));
  Serial.println(buffer);
#endif
  return inputStates;
}



void adamController::printBin(uint8_t binaryVal) {
  char buffer[64];
  char binString[9];
  itoa(binaryVal, binString, 2);  //trying some magic to make sprinf work to print status in columns
  int zeroPadding = int(8 - strlen(binString));
  sprintf(buffer, "{\"status\":\"%s: Printing Binary: %s%s\"}", moduleName, leadingZeros[zeroPadding], binString);
  Serial.println(buffer);
}


adamController::dataArray adamController::read_analog_inputs(uint8_t numInputs) {
  // dataArray analogVals; // Use the global variable its easier!
  int response = modbusTCP.requestFrom(INPUT_REGISTERS, a_in[0], numInputs);  //HOLDING_REGISTERS
  int numReadings = modbusTCP.available();                                    // Is this line even needed? requestFrom returns number of readings
  uint16_t readBuffer[numReadings];
  char buffer[514] = { 0 };
  if (response > 0) {
    for (int i = 0; i < numReadings; i++) {
      readBuffer[i] = modbusTCP.read();
      d_array.i_data[i] = readBuffer[i];  // always save the DAQ reading to the i_data buffer
      d_array.timeStamp_mS[i] = millis();
      switch (analogType) {
        case DAC_OUTPUT:
          // no other conversion needed, just copy int data to float variable to avoid breaking things when changes are made and user forgets to change i_data to f_data
          d_array.f_data[i] = float(d_array.i_data[i]);
          break;
        case VOLTAGE_OUTPUT:
          d_array.f_data[i] = adamController::adc_to_voltage(readBuffer[i]);  // do the conversion to voltage/current here
          break;
        case CURRENT_OUTPUT:
          d_array.f_data[i] = adamController::adc_to_current(readBuffer[i]);  // do the conversion to voltage/current here
          break;
        case TEMP_OUTPUT:
          d_array.f_data[i] = adamController::adc_to_temperature(readBuffer[i]);  // do the conversion to voltage/current here
          break;
        default:
          d_array.f_data[i] = float(d_array.i_data[i]);
          Serial.print(moduleName);
          Serial.println(F("{\"error\":\"Error: Unknown analog data type requested\"}"));
          break;
      }
    }
#if PRINT_SCALED_DATA == true
    char floatString[8][8];
    for (int i = 0; i < numReadings; i++) {
      dtostrf(d_array.f_data[i], 2, 2, floatString[i]);
    }
    sprintf(buffer, "{\"status\":\"%s: Read Analog Inputs %s: %s, %s, %s, %s, %s, %s\"}", moduleName, dataTypeName[analogType], floatString[0], floatString[1], floatString[2], floatString[3], floatString[4], floatString[5]);
#elif PRINT_RAW_DATA == true
    sprintf(buffer, "{\"status\":\"%s: Read Analog Inputs (ADC): %u, %u, %u, %u, %u, %u\"}", moduleName, readBuffer[0], readBuffer[1], readBuffer[2], readBuffer[3], readBuffer[4], readBuffer[5]);
#endif
  } else {
    sprintf(buffer, "{\"error\":\"%s: Unable to read input status\"}", moduleName);
    // inputStates = -1;
  }
#if PRINT_RAW_DATA == true || PRINT_SCALED_DATA == true
  Serial.print(F("PRINT_X_DATA: "));
  Serial.println(buffer);
#endif
  //delete buffer;  // doesnt work
  return d_array;
}



int16_t adamController::set_mA_analog_output(int outputNum, float outputVal) {
  int16_t response;
  uint16_t dac_val;
  // int16_t holdingVal;
  //holdingVal =  modbusTCP.holdingRegisterRead(10);
// all this for debugging
 // Serial.print("Output Number: ");
 // Serial.print(a_out[outputNum], HEX);
 // Serial.print("  outputValue: ");
 // Serial.print(outputVal);

  dac_val = current_4_20mA_to_dac(outputVal);

//  Serial.print("  dac_val: ");
 // Serial.println(dac_val);

  //adamController::report_modbus_status();

  if (modbusConnected) {  // specific guard clause placed to avoid timeout bug NEEDS TESTING not sure how well used this variable is
     response = modbusTCP.holdingRegisterWrite(a_out[outputNum], dac_val);  // <- This is also the line that is causing the hangup (when ethernet unplugged from startup) issue, when commented out no issues
  } else {
    Serial.println("{\"ERROR\":\"I can't do that dave. ModBus is disconnected\"");
  }

#if DEBUG_ADAM == true
  Serial.print(F("DEBUG_ADAM: Response: "));
  Serial.print(response);
  Serial.print(" mA_val: ");
  Serial.print(outputVal);
  Serial.print(" DAC_val: ");
  Serial.print(dac_val);
  Serial.println("");
#endif
  return response;
}



uint8_t adamController::analogAsDigital(float dataArray[8]) {
  //  Serial.println("Data In: ");
  // adamController::printBin(fuzzyData);
  for (int i = 0; i < 8; i++) {  // this function looks odd, but its basically just sorting a float into high or low, or the origional value
                                 //   Serial.print(dataArray[i]);
                                 //    Serial.print(" ");
                                 //   Serial.print(bitmask[i]);
                                 //   Serial.print(" ");
    if (dataArray[i] >= FUZZY_LOGIC_HIGH) {
      g_AIasDI_State |= bitmask[i];
      //     Serial.print(" 1 ");
    } else if (dataArray[i] <= FUZZY_LOGIC_LOW) {
      //    Serial.print(" 0 ");
      g_AIasDI_State &= not_bitmask[i];  // bitmask should be all 1s then 0 for clearing bit
    }                                    // flips the bitmask and resets all 0s (should just be 1)
                                         //    adamController::printBin(fuzzyData);
                                         //   Serial.println();
  }
#if DEBUG_ANALOG_AS_DIGITAL == true
  Serial.print("DEBUG_ANALOG_AS_DIGITAL: ");
  adamController::printBin(g_AIasDI_State);
#endif
  return g_AIasDI_State;
}



float adamController::adc_to_voltage(uint16_t _adcvalue) {
  float voltage = float(_adcvalue) - 32768.0;
  voltage = voltage / 3257.333;
  return voltage;
}

float adamController::adc_to_current(uint16_t _adcvalue) {
  float current = float(_adcvalue);  // - 32768.0;
  current = current / 3276.799;
  return current;
}

float adamController::adc_to_temperature(uint16_t _adcvalue) {
  float temperature = float(_adcvalue);  // - 32768.0;
  temperature = temperature * 0.0209;
  return temperature;
}

// DAC is 10 bits so max val = 4095
uint16_t adamController::current_4_20mA_to_dac(float _mA_value) {
  if (_mA_value < 4) {
    _mA_value = 4;
  }
  _mA_value = _mA_value - 4;
  uint16_t dac_value = round(_mA_value * 255.9375);
  return dac_value;
}

bool adamController::report_modbus_status() {
  if (modbusConnected) {
    Serial.println("ModBus connected");
  } else {
    Serial.println("No ModBus Connection");
  }
}
