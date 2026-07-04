import pandas as pd
import sqlite3
import os

#manual messy dataset
def create_sample_csv(path="raw_data.csv"):
    data = {
        "employee_id": [101, 102, 103, 104, 104, 105, None],
        "name": ["Ankit", "Bhavya", "Chirag", "Divya", "Divya", "Esha", "Farhan"],
        "department": ["IT", "HR", "IT", None, None, "Finance", "IT"],
        "salary": ["50000", "45000", None, "60000", "60000", "55000", "abc"],
        "joining_date": ["2022-01-15", "2021-07-01", "2023-03-10", "2020-11-05",
                          "2020-11-05", "2019-06-20", "2022-09-01"]
    }
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    print(f"Sample raw CSV created at: {path}")
    return path


# ----------EXTRACT ----------
def extract(csv_path):
    print("\n--- EXTRACT ---")
    df = pd.read_csv(csv_path)
    print(f"Rows extracted: {len(df)}")
    print(df)
    return df


# ----------TRANSFORM ----------
def transform(df):
    print("\n--- TRANSFORM ---")

    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicate row(s)")

    df = df.dropna(subset=["employee_id"])

    df["department"] = df["department"].fillna("Unknown")

    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    median_salary = df["salary"].median()
    df["salary"] = df["salary"].fillna(median_salary)

    df["joining_date"] = pd.to_datetime(df["joining_date"], errors="coerce")

    df["employee_id"] = df["employee_id"].astype(int)
    df["salary"] = df["salary"].astype(float)

    print("Cleaned data:")
    print(df)
    print("\nData types after cleaning:")
    print(df.dtypes)

    return df


# ----------LOAD ----------
def load(df, db_path="employees.db", table_name="employees"):
    print("\n--- LOAD ---")
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    result = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    print(f"Loaded {len(result)} rows into '{table_name}' table in {db_path}")
    print(result)

    conn.close()
    return db_path


# ---------- RUN THE PIPELINE ----------
def run_pipeline():
    csv_path = create_sample_csv()
    raw_df = extract(csv_path)
    clean_df = transform(raw_df)
    load(clean_df)
    print("\n ETL pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
