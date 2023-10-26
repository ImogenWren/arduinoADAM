'''


'''



class sensorCalc:
    def __init__(self):
        print(f'Sensor Voltage/Current to Process Value Library')


    def current_to_flowmeter(self, current_mA, range_min=2, range_max=25, offset=1.3):   # for ABB D10A3255xxA1 flowmeter
        range = range_max - range_min
        flow_per_mA = range/16
        flowrate = round(((flow_per_mA * (current_mA-4))+ offset),3)       #
        print(f"Convert Current: {current_mA} to flow-rate: {flowrate} L/h")
        print("ERROR/TODO: Calculated value does not precisely match gauge value") #TODO Make sure calculations are accurate
        return flowrate


    def voltage_to_pressure(self, voltage, bar_min = 0,  bar_max = 30, Vmin=1, Vmax=6):
        barRange = bar_max - bar_min
        vRange = Vmax - Vmin
        factor = barRange/vRange
        #print(f"Voltage to Pressure Factor: {factor}")
        pressure = round(((voltage-Vmin)*factor), 3)
        #print(f"Calculating Voltage: {voltage} V = Pressure: {pressure} bar")
        return pressure


#TODO fix this function here
    def voltage_to_temp(self, voltage, degC_min=-50, degC_max=100, Vmin=0, Vmax=10):
        tempRange = degC_max - degC_min
        vRange = Vmax - Vmin
        factor = barRange / vRange
        # print(f"Voltage to Pressure Factor: {factor}")
        pressure = round(((voltage - Vmin) * factor), 3)
        # print(f"Calculating Voltage: {voltage} V = Pressure: {pressure} bar")
        return pressure