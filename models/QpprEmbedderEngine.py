from datetime import datetime
import os
from docxtpl import DocxTemplate
import docx2pdf
import pythoncom

def QpprExport(paperData):
    questionMarkersList = ('id', 'userId', 'paperId', 'status', 'cieNumber', 'departmentName', 'semester', 'courseName', 'electiveChoice', 'date', 'timings', 'courseCode', 'maxMarks', 'mandatoryCount', 'q1a', 'co1a', 'lvl1a', 'marks1a', 'module1a', 'q1b', 'co1b', 'lvl1b', 'marks1b', 'module1b', 'q2a', 'co2a', 'lvl2a', 'marks2a', 'module2a', 'q2b', 'co2b', 'lvl2b', 'marks2b', 'module2b', 'q3a', 'co3a', 'lvl3a', 'marks3a', 'module3a', 'q3b', 'co3b', 'lvl3b', 'marks3b', 'module3b', 'q4a', 'co4a', 'lvl4a', 'marks4a', 'module4a', 'q4b', 'co4b', 'lvl4b', 'marks4b', 'module4b')
    
    paperDataDictionary = dict(zip(questionMarkersList, paperData))
    courseCode = paperDataDictionary['courseCode']
    uniqueNameFactor = paperDataDictionary['paperId']
    
    templatePath = './static/DocxTemplates/QuestionPaperTemplate_10_10.docx'
    questionPaperPreName = courseCode + "__" + uniqueNameFactor + ".docx"
    questionPaperPreOutputPath = './static/GeneratedDocx/' + questionPaperPreName
    questionPaperName = courseCode + "__" + uniqueNameFactor + ".pdf"
    questionPaperOutputPath = './static/GeneratedPapers/' + questionPaperName
    
    doc = DocxTemplate(templatePath)
    context = paperDataDictionary
    doc.render(context)
    doc.save(questionPaperPreOutputPath)
    
    # Ensure COM initialization
    pythoncom.CoInitialize()
    try:
        # Convert DOCX to PDF
        docx2pdf.convert(questionPaperPreOutputPath, questionPaperOutputPath)
    finally:
        pythoncom.CoUninitialize()
    
    if os.path.exists(questionPaperOutputPath):
        print(f"\n\n[EVENT] [{datetime.now().strftime("%B %d, %Y %I:%M:%S %p")}] Question paper {questionPaperName} was generated and saved to folder GeneratedPapers. ")
        print(f"\n\n[EVENT] [{datetime.now().strftime("%B %d, %Y %I:%M:%S %p")}] Hence deleting temporary helper DOCX file: {questionPaperPreName}...")
        os.remove(questionPaperPreOutputPath)
    
    return questionPaperOutputPath
