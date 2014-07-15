# improt the MYSQL connector
import mysql.connector

# import errorcode from mysql.connector
from mysql.connector import errorcode

# use try statement to catch errors
try:
    # Ask for username then database
    user = raw_input("Enter Username: ")
    database = raw_input("Enter Database: ")

    cnx = mysql.connector.connect(user,database)

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exists")
    else:
        print(err)
else:
      cnx.close()
