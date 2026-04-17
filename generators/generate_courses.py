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
    instructors_file = os.path.join(BRONZE_PATH, "instructors.csv")
    if os.path.exists(instructors_file):
        inst_df = pd.read_csv(instructors_file)
        instructor_ids = inst_df['instructor_id'].tolist()
    else:
        instructor_ids = [f"INS-{i+1:03d}" for i in range(20)]

    semesters_file = os.path.join(BRONZE_PATH, "semesters.csv")
    if os.path.exists(semesters_file):
        sem_df = pd.read_csv(semesters_file)
        semester_ids = sem_df['semester_id'].tolist()
    else:
        semester_ids = [f"SEM-{i+1:03d}" for i in range(6)]

    departments = ["Computer Science", "Mathematics", "Physics", "Engineering", "Business"]
    data = []
    for i in range(60):
        data.append({
            "course_id": f"CRS-{i+1:04d}",
            "name": f"{fake.catch_phrase()} 101",
            "department": fake.random_element(departments),
            "credit_hours": random.choice([3, 4]),
            "instructor_id": random.choice(instructor_ids),
            "capacity": random.randint(25, 40),
            "semester_id": random.choice(semester_ids),
            "created_at": datetime.now().isoformat()
        })
    df = pd.DataFrame(data)
    os.makedirs(BRONZE_PATH, exist_ok=True)
    df.to_csv(os.path.join(BRONZE_PATH, "courses.csv"), index=False)
    print("Generated 60 courses.")

if __name__ == "__main__":
    generate()
