
from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

# Import the db instance and all models from models.py
from models import db, Exercise, Workout, WorkoutExercise

from schemas import (
    exercise_schema,
    exercises_schema,
    workout_schema,
    workouts_schema,
    workout_exercise_schema,
)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

# This turns off a feature we don't need (saves memory)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect Flask-Migrate so we can run 'flask db migrate' commands
migrate = Migrate(app, db)

# Connect the SQLAlchemy db to our Flask app
db.init_app(app)



def make_json_response(data, status_code=200):

    response = make_response(jsonify(data), status_code)
    response.headers["Content-Type"] = "application/json"
    return response

# WORKOUT ENDPOINTS

@app.route("/workouts", methods=["GET"])
def get_workouts():

    # Query the database for every Workout record
    all_workouts = Workout.query.all()

    result = workouts_schema.dump(all_workouts)

    return make_json_response(result, 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):

    workout = db.session.get(Workout, id)

    # If no workout was found with that ID, return a 404 error
    if not workout:
        return make_json_response({"error": f"Workout with id {id} not found."}, 404)

    result = workout_schema.dump(workout)
    return make_json_response(result, 200)


@app.route("/workouts", methods=["POST"])
def create_workout():

    data = request.get_json()

    try:
        validated_data = workout_schema.load(data)
    except ValidationError as err:

        return make_json_response({"errors": err.messages}, 422)
  
    new_workout = Workout(
        date=validated_data["date"],
        duration_minutes=validated_data["duration_minutes"],
        notes=validated_data.get("notes"),  
    )

    # Add to the session  and commit 
    db.session.add(new_workout)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Undo any partial changes if something goes wrong
        return make_json_response({"error": str(e)}, 500)

    # Return the newly created workout 
    return make_json_response(workout_schema.dump(new_workout), 201)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):

    workout = db.session.get(Workout, id)

    if not workout:
        return make_json_response({"error": f"Workout with id {id} not found."}, 404)

    db.session.delete(workout)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_json_response({"error": str(e)}, 500)

    return make_json_response({}, 204)

# EXERCISE ENDPOINTS

@app.route("/exercises", methods=["GET"])
def get_exercises():
    all_exercises = Exercise.query.all()
    result = exercises_schema.dump(all_exercises)
    return make_json_response(result, 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):

    exercise = db.session.get(Exercise, id)

    if not exercise:
        return make_json_response({"error": f"Exercise with id {id} not found."}, 404)

    result = exercise_schema.dump(exercise)
    return make_json_response(result, 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():

    data = request.get_json()

    try:
        validated_data = exercise_schema.load(data)
    except ValidationError as err:
        return make_json_response({"errors": err.messages}, 422)

    new_exercise = Exercise(
        name=validated_data["name"],
        category=validated_data["category"],
        equipment_needed=validated_data.get("equipment_needed", False),
    )

    db.session.add(new_exercise)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_json_response({"error": str(e)}, 500)

    return make_json_response(exercise_schema.dump(new_exercise), 201)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):

    exercise = db.session.get(Exercise, id)

    if not exercise:
        return make_json_response({"error": f"Exercise with id {id} not found."}, 404)

    db.session.delete(exercise)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_json_response({"error": str(e)}, 500)

    return make_json_response({}, 204)

# WORKOUTEXERCISE ENDPOINT
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):

    workout = db.session.get(Workout, workout_id)
    if not workout:
        return make_json_response({"error": f"Workout with id {workout_id} not found."}, 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return make_json_response({"error": f"Exercise with id {exercise_id} not found."}, 404)

    data = request.get_json()

    try:
        validated_data = workout_exercise_schema.load(data)
    except ValidationError as err:
        return make_json_response({"errors": err.messages}, 422)

    # Create the join record that links this workout to this exercise
    new_workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=validated_data.get("reps"),
        sets=validated_data.get("sets"),
        duration_seconds=validated_data.get("duration_seconds"),
    )

    db.session.add(new_workout_exercise)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_json_response({"error": str(e)}, 500)

    return make_json_response(workout_exercise_schema.dump(new_workout_exercise), 201)

if __name__ == "__main__":
    app.run(port=5555, debug=True)