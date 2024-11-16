import pdfkit
import datetime

def QpprEmbedder(paperData):
    id, userId, paperId, status, cieNumber, departmentName, semester, courseName, electiveChoice, date, timings, courseCode, maxMarks, mandatoryCount, q1a, co1a, lvl1a, marks1a, module1a, q1b, co1b, lvl1b, marks1b, module1b, q2a, co2a, lvl2a, marks2a, module2a, q2b, co2b, lvl2b, marks2b, module2b, q3a, co3a, lvl3a, marks3a, module3a, q3b, co3b, lvl3b, marks3b, module3b, q4a, co4a, lvl4a, marks4a, module4a, q4b, co4b, lvl4b, marks4b, module4b = paperData
    html_table = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exam Paper</title>
        <style>
            body {{
                font-family: "Times New Roman", sans-serif;
                padding: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                border: 1px solid black;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
                border: 1px solid black;
            }}
            .cie-header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header {{
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .header img {{
                width: 100px;
                margin-right: 20px;
            }}
            .header-text {{
                text-align: center;
            }}
            .header-text h1 {{
                margin: 0;
                font-family: 'Times New Roman', Times, serif;
                font-size: 24px;
                font-weight: bold;
            }}
            #p1 {{
                font-family: 'Times New Roman';
                font-size: xx-small;
                margin: 5px 0;
            }}
            #p2 {{
                font-family: 'Times New Roman';
                font-size: small;
                margin: 5px 0;
            }}
            hr {{
                border: 1px solid black;
                width: 100%;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div style="display:flex; align-items:center; justify-content:center; padding:20px; text-align:center; flex-direction:row;">
            <img src="data:image/png;base64,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" style="width: 100px; margin-right: 20px;" alt="SKIT Logo">
            <div style="margin: 5px 0;">
                <h1 style="margin: 0; font-family: 'Times New Roman', Times, serif; font-size: 32px; font-weight: bold;">SRI KRISHNA INSTITUTE OF TECHNOLOGY</h1>
                <p style="font-family: 'Times New Roman'; font-size: x-small; margin: 5px 0;">(Accredited by NAAC, Approved by A.I.C.T.E., New Delhi, Recognised by Govt. of Karnataka & Affiliated to V T U, Belagavi)</p>
                <p style="font-family: 'Times New Roman'; font-size: medium; margin: 5px 0;">#29, Chimney Hills, Hesaraghatta Main Road, Chikkabanavara Post, Bengaluru - 560090</p>
            </div>
        </div>
        <hr>
        <div class="cie-header">
            <h2 style="text-align:center;">IA - {cieNumber}</h2>
        </div>
        <table>
            <tr>
                <td colspan="2">Dept: {departmentName}</td>
                <td>Sem / Div: {semester}</td>
                <td colspan="2">Course: {courseName}</td>
                <td>Elective: {electiveChoice}</td>
            </tr>
            <tr>
                <td colspan="2">Date: {date}</td>
                <td>Timings: {timings}</td>
                <td colspan="2">C Code: {courseCode}</td>
                <td>Max Marks: {maxMarks}</td>
            </tr>
            <tr>
                <td colspan="6" style="font-weight: bold; text-align: center">Note: Answer ANY {mandatoryCount} full questions. All questions carry 20 marks.</td>
            </tr>
            <tr class="column_headers">
                <td style="text-align:center; font-weight: bold;">QNo.</td>
                <td style="text-align:center; font-weight: bold;">Questions</td>
                <td style="text-align:center; font-weight: bold;">CO</td>
                <td style="text-align:center; font-weight: bold;">Level</td>
                <td style="text-align:center; font-weight: bold;">Marks</td>
                <td style="text-align:center; font-weight: bold;">Module</td>
            </tr>
            <tr>
                <td rowspan="2" style="text-align:center;">1</td>
                <td>{q1a}</td>
                <td style="text-align:center;">{co1a}</td>
                <td style="text-align:center;">{lvl1a}</td>
                <td style="text-align:center;">{marks1a}</td>
                <td style="text-align:center;">{module1a}</td>
            </tr>
            <tr>
                <td>{q1b}</td>
                <td style="text-align:center;">{co1b}</td>
                <td style="text-align:center;">{lvl1b}</td>
                <td style="text-align:center;">{marks1b}</td>
                <td style="text-align:center;">{module1b}</td>
            </tr>
            <tr>
                <td style="text-align:center; font-weight: bold;" colspan="5">OR</td>
            </tr>
            <tr>
                <td rowspan="2" style="text-align:center;">2</td>
                <td>{q2a}</td>
                <td style="text-align:center;">{co2a}</td>
                <td style="text-align:center;">{lvl2a}</td>
                <td style="text-align:center;">{marks2a}</td>
                <td style="text-align:center;">{module2a}</td>
            </tr>
            <tr>
                <td>{q2b}</td>
                <td style="text-align:center;">{co2b}</td>
                <td style="text-align:center;">{lvl2b}</td>
                <td style="text-align:center;">{marks2b}</td>
                <td style="text-align:center;">{module2b}</td>
            </tr>
            <tr>
                <td colspan="6"></td>
            </tr>
            <tr>
                <td rowspan="2" style="text-align:center;">3</td>
                <td>{q3a}</td>
                <td style="text-align:center;">{co3a}</td>
                <td style="text-align:center;">{lvl3a}</td>
                <td style="text-align:center;">{marks3a}</td>
                <td style="text-align:center;">{module3a}</td>
            </tr>
            <tr>
                <td>{q3b}</td>
                <td style="text-align:center;">{co3b}</td>
                <td style="text-align:center;">{lvl3b}</td>
                <td style="text-align:center;">{marks3b}</td>
                <td style="text-align:center;">{module3b}</td>
            </tr>
            <tr>
                <td style="text-align:center; font-weight: bold;" colspan="5">OR</td>
            </tr>
            <tr>
                <td rowspan="2" style="text-align:center;">4</td>
                <td>{q4a}</td>
                <td style="text-align:center;">{co4a}</td>
                <td style="text-align:center;">{lvl4a}</td>
                <td style="text-align:center;">{marks4a}</td>
                <td style="text-align:center;">{module4a}</td>
            </tr>
            <tr>
                <td>{q4b}</td>
                <td style="text-align:center;">{co4b}</td>
                <td style="text-align:center;">{lvl4b}</td>
                <td style="text-align:center;">{marks4b}</td>
                <td style="text-align:center;">{module4b}</td>
            </tr>
        </table>
    </body>
    </html>
    '''
    
    currentTimeCode = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    table_op_path = "./static/GeneratedPapers/" + courseCode + "__" + currentTimeCode + ".pdf"

    options = {
        'page-size': 'A4',
        'margin-top': '10mm',    # Adjust margins
        'margin-right': '5mm',
        'margin-bottom': '10mm',
        'margin-left': '5mm'
    }

    pdfkit.from_string(html_table, table_op_path, options=options)

    print("\nQuestion paper save successful.\n")
    
    return table_op_path