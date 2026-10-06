# 🤖 Nexus ERP: Agentic Accounts Payable Orchestrator

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

An **Intelligent Process Automation (IPA)** system designed to autonomously manage Accounts Payable workflows. Built as a Master's degree project for the Faculty of Computer Applications & Information Technology (FCAIT), this system elevates standard Robotic Process Automation (RPA) by introducing **Agentic AI** behaviors and a **Human-in-the-Loop (HITL)** exception architecture.

## 🌟 Core Architecture & Features

Traditional RPA scripts break when data mismatches occur. Nexus ERP utilizes an "agentic" approach: it processes valid data autonomously and gracefully halts to route anomalies to human managers.

- **Continuous Ingestion Pipeline:** A Python backend continuously polls a designated Gmail inbox using the Gmail API, autonomously identifying and downloading unread vendor invoices.
- **Automated Data Extraction:** Uses `PyPDF2` and RegEx to parse unstructured PDF documents and extract key financial identifiers (Vendor, Invoice ID, Quantities, Unit Price).
- **Strict 3-Way Match Verification:** Queries a local SQLite database to validate the extracted Invoice against existing **Purchase Orders (PO)** and **Goods Received Notes (GRN)**. 
- **Agentic UI Orchestration:** If the 3-Way Match succeeds, a Playwright bot physically takes over the browser, inputs the data into a React ERP dashboard, and commits the record.
- **Human-in-the-Loop (HITL) Alerting:** If a discrepancy is detected (e.g., price mismatch), the agent halts to prevent bad data entry. It triggers an automated SMTP email to the department manager with intervention instructions.
- **Manager Override Interface:** The React frontend dynamically responds to exceptions, locking down standard workflows and presenting a restricted "Manager Override: Force Approve" or "Reject" dashboard.

## 🛠️ Technology Stack

*   **Frontend:** React.js, Vite, CSS3
*   **Backend / RPA Engine:** Python 3, Playwright
*   **Database:** SQLite3
*   **APIs & Libraries:** Google Gmail API (`google-auth`, `google-api-python-client`), `PyPDF2`, `smtplib` (SMTP Email)

## 📂 Project Structure

```text
auto-3way-match/
├── database/
│   └── rpa_database.db          # SQLite Database (PO & GRN records)
├── rpa_backend/
│   ├── main.py                  # Core Agentic Orchestrator
│   ├── ingestion_engine.py      # Gmail API integration
│   ├── extraction_engine.py     # PDF parsing and Regex logic
│   ├── verification_brain.py    # 3-Way Match logic
│   ├── notification_engine.py   # HITL SMTP Alert system
│   └── playwright_bot.py        # Browser automation bot
├── src/                         
│   └── App.jsx                  # React ERP Dashboard with Manager Override UI
├── credentials.json             # Google API Client Secrets (Excluded via .gitignore)
└── README.md
```

## 🚀 Installation & Setup

### 1. Frontend Setup (React)
```bash
# Navigate to project root
npm install
npm run dev
# The React dashboard will launch on http://localhost:5173
```

### 2. Backend Setup (Python)
```bash
# Create and activate virtual environment
python -m venv .venv

# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install playwright PyPDF2 google-api-python-client google-auth-httplib2 google-auth-oauthlib
playwright install
```

### 3. Environment & Security Configuration
1. Obtain an **OAuth 2.0 Client ID** from Google Cloud Console, download it, and save it in the root folder as `credentials.json`.
2. In `rpa_backend/notification_engine.py`, configure your sender email, manager email, and a **16-digit Google App Password**. 
3. *Note: Sensitive tokens and credentials are intentionally excluded from this repository via `.gitignore`.*

## 🧪 Demo Workflow

To demonstrate the system's Agentic capabilities, run the continuous pipeline:
```bash
python rpa_backend/main.py
```

**Scenario A: The Happy Path (Autonomous Entry)**
1. Email `invoice_techsolutions.pdf` ($1,000 Total) to the designated inbox.
2. The agent extracts the data, verifies the 3-way match, opens the browser, logs into the React app, and commits the entry without human intervention.

**Scenario B: Human-in-the-Loop Exception (Manager Override)**
1. Email `invoice_discrepancy.pdf` ($1,200 Total) to the inbox.
2. The verification brain detects the $200 discrepancy.
3. The Playwright bot logs an exception on the UI while `notification_engine.py` immediately emails the manager.
4. The manager reviews the physical PDF, clicks the "Manager Override" button on the React dashboard, and securely forces the commit.

---
**Developed by Khushboo**  
*Contributed by Mahak*  
