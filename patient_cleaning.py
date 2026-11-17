import numpy as np
import pandas as pd

data = {
    "patient_id": ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008"],
    "name":       ["  maria SILVA ", "John Carter", "ana souza", "Carlos Lima",
                   "John Carter", "Lucia Rocha", "Pedro Alves", "SARA KIM"],
    "gender":     ["F", "male", "Female", "M", "Male", "unknown", None, "f"],
    "birth_date": ["1985-03-12", "1962/11/02", "12 Jul 1993", "1978-09-30",
                   "1962-11-02", "2090-01-01", None, "1990-05-14"],
    "weight_kg":  [62, 85, 0, 78, 85, 55, 70, -1],
    "height_cm":  [165, 180, 160, 999, 180, 158, 175, 168],
    "blood_type": ["A+", "O-", "b+", "AB+", "O-", "", "O+", "A-"],
    "phone":      ["(11) 5550-1010", "555-0102", "N/A", "555 0104",
                   "555-0102", "555-0106", "555-0107", "555-0108"],
}
df = pd.DataFrame(data)
rows_before = len(df)

# 1. Strip whitespace, turn placeholders into real missing values
text_cols = ["name", "gender", "birth_date", "blood_type", "phone"]
for col in text_cols:
    df[col] = df[col].str.strip()

placeholders = ["N/A", "n/a", "", "unknown", "Unknown"]
df[text_cols] = df[text_cols].replace(placeholders, np.nan)

# 2. Impossible numeric values become missing
df["weight_kg"] = df["weight_kg"].where(df["weight_kg"].between(20, 300))
df["height_cm"] = df["height_cm"].where(df["height_cm"].between(50, 250))

# 3. Standardize text
df["name"] = df["name"].str.title()
df["blood_type"] = df["blood_type"].str.upper()
gender_map = {"m": "Male", "male": "Male", "f": "Female", "female": "Female"}
df["gender"] = df["gender"].str.lower().map(gender_map)

# 4. Dates
df["birth_date"] = pd.to_datetime(df["birth_date"], format="mixed", errors="coerce")
today = pd.Timestamp("2024-01-15")
df.loc[df["birth_date"] > today, "birth_date"] = pd.NaT

# 5. Phone numbers: digits only
df["phone"] = df["phone"].str.replace(r"\D", "", regex=True)

# 6. Duplicates (after standardizing!)
df = df.drop_duplicates(subset=["name", "birth_date", "gender"], keep="first")

# 7. Quality report and review flag
critical = ["birth_date", "gender", "weight_kg", "height_cm"]
df["needs_review"] = df[critical].isnull().any(axis=1)

print(f"Rows before: {rows_before} | Rows after: {len(df)}")
print("\nMissing values (%):")
print((df.isnull().mean() * 100).round(1))
print("\nPatients needing review:")
print(df[df["needs_review"]][["patient_id", "name"]])

df.to_csv("patients_clean.csv", index=False)