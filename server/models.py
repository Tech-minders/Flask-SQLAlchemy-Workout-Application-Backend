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

     #VALIDATIONS 
    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        return value.strip()  
    
    @validates("category")
    def validate_category(self, key, value):
        allowed = ["strength", "cardio", "flexibility", "balance", "other"]
        if value.lower() not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(allowed)}")
        return value.lower()

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
    
    # VALIDATIONS 
 
    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or value < 1:
            raise ValueError("Duration must be at least 1 minute.")
        return value
 
    @validates("date")
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("Workout date is required.")
        return value



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

    # VALIDATIONS
    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value < 1:
            raise ValueError("Reps must be at least 1.")
        return value
 
    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value < 1:
            raise ValueError("Sets must be at least 1.")
        return value
 
    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and value < 1:
            raise ValueError("Duration in seconds must be at least 1.")
        return value

    
    def __repr__(self):
        return (
            f"<WorkoutExercise workout={self.workout_id} "
            f"exercise={self.exercise_id} "
            f"sets={self.sets} reps={self.reps}>"
        )

