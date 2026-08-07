# Intelligent Invoice Processing & Automated Three-Way Matching System

An end-to-end, Agentic AI-driven RPA pipeline designed to eliminate manual data entry in Accounts Payable operations. This system securely scans live emails, intelligently extracts unstructured PDF data, performs strict database validations, and autonomously drives a web ERP interface.

## 🚀 Key Features
* **Live Ingestion:** Secure OAuth 2.0 integration with the Gmail API for real-time document fetching.
* **Intelligent Parsing:** `pdfplumber` and Regex-powered extraction engine for unstructured text and temporal data.
* **Verification Brain:** Localized SQLite rules engine validating exact quantities, pricing, and chronological dates across Purchase Orders (POs) and Goods Received Notes (GRNs).
* **Headless Web RPA:** Playwright browser automation for hands-free ERP data entry.
* **Proactive Exception Handling:** Automated SMTP alerts halt the pipeline and flag discrepancies to prevent overbilling.

## 🧠 System Architecture

```mermaid
graph TD
    A[Gmail Inbox] -->|Live OAuth Ingestion| B(pdfplumber & Regex Engine)
    B --> C{Three-Way Match Verification}
    C -->|Check PO & GRN| D[(SQLite Database)]
    C -->|Match Success| E[Playwright ERP Entry]
    C -->|Discrepancy Detected| F[SMTP Exception Alert]