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
cursor.execute("DROP TABLE IF EXISTS Gallery_Details;")

try:
    cursor.execute("""
    CREATE TABLE Gallery_Details (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      name        VARCHAR(50) NOT NULL,
      owner       VARCHAR(50) NOT NULL,    
      height      integer NOT NULL,
      age         integer NOT NULL
    );
  """)
except RuntimeError as err:
    print("runtime error: {0}".format(err))


# Load data from details.csv into table 
cursor.execute("""
    LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/details.csv'
    INTO TABLE Gallery_Details
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;

  """)
db.commit()

