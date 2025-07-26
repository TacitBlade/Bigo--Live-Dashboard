# 📊 Bigo Live Dashboard

A comprehensive dashboard for managing Bigo Live PK matches, schedules, and host payments.

## 🚀 Features

### 📈 PK Viewer (`pages/1-PK_viewer.py`)
- **Multi-sheet data integration** from Google Sheets
- **Real-time filtering** by date, agency, and search terms
- **Quick date filters** (Today, This Week, All)
- **Visual highlighting** for same-agency matches
- **Excel export** functionality
- **Responsive data loading** with error handling

### 📅 Schedule Management (`pages/2_Schedule.py`)
- **Weekly PK schedule** overview
- **Host and day filtering** options
- **Color-coded event types** (Talent, Family, Agency, Group)
- **Performance statistics** and metrics
- **Schedule export** to CSV
- **Dynamic schedule data** with realistic events

### 💰 Payment Calculator (`pages/3_Pay.py`)
- **Automated payment calculations** based on:
  - PK wins and performance
  - Streaming hours
  - Beans earned
  - Agency tier multipliers
  - Win rate bonuses
- **Interactive payment settings** via sidebar
- **Visual payment breakdown** and analysis
- **Top performer highlighting**
- **Export functionality** for reports

## 🛠️ Recent Fixes & Improvements

### ✅ Critical Issues Resolved
1. **Undefined Variable Fix**: Fixed `filtered_df` error in PK viewer page
2. **Auto-refresh Logic**: Improved refresh mechanism to prevent infinite loops
3. **Error Handling**: Enhanced Google Sheets connectivity with better error messages
4. **Type Safety**: Added type hints and improved pandas operations
5. **Configuration**: Fixed CORS and security settings in Streamlit config

### 🔧 Infrastructure Improvements
- **Python Environment**: Configured virtual environment properly
- **Dependencies**: Updated and installed all required packages
- **Code Structure**: Improved modularity and error handling
- **UI/UX**: Enhanced visual styling and user feedback

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/TacitBlade/Bigo--Live-Dashboard.git
cd Bigo--Live-Dashboard
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📊 Google Sheets Integration

### Sheet URLs Configuration
Update the `sheet_urls` dictionary in both `app.py` and `pages/1-PK_viewer.py`:

```python
sheet_urls = {
    "Sheet 1": "your_google_sheet_url_1",
    "Sheet 2": "your_google_sheet_url_2", 
    "Sheet 3": "your_google_sheet_url_3",
}
```

### Required Column Names
Ensure your Google Sheets contain these columns:
- `Date`
- `Time`
- `Agency Name.1`
- `ID1`
- `Agency Name.2`
- `ID.2`

### Sheet Permissions
- Make sure sheets are publicly accessible or configure authentication
- Use the "Anyone with the link can view" sharing setting

## 🎨 Configuration Options

### Streamlit Configuration (`.streamlit/config.toml`)
```toml
[theme]
base="light"

[server]
headless = true
enableCORS = true
enableXsrfProtection = true

[client]
showSidebarNavigation = true
```

### Payment Calculator Settings
Adjust payment parameters in the sidebar:
- Agency tier multipliers (Platinum, Gold, Silver)
- Base win bonus and hourly rates
- Beans conversion rates
- Win rate bonus thresholds
  - Beans ➜ Diamonds
  - PK Stats & Targets
- 📝 **Automated Paysheet Generator**
- 📊 **Google Sheets Integration**
- 🎥 **Training Resource Viewer**
- 🧾 **Customizable Agency Settings**
- ☁️ **One-click AWS Deployment**

---

## 🗂 Project Structure

```
bigo-live-dashboard/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── google_credentials.json # Google Service Account credentials (ignored by Git)
├── config/                 # App and AWS configuration
├── utils/                  # Auth, calculators, paysheet, GSheets logic
├── templates/              # Training videos, PDFs
├── static/                 # CSS styles
├── scripts/                # AWS deployment script
└── README.md              # Project documentation
```
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


