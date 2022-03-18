import mysql.connector as mysql
import os

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

# Create Track_db Database
cursor.execute("CREATE DATABASE IF NOT EXISTS Track_db;")
cursor.execute("USE Track_db")

# Delete existing, then Create objects table
cursor.execute("DROP TABLE IF EXISTS objects;")

try:
    cursor.execute("""
    CREATE TABLE objects (
      color        VARCHAR(50) NOT NULL,
      lower1      INT NOT NULL,
      upper1      INT NOT NULL,
      lower2      INT NOT NULL,
      upper2      INT NOT NULL,
      name        VARCHAR(50) NOT NULL
    );
  """)
    cursor.execute("""
    INSERT INTO objects
      VALUES ("Red", 0, 10, 160, 179, "Screwdriver");
    """)
    cursor.execute("""
    INSERT INTO objects
      VALUES ("Green", 30, 80, 30, 80, "Spoon");
    """)
    cursor.execute("""
    INSERT INTO objects
      VALUES ("Blue", 90, 140, 90, 140, "Shirt");
    """)
except RuntimeError as err:
    print("runtime error: {0}".format(err))

db.commit()
# Delete existing, then Create found_objects table
cursor.execute("DROP TABLE IF EXISTS found_objects;")

try:
    cursor.execute("""
    CREATE TABLE found_objects (
      object_name        VARCHAR(50) NOT NULL,
      Latitude        FLOAT(7,4) NOT NULL,
      Longitude        FLOAT(7,4) NOT NULL,
      Address           VARCHAR(50) NOT NULL 
    );
  """)
except RuntimeError as err:
    print("runtime error: {0}".format(err))

db.commit()

# Delete existing, then Create found table
cursor.execute("DROP TABLE IF EXISTS found;")

try:
    cursor.execute("""
    CREATE TABLE found (
      object_name        VARCHAR(50) NOT NULL,
      Latitude        FLOAT(7,4) NOT NULL,
      Longitude        FLOAT(7,4) NOT NULL,
      Address           VARCHAR(50) NOT NULL 
    );
  """)
except RuntimeError as err:
    print("runtime error: {0}".format(err))

db.commit()
