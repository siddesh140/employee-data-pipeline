from faker import Faker
import random
import pandas as pd

fake = Faker()

data = []

for i in range(1000):
    data.append({
        "employee_id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email() if random.random() > 0.2 else "invalid_email",
        "hire_date": fake.date_this_decade(),
        "job_title": fake.job(),
        "department": random.choice(["IT", "HR", "Finance"]),
        "salary": f"${random.randint(30000,100000):,}",
        "manager_id": random.randint(1, 100),
        "address": fake.address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip_code": fake.zipcode(),
        "birth_date": fake.date_of_birth(minimum_age=22, maximum_age=60),
        "status": random.choice(["Active", "Inactive"])
    })

df = pd.DataFrame(data)
df.to_csv(r"D:/Create_Data/data/employees_raw.csv", index=False)