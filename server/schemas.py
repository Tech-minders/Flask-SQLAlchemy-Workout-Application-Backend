from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError


# EXERCISE SCHEMA

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error="Name must be between 1 and 100 characters.")
    )

    # validate
    category = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["strength", "cardio", "flexibility", "balance", "other"],
            error="Category must be one of: strength, cardio, flexibility, balance, other."
        )
    )
    
    equipment_needed = fields.Bool(load_default=False)

    workouts = fields.List(fields.Nested(lambda: WorkoutSummarySchema()), dump_only=True)

    #SCHEMA VALIDATION
    @validates("name")
    def validate_name_not_numbers(self, value):
        if value.strip().isdigit():
            raise ValidationError("Exercise name cannot be only numbers.")


class WorkoutSummarySchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.Str()


#WORKOUT SCHEMA

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    
    date = fields.Date(
        required=True,
        error_messages={"required": "Workout date is required."}
    )
   
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Duration must be at least 1 minute.")
    )
  
    notes = fields.Str(allow_none=True, load_default=None)

    workout_exercises = fields.List(
        fields.Nested(lambda: WorkoutExerciseDetailSchema()),
        dump_only=True
    )

    # SCHEMA VALIDATION 
    @validates("duration_minutes")
    def validate_max_duration(self, value):
        if value > 1440:
            raise ValidationError("A workout cannot be longer than 24 hours (1440 minutes).")


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

    reps = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1, error="Reps must be at least 1.")
    )
    sets = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1, error="Sets must be at least 1.")
    )
    duration_seconds = fields.Int(
        allow_none=True,
        load_default=None,
        validate=validate.Range(min=1, error="Duration in seconds must be at least 1.")
    )

    # SCHEMA VALIDATION
    @validates_schema
    def validate_at_least_one_metric(self, data, **kwargs):
        if not any([data.get("reps"), data.get("sets"), data.get("duration_seconds")]):
            raise ValidationError(
                "You must provide at least one of: reps, sets, or duration_seconds."
            )


class WorkoutExerciseDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)
    exercise = fields.Nested(ExerciseSummarySchema(), dump_only=True)

#instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()