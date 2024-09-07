# Syllabus-Generator

# Syllabus Extractor & Smart Curriculum Generator

This project is a **Streamlit** app that extracts course syllabi from Udemy and generates a smart, combined curriculum using the **Google Gemini API**. The extracted syllabi can also be downloaded as a PDF.

## Features

- Extract syllabi from multiple Udemy courses using Selenium.
- Generate a combined, integrated syllabus from the extracted content using the Google Gemini AI model.
- Download the generated syllabus as a PDF.
- User-friendly interface with the ability to add/remove course URLs.

## Installation

1. Clone the repository:
   git clone https://github.com/JAYASIMA/Syllabus-Generator.git
   cd Syllabus-Generator

2. Install the required Python packages:
   pip install -r requirements.txt

3. Set up your Google Gemini API key in the script (app.py):
   google_api_key="your_google_api_key"

4. Run the app:
   streamlit run app.py

Usage:
Enter the URLs of the Udemy courses from which you want to extract the syllabus.
Click the Generate Syllabus button to extract and combine syllabi.
Once the syllabus is generated, you can download it as a PDF.

Dependencies:
Streamlit: Interactive interface for the app.
SeleniumBase: Web scraping library to extract the syllabus from Udemy.
Google Gemini API: AI model used to generate a combined syllabus.
xhtml2pdf: Library to convert HTML to PDF.
markdown: Used for rendering syllabus content.
  
