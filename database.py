import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",  # sesuaikan
        database="event_management",
        cursorclass=pymysql.cursors.DictCursor
    )
