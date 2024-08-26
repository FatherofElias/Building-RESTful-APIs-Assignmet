from flask import Flask
from mysql.connector import connect, Error
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    try:
        conn = connect(
            host=app.config['host'],
            database=app.config['database'],
            user=app.config['user'],
            password=app.config['password']
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        return "Database connected successfully!"
    else:
        return "Failed to connect to the database."

if __name__ == '__main__':
    app.run(debug=True)