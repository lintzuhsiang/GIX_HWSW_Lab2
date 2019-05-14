import pyodbc
import datetime
from CRUD_m import create_data
from CRUD_m import close_connection
from CRUD_m import get_connection
# server = 'lung.database.windows.net'
# database = 'lung'
# username = 'pi'
# password = 'R@spberry'
# driver= '{ODBC Driver 17 for SQL Server}'
#cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
#cursor = cnxn.cursor()
cnxn = get_connection()

device_id = '001'
patient_id = '001'
id_ = '002'
table_name = 'lung_transaction'
date = datetime.datetime.now()
print("insert columns...")
for i in range(10):
	data = {'ID':id_,'DATE':date,'VALUE':str(i),'DEVICE_ID':device_id,'PATIENT_ID':patient_id,'TYPE':'pedal'}
	create_data(table_name,data,cnxn)


print("fetch data...")
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM lung_transaction WHERE ID='002'")
row = cursor.fetchone()
while row:
    #print (str(row[0]) + " " + str(row[1]))
    print(row)
    row = cursor.fetchone()

