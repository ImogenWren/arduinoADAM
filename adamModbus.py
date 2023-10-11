'''

adamModbus

- Attempt to move away from ASCII commands and towards a more robust implementation using MODBUS

https://control.com/forums/threads/reading-di-do-status-of-adam-6050.27164/
'''

#import pymodbus
#import minimalmodbus


from pymodbus.client import ModbusTcpClient

# Create a Modbus TCP client
client = ModbusTcpClient('192.168.1.111')  # Replace with your device's IP address

# Connect to the Modbus TCP server
client.connect()


# Perform Modbus operations here
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder



# Build a command  -- UNTESTED FODUND IN RANDOM DOCS
#https://github.com/eterey/pymodbus3/blob/master/examples/common/modbus-payload.py

builder = BinaryPayloadBuilder(endian=Endian.Little)
builder.add_string('abcdefgh')
builder.add_32bit_float(22.34)
builder.add_16bit_uint(0x1234)
builder.add_8bit_int(0x12)
builder.add_bits([0,1,0,1,1,0,1,0])
payload = builder.build()
address = 0x01
result  = client.write_registers(address, payload, skip_encode=True)


# Read a holding register value
result = client.read_holding_registers(address=301, count=1, unit=1)
if result.isError():
    print("Error reading register!")
else:
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
    value = decoder.decode_32bit_float()

    print("Register value:", value)



# Close the connection
client.close()