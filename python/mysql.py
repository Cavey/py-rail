
import MySQLdb # Use python MySQL module for writing to a database.

# Open database connection
db = MySQLdb.connect("localhost","testuser","test123","TESTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

def record_event(description):
    sql = "INSERT INTO logs ( description ) VALUES ('%s')" % description
    # Execute the SQL command
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
except:
    # Rollback in case there is any error
    db.rollback()

def db_close()
    db.close()
