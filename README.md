# Intelligent Invoice Processing & Automated Three-Way Matching System 🧾🤖

An end-to-end, Agentic AI-driven RPA pipeline designed to eliminate manual data entry in Accounts Payable operations. This system securely scans live emails, intelligently extracts unstructured PDF data, performs strict database validations, and autonomously drives a web ERP interface.

The system utilizes a **Closed-Loop RPA** architecture powered by **Python**, **Playwright**, **pdfplumber**, and **Google Workspace APIs**, featuring a localized **SQLite Verification Brain** and a responsive **React (Vite)** mock ERP frontend.

---

## 🌟 Key Features

* **Live Ingestion via Gmail API:** Secure OAuth 2.0 integration for real-time document fetching directly from a live inbox.
* **Intelligent Document Parsing:** `pdfplumber` and Regex-powered extraction engine for unstructured text, financial figures, and temporal data.
* **Three-Way Match Verification Brain:** Localized SQLite rules engine that strictly validates exact quantities, pricing, and chronological dates across Purchase Orders (POs) and Goods Received Notes (GRNs).
* **Headless Web RPA:** Playwright browser automation for hands-free, error-free data entry into the target ERP dashboard.
* **Proactive Exception Handling:** Automated rules engine that halts the pipeline and flags discrepancies (e.g., date mismatches, overbilling) to prevent financial errors.
* **Real-Time Analytics Dashboard:** A React frontend that dynamically tracks successful entries, total monetary value logged, and caught exceptions.

---

## 🏗️ Tech Stack & Architecture

### **Backend (RPA Pipeline)**
* **Framework:** Python (3.8+)
* **Browser Automation:** Playwright
* **Document Extraction:** `pdfplumber`, Regex
* **API Integrations:** Google Client Library (`google-auth`, `gmail-api`)
* **Database:** SQLite3 (Local Verification Brain)
* **Document Generation:** `reportlab` (for mock testing)

### **Frontend (Target ERP)**
* **Framework:** React.js (Vite)
* **Styling:** CSS3 (Dashboard layout & Analytics panel)

---

## 📁 Repository Structure

```text
auto-3way-match/
├── rpa_backend/
│   ├── main.py                   # Master orchestrator script
│   ├── ingestion_engine.py       # Gmail API & PDF downloading logic
│   ├── extraction_engine.py      # pdfplumber parsing rules
│   ├── exception_engine.py       # Discrepancy flagging logic
│   └── requirements.txt          # Python dependencies
├── mock-erp-system/              # Target React ERP Interface
│   ├── src/
│   │   ├── App.jsx               # Main React dashboard & logic
│   │   └── App.css               # Dashboard styling
│   ├── package.json
│   └── vite.config.js
├── database/                     # SQLite Verification Brain
│   ├── db_setup.py               # DB initialization and seeding script
│   └── company_records.db        # Seeded POs and GRNs
├── data/                         
│   └── raw_invoices/             # Local storage for downloaded PDFs
├── generate_test_pdf.py          # Script to generate mock PDFs for testing
├── .gitignore                    # Security exclusions
└── README.md

---

## 🚀 Quick Start Guide

### 📋 Prerequisites

Before running the project, make sure you have the following installed:

- **Python**: v3.8 or higher
- **Node.js**: v18.0 or higher
- **Git**
- A **Google Cloud account** (for Gmail API access)

---

### 1️⃣ Setting Up the Backend (Python RPA)

**Step 1: Navigate to the Root Directory**
```bash
cd auto-3way-match
```

**Step 2: Create and Activate a Virtual Environment**

*Windows (PowerShell)*
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

*macOS/Linux*
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r rpa_backend/requirements.txt
```

**Step 4: Install Playwright Binaries**
```bash
playwright install
```

**Step 5: Configure Google API Credentials**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Gmail API**.
3. Create **OAuth 2.0 Client IDs** (Select "Desktop App").
4. Download the generated credentials JSON file, rename it exactly to `credentials.json`, and place it in the root folder.

**Step 6: Initialize Database & Generate Test Data**
```bash
python database/db_setup.py
python generate_test_pdf.py
```

---

### 2️⃣ Setting Up the Frontend (React ERP)

**Step 1: Navigate to the Frontend Directory**

Open a **new terminal** and run:
```bash
cd mock-erp-system
```

**Step 2: Install Dependencies**
```bash
npm install
```

**Step 3: Start the React Development Server**
```bash
npm run dev
```

The mock ERP frontend will run at:
- **Vite Server:** http://localhost:5173

## 👥 Authors & Contributors

* **Khushboo Yadav** – *System Architecture, RPA Pipeline Development, Database Rules Engine, & React Frontend Design*
* **Mahak Maheshwari** – *Contributor*

---

## 🏫 Academic Details

* **University:** GLS University (Faculty of Computer Applications & Information Technology - FCAIT)
* **Degree:** Master of Science in Information Technology (MSc IT)
* **Focus Area:** Robotic Process Automation (RPA) & Agentic AI