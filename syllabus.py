import streamlit as st
import time
from xhtml2pdf import pisa
import markdown
import io


# Function to convert HTML to PDF
def convert_html_to_pdf(html_content):
    pdf = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf)
    if pisa_status.err:
        return None
    return pdf.getvalue()


def generate_response(data):
    from langchain_google_genai import ChatGoogleGenerativeAI

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        backoff_factor=2,
        verbose=True,
        streaming=True,
        top_k=None,
        top_p=None,
        safety_settings=None,
        google_api_key="YOUR GEMINI API KEY",
        google_cse_id=None,
    )

    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an educational consultant AI, and your mission is to analyze and compare the syllabus content of multiple courses.
                After comparing, generate a comprehensive syllabus that combines the key topics, ensuring a balanced and 
                integrated curriculum that covers all essential areas. 
                Provide a combined syllabus that integrates the main topics and ensures a cohesive learning experience.""",
            ),
            ("human", "{course}"),
        ]
    )

    chain = prompt | llm
    ai_msg = chain.invoke(
        {
            "course": data,
        }
    )

    return ai_msg.content


def extract_syllabus(udemy_url):
    from selenium.webdriver.common.by import By
    from seleniumbase import Driver

    # Create a Driver instance with undetected_chromedriver (uc) and headless mode
    driver = Driver(uc=True, headless=False)

    # Open the URL and wait for the page to load
    url = udemy_url
    driver.get(url)
    print(driver.title)

    # Get the course title
    name = driver.find_element(By.CSS_SELECTOR, "h1[data-purpose='lead-title']").text

    time.sleep(5)
    element = driver.find_element(
        By.CSS_SELECTOR,
        'div[data-purpose="course-curriculum"] button[data-purpose="expand-toggle"].ud-btn.ud-btn-medium.ud-btn-ghost',
    )
    element.click()

    # Scrape the syllabus section
    data = {}
    div = driver.find_element(By.CSS_SELECTOR, 'div[data-purpose="course-curriculum"]')
    for section in div.find_elements(
        By.CSS_SELECTOR,
        "div.accordion-panel-module--panel--Eb0it.section--panel--qYPjj",
    ):
        title_element = section.find_element(
            By.CSS_SELECTOR, "span.section--section-title--svpHP"
        )
        subdata = []

        for sublinks in section.find_elements(By.CSS_SELECTOR, "span.ud-btn-label"):
            subdata.append(sublinks.text)

        for subtitles in section.find_elements(
            By.CSS_SELECTOR, "span.section--item-title--EWIuI "
        ):
            subdata.append(subtitles.text)

        data[title_element.text] = subdata

    # Combine course title and syllabus into a dictionary
    course_data = {"course_title": name, "syllabus": data}

    driver.quit()

    return course_data


st.title("Udemy CourseMate: Syllabus Extractor & Smart Curriculum Generator")

# Initialize session state for storing course links
if "course_links" not in st.session_state:
    st.session_state.course_links = ["", ""]


# Function to add a new course link input field
def add_course_link():
    st.session_state.course_links.append("")


# Function to remove a course link input field
def remove_course_link(index):
    if st.session_state.course_links:
        st.session_state.course_links.pop(index)


# Display input fields for each course link
for i, link in enumerate(st.session_state.course_links):
    col1, col2 = st.columns([8, 2])
    with col1:
        st.session_state.course_links[i] = st.text_input(
            f"Enter Udemy course link {i+1}:", link, key=f"course_link_{i}"
        )
    with col2:
        st.button(f"X", key=f"remove_{i}", on_click=lambda: remove_course_link(i))

# Buttons to add or remove course links
st.button("Add another course link", on_click=add_course_link)

# Button to extract syllabi
if st.button("Generate Syllabus"):
    if st.session_state.course_links:
        with st.spinner("Extracting syllabus..."):
            # Initialize progress bar
            p1 = st.progress(0)
            course = {}

            # Extract syllabi for each course
            for i, link in enumerate(st.session_state.course_links):
                p1.progress(int((i / len(st.session_state.course_links)) * 100))
                syllabus = extract_syllabus(link)
                course[f"course_{i+1}"] = syllabus

        p1.progress(100)  # Complete progress
        st.success("Syllabus Extracted")
        # st.json(syllabi)

        # Store the result in session state for later use

        with st.spinner("Generating syllabus..."):
            p2 = st.progress(0)
            p2.progress(10)
            # Generate a syllabus using the response
            syllabus = generate_response(course)
            p2.progress(50)
            st.text("Generated Syllabus:")
            p2.progress(100)
            st.markdown(syllabus)

            html_text = markdown.markdown(syllabus)

            # Convert HTML to PDF
            pdf = convert_html_to_pdf(html_text)

            if pdf:
                st.success("PDF generated successfully!")

                # Provide download link for PDF
                st.download_button(
                    label="Download PDF",
                    data=pdf,
                    file_name="output.pdf",
                    mime="application/pdf",
                )

    else:
        st.error("Please enter at least one Udemy course link.")
