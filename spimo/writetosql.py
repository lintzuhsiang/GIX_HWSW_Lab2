import datetime
from CRUD_pi import create_data
from CRUD_pi import get_connection

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
    id = "1"
    date = "2019-05-09"
    value = 1
    type = "padal"
    data = {'id': id, 'date':date, 'value': value ,'device_id':device_id, 'patient_id':patient_id, 'type':type }
    table_name = 'lung_transaction'
    create_data(table_name, data)

print ("done")
