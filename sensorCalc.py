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
        #print("ERROR/TODO: Calculated value does not precisely match gauge value") #TODO Make sure calculations are accurate
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
        #2.53 v = 25 degC
        factor = 9.88
        tempRange = degC_max - degC_min
        vRange = Vmax - Vmin
        #factor = tempRange / vRange
        # print(f"Voltage to Pressure Factor: {factor}")
        temperature = round(((voltage) * factor), 3)
        # print(f"Calculating Voltage: {voltage} V = Pressure: {pressure} bar")
        return temperature


    def current_20mA_to_power(self, current, P_min=0, P_max=1053, I_min=0, I_max=20):
        # 3.123 mA = 205.6 W
        powerRange = P_max - P_min
        I_range = I_max - I_min
        #factor = powerRange / I_range
        factor = 65.834
        #print(f"Current to Power Factor: {factor}")
        power = round((((current-I_min)*factor)),1)     #-2.05 offset?
        #print(f"Calculating Power: {current} mA = {power} W")
        return power

    def current_to_pressure(self, current, bar_min = 0, bar_max=100, I_min=0, I_max=20):
        pressureRange = bar_max - bar_min
        I_range = I_max - I_min
        factor = pressureRange / I_range
        print(f"Current to Pressure Factor: {factor} ")
        pressure = round(((current-I_min)*factor),3)
        print(f"Calculating Current: {current} mA = Pressure: {pressure} bar")
        return pressure

    def current_to_temperature(self, current, temp_min=0, temp_max=100,I_min=0, I_max=20):
        tempRange = temp_max - temp_min
        vRange = I_max - I_min
        factor = tempRange / vRange
        print(f"Current to Pressure Factor: {factor}")
        temperature = round(((current - I_min) * factor), 3)
        print(f"Calculating Current: {current} mA = Temp: {temperature} degC")
        return temperature