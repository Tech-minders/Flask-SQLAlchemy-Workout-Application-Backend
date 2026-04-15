from flask import Flask, make_response
from flask_migrate import Migrate
from flask import Flask, make_response, request, jsonify

from models import *

from schemas import (
    exercise_schema,
    exercises_schema,
    workout_schema,
    workouts_schema,
    workout_exercise_schema,
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# WORKOUT ROUTES 

@app.route('/workouts', methods=['GET'])
def get_workouts():
    return make_response(jsonify([]), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    return make_response(jsonify({}), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    return make_response(jsonify({}), 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    return make_response(jsonify({}), 204)


#EXERCISE ROUTES 

@app.route('/exercises', methods=['GET'])
def get_exercises():
    return make_response(jsonify([]), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    return make_response(jsonify({}), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    return make_response(jsonify({}), 201)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    return make_response(jsonify({}), 204)


#  WORKOUT-EXERCISE ROUTE
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    return make_response(jsonify({}), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)