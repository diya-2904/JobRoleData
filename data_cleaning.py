import pandas as pd
import json

# Load the CSV file
file_path = r"c:\Users\DIYA\OneDrive\Desktop\JobRoleData\s_user_jobrole.csv"
df = pd.read_csv(file_path, skiprows=1)  # Skip the first row if it's metadata

# Map columns to schema
schema = {
    "id": "int",
    "industries": "str",
    "department": "str",
    "sub_department": "str",
    "department_id": "int",
    "jobrole": "str",
    "description": "str",
    "jobrole_category": "str",
    "performance_expectation": "str",
    "status": "str",
    "related_jobrole": "str",
    "required_skill_experience": "str",
    "location": "str",
    "salary_range": "str",
    "company_information": "str",
    "responsibilities": "str",
    "benefits": "str",
    "keyword_tags": "str",
    "job_posting_date": "str",
    "application_deadline": "str",
    "contact_information": "str",
    "internal_tracking": "str",
    "education": "str",
    "experience": "str",
    "training": "str",
    "sub_institute_id": "int",  # Primary organization key
    "created_by": "str",
    "updated_by": "str",
    "deleted_by": "str",
    "created_at": "str",
    "updated_at": "str",
    "deleted_at": "str",
}

# Apply schema mapping
df = df.astype(schema)
print("Schema mapping completed.")

# Detect duplicates based on 'id'
duplicates = df[df.duplicated(subset=["id"], keep=False)]
print("Duplicate rows detected:")
print(duplicates)

# Remove duplicates, keeping the first occurrence
df_cleaned = df.drop_duplicates(subset=["id"], keep="first")
print("Duplicates removed. Cleaned dataset shape:", df_cleaned.shape)

# Check for missing or invalid sub_institute_id
invalid_sub_institute = df_cleaned[df_cleaned["sub_institute_id"].isnull()]
if not invalid_sub_institute.empty:
    print("Invalid sub_institute_id detected:")
    print(invalid_sub_institute)

# Drop rows with missing sub_institute_id
df_cleaned = df_cleaned.dropna(subset=["sub_institute_id"])
print("Rows with missing sub_institute_id removed.")

# Sprint 2: Data Cleaning & Transformation (ETL)

# 1. Handling Nulls: Flag missing values in critical columns
critical_columns = ["required_skill_experience", "jobrole"]
for col in critical_columns:
    df_cleaned[f"{col}_missing"] = df_cleaned[col].isnull()
    print(f"Missing values flagged in column: {col}")

# 2. Standardization: Clean industries and department columns
columns_to_clean = ["industries", "department"]
for col in columns_to_clean:
    df_cleaned[col] = df_cleaned[col].str.strip().str.title()  # Remove spaces and ensure title case
    print(f"Column '{col}' standardized.")

# Save the cleaned dataset
output_path = r"c:\Users\DIYA\OneDrive\Desktop\JobRoleData\cleaned_s_user_jobrole.csv"
df_cleaned.to_csv(output_path, index=False)
print(f"Cleaned dataset saved to {output_path}")

# Generate schema document
schema_doc = {
    "columns": list(schema.keys()),
    "data_types": schema,
    "primary_key": "sub_institute_id",
}
schema_doc_path = r"c:\Users\DIYA\OneDrive\Desktop\JobRoleData\data_schema.json"

with open(schema_doc_path, "w") as f:
    json.dump(schema_doc, f, indent=4)
print(f"Data schema document saved to {schema_doc_path}")

# Sprint 3: Exploratory Data Analysis (EDA) & Pattern Identification

# 1. Statistical Profiling: Generate summary statistics
eda_report = {}

# Summary statistics for industries, department, and jobrole per sub_institute_id
eda_report["industries_summary"] = df_cleaned.groupby("sub_institute_id")["industries"].value_counts().to_dict()
eda_report["department_summary"] = df_cleaned.groupby("sub_institute_id")["department"].value_counts().to_dict()
eda_report["jobrole_summary"] = df_cleaned.groupby("sub_institute_id")["jobrole"].value_counts().to_dict()

# 2. Trend Analysis: Analyze jobrole frequency across industries
jobrole_trends = df_cleaned.groupby("industries")["jobrole"].value_counts()
eda_report["jobrole_trends"] = jobrole_trends.to_dict()

# 3. Stakeholder Requirements Mapping: Translate findings into analytics requirements
# Example: Identify top industries and departments with the highest jobrole frequency
top_industries = jobrole_trends.groupby(level=0).sum().sort_values(ascending=False).head(5)
top_departments = df_cleaned["department"].value_counts().head(5)

eda_report["top_industries"] = top_industries.to_dict()
eda_report["top_departments"] = top_departments.to_dict()

# Save the EDA report
eda_report_path = r"c:\Users\DIYA\OneDrive\Desktop\JobRoleData\eda_report.json"
with open(eda_report_path, "w") as f:
    json.dump(eda_report, f, indent=4)
print(f"EDA report saved to {eda_report_path}")