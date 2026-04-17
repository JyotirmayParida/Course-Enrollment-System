import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
import random
from faker import Faker
from datetime import datetime
from config.settings import BRONZE_PATH

fake = Faker()

def generate():
    try:
        student_ids = pd.read_csv(os.path.join(BRONZE_PATH, "students.csv"))['student_id'].tolist()
    except Exception:
        student_ids = [f"STU-{i+1:04d}" for i in range(500)]
        
    try:
        course_ids = pd.read_csv(os.path.join(BRONZE_PATH, "courses.csv"))['course_id'].tolist()
    except Exception:
        course_ids = [f"CRS-{i+1:04d}" for i in range(60)]
        
    try:
        semester_ids = pd.read_csv(os.path.join(BRONZE_PATH, "semesters.csv"))['semester_id'].tolist()
    except Exception:
        semester_ids = [f"SEM-{i+1}" for i in range(6)]

    grades = ["A", "B", "C", "D", "F", "W"]
    data = []
    
    existing_enrollments = set()
    
    attempts = 0
    while len(data) < 2000 and attempts < 20000:
        attempts += 1
        student = random.choice(student_ids)
        course = random.choice(course_ids)
        semester = random.choice(semester_ids)
        
        enroll_key = (student, course, semester)
        if enroll_key in existing_enrollments:
            continue
            
        existing_enrollments.add(enroll_key)
        data.append({
            "enrollment_id": f"ENR-{len(data)+1:05d}",
            "student_id": student,
            "course_id": course,
            "semester_id": semester,
            "grade": random.choices(grades, weights=[30, 30, 20, 10, 5, 5])[0],
            "created_at": datetime.now().isoformat()
        })
        
    df = pd.DataFrame(data)
    os.makedirs(BRONZE_PATH, exist_ok=True)
    df.to_csv(os.path.join(BRONZE_PATH, "enrollments.csv"), index=False)
    print("Generated 2000 enrollments.")

if __name__ == "__main__":
    generate()
