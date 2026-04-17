import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from faker import Faker
from datetime import datetime
from config.settings import BRONZE_PATH

fake = Faker()

def generate():
    data = []
    departments = ["Computer Science", "Mathematics", "Physics", "Engineering", "Business"]
    for i in range(20):
        data.append({
            "instructor_id": f"INS-{i+1:03d}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "department": fake.random_element(departments),
            "hire_date": fake.date_between(start_date='-10y', end_date='today').isoformat(),
            "created_at": datetime.now().isoformat()
        })
    df = pd.DataFrame(data)
    os.makedirs(BRONZE_PATH, exist_ok=True)
    df.to_csv(os.path.join(BRONZE_PATH, "instructors.csv"), index=False)
    print("Generated 20 instructors.")

if __name__ == "__main__":
    generate()
