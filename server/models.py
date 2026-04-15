from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# EXERCISE MODEL
class Exercise(db.Model):

    __tablename__ = "exercises" 

    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # RELATIONSHIPS
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )
   
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True  
    )

    def __repr__(self):
        return f"<Exercise id={self.id} name='{self.name}' category='{self.category}'>"

# WORKOUT MODEL
class Workout(db.Model):

    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # RELATIONSHIPS
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )
 
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True
    )

    def __repr__(self):
        return f"<Workout id={self.id} date='{self.date}' duration={self.duration_minutes}min>"

# WORKOUTEXERCISE MODEL -Join Table
class WorkoutExercise(db.Model):
 
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    #RELATIONSHIPS
    workout = db.relationship("Workout", back_populates="workout_exercises")
  
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    
    def __repr__(self):
        return (
            f"<WorkoutExercise workout={self.workout_id} "
            f"exercise={self.exercise_id} "
            f"sets={self.sets} reps={self.reps}>"
        )

