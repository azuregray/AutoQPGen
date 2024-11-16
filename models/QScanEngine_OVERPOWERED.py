import fitz
import random
import re
import spacy
from tkinter import filedialog

# Load a pretrained spaCy model for NER
nlp = spacy.load("en_core_web_sm")

def clean_question_text(question_text):
    question_text = re.sub(r'^\d+\s*\n*\d*\s*', '', question_text)
    question_text = question_text.replace("\n", " ")
    return question_text.strip()


# def get_random_questions(extracted_data, num_questions=8):
#     questions = extracted_data["Questions"]
#     random.shuffle(questions)
#     return questions[:num_questions] if len(questions) >= num_questions else questions


def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text


# Function to extract information from text using spaCy NER model
def extract_info_with_ner(text):
    info = {
        "Subject Name": None,
        "Subject Code": None,
        "SEM": None,
        "Faculty": None,
        "Questions": []
    }
    subject_name = re.search(r"Subject Name:\s*(.*)", text)
    subject_code = re.search(r"Subject Code:\s*(\S+)", text)
    sem = re.search(r"SEM\s*:\s*(\S+)", text)
    faculty = re.search(r"Faculty\s*:\s*(.*)", text)
    
    # Populate metadata if found
    if subject_name:
        info["Subject Name"] = subject_name.group(1).strip()
    if subject_code:
        info["Subject Code"] = subject_code.group(1).strip()
    if sem:
        info["SEM"] = sem.group(1).strip()
    if faculty:
        info["Faculty"] = faculty.group(1).strip()

    # Use regex to capture questions, CO, Level, and Marks
    questions = re.findall(r"(\d+)[\.\)]\s*(.*?)\s+CO(\d+)\s+L(\d+)\s+(\d+)", text, re.DOTALL)
    for q_no, question, co, level, marks in questions:
        cleaned_question = clean_question_text(question)
        info["Questions"].append({
            "SL#": int(q_no),
            "Question": cleaned_question,
            "CO": f"CO{co}",
            "Level": f"L{level}",
            "Marks": int(marks)
        })
    
    return info


# def generate_question_papers(extracted_data, num_sets=3, num_questions=8):
#     question_papers = []
#     for _ in range(num_sets):
#         selected_questions = get_random_questions(extracted_data, num_questions)
#         question_papers.append(selected_questions)
#     return question_papers


# ----------------------------------------------------------------------------------------------------------------------------------------------
pdf_path = filedialog.askopenfilename()
pdf_text = extract_text_from_pdf(pdf_path)
extracted_data = extract_info_with_ner(pdf_text)
# question_papers = generate_question_papers(extracted_data, num_sets=3, num_questions=8)


print("Subject Name:", extracted_data["Subject Name"])
print("Subject Code:", extracted_data["Subject Code"])
print("SEM:", extracted_data["SEM"])
print("Faculty:", extracted_data["Faculty"])
print("\n\n[DEBUG LOG] Questions Data is as follows:\n", extracted_data)

# for i, question_set in enumerate(question_papers, start=1):
#     print(f"\nQuestion Paper Set {i}:")
#     for question in question_set:
#         print(question)
