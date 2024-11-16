import fitz
import random
import re
import spacy

# Load a pretrained spaCy model for NER
nlp = spacy.load("en_core_web_sm")

def clean_question_text(question_text):
    question_text = re.sub(r'^\d+\s*\n*\d*\s*', '', question_text)
    question_text = question_text.replace("\n", " ")
    return question_text.strip()


def listRandomizer(itemsList, numberOfItems):
    random.shuffle(itemsList)
    if len(itemsList) >= numberOfItems:
        return itemsList[:numberOfItems]
    else:
        return itemsList


def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text


# Function to extract information from text using spaCy NER model
def extract_info_with_ner(text):
    info = {
        "subjectName": None,
        "subjectCode": None,
        "semester": None,
        "facultyName": None,
        "qBankContent": []
    }
    subjectName = re.search(r"Subject Name:\s*(.*)", text)
    subjectCode = re.search(r"Subject Code:\s*(\S+)", text)
    semester = re.search(r"SEM\s*:\s*(\S+)", text)
    facultyName = re.search(r"Faculty\s*:\s*(.*)", text)
    
    # Populate metadata if found
    if subjectName:
        info["subjectName"] = subjectName.group(1).strip()
    if subjectCode:
        info["subjectCode"] = subjectCode.group(1).strip()
    if semester:
        info["semester"] = semester.group(1).strip()
    if facultyName:
        info["facultyName"] = facultyName.group(1).strip()

    questions = re.findall(r"(\d+)[\.\)]\s*(.*?)\s+CO(\d+)\s+L(\d+)\s+(\d+)", text, re.DOTALL)
    for q_no, question, co, level, marks in questions:
        cleaned_question = clean_question_text(question)
        info["qBankContent"].append({
            "question": cleaned_question,
            "co": co,
            "level": level
        })
    
    return info


def QScanExport(questionBankPath):
    qBankDataLevel1 = extract_text_from_pdf(questionBankPath)
    qBankDataLevel2 = extract_info_with_ner(qBankDataLevel1)
    
    facultyName = qBankDataLevel2["facultyName"]
    courseName = qBankDataLevel2["subjectName"]
    courseCode = qBankDataLevel2["subjectCode"]
    semester = qBankDataLevel2["semester"]
    
    qBankContentList = listRandomizer(qBankDataLevel2["qBankContent"], 8)
    questionsList = []
    coList = []
    levelsList = []
    modulesList = []
    
    for content in qBankContentList:
        questionsList.append(content["question"])
        coList.append(content["co"])
        levelsList.append(content["level"])
        modulesList.append(content["co"])
    
    return {key: value for key, value in locals().items() if key in ['facultyName', 'courseName', 'courseCode', 'semester', 'questionsList', 'coList', 'levelsList', 'modulesList']}
