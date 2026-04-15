from marshmallow import Schema, fields

#EXERCISE SCHEMA 

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    category = fields.Str()
    equipment_needed = fields.Bool()
   
    workouts = fields.List(fields.Nested(lambda: WorkoutSummarySchema()), dump_only=True)


class WorkoutSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.Str()


# WORKOUT SCHEMA 

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)

    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.Str()
    
    workout_exercises = fields.List(
        fields.Nested(lambda: WorkoutExerciseDetailSchema()),
        dump_only=True
    )


class ExerciseSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    category = fields.Str()
    equipment_needed = fields.Bool()


# WORKOUTEXERCISE SCHEMA 

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)


class WorkoutExerciseDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    # Nest the exercise summary 
    exercise = fields.Nested(ExerciseSummarySchema(), dump_only=True)

#instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()