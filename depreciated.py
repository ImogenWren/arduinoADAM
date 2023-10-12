'''
 Depreciated code from other examples


'''



# Connect to the Modbus TCP server
#client.connect()


# Perform Modbus operations here
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder



# Build a command  -- UNTESTED FODUND IN RANDOM DOCS
#https://github.com/eterey/pymodbus3/blob/master/examples/common/modbus-payload.py

builder = BinaryPayloadBuilder(endian=Endian.Little)


builder.add_32bit_float(22.34)
builder.add_16bit_uint(0x1234)
builder.add_8bit_int(0x12)
builder.add_bits([0,1,0,1,1,0,1,0])

builder.add_string('01 05 00 11 FF 00')
payload = builder.build()
address = 0x11
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

