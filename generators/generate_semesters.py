import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from datetime import datetime
from config.settings import BRONZE_PATH

def generate():
    data = []
    for i in range(6):
        data.append({
            "semester_id": f"SEM-{i+1}",
            "name": f"Semester {i+1}",
            "start_date": f"202{3+(i//2)}-{1 if i%2==0 else 8}-01",
            "end_date": f"202{3+(i//2)}-{6 if i%2==0 else 12}-15",
            "created_at": datetime.now().isoformat()
        })
    df = pd.DataFrame(data)
    os.makedirs(BRONZE_PATH, exist_ok=True)
    df.to_csv(os.path.join(BRONZE_PATH, "semesters.csv"), index=False)
    print("Generated 6 semesters.")

if __name__ == "__main__":
    generate()
