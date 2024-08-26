# Task 1 Flask application basic route

from flask import Flask
from db import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        return "Database connected successfully!"
    else:
        return "Failed to connect to the database."

if __name__ == '__main__':
    app.run(debug=True)