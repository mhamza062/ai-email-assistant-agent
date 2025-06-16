# 📬 AI Gmail Assistant (Python + Gemini API)

This AI-powered assistant:
- Reads your unread Gmail messages
- Classifies them (like Urgent, Spam, Personal, etc.)
- Writes polite and smart replies using Gemini AI
- Saves replies as Gmail drafts — ready for you to send!

---

## 📦 Files in the Project

├── app.py # Main working code
├── requirements.txt # Python libraries
├── .env # Your Gemini API key (keep secret)
├── client_secret.json # Your Gmail API credentials (keep secret)
├── README.md # This file


---

## ✅ How to Use

### 1. Clone this project

```bash
git clone https://github.com/yourusername/ai-gmail-assistant.git
cd ai-gmail-assistant
```
### 2. Get Your Gmail API Key
Go to Google Cloud Console

Create new project

Enable Gmail API

Go to Credentials → Create OAuth client ID

Download the client_secret.json file

Put it in your project folder
### 3. Get Gemini API Key
Go to https://makersuite.google.com/app/apikey

Copy your key

Create a file named .env and paste:
GEMINI_API_KEY=your_key_here

### 4. Install Required Libraries
pip install -r requirements.txt

### 5. Run the App
python app.py

First time, it will ask you to open a link and paste a code from Google.

It will then fetch 5 unread emails, classify them, write replies, and save drafts.

🔐 Important Notes
Don’t upload .env or client_secret.json to GitHub.

Use .gitignore to keep them private.

🚀 Deployment Tips
Platform	Free	Auto Restart	Notes
Replit	✅	❌ (manual restart)	Easy to use for testing
Railway	⚠️	✅	Limited free usage
Google VM	⚠️	✅	Good for long-term

For learning or demo, Replit is easiest.
