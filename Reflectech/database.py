import mysql.connector as mycon 

connection = mycon.connect(
    host = "localuser", 
    user ="root",
    password ="lolu123", 
    database = "reflectech"
)
cur = connection.cursor()

