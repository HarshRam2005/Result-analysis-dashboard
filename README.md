# Result-analysis-dashboard
# 📊 Result Analysis Dashboard

## Overview
Result Analysis Dashboard is a Python-based desktop application developed using Tkinter that automates the process of extracting, converting, and analyzing student result data from PDF files.

The system reads result PDFs, extracts student details, converts the data into Excel format, performs statistical analysis, and displays results through an interactive graphical dashboard.

This project reduces manual work, improves accuracy, and helps educational institutions quickly analyze academic performance.

---

## Features

✔ Upload PDF result files  
✔ Extract student details automatically  
✔ Convert PDF data into Excel format  
✔ Calculate CGPA statistics  
✔ Identify topper details  
✔ Generate average CGPA  
✔ Display Top 5 students  
✔ Calculate subject-wise pass percentage  
✔ Identify best and weak subjects  
✔ Display CGPA distribution graph  
✔ Download generated Excel file  

---

## Technologies Used

- Python
- Tkinter (GUI)
- PDFPlumber
- Pandas
- Regular Expressions (re)
- Matplotlib
- OpenPyXL

---

## Required Libraries

Install the required dependencies:

```bash
pip install pdfplumber pandas matplotlib openpyxl
```

---

## Project Structure

```text
Result-Analysis-Dashboard/
│
├── main.py
├── README.md
├── sample_result.pdf
├── temp.xlsx
└── requirements.txt
```

---

## Working Process

### Step 1: Upload PDF
- Click the **Upload PDF** button.
- Select the result PDF file.

### Step 2: Convert PDF
- Click **Convert**
- System extracts:
  - Seat Number
  - Student Name
  - CGPA
  - Result status
  - Subject marks

### Step 3: Automatic Analysis
The system performs:

- Topper identification
- Average CGPA calculation
- Pass percentage calculation
- Best subject identification
- Weak subject identification
- Subject-wise pass percentage

### Step 4: Visual Dashboard
The dashboard displays:

- Top 5 Students table
- Subject pass percentage table
- CGPA distribution graph

### Step 5: Download Excel
Click **Download** to save the generated Excel file.

---

## Output Example

### Summary Section

```text
Topper: John Doe (9.82)

Average CGPA: 8.15

Best Subject: Database Management System

Weak Subject: Computer Networks
```

### Graph

CGPA Distribution Histogram

---

## Advantages

- Reduces manual effort
- Faster result processing
- Improves accuracy
- Easy to use GUI
- Generates meaningful insights
- Useful for educational institutions

---

## Future Enhancements

- Support multiple PDF formats
- Student performance prediction using Machine Learning
- Export reports in PDF format
- Database integration
- Subject-wise graphical comparison
- Cloud storage support

---

## Author

Harshavardhan Ramchandra Gharal  
Computer Engineering Student  
Modern Education Society's Wadia College of Engineering

Email: harshavardhangharal@gmail.com

---

## License

This project is developed for educational and research purposes.
