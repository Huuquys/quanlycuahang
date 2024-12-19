import mysql.connector

def Myconnection():
    global db_connection
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="quanlydailydouong"
        )
        return db_connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Sử dụng kết nối
db_conn = Myconnection()
if db_conn:
    print("Connection successful!")
else:
    print("Failed to connect to database.")

# Đóng kết nối
def CloseConnection(c):
    try:
        if(c!=None):
            c.close()
    except ConnectionError as e:
        print("Error: {e}")