import serial

ser = serial.Serial(
    port='/dev/cu.usbmodem14101',
    baudrate=57600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

def read_per_breath():
    flag = True
    while flag:
        data = ser.readline()
        # print(data)
        if data != '' and data != "\r\n":
            data_new = data.decode('utf-8')
            data_number = (data_new[0:(len(data_new) - 2)])
            print(data_number)

if __name__ == "__main__":
    read_per_breath()

