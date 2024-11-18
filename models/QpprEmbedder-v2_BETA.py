from datetime import datetime
import os
from docxtpl import DocxTemplate
import docx2pdf
from tkinter import filedialog

def QpprExport(paperData):
    questionMarkersList = ('id', 'userId', 'paperId', 'status', 'cieNumber', 'departmentName', 'semester', 'courseName', 'electiveChoice', 'date', 'timings', 'courseCode', 'maxMarks', 'mandatoryCount', 'q1a', 'co1a', 'lvl1a', 'marks1a', 'module1a', 'q1b', 'co1b', 'lvl1b', 'marks1b', 'module1b', 'q2a', 'co2a', 'lvl2a', 'marks2a', 'module2a', 'q2b', 'co2b', 'lvl2b', 'marks2b', 'module2b', 'q3a', 'co3a', 'lvl3a', 'marks3a', 'module3a', 'q3b', 'co3b', 'lvl3b', 'marks3b', 'module3b', 'q4a', 'co4a', 'lvl4a', 'marks4a', 'module4a', 'q4b', 'co4b', 'lvl4b', 'marks4b', 'module4b')
    
    paperDataDictionary = dict(zip(questionMarkersList, paperData))
    filePath = filedialog.askopenfilename()
    doc = DocxTemplate(filePath)
    context = paperDataDictionary
    doc.render(context)
    
    courseCode = paperDataDictionary['courseCode']
    currentTimeCode = datetime.now().strftime("%Y%m%d-%H%M%S")
    questionPaperPreName = courseCode + "__" + currentTimeCode + ".docx"
    questionPaperName = courseCode + "__" + currentTimeCode + ".pdf"
    # questionPaperOutputPath = "./static/GeneratedPapers/" + questionPaperName
    doc.save(questionPaperPreName)
    docx2pdf.convert(questionPaperPreName, questionPaperName)
    
    if os.path.exists(questionPaperName):
        print(f"\n\n[EVENT] [{datetime.now().strftime("%B %d, %Y %I:%M:%S %p")}] Question paper {questionPaperName} was generated and saved to folder GeneratedPapers. ")
        print(f"\n\n[EVENT] [{datetime.now().strftime("%B %d, %Y %I:%M:%S %p")}] Deleting inter-provess helper DOCX file: {questionPaperPreName}")
        os.remove(questionPaperPreName)
    
    # return questionPaperOutputPath
    return questionPaperName


paperData = (1, '7af1e1f279', '0bc60038', 'Paper was created.', '01', 'AIML', 'VI', 'SOFTWARE ENGINEERING & PROJECT MANAGEMENT', 'NO', 'Date', 'Time', '21CS61', '40', 'TWO', 'a. What is object oriented development (OOD)? Explain OOD  briefly.', '1', '2', '10', '1', 'b. How prototyping helps in software development', '1', '3', '10', '1', 'a. Discuss the maintenance aspects of software engineering.', '1', '1', '10', '1', 'b. Name the umbrella activities in software process.', '1', '2', '10', '1', 'a. Which model will work better Prototype or Spiral? Justify with  proper example.', '1', '1', '10', '1', 'b. What is object orientation? What are important characteristics  of OO approach? Explain.', '1', '2', '10', '1', 'a. What are the different stages in classic project life cycle?  Explain?', '2', '2', '10', '2', 'b. A university has decided to engage a software company for the  automation of student result management system of its Mtech  Programme. Develop the following documents which may  provide holistic view of the system.  i. Problem Statement iii. Use case diagram  ii. Context diagram iv. ER diagram', '2', '2', '10', '2')
status = QpprExport(paperData)
print("\nQuestion paper has been successfully exported. Check the output folder.")