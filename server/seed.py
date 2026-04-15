from app import app
from models import *
from datetime import date

with app.app_context():

    print("Clearing old data...")
    WorkoutExercise.query.delete()
    Exercise.query.delete()
    Workout.query.delete()
    db.session.commit()
    print("Old data cleared.")

    # Create Exercises
    print("Seeding exercises...")

    push_up = Exercise(name="Push-Up", category="strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="strength", equipment_needed=False)
    plank = Exercise(name="Plank", category="strength", equipment_needed=False)
    jumping_jacks = Exercise(name="Jumping Jacks", category="cardio", equipment_needed=False)
    barbell_row = Exercise(name="Barbell Row", category="strength", equipment_needed=True)
    treadmill_run = Exercise(name="Treadmill Run", category="cardio", equipment_needed=True)
    yoga_stretch = Exercise(name="Yoga Stretch", category="flexibility", equipment_needed=False)

    db.session.add_all([push_up, squat, plank, jumping_jacks, barbell_row, treadmill_run, yoga_stretch])
    db.session.commit()  
    print(f"  Created {Exercise.query.count()} exercises.")

    # Create Workouts

    print("Seeding workouts...")

    workout1 = Workout(
        date=date(2024, 1, 10),
        duration_minutes=45,
        notes="Morning strength session. Felt strong today!"
    )

    workout2 = Workout(
        date=date(2024, 1, 12),
        duration_minutes=30,
        notes="Quick cardio. Heart rate stayed high throughout."
    )

    workout3 = Workout(
        date=date(2024, 1, 15),
        duration_minutes=60,
        notes=None  
    )

    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()
    print(f"  Created {Workout.query.count()} workouts.")

  
    # Link Exercises to Workouts

    print("Seeding workout_exercises...")

    # Workout 1
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=push_up.id, sets=3, reps=15)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=squat.id, sets=4, reps=12)
    we3 = WorkoutExercise(workout_id=workout1.id, exercise_id=plank.id, duration_seconds=60)
    we4 = WorkoutExercise(workout_id=workout1.id, exercise_id=barbell_row.id, sets=3, reps=10)

    # Workout 2
    we5 = WorkoutExercise(workout_id=workout2.id, exercise_id=jumping_jacks.id, sets=3, reps=50)
    we6 = WorkoutExercise(workout_id=workout2.id, exercise_id=treadmill_run.id, duration_seconds=1200)

    # Workout 3
    we7 = WorkoutExercise(workout_id=workout3.id, exercise_id=squat.id, sets=5, reps=8)
    we8 = WorkoutExercise(workout_id=workout3.id, exercise_id=push_up.id, sets=4, reps=20)
    we9 = WorkoutExercise(workout_id=workout3.id, exercise_id=yoga_stretch.id, duration_seconds=300)

    db.session.add_all([we1, we2, we3, we4, we5, we6, we7, we8, we9])
    db.session.commit()
    print(f"  Created {WorkoutExercise.query.count()} workout_exercise records.")

    # Verify 
   
    print("\nSeeding complete, summary:")
    print(f"Exercises: {Exercise.query.count()}")
    print(f"Workouts: {Workout.query.count()}")
    print(f"WorkoutExercises:{WorkoutExercise.query.count()}")
    print("\n Sample - Workout 1 exercises:")
    for we in workout1.workout_exercises:
        print(f" - {we.exercise.name}: {we.sets} sets x {we.reps} reps | duration: {we.duration_seconds}s")