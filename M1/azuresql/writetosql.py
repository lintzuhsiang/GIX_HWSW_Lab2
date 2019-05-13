import datetime
import serial
from CRUD_m import create_data
from CRUD_m import close_connection
from CRUD_m import get_connection

ser = serial.Serial(
    port='/dev/cu.usbmodem14101',
    baudrate=57600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

def read_per_breath():
    data = ser.readline()
    if data != '' and data != "\r\n":
        data_new = data.decode('utf-8')
        data_number = (data_new[0:(len(data_new) - 2)])
        print(data_number)
        return data_number

if __name__ == "__main__":
    flag = True
    connection = get_connection()
    device_id = "001"
    patient_id = "001"
    while flag:
        id = "1"
        date = datetime.datetime.now()
        value = read_per_breath()
        data = {'id': id, 'date':date, 'value': value ,'device_id':device_id, 'patient_id':patient_id}
        table_name = 'lung_transaction'
        create_data(table_name, data, connection)

    close_connection(connection)

print ("done")
