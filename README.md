![AUTOQPGEN_LOGO](https://raw.githubusercontent.com/azuregray/AutoQPGen/main/Assets/AutoQPGen_GitHubSocialMediaCover.png)


# **A U T O &emsp; Q P &emsp; G E N**</p>

![SKIT EMBLEM](https://raw.githubusercontent.com/azuregray/AutoQPGen/main/Assets/SKIT_Emblem.jpg)

### **`SRI KRISHNA INSTITUTE OF TECHNOLOGY`**

#### `DESCRIPTION` &ensp; An Institution-wide Automation-driven Assessment Creation and Management Platform.

#### `PROJECT DURATION` &ensp; June 2024 - November 2024 (5 Months)

> **`Final Year Project 2021 Batch`** 💙

> **Department of AI & ML - Sri Krishna Institute of Technology, Bangalore**

> **`1KT21AI014` D A R S H A N &ensp; S &ensp; `TEAM LEADER` >> [**`GITHUB`**](https://github.com/azuregray/) | [**`LINKEDIN`**](https://linkedin.com/in/arcticblue)**

> **`1KT21AI011` C H E T H A N &ensp; G O W D A &ensp; M &ensp; V >> [**`GITHUB`**](https://github.com/chethangowdamv) | [**`LINKEDIN`**](https://www.linkedin.com/in/chethan-gowda-m-v-98a2a0229)**

> **`1KT21AI013` D A N U S H &ensp; V >> [**`GITHUB`**](https://github.com/thedynamics) | [**`LINKEDIN`**](https://www.linkedin.com/in/masterofseas)**

---
## **`SKILLS LEARNT / TECHNOLOGIES USED`**
**`( HTML5 )`** **`( CSS3 )`** **`( JAVASCRIPT )`**  
**`( PYTHON )`** **`( FLASK )`** **`( SECRETS )`**  
**`( DJANGO )`** **`( SQLITE )`** **`( GIT )`**  
**`( GITHUB )`** **`( PIP )`** **`( MARKDOWN )`**  
**`( SHELL SCRIPTING )`** **`( POWERSHELL )`** **`( PYTORCH )`**  
**`( TENSORFLOW )`** **`( PDF RENDERING )`** **`( NLP )`**  
**`( SPACY )`**

---
## **`DEPLOYMENT & USAGE`**
> 1️⃣ **Step 01**: Please visit the Original Repository [**`AutoQPGen`**](https://github.com/azuregray/AutoQPGen) and find the Green `CODE` button and click on "Downlaoad ZIP".  
> or just [**`Click here to download`**](https://github.com/azuregray/AutoQPGen/archive/refs/heads/main.zip).

> 2️⃣ **Step 02**: Extract the downloaded `AutoQPGen-main.zip` file into its folder and open the same.

> 3️⃣ **Step 03**: Once you are in the repo folder, Install the requirements.  
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
### **`DEPENDENCY ISSUE`**
> We have noticed that there is a general bug in PyMuPDF library which can give the following error: `Attribute Error : fitz has no attribute open()`. If you faced the same, please do not panic!  
> Since fitz is just a wrapper for PyMuPDF library, this error can be fixed easily by force-reinstalling PyMuPDF with the following command in your Terminal:  
> `Interpreter: PowerShell`
```
python -m pip install --force-reinstall pymupdf
```
> Refer [PyMuPDF/issues](https://github.com/pymupdf/PyMuPDF/issues/660) for more information on the same.
---
### **`QUICK TIPS`**
> **`01`** - To quickly setup the entire project to get it ready to RUN FRESH, feel free to invoke resetApp() from kickstarter.py:  
> `Interpreter: PowerShell`
```
python -c "import kickstarter; kickstarter.resetApp()"
```
> **`02`** - To quickly setup the entire project to get it ready to SHARE with Team or GITHUB PUSH, feel free to invoke unsetApp() from kickstarter.py:  
> `Interpreter: PowerShell`
```
python -c "import kickstarter; kickstarter.unsetApp()"
```
---
## **`FOR RESPECTED CONTRIBUTORS`** 🔰
> Please refer the [**`OFFICIAL GITHUB CONTRIBUTION GUIDE`**](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project) 
---

## **`LINK TO THE ORIGINAL REPOSITORY`** ✅

> **https://github.com/azuregray/AutoQPGen/**

---
