# BMI Calculator

A Python-based BMI Calculator application developed as part of the Oasis Infobyte Internship.

## Features

- Calculate BMI using weight and height
- BMI displayed up to 2 decimal places
- BMI category classification
- Input validation
- Tkinter graphical user interface
- Color-coded BMI results
- SQLite database for storing BMI records
- Multiple user records
- BMI history
- BMI trend graph using Matplotlib
- Error handling for invalid inputs

## BMI Categories

| BMI Range | Category |
|---|---|
| Below 18.5 | Underweight |
| 18.5 - 24.9 | Normal |
| 25 - 29.9 | Overweight |
| 30 and above | Obese |

## Technologies Used

- Python
- Tkinter
- SQLite
- Matplotlib

## Project Structure

```text
Python-Task2-BMICalculator/
│
├── main.py
├── bmi.py
├── database.py
├── requirements.txt
├── README.md
│
├── data/
│   └── bmi_history.db
│
└── screenshots/