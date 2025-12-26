import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the feature-engineered dataset
df = pd.read_csv('feature_engineered_s_user_jobrole.csv')

# Set up the dashboard with subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Job Role Distribution Dashboard', fontsize=16)

# 1. Distribution of jobrole categories
category_counts = df['jobrole_category'].value_counts()
axes[0, 0].bar(category_counts.index, category_counts.values, color='skyblue')
axes[0, 0].set_title('Distribution of Job Role Categories')
axes[0, 0].set_xlabel('Category')
axes[0, 0].set_ylabel('Count')
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Job roles across industries (top 10 industries)
industry_counts = df['industries'].value_counts().head(10)
axes[0, 1].bar(industry_counts.index, industry_counts.values, color='lightgreen')
axes[0, 1].set_title('Top 10 Industries by Job Role Count')
axes[0, 1].set_xlabel('Industry')
axes[0, 1].set_ylabel('Count')
axes[0, 1].tick_params(axis='x', rotation=45)

# 3. Job roles across departments (top 10 departments)
dept_counts = df['department'].value_counts().head(10)
axes[1, 0].bar(dept_counts.index, dept_counts.values, color='salmon')
axes[1, 0].set_title('Top 10 Departments by Job Role Count')
axes[1, 0].set_xlabel('Department')
axes[1, 0].set_ylabel('Count')
axes[1, 0].tick_params(axis='x', rotation=45)

# 4. Heatmap of jobrole_category vs industries (simplified)
# Group by industry and category, count
pivot = df.groupby(['industries', 'jobrole_category']).size().unstack().fillna(0)
# Take top industries for readability
top_industries = df['industries'].value_counts().head(5).index
pivot_top = pivot.loc[top_industries]
sns.heatmap(pivot_top, ax=axes[1, 1], cmap='Blues', annot=True, fmt='g')
axes[1, 1].set_title('Job Role Categories Across Top Industries')
axes[1, 1].set_xlabel('Category')
axes[1, 1].set_ylabel('Industry')

plt.tight_layout()
plt.savefig('jobrole_distribution_dashboard.png')
plt.show()

print("Visualization dashboard saved as 'jobrole_distribution_dashboard.png'")