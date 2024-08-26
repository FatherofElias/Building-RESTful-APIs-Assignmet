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

# For Task 3 Schema for workoutsession table
class WorkoutSessionSchema(Schema):
    session_id = fields.Int(required=True)
    member_id = fields.Int(required=True)
    session_date = fields.Str(required=True)  # Change to Str to match the format returned by MySQL
    session_time = fields.Str(required=True)  # Change to Str to match the format returned by MySQL
    activity = fields.Str(required=True)

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

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

# For Task 3

@app.route('/workouts', methods=['POST'])
def add_workout_session():
    data = request.get_json()
    errors = workout_session_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    session_id = data.get('session_id')
    member_id = data.get('member_id')
    session_date = data.get('session_date')
    session_time = data.get('session_time')
    activity = data.get('activity')

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO WorkoutSessions (session_id, member_id, session_date, session_time, activity)
                VALUES (%s, %s, %s, %s, %s)
            """, (session_id, member_id, session_date, session_time, activity))
            conn.commit()
            return jsonify({"message": "Workout session added successfully!"}), 201
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# Route to update a workout session by ID
@app.route('/workouts/<int:session_id>', methods=['PUT'])
def update_workout_session(session_id):
    data = request.get_json()
    errors = workout_session_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    member_id = data.get('member_id')
    session_date = data.get('session_date')
    session_time = data.get('session_time')
    activity = data.get('activity')

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM WorkoutSessions WHERE session_id = %s", (session_id,))
            if cursor.fetchone()[0] == 0:
                return jsonify({"error": "Workout session not found"}), 404

            cursor.execute("""
                UPDATE WorkoutSessions
                SET member_id = %s, session_date = %s, session_time = %s, activity = %s
                WHERE session_id = %s
            """, (member_id, session_date, session_time, activity, session_id))
            conn.commit()
            return jsonify({"message": "Workout session updated successfully!"}), 200
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500
    
# Route to view all workout sessions
@app.route('/workouts', methods=['GET'])
def get_all_workout_sessions():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT session_id, member_id, session_date, session_time, activity FROM WorkoutSessions")
            sessions = cursor.fetchall()
            print(sessions)  # Debugging print statement
            result = workout_sessions_schema.dump([{
                "session_id": session[0],
                "member_id": session[1],
                "session_date": session[2],
                "session_time": session[3],
                "activity": session[4]
            } for session in sessions])
            return jsonify(result), 200
        except Error as e:
            print(f"Error: {e}")  # Debugging print statement
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# Route to retrieve all workout sessions for a specific member
@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_workout_sessions_for_member(member_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT session_id, member_id, session_date, session_time, activity FROM WorkoutSessions WHERE member_id = %s", (member_id,))
            sessions = cursor.fetchall()

            # Ensure the sessions are correctly formatted
            formatted_sessions = [{
                "session_id": session[0],
                "member_id": session[1],
                "session_date": session[2],
                "session_time": session[3],
                "activity": session[4]
            } for session in sessions]

            return jsonify(formatted_sessions), 200
        except Error as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500



if __name__ == '__main__':
    app.run(debug=True)