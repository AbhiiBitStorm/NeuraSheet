import pandas as pd
from pathlib import Path

# Sample data
data = {
    'Name': ['Rahul', 'Priya', 'Amit', 'Sneha', 'Vikas'],
    'Age': [25, 30, 35, 28, 32],
    'City': ['Delhi', 'Mumbai', 'Bangalore', 'Delhi', 'Mumbai'],
    'Salary': [50000, 60000, 75000, 55000, 70000]
}

df = pd.DataFrame(data)
df.to_excel('test_files/sample.xlsx', index=False)
print("✅ Sample Excel file created!")