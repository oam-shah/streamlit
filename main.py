import streamlit as st
import sqlite3
from fpdf import FPDF
import os
from datetime import date

# SQLite database configuration
DB_NAME = 'admissions.db'

# Create the admissions table
def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS admissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  dob TEXT,
                  age INTEGER,
                  standard TEXT,
                  student_type TEXT,
                  joining_date TEXT,
                  contact1 TEXT,
                  contact2 TEXT,
                  address TEXT,
                  city TEXT,
                  aadhar TEXT,
                  email TEXT,
                  current_standard TEXT,
                  school TEXT,
                  subjects TEXT,
                  percentage REAL,
                  student_type2 TEXT)''')
    conn.commit()
    conn.close()

# Generate PDF
def generate_pdf(data, student_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Admission Form', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)

    sections = {
        'Personal Information': ['Name', 'Date of Birth', 'Age'],
        'Contact Details': ['Contact 1', 'Contact 2', 'Address', 'City'],
        'Educational Details': ['Standard', 'Student Type', 'Joining Date', 'Current Standard', 'School', 'Subjects', 'Percentage', 'Student Type 2']
    }

    for section, fields in sections.items():
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, section, 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        for field in fields:
            pdf.cell(40, 10, f'{field}:', 0, 0, 'L')
            pdf.cell(0, 10, str(data[field]), 0, 1, 'L')
        pdf.ln()

    # Save PDF with student's name as file name
    pdf_path = os.path.join('C:/Users/oam/Downloads/Python Student admission form', f'{student_name}.pdf')
    pdf.output(pdf_path)
    return pdf_path

# Streamlit web app
def admission_form():
    st.title('Admission Form')

    # Form inputs
    name = st.text_input('Name')
    dob = st.date_input('Date of Birth')
    age = st.number_input('Age', min_value=0, max_value=150, step=1, value=0)
    standard = st.selectbox('Standard', ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th'])
    student_type = st.selectbox('Student Type', ['Regular', 'New Admission'])
    joining_date = st.date_input('Joining Date')
    contact1 = st.text_input('Contact 1')
    contact2 = st.text_input('Contact 2')
    address = st.text_area('Address')
    city = st.text_input('City')
    aadhar = st.text_input('Aadhar')
    email = st.text_input('Email')
    current_standard = st.selectbox('Current Standard', ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th'])
    school = st.text_input('School')
    subjects = st.multiselect('Subjects', ['English', 'Mathematics', 'EVS (General Science)', 'Hindi', 'Marathi'])
    percentage = st.number_input('Percentage', min_value=0.0, max_value=100.0, step=0.01, value=0.0)
    student_type2 = st.selectbox('Student Type 2', ['Regular', 'Backlog'])

    if dob:
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    if st.button('Submit'):
        # Insert data into the database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''INSERT INTO admissions
                     (name, dob, age, standard, student_type, joining_date, contact1, contact2, address, city, aadhar, email, current_standard, school, subjects, percentage, student_type2)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (name, dob, age, standard, student_type, joining_date, contact1, contact2,
                   address, city, aadhar, email, current_standard, school, ', '.join(subjects), percentage, student_type2))
        conn.commit()
        conn.close()

        # Generate PDF
        data = {
            'Name': name,
            'Date of Birth': dob,
            'Age': age,
            'Standard': standard,
            'Student Type': student_type,
            'Joining Date': joining_date,
            'Contact 1': contact1,
            'Contact 2': contact2,
            'Address': address,
            'City': city,
            'Aadhar': aadhar,
            'Email': email,
            'Current Standard': current_standard,
            'School': school,
            'Subjects': ', '.join(subjects),
            'Percentage': percentage,
            'Student Type 2': student_type2
        }
        pdf_path = generate_pdf(data, name)  # Pass the student's name as an argument

        st.success('Form submitted successfully!')
        st.markdown(f"Download PDF: [admission_form.pdf]({pdf_path})")

if __name__ == '__main__':
    create_table()
    admission_form()
