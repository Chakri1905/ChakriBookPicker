import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="chakri",
  password="Chakri@1905",
auth_plugin='mysql_native_password'
)

print(mydb)
