'''

adamModbus

- Attempt to move away from ASCII commands and towards a more robust implementation using MODBUS


'''

#import pymodbus
#import minimalmodbus


from pymodbus.client.sync import ModbusTcpClient

# Create a Modbus TCP client
client = ModbusTcpClient('192.168.1.111')  # Replace with your device's IP address

# Connect to the Modbus TCP server
client.connect()


# Perform Modbus operations here
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

# Read a holding register value
result = client.read_holding_registers(address=100, count=1, unit=1)
if result.isError():
    print("Error reading register!")
else:
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big)
    value = decoder.decode_32bit_float()

    print("Register value:", value)



# Close the connection
client.close()