# Flask-SQLAlchemy-Workout-Application-Backend

# Workout Tracker API

A RESTful backend API for a personal trainer workout tracking application, built with **Flask**, **SQLAlchemy**, and **Marshmallow**.

---

## Project Description

This API allows personal trainers to:
- Create and manage **workouts** (with date, duration, and notes)
- Create and manage reusable **exercises** (with category and equipment info)
- **Add exercises to workouts** with specific sets, reps, or timed durations

The app uses a relational database with three tables: `workouts`, `exercises`, and a join table `workout_exercises` that links them together.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Tech-minders/Flask-SQLAlchemy-Workout-Application-Backend.git
cd Flask-SQLAlchemy-Workout-Application-Backend
```

### 2. Install dependencies using Pipenv
```bash
pipenv install
pipenv shell
```

### 3. Move into the server directory
```bash
cd server
```

### 4. Initialize the database and run migrations
```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
```

### 5. Seed the database with example data
```bash
python seed.py
```

---

## Running the App

Or alternatively:
```bash
python app.py
```

The API will be available at: `http://localhost:5555`

---

## API Endpoints

### Workouts

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Get a single workout with its exercises (includes reps/sets/duration) |
| POST | `/workouts` | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout (also deletes linked WorkoutExercise records) |

**POST /workouts — Request body:**
```json
{
  "date": "2024-01-15",
  "duration_minutes": 45,
  "notes": "Felt strong today!"
}
```

---

### Exercises

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Get a single exercise with its associated workouts |
| POST | `/exercises` | Create a new exercise |
| DELETE | `/exercises/<id>` | Delete an exercise (also deletes linked WorkoutExercise records) |

**POST /exercises — Request body:**
```json
{
  "name": "Push-Up",
  "category": "strength",
  "equipment_needed": false
}
```

Valid categories: `strength`, `cardio`, `flexibility`, `balance`, `other`

---

### WorkoutExercises (Adding an exercise to a workout)

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

**Request body (at least one field required):**
```json
{
  "sets": 3,
  "reps": 12,
  "duration_seconds": null
}
```

---

## Validations

The API enforces data quality at three levels:

**Table constraints** (database level):
- Exercise `name` is required and must be unique
- Exercise `category` is required
- Workout `date` and `duration_minutes` are required
- `workout_id` and `exercise_id` in WorkoutExercises cannot be null

**Model validations** (Python/SQLAlchemy level):
- Exercise category must be one of: `strength`, `cardio`, `flexibility`, `balance`, `other`
- Workout duration must be at least 1 minute
- WorkoutExercise reps, sets, and duration_seconds must be positive if provided

**Schema validations** (Marshmallow level):
- Exercise name must be between 1–100 characters
- Workout duration cannot exceed 1440 minutes (24 hours)
- When creating a WorkoutExercise, at least one of reps, sets, or duration_seconds must be provided