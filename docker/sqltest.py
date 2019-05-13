import pyodbc
server = 'lung.database.windows.net'
database = 'lung'
username = 'pi'
password = 'R@spberry'
#driver= '{ODBC Driver 17 for SQL Server}'
driver = 'FreeTDS'
TDS_Version = '4.2'
cnxn = pyodbc.connect('DRIVER='+driver+';TDS_Version='+TDS_Version+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
cursor.execute("SELECT * FROM dbo.lung_transaction")
row = cursor.fetchone()
while row:
    print (str(row[0]) + " " + str(row[1]))
    row = cursor.fetchone()
