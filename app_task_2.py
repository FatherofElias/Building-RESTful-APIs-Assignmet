from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError, Schema, fields
import mysql.connector
from mysql.connector import Error
from db import get_db_connection


app = Flask(__name__)
ma = Marshmallow(app)

# For Task 2 defining the schema for MEMBERS


# Marshmallow schema for Members
class MemberSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    age = fields.Int(required=True)

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)


# Route to add a new member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    errors = member_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    id = data.get('id')
    name = data.get('name')
    age = data.get('age')

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Members (id, name, age)
                VALUES (%s, %s, %s)
            """, (id, name, age))
            conn.commit()
            return jsonify({"message": "Member added successfully!"}), 201
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# Route to retrieve a member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, age FROM Members WHERE id = %s", (id,))
            member = cursor.fetchone()
            if member:
                return jsonify({"id": member[0], "name": member[1], "age": member[2]}), 200
            else:
                return jsonify({"error": "Member not found"}), 404
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# Route to update a member by ID
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    errors = member_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_name = data.get('name')
    new_age = data.get('age')

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Members WHERE id = %s", (id,))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Member not found"}), 404

            cursor.execute("""
                UPDATE Members
                SET name = %s, age = %s
                WHERE id = %s
            """, (new_name, new_age, id))
            conn.commit()
            return jsonify({"message": "Member updated successfully!"}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# Route to delete a member by ID
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Members WHERE id = %s", (id,))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Member not found"}), 404

            cursor.execute("DELETE FROM Members WHERE id = %s", (id,))
            conn.commit()
            return jsonify({"message": "Member deleted successfully!"}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

if __name__ == '__main__':
    app.run(debug=True)