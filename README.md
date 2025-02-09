![AUTOQPGEN_LOGO](https://raw.githubusercontent.com/azuregray/AutoQPGen/main/Assets/AutoQPGen_GitHubSocialMediaCover.png)


# **A U T O &emsp; Q P &emsp; G E N**

#### `DESCRIPTION` &ensp; An Institution-wide Assessment Creation and Management Platform.

### **`SRI KRISHNA INSTITUTE OF TECHNOLOGY`**

> **`Final Year Project 2021 Batch`** 💙

> **Department of AI & ML - Sri Krishna Institute of Technology, Bangalore**
---
## **`SKILLS LEARNT / TECHNOLOGIES USED`**
**`( HTML5 )`** **`( CSS3 )`** **`( JAVASCRIPT )`**  
**`( PYTHON )`** **`( FLASK )`** **`( SECRETS )`**  
**`( DJANGO )`** **`( SQLITE )`** **`( GIT )`**  
**`( GITHUB )`** **`( PIP )`** **`( MARKDOWN )`**  
**`( SHELL SCRIPTING )`** **`( POWERSHELL )`** **`( PYTORCH )`**  
**`( TENSORFLOW )`** **`( PDF RENDERING )`** **`( NLP )`**  
**`( SPACY )`** **`(PDF Structured Extraction)`**

---
## **`DEPLOYMENT & USAGE`**
> 1️⃣ **Step 01**: Please visit the Original Repository [**`AutoQPGen`**](https://github.com/azuregray/AutoQPGen) and find the Green `CODE` button and click on "Download ZIP".  
> or just [**`Click here to download`**](https://github.com/azuregray/AutoQPGen/archive/refs/heads/main.zip).

> 2️⃣ **Step 02**: Extract the downloaded `AutoQPGen-main.zip` file into its folder and open the same.

> 3️⃣ **Step 03**: Once you are in the folder, Install the requirements.  
> To take the help of `requirements.txt`, just run this in Terminal:  
> `Interpreter: PowerShell`
```
python -m pip install -r requirements.txt
```

> 4️⃣ **Step 04**: It is required to have Microsoft Office installed on the server machine that hosts the folder.  
> This is important for question paper functionalities as it uses on-device MSO365 service for all the conversion and substitution functionalities.

> 5️⃣ **Step 05**: Next thing to be focused on is to install the very important NER Model for SpaCy. Just run this in the Terminal:  
> `Interpreter: PowerShell`
```
python -m spacy download en_core_web_sm
```

> 6️⃣ **Step 06**: Once that is successful, finally run `app.py` in Terminal:  
> `Interpreter: PowerShell`
```
python ./app.py
```

> 7️⃣ **Step 07**: After running the command in `Step 06`, please do a `Ctrl + Click` on the localhost URL where the service is being hosted, which is generated in the same terminal windows running `app.py`.  
> For example: `https://127.0.0.1:5000`

---
### **`QUICK TIPS`**
> **`01`** - To quickly setup the entire project to get it ready to RUN FRESH, feel free to invoke readyApp() from kickstarter.py:  
> `Interpreter: PowerShell`
```
python -c "import kickstarter; kickstarter.readyApp()"
```
> **`02`** - To quickly setup the entire project to get it ready to SHARE with Team or GITHUB PUSH, feel free to invoke offloadApp() from kickstarter.py:  
> `Interpreter: PowerShell`
```
python -c "import kickstarter; kickstarter.offloadApp()"
```

---
### **`CRITICAL GUIDELINES FOR QUESTION BANK CREATION`**
> You can find the official Question Bank format that AutoQPGen supports at /Assets/SampleQuestionBanks/Template/

> **`01`** - It is highly recommended that you use the provided Template DOCX file to make new Question Banks.  

> **`02`** - Make sure you have either a period "." or a Closed Paranthesis ")" immediately next to Sl. No. in each row.  

> **`03`** - It is recommended to not have any extra text in between the pages / tables / rows as that may interfere with the data extraction.  

> **`04`** - It is important that CO and Levels column entries are accompanied by prefixes such as "CO" and "L" respectively.  

> **`05`** - You can have as many question as you like per module but just make sure all the entries are filled to avoid unintended errors.  

> **`06`** - Be very cautious to ensure that each question bank has not more than TWO modules.  

> **`07`** - AutoQPGen system gives priority to the Module field in each row rather than the sub-header that is mentioned before each table so make sure that is filled to ensure your question ends up in the right module.  

---
### **`A SMALL NOTE`**
> As for the scope of the project, we have only included only One variant of question paper template in /static/DocxTemplates.

> Any new templates or change in template here may require corresponding changes in /models/DocxDownloader.py and a user-side mechanism for selection of desired Question Paper template out of the available ones at runtime during question bank creation.  

---
## **`FOR RESPECTED CONTRIBUTORS`** 🔰
> Please refer the [**`OFFICIAL GITHUB CONTRIBUTION GUIDE`**](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project) 
---

## **`LINK TO THE ORIGINAL REPOSITORY`** ✅

> **https://github.com/azuregray/AutoQPGen/**

---
