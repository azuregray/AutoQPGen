import fitz
import random
import re
import spacy

# # GenAI Requirements
# import os
# from time import sleep
# import google.generativeai as genai

# Load a pretrained spaCy model for NER
nlp = spacy.load("en_core_web_sm")

def clean_question_text(question_text):
    textStage1 = re.sub(r'^\d+\s*\n*\d*\s*', '', question_text)
    textStage2 = textStage1.replace("\n", " ")
    finalText = textStage2.strip()
    return finalText

def questionSetter(listOfDictionaries, howMany):
    uniqueModNums = list(set(item['modnum'] for item in listOfDictionaries)) # Finding unique module numbers using FUNDAMENTAL PROPERTY OF SETS
    
    sorted_list = sorted(listOfDictionaries, key=lambda x: x['modnum']) # Sorting structured quesitions data based on ModuleNumber values
    
    firstModGroup = [item for item in sorted_list if item['modnum'] == uniqueModNums[0]] # Split the list into two groups (lists) based on modnum
    secondModGroup = [item for item in sorted_list if item['modnum'] == uniqueModNums[1]]
    
    random.shuffle(firstModGroup)        # Randomize each group
    random.shuffle(secondModGroup)
    
    return firstModGroup[:howMany // 2] + secondModGroup[:howMany // 2] # Return ListOfDictionaries required n questions by joining first n/2 items from each list

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

    questions = re.findall(r"(\d+)[\.\)]\s*(.*?)\s+CO(\d+)\s+L(\d+)\s+(\d+)\s+(\d+)", text, re.DOTALL | re.IGNORECASE)
    for q_no, question, co, level, marks, modnum in questions:
        cleaned_question = clean_question_text(question)
        # rephrasedQuestion = GenAIRephraser(cleaned_question) # Question rephrasal using GenerativeAI model
        info["qBankContent"].append({ # This creates a LIST OF DICTIONARIES
            "question": cleaned_question,
            "co": co,
            "level": level,
            "modnum": modnum
        })
        
    return info


def QScanExport(questionBankPath):
    qBankDataLevel1 = extract_text_from_pdf(questionBankPath)
    qBankDataLevel2 = extract_info_with_ner(qBankDataLevel1)
    
    facultyName = qBankDataLevel2["facultyName"]
    courseName = qBankDataLevel2["subjectName"]
    courseCode = qBankDataLevel2["subjectCode"]
    semester = qBankDataLevel2["semester"]
    questionsList = []
    coList = []
    levelsList = []
    modulesList = []
    
    qBankContentList = questionSetter(qBankDataLevel2["qBankContent"], 8)
    
    for content in qBankContentList:
        questionsList.append(content["question"])
        coList.append(content["co"])
        levelsList.append(content["level"])
        modulesList.append(content["modnum"])
    
    return {key: value for key, value in locals().items() if key in ['facultyName', 'courseName', 'courseCode', 'semester', 'questionsList', 'coList', 'levelsList', 'modulesList']}

# WARNING ----------------------- 
# This QScanEngine.py currently purely return data extracted from the input Question Bank itself, and
# NOT the required newly rephrased questions using ML (Google Gemini-1.5-Flash in this case).
# This is due to the fact that Gemini API Free usage has restrictions on per day and per day prompts limit.
# Specifically for Gemini-1.5-Flash -> Free Tier: 15 REQUESTS PER MINUTE, 1 MILLION TOKENS PER MINUTE, 1,500 REQUESTS PER DAY
# So using that during development can use up the day's limit before you even notice.
# Hence, THE BELOW GENAI FUNTION USING THE ABOVE MENTIONED FUNCTIONALITY HAS BEEN GREYED OUT.

# Web Link for rate limits for various GenAI Models offered by Google :: https://ai.google.dev/gemini-api/docs/models/gemini#rate-limits

# IMPORTANT :: REMEMBER TO NEVER PUSH THE PRIVATE GEMINI API KEY TO OPEN-SOURCE!!
# If done so, please delete the API key immediately as soon as you realize at any of the below links:
# Web Link for Google AI Studio - API Key Dashboard :: https://aistudio.google.com/app/apikey
# Web Link for Google Cloud Console - API Credentials :: https://console.cloud.google.com/apis/credentials
# ---------------------------------------------------------------------------------------------------


# NOTE FOR DEVELOPERS: Use print(os.environ["GEMINI_API_KEY"]) to
# see the privately stored environment variable "GEMINI_API_KEY" on the deployment machine.


# def GenAIRephraser(question):
#     genai.configure(api_key = os.environ["GEMINI_API_KEY"])
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     if str(question).count(".") > 1:
#         processedQuestion = str(question).split(".", 1)[1].strip()
#     else:
#         processedQuestion = question
#     response = model.generate_content(f'Assume yourself as a university question paper setter: rephrase this question to another similar difficulty question and give me response without the quotation marks: "{processedQuestion}"')
#     sleep(4) # 15 Requests Per Minute means a dealy of atleast 4 seconds between requests.
#     return response.text
