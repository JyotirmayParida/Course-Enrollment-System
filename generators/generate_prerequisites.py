import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random
import pandas as pd
from faker import Faker
from datetime import datetime
from config.settings import BRONZE_PATH

fake = Faker()

def has_cycle(graph):
    visited = set()
    rec_stack = set()
    
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False

    for node in list(graph.keys()):
        if node not in visited:
            if dfs(node):
                return True
    return False

def generate_prereqs(num_records, course_ids):
    prerequisites = []
    graph = {cid: [] for cid in course_ids}
    
    count = 0
    attempts = 0
    while count < num_records and attempts < num_records * 100:
        attempts += 1
        course = random.choice(course_ids)
        prereq = random.choice(course_ids)
        
        if course == prereq:
            continue
            
        if prereq in graph[course]:
            continue
            
        graph[course].append(prereq)
        
        if has_cycle(graph):
            graph[course].remove(prereq)
        else:
            prerequisites.append({
                "prerequisite_id": f"PRQ-{count+1:04d}",
                "course_id": course,
                "prerequisite_course_id": prereq,
                "created_at": datetime.now().isoformat()
            })
            count += 1
            
    return pd.DataFrame(prerequisites)

def generate():
    courses_file = os.path.join(BRONZE_PATH, "courses.csv")
    if os.path.exists(courses_file):
        courses_df = pd.read_csv(courses_file)
        course_ids = courses_df['course_id'].tolist()
    else:
        course_ids = [f"CRS-{i+1:04d}" for i in range(60)]
        
    df = generate_prereqs(80, course_ids)
    os.makedirs(BRONZE_PATH, exist_ok=True)
    df.to_csv(os.path.join(BRONZE_PATH, "prerequisites.csv"), index=False)
    print("Generated 80 prerequisites without circular dependencies.")

if __name__ == "__main__":
    generate()
