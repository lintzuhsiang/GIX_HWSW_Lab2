# SQL Server Database Connection Properties

import pyodbc


# Return the sql connection
def get_connection():
    server = 'lung.database.windows.net'
    database = 'lung'
    username = 'pi'
    password = 'R@spberry'
    driver= '{FreeTDS}'
    TDS_VERSION = 8.0
    connection = pyodbc.connect('DRIVER={};SERVER={};PORT=1433;DATABASE={};UID={};PWD={};TDS_VERSION={}'.format(driver, server, database, username, password,TDS_VERSION))
    print(connection)
    return connection

def create_data(table_name, data):
    str = ""
    value_list = []
    # Get the sql connection
    connection = get_connection()
    for i in range(len(data)):
        tmpstr = "?,"
        str = str + tmpstr
    sql_query = str[:-1]
    sql_query = "Insert Into " + table_name + " Values("+sql_query+")"
    cursor = connection.cursor()

    for key in data:
         value_list.append(data[key])

    cursor.execute(sql_query, value_list)

    # Commit the data
    connection.commit()
    print('Data Saved')

    # Close the connection
    connection.close()



def read_data(table_name, data):
    # Get the sql connection
    connection = get_connection()
    cursor = connection.cursor()

    sql_query = "select * from " + table_name
    if len(data)>0:
        sql_query = sql_query + " where 1=1"
        for key, value in data.items():
            sql_query = sql_query + " and " + key + " = " + "'" +value+ "'"
    # Execute the sql query
    print(sql_query)
    result = cursor.execute(sql_query)
    print('Data Read')
    # Print the data
    # for row in result:
    #     print('row = %r' % (row,))
    return result


def update_data(table_name, data, condition_id):
    # Get the sql connection
    value_list = []
    connection = get_connection()
    cursor = connection.cursor()

    sql_query = "Update " + table_name + " Set "
    if len(data)>0:
        for key in data:
            sql_query = sql_query + key + " = ?, "
        sql_query = sql_query[:-2]
        sql_query = sql_query + " where 1=1"
    if len(condition_id)>0:
        for key in condition_id:
            sql_query = sql_query + " and " + key+" =?"

    # Execute the update query
    for key in data:
        value_list.append(data[key])
    for key in condition_id:
        value_list.append(condition_id[key])

    cursor.execute(sql_query, value_list)
    connection.commit()
    print('Data Updated Successfully')
