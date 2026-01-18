import pandas as pd
import numpy as np

np.random.seed(42)

NUM_EMPLOYEES = 1000
TODAY = pd.Timestamp("2026-01-01")

# -------------------- Employees Table --------------------
employees = pd.DataFrame({
    "Employee_ID": range(1, NUM_EMPLOYEES + 1),
    "Gender": np.random.choice(["Male", "Female"], NUM_EMPLOYEES),
    "Age": np.random.randint(22, 60, NUM_EMPLOYEES),
    "Department": np.random.choice(["IT", "Sales", "HR", "Finance"], NUM_EMPLOYEES),
    "Job_Role": np.random.choice(["Analyst", "Manager", "Executive"], NUM_EMPLOYEES),
    "Hire_Date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2018-01-01", "2024-12-31"),
            NUM_EMPLOYEES
        )
    )
})

# -------------------- Employment Status --------------------
employees["Employment_Status"] = "Active"
left_mask = np.random.rand(NUM_EMPLOYEES) < 0.25  # 25% Left
employees.loc[left_mask, "Employment_Status"] = "Left"

# -------------------- Exit Date --------------------
employees["Exit_Date"] = pd.NaT
employees.loc[left_mask, "Exit_Date"] = (
    employees.loc[left_mask, "Hire_Date"]
    + pd.to_timedelta(
        np.random.randint(180, 1800, left_mask.sum()),
        unit="D"
    )
)

# -------------------- Tenure (SAFE CALCULATION) --------------------
employees["Tenure_Months"] = None

# For Left employees
employees.loc[left_mask, "Tenure_Months"] = (
    (employees.loc[left_mask, "Exit_Date"]
     - employees.loc[left_mask, "Hire_Date"])
    .dt.days / 30
)

# For Active employees
employees.loc[~left_mask, "Tenure_Months"] = (
    (TODAY - employees.loc[~left_mask, "Hire_Date"])
    .dt.days / 30
)

# -------------------- Performance Table --------------------
performance = pd.DataFrame({
    "Employee_ID": employees["Employee_ID"],
    "Monthly_Target": np.random.randint(80, 150, NUM_EMPLOYEES),
    "Monthly_Achieved": np.random.randint(50, 160, NUM_EMPLOYEES),
    "Performance_Rating": np.random.randint(1, 6, NUM_EMPLOYEES),
    "Overtime_Hours": np.random.randint(0, 20, NUM_EMPLOYEES)
})

# -------------------- Compensation Table --------------------
compensation = pd.DataFrame({
    "Employee_ID": employees["Employee_ID"],
    "Salary": np.random.randint(30000, 120000, NUM_EMPLOYEES),
    "Bonus": np.random.randint(2000, 10000, NUM_EMPLOYEES),
    "Benefits_Cost": np.random.randint(1000, 5000, NUM_EMPLOYEES)
})

# -------------------- Save CSV --------------------
employees.to_csv("HR_Employees.csv", index=False)
performance.to_csv("HR_Performance.csv", index=False)
compensation.to_csv("HR_Compensation.csv", index=False)

print("✅ HR Analytics data generated successfully!")
