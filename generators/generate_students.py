import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from faker import Faker
from datetime import datetime
from config.settings import BRONZE_PATH

fake = Faker()

def generate():
    majors = ["Computer Science", "Mathematics", "Physics", "Engineering", "Business", "Biology", "Chemistry"]
    data = []
    for i in range(500):
        data.append({
            "student_id": f"STU-{i+1:04d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "enrollment_date": fake.date_between(start_date='-4y', end_date='today').isoformat(),
            "major": fake.random_element(majors),
            "created_at": datetime.now().isoformat()
        })
    df = pd.DataFrame(data)
    os.makedirs(BRONZE_PATH, exist_ok=True)
    df.to_csv(os.path.join(BRONZE_PATH, "students.csv"), index=False)
    print("Generated 500 students.")

if __name__ == "__main__":
    generate()
