import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the student dataset
df = pd.read_csv("Student_Performance/student_data.csv")
# Display the dataset
print("Student Dataset:")
print(df)

# Display first 5 records
print("\nFirst 5 Records:")
print(df.head())

# Display information about the dataset
print("\nDataset Information:")
print(df.info())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Calculate Total Marks
df['Total'] = df['Assignment'] + df['MST'] + df['Final Exam']

# Calculate Percentage
df['Percentage'] = (df['Total'] / 120) * 100

# Assign Grade
def calculate_grade(percentage):
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B'
    elif percentage >= 60:
        return 'C'
    elif percentage >= 50:
        return 'D'
    else:
        return 'F'

df['Grade'] = df['Percentage'].apply(calculate_grade)

# Display final student performance
print("\nStudent Performance:")
print(df[['Student', 'Total', 'Percentage', 'Grade']])

# Find the Top 5 Students
top_students = df.sort_values('Percentage', ascending=False).head(5)

print("\nTop 5 Students:")
print(top_students[['Student', 'Department', 'Percentage', 'Grade']])


# Calculate Average Percentage
average_percentage = df['Percentage'].mean()

print("\nAverage Percentage of Students:")
print(round(average_percentage, 2))


# Find Highest and Lowest Percentage
highest_percentage = df['Percentage'].max()
lowest_percentage = df['Percentage'].min()

print("\nHighest Percentage:")
print(round(highest_percentage, 2))

print("\nLowest Percentage:")
print(round(lowest_percentage, 2))


# Department-wise Average Percentage
department_average = df.groupby('Department')['Percentage'].mean()

print("\nDepartment-wise Average Percentage:")
print(department_average)


# Find students with attendance below 75%
low_attendance = df[df['Attendance'] < 75]

print("\nStudents with Attendance Below 75%:")
print(low_attendance[['Student', 'Department', 'Attendance']])


# -------------------------------
# Data Visualization
# -------------------------------

# 1. Department-wise Average Percentage
department_average.plot(kind='bar')

plt.title('Department-wise Average Percentage')
plt.xlabel('Department')
plt.ylabel('Average Percentage')
plt.xticks(rotation=0)
plt.show()


# 2. Grade Distribution
grade_count = df['Grade'].value_counts()

grade_count.plot(kind='pie', autopct='%1.1f%%')

plt.title('Grade Distribution')
plt.ylabel('')
plt.show()


# 3. Student Percentage
plt.figure(figsize=(10, 5))

plt.bar(df['Student'], df['Percentage'])

plt.title('Student Percentage')
plt.xlabel('Student')
plt.ylabel('Percentage')
plt.xticks(rotation=90)
plt.show()