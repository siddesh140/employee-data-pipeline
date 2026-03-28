from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.functions import to_date

spark = SparkSession.builder \
    .appName("Employee Data Pipeline") \
    .getOrCreate()

# STEP 1: READ
df = spark.read.csv("/home/jovyan/work/data/employees_raw.csv", header=True, inferSchema=True)

print("Raw Data:")
df.show(5)

# STEP 2: CLEANING

# Remove duplicates (initial)
df_clean = df.dropDuplicates(["employee_id", "email"])

# Email lowercase
df_clean = df_clean.withColumn("email", lower(col("email")))

# Filter valid emails
df_clean = df_clean.filter(
    col("email").rlike("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+$")
)

# Remove null critical fields
df_clean = df_clean.dropna(subset=["employee_id", "email"])

# Salary cleaning
df_clean = df_clean.withColumn(
    "salary",
    regexp_replace(col("salary"), "[$,]", "").cast("double")
)

# Name formatting
df_clean = df_clean.withColumn("first_name", initcap(col("first_name"))) \
                   .withColumn("last_name", initcap(col("last_name")))

# Date conversion
df_clean = df_clean.withColumn(
    "birth_date",
    to_date(col("birth_date"), "yyyy-MM-dd")
)

df_clean = df_clean.withColumn(
    "hire_date",
    to_date(col("hire_date"), "yyyy-MM-dd")
)

# Remove future hire_date (assignment requirement 🔥)
df_clean = df_clean.filter(col("hire_date") <= current_date())

# STEP 3: TRANSFORMATIONS

df_clean = df_clean.withColumn("full_name", concat_ws(" ", "first_name", "last_name"))

df_clean = df_clean.withColumn("email_domain", split(col("email"), "@").getItem(1))

df_clean = df_clean.withColumn("age", year(current_date()) - year(col("birth_date")))

df_clean = df_clean.withColumn(
    "tenure_years",
    year(current_date()) - year(col("hire_date"))
)

df_clean = df_clean.withColumn(
    "salary_band",
    when(col("salary") < 50000, "Junior")
    .when((col("salary") >= 50000) & (col("salary") <= 80000), "Mid")
    .otherwise("Senior")
)

# STEP 4: CAST

df_clean = df_clean \
    .withColumn("employee_id", col("employee_id").cast("int")) \
    .withColumn("manager_id", col("manager_id").cast("int")) \
    .withColumn("tenure_years", col("tenure_years").cast("int"))

# ✅ FINAL DEDUP (VERY IMPORTANT)
df_clean = df_clean.dropDuplicates(["email"])

print("Cleaned Data:")
df_clean.show(5)

# STEP 5: LOAD

df_clean.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/employee_db") \
    .option("dbtable", "employees_clean") \
    .option("user", "admin") \
    .option("password", "admin") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

print("Data loaded successfully!")
