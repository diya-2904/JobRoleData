import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the cleaned dataset
df = pd.read_csv('cleaned_s_user_jobrole.csv')

# Function to categorize jobrole based on keywords
def categorize_jobrole(jobrole):
    if pd.isna(jobrole) or not isinstance(jobrole, str):
        return 'Other'
    jobrole_lower = jobrole.lower()
    if any(word in jobrole_lower for word in ['manager', 'director', 'chief', 'head', 'vice president', 'general manager', 'president', 'partner', 'senior manager']):
        return 'Management'
    elif any(word in jobrole_lower for word in ['engineer', 'technician', 'specialist', 'analyst', 'architect', 'developer', 'scientist', 'researcher']):
        return 'Technical'
    elif any(word in jobrole_lower for word in ['assistant', 'executive', 'coordinator', 'officer', 'clerk', 'associate', 'administrator']):
        return 'Support'
    elif any(word in jobrole_lower for word in ['operator', 'worker', 'supervisor']):
        return 'Operational'
    else:
        return 'Other'

# Populate jobrole_category
df['jobrole_category'] = df['jobrole'].apply(categorize_jobrole)

# Encode jobrole_category to numeric 
le = LabelEncoder()
df['jobrole_category_encoded'] = le.fit_transform(df['jobrole_category'])

# One-hot encode jobrole_category
one_hot = pd.get_dummies(df['jobrole_category'], prefix='is')
df = pd.concat([df, one_hot], axis=1)

# Save the feature-engineered dataset
df.to_csv('feature_engineered_s_user_jobrole.csv', index=False)

print("Feature engineering completed. Dataset saved as 'feature_engineered_s_user_jobrole.csv'")