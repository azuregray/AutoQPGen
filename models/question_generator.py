# import google.generativeai as genai
import os, fitz, random
from PyPDF2 import PdfReader

def remove_consecutive_whitespace(word):
    new_word = ""
    charindex = 0
    while charindex < len(word):
        if word[charindex].isspace():
            if charindex + 1 < len(word) and word[charindex + 1].isspace():
                charindex += 1
                continue
        new_word += word[charindex]
        charindex += 1
    
    return new_word

def floatcheck(word):
    processed_word = ''.join(word.split())
    try:
        float_value = float(processed_word)
        return True
    except ValueError:
        return False

def intcheck(word):
    try:
        intvalue = int(word)
        return True
    except ValueError:
        return False

def wordcounter(sentence):
    wordslist = sentence.split()
    return len(wordslist)

def extract_questions_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    pdf_pagecount = pdf_document.page_count

    print("Total number of pages: ", pdf_pagecount)
    print('\n\n')

    rawdata_prefilter = []

    for pagenumber in range(pdf_pagecount):
        print(f"Processing Page 0{pagenumber + 1}\n")
        page = pdf_document.load_page(pagenumber)  # Load the first page
        rawdata_unprocessed_unstripped = page.get_text("text")
        rawdata_processed_unstripped = rawdata_unprocessed_unstripped.split("\n")
        rawdata_stripped = []
        for item in rawdata_processed_unstripped:
            rawdata_stripped.append(item.strip())
        for item in rawdata_stripped:
            rawdata_prefilter.append(item)


    print("\n\nRaw Data Extracted from pages successfully. Now moving on to data preprocessing.\n")
    rawdata = []
    totalsentences = len(rawdata_prefilter)
    sentencecount = 0

    for sentence in rawdata_prefilter:
        sentencecount += 1
        print(f"Processing Word: ({sentencecount}/{totalsentences})")
        if sentence == '':
            continue
        elif sentence == ' ':
            continue
        elif ('SRI' and 'KRISHNA' and 'INSTITUTE' and 'OF' and 'TECHNOLOGY') in sentence:
            continue
        elif sentence.startswith('(') and sentence.endswith(')'):
            continue
        elif sentence == 'Department of Artificial Intelligence and Machine Learning':
            continue
        elif sentence.startswith('#29, Chimney Hills') and sentence.endswith('560090'):
            continue
        elif sentence == 'CO' or sentence == 'Level' or sentence == 'Marks' or sentence == 'SL#' or sentence == 'Question' or sentence == 'Faculty Signature':
            continue
        elif floatcheck(sentence):
            continue
        elif len(sentence) < 2:
            continue
        elif sentence.startswith("Issue") or sentence.startswith("Submission"):
            continue
        elif sentence.startswith("Assignment") and sentence.endswith("Questions"):
            continue
        else:
            filtered_word = remove_consecutive_whitespace(sentence)
            rawdata.append(filtered_word)


    raw_co_data = []
    raw_levels_data = []
    CO_list = []
    Levels_list = []

    subject_name = ""
    semester = ""
    faculty_name = ""
    subject_code = ""

    lines_Discard = []

    lineIndex = 0
    for line in rawdata:
        if line.startswith("CO") or line.startswith("Co") and len(line) == 3:
            raw_co_data.append(line)
            CO_list.append(str(line)[-1])
            lines_Discard.append(lineIndex)
        elif line.startswith("L") and len(line) == 2:
            raw_levels_data.append(line)
            Levels_list.append(str(line)[-1])
            lines_Discard.append(lineIndex)
        elif line.startswith("Subject Name") and ":" in line:
            subject_name = line.split(':')[1].strip().title()
            lines_Discard.append(lineIndex)
        elif line.startswith("SEM") and ":" in line:
            semester = line.split(':')[1].strip()
            lines_Discard.append(lineIndex)
        elif line.startswith("Faculty") and ":" in line:
            faculty_name = line.split(':')[1].strip().title()
            lines_Discard.append(lineIndex)
        elif line.startswith("Subject Code") and ":" in line:
            subject_code = line.split(':')[1].strip()
            lines_Discard.append(lineIndex)
        lineIndex += 1

    for index in sorted(lines_Discard, reverse=True):
        rawdata.pop(index)

    lines_Discard = []
    for lineIndex in range(len(rawdata)):
        if intcheck(rawdata[lineIndex][1]) and rawdata[lineIndex][2] == '.':
            temp = rawdata[lineIndex].split('. ', 1)[1]
            rawdata[lineIndex] = temp
        elif intcheck(line[1]) and intcheck(rawdata[lineIndex][2]) and rawdata[lineIndex][3] == '.':
            temp = rawdata[lineIndex].split(' ', 1)[1]
            rawdata[lineIndex] = temp
        elif not rawdata[lineIndex - 1].endswith(('.','?')):
            temp = rawdata[lineIndex - 1] + " " + rawdata[lineIndex]
            rawdata[lineIndex-1] = temp
            lines_Discard.append(lineIndex)
        elif rawdata[lineIndex].startswith('i') and rawdata[lineIndex][1] == ".":
            temp = rawdata[lineIndex - 1] + " " + rawdata[lineIndex]
            rawdata[lineIndex-1] = temp
            lines_Discard.append(lineIndex)
        elif rawdata[lineIndex].startswith('i') and rawdata[lineIndex][2] == ".":
            temp = rawdata[lineIndex - 1] + " " + rawdata[lineIndex]
            rawdata[lineIndex-1] = temp
            lines_Discard.append(lineIndex)
        elif rawdata[lineIndex].startswith('i') and rawdata[lineIndex][3] == ".":
            temp = rawdata[lineIndex - 1] + " " + rawdata[lineIndex]
            rawdata[lineIndex-1] = temp
            lines_Discard.append(lineIndex)
        elif wordcounter(rawdata[lineIndex]) == 1:
            temp = rawdata[lineIndex - 1] + " " + rawdata[lineIndex]
            rawdata[lineIndex-1] = temp
            lines_Discard.append(lineIndex)
        lineIndex += 1

    for index in sorted(lines_Discard, reverse=True):
        rawdata.pop(index)
    
    questions_count = len(rawdata)
    
    rawdata_length_half = int(len(rawdata)/2)
    questions_first_half = rawdata[:rawdata_length_half]
    questions_second_half = rawdata[rawdata_length_half:]
    co_first_half = CO_list[:int(len(CO_list)/2)]
    co_second_half = CO_list[int(len(CO_list)/2):]
    levels_first_half = Levels_list[:int(len(Levels_list)/2)]
    levels_second_half = Levels_list[int(len(Levels_list)/2):]
    
    shuffled_questions_first_half = []
    shuffled_co_first_half = []
    shuffled_levels_first_half = []
    shuffled_questions_second_half = []
    shuffled_co_second_half = []
    shuffled_levels_second_half = []
    
    # shuffled_first_half.extend(random.sample(questions_first_half, 4))
    # shuffled_second_half.extend(random.sample(questions_second_half, 4))
    while True:
        try:
            for _ in range(4):
                random_i = random.randint(0, rawdata_length_half)
                shuffled_questions_first_half.append(questions_first_half[random_i])
                shuffled_questions_second_half.append(questions_second_half[random_i])
                shuffled_co_first_half.append(co_first_half[random_i])
                shuffled_co_second_half.append(co_second_half[random_i])
                shuffled_levels_first_half.append(levels_first_half[random_i])
                shuffled_levels_second_half.append(levels_second_half[random_i])
            break
        except IndexError as e:
            print(f"Error occured while SHUFFLING QUESTIONS: {e}... Retrying...")
    
    final_8questions = shuffled_questions_first_half + shuffled_questions_second_half
    final_8co_list = shuffled_co_first_half + shuffled_co_second_half
    final_8levels_list = shuffled_levels_first_half + shuffled_levels_second_half
    
    return {key: value for key, value in locals().items() if key in ['faculty_name', 'subject_name', 'subject_code', 'semester', 'final_8questions', 'final_8co_list', 'final_8levels_list']}


# WARNING ----------------------- 
# This question_generator.py will now return pure data extracted from the input Question Bank itself, and
# NOT the required newly rephrased questions using ML (Gemini-Pro in this case).
# This is due to the fact that Gemini API free usage has restrictions on daily prompts limit.
# So using that during development can use up the day's limit before you even notice.
# Hence, THE BELOW GENAI FUNTION USING THE ABOVE MENTIONED FUNCTIONALITY HAS BEEN GREYED OUT.

# IMPORTANT :: REMEMBER TO NEVER PUSH THE PRIVATE GEMINI API KEY TO OPEN-SOURCE!!
# If done so, please delete the API key immediately as soon as you realize at any of the below links:
# Web Link for Google AI Studio - API Key Dashboard :: https://aistudio.google.com/app/apikey
# Web Link for Google Cloud Console - API Credentials :: https://console.cloud.google.com/apis/credentials
#---------------------------------------------------------------------------------------------------


# NOTE FOR DEVELOPERS: Use print(os.environ["GEMINI_API_KEY"]) to
# see the privately stored environment variable "GEMINI_API_KEY" on the deployment machine.


# def generate_new_questions(pdf_path):
#     question_bank = extract_questions_from_pdf(pdf_path)
#     if not question_bank:
#         return []
    
#     genai.configure(api_key = os.environ["GEMINI_API_KEY"])
#     model = genai.GenerativeModel('gemini-pro')
#     new_questions = []
#     for question in question_bank:
#         if str(question).count(".") > 1:
#             processed_question = str(question).split(".", 1)[1].strip()
#         else:
#             processed_question = question
        
#         response = model.generate_content(f'Just give me on point answer: rephrase the question to another same kind of question without the quotation marks: "{question}"')
#         new_questions.append(response.text)

#     return new_questions
