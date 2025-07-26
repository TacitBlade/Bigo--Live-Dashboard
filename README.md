# 📊 Bigo Live Dashboard

A Streamlit-based analytics and management dashboard for Bigo Live agencies. This tool integrates with Google Sheets and AWS, enabling real-time data visualization, performance tracking, and automated paysheet generation for hosts and managers.

---

## 🚀 Features

- 🔐 **Host & Admin Authentication**
- 📈 **Performance Calculators**
  - Beans ➜ Diamonds
  - PK Stats & Targets
- 📝 **Automated Paysheet Generator**
- 📊 **Google Sheets Integration**
- 🎥 **Training Resource Viewer**
- 🧾 **Customizable Agency Settings**
- ☁️ **One-click AWS Deployment**

---

## 🗂 Project Structure

bigo-live-dashboard/
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── google_credentials.json # Google Service Account credentials (ignored by Git)
├── config/ # App and AWS configuration
├── utils/ # Auth, calculators, paysheet, GSheets logic
├── templates/ # Training videos, PDFs
├── static/ # CSS styles
├── scripts/ # AWS deployment script
└── README.md # Project documentation


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/bigo-live-dashboard.git
cd bigo-live-dashboard

### 2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Google Sheets API

Create a Google Service Account.

Share the relevant Google Sheet(s) with the service account email.

Download the credentials file and save it as google_credentials.json (already ignored by Git).

### 5. Run the App

streamlit run app.py

☁️ Deployment (AWS)

bash scripts/deploy_aws.sh

📘 Customization
Styling: Modify static/styles.css for branding.

Videos: Add your training resources to templates/video_links.json.

Pay Logic: Update utils/paysheet.py as per your agency’s payout rules.

📄 License
This project is for private use within Bigo agencies. Not for public distribution without permission.

👤 Authors
Your Tacitblade-Developer & Project Owner


🧠 Want help building more?

We're working on:

Mobile version (React Native or Flutter)

AI-based host performance prediction

Smart scheduling & reminders

Let us know what features you need!


---

Would you like me to customize the author/links, or generate badges (e.g., Python version, license, etc.)?


