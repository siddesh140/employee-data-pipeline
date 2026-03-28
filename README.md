# 🚀 Employee Data Pipeline (PySpark + PostgreSQL + Docker)

## 📌 Project Overview

This project demonstrates an end-to-end **Data Engineering Pipeline** that processes raw employee data using **PySpark**, performs data cleaning and transformation, and loads the processed data into a **PostgreSQL database**.

The entire pipeline is containerized using **Docker**, ensuring consistency and reproducibility.

---

## 🧠 Architecture
CSV (Raw Data)
↓
PySpark (Cleaning & Transformation)
↓
PostgreSQL (Storage)
↑
Docker (Environment Management)


---

## ⚙️ Tech Stack

- 🐍 Python (PySpark)
- 🐘 PostgreSQL
- 🐳 Docker & Docker Compose
- 🔌 JDBC Driver (PostgreSQL)

---

## 📂 Project Structure
employee-data-pipeline/
│
├── data/
│ └── employees_raw.csv
│
├── scripts/
│ └── spark_job.py
│
├── sql/
│ └── create_table.sql
│
├── jars/
│ └── postgresql-42.x.x.jar
│
├── docker-compose.yml
└── README.md


---

## 🔄 Pipeline Workflow

### 1️⃣ Data Ingestion
- Read raw CSV using PySpark

### 2️⃣ Data Cleaning
- Remove duplicates
- Handle null values (selective filtering)
- Validate email format
- Clean salary values

### 3️⃣ Data Transformation
- Create `full_name`
- Extract `email_domain`
- Calculate `age`
- Calculate `tenure_years`
- Categorize `salary_band`

### 4️⃣ Data Validation
- Remove invalid emails
- Filter future hire dates
- Handle corrupted records

### 5️⃣ Data Loading
- Load processed data into PostgreSQL using JDBC

---

## 🚀 How to Run

### 🔹 Step 1: Start Docker Containers
```bash
docker compose up -d

🔹 Step 2: Create Table in PostgreSQL
docker exec -it postgres_db psql -U admin -d employee_db
\i /path/to/create_table.sql

🔹 Step 3: Run Spark Job
docker exec -it spark_app spark-submit \
--jars /home/jovyan/work/jars/postgresql-42.x.x.jar \
/home/jovyan/work/scripts/spark_job.py

🔹 Step 4: Verify Data
docker exec -it postgres_db psql -U admin -d employee_db
SELECT COUNT(*) FROM employees_clean;

📊 Output
Cleaned and transformed employee data
Stored in PostgreSQL table: employees_clean
Example result:
COUNT = 802

🚧 Challenges Faced & Solutions

| Problem                | Solution                                  |
| ---------------------- | ----------------------------------------- |
| Docker image issues    | Switched to stable PySpark image          |
| File path errors       | Used correct container paths              |
| JDBC driver missing    | Added PostgreSQL JAR                      |
| Data type mismatch     | Used explicit casting                     |
| Date format issues     | Used `to_date()`                          |
| Over-cleaning (0 rows) | Applied selective null filtering          |
| Duplicate key error    | Deduplicated using email                  |
| Column object error    | Correct use of `col()` and DataFrame APIs |


🧠 Key Learnings
Importance of data quality handling
Difference between local vs container environment
Handling schema mismatches
Debugging real-world pipeline issues
Balancing data cleaning vs data loss

🎯 Future Improvements
Implement upsert (ON CONFLICT)
Add logging and monitoring
Use Airflow for orchestration
Store data in data warehouse (Snowflake/BigQuery)

👨‍💻 Author
Siddesh Yerawar
