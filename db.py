# For Task 1 to handle database connection

from mysql.connector import connect, Error
from config import Config

def get_db_connection():
    try:
        conn = connect(
            host=Config.host,
            database=Config.database,
            user=Config.user,
            password=Config.password
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None