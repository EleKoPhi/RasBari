import smbus
import time
bus = smbus.SMBus(1)

address = 0x05

def send_data(value):
    try:
        bus.write_byte(address, value)
        return -1
    except:
        print("I2C error")

def read_data():
    data_in = bus.read_byte(address)
    return data_in


data_out = -1
while True:
    
    data_out+=1
    if data_out == 11:data_out=0
    
    send_data(data_out)
    #print("I2C - SEND")

    time.sleep(0.1)
    
