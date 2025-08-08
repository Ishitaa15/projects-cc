# projects-cc
AI-Powered File Organization System
AI-Powered File Organizer
A Streamlit web application that connects to your Dropbox account, automatically categorizes files, summarizes text documents, detects duplicates, and visualizes file distribution — all powered by Python, NLP, and AI.

🚀 Features
Dropbox Integration – Securely connects to your Dropbox account to fetch files.
File Categorization – Automatically groups files into categories like Documents, Media, Code, etc.
Text Summarization – Uses spaCy NLP to generate quick summaries of .txt and .docx files.
Duplicate Detection – Finds and lists duplicate files using file hashes.
Data Visualization – Displays file distribution across categories in bar chart format.
Interactive UI – Built with Streamlit for easy, user-friendly interaction.

🛠️ Technologies Used
Python 3.x
Dropbox API
spaCy (en_core_web_sm)
pandas
matplotlib
streamlit
python-docx
chardet

Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
2️⃣ Create a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3️⃣ Install Dependencies

pip install -r requirements.txt
4️⃣ Set Up Dropbox Access Token
Create a .env file in the project root.

Add your Dropbox API token:

DROPBOX_ACCESS_TOKEN=your_access_token_here
⚠ Never commit your access token to GitHub! Keep it in .env and add .env to .gitignore.

5️⃣ Download spaCy Model
bash
Copy
Edit
python -m spacy download en_core_web_sm
6️⃣ Run the App
bash
Copy
Edit
streamlit run app.py
The app will open in your default browser at: http://localhost:8501

📂 Project Structure
├── app.py              # Main Streamlit app
├── requirements.txt    # Dependencies
├── .env                # Environment variables (not committed)
└── README.md           # Project documentation


How It Works
Connects to Dropbox and fetches file metadata.

Categorizes files based on their extensions.

Summarizes text/docx files using NLP.

Finds duplicate files by comparing hashes.

Visualizes file distribution in a bar chart.


Security Notes
Do not expose your Dropbox access token in code.
Always store secrets in .env and keep .env in .gitignore.




👩‍💻 Author
Ishita Tandon
@ishitaa15
