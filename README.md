# Student Performance Analysis System

A beginner-friendly Python mini project that analyzes student academic performance using Pandas, NumPy and Matplotlib.

## Aim

To analyze student performance based on attendance, assignment marks, MST marks and final examination marks using Python.

## Project Overview

This project takes student academic data from a CSV file and performs basic data analysis and visualization. It calculates total marks, percentage and grades, identifies top-performing students, compares departments and finds students with low attendance.

## Features

- Load student data from CSV
- Display and inspect the dataset
- Check for missing values
- Calculate total marks
- Calculate percentage
- Assign grades
- Find top 5 students
- Calculate average percentage
- Find highest and lowest percentage
- Compare CSE and DS departments
- Find students with attendance below 75%
- Generate graphs using Matplotlib

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib

## Dataset

The dataset contains 30 students with the following information:

| Column | Description |
|---|---|
| Student | Student name |
| Department | CSE or DS |
| Attendance | Attendance percentage |
| Assignment | Assignment marks out of 20 |
| MST | MST marks out of 20 |
| Final Exam | Final examination marks out of 80 |

The total marks are calculated out of 120.

## Results

The current analysis produced the following results:

- Average student percentage: **87.03%**
- Highest percentage: **99.17%**
- Lowest percentage: **66.67%**
- CSE average percentage: **87.94%**
- DS average percentage: **86.11%**
- Students with attendance below 75%: **7**

### Top 5 Students

1. Tanya
2. Neha
3. Navjot
4. Mandeep
5. Isha

All five students achieved an A+ grade.

## Visualizations

The project generates three visualizations:

1. Department-wise Average Percentage
2. Grade Distribution
3. Student Percentage

## How to Run

Clone or download this repository.

Open the project folder in VS Code and run:

```bash
python student_performance.py
