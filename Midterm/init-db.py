import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv  # only required if using dotenv for creds

# Store MySql credentials
load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']



# Connect to MySql
db = mysql.connect(user=db_user, password=db_pass,
                   host=db_host)
cursor = db.cursor()

# Create Triton_Gallery Database
cursor.execute("CREATE DATABASE IF NOT EXISTS Midterm_db;")
cursor.execute("USE Midterm_db")

# Delete existing, then Create Gallery_Details table
cursor.execute("DROP TABLE IF EXISTS Data_Table;")

try:
    cursor.execute("""
    CREATE TABLE Data_Table (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      temperature    float(5,2) NOT NULL,
      humidity       float(5,2) NOT NULL,    
      distance      float(5,2) NOT NULL
    );
  """)
except RuntimeError as err:
    print("runtime error: {0}".format(err))

db.commit()

