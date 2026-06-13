# 💍 NF QueryGPT 

> Generative Semantic Data Mesh & Business Intelligence Assistant for NikahForever.

NF QueryGPT is an AI-powered conversational data analytics assistant that translates plain English and conversational Hinglish prompts into optimized, secure SQLite queries. It abstracts database complexity for non-technical managers, enabling direct data extraction through an enterprise-grade executive dashboard interface.

![NF QueryGPT License](https://img.shields.io/badge/Security-Strict%20Read--Only-0ea5e9?style=flat-square)
![Streamlit App](https://img.shields.io/badge/Deployment-Streamlit%20Cloud-38bdf8?style=flat-square)
![Model](https://img.shields.io/badge/Engine-Gemini%202.5%20Flash-01406d?style=flat-square)

---

## 🚀 Core Value Proposition

In fast-paced platforms like NikahForever, everyday business questions (e.g., *"How many premium users registered from Delhi this week?"*) frequently stall in data engineering backlogs. **NF QueryGPT** resolves this bottleneck by turning plain text inputs into clear tabular data, visual distributions, and exportable reports in seconds.

### Why Relational DB over NoSQL (e.g., Firebase)?
During development, a key architectural decision was made to lean heavily on an explicit relational data schema over NoSQL collection models:
* **Complex Multi-Table Joins:** The NikahForever dataset spans **12 distinct tables** (User demographic metrics, subscription plans, matching matrix states, verification records, etc.). Fetching across these via NoSQL requires highly complex client-side code or denormalization redundancy.
* **Semantic Join Mapping:** SQL foreign keys provide a highly structural logical map. This maps seamlessly to LLM attention mechanisms, enabling highly accurate query compilation across deep generational histories.

---

## ✨ Features

- **🗣️ Natural Hinglish Processing:** Understands localized colloquial phrases out of the box (e.g., mapping words like *umra* to age, *sheher* to city, *ladka/ladki* to gender column structures).
- **🔒 Sandbox Shield Security:** Enforces strict execution safety. Any destructive DDL/DML tokens (such as `DROP`, `DELETE`, `INSERT`, `UPDATE`) are caught immediately by regular expression token check interceptors before hitting the connection.
- **🔄 Autonomous Self-Healing:** If a generated query fails due to a schema mismatch or minor syntax variant, a background repair loop catches the error log, compares it against the table schemas, and automatically deploys a corrected query without crashing the UI.
- **🧠 Multi-Turn Conversational Context:** Tracks past queries within the session state, allowing users to ask natural follow-up questions (e.g., Query 1: *"Show me users in Delhi."* $\rightarrow$ Query 2: *"How many of them are premium?"*).
- **📉 Visual Report Compilations:** Automatically shifts presentation layouts based on data shape—rendering numbers as metric cards, segments as categorical charts, or complex indices as interactive dataframes with one-click CSV exporting.

---

## 🛠️ System Architecture Diagram

[ Unstructured Text / Hinglish Prompt ]
                     │
                     ▼
      [ Conversational History Stack ]
                     │
                     ▼
     [ Gemini 2.5 Flash Generator Node ]
                     │
                     ▼
    [ String Tokenization Guardrail Shield ]
    (Blocks ALTER, DROP, DELETE, INSERT)
                     │
                     ▼
   [ Read-Only Database Connection URI ] ---> (On Error: Self-Healing Loop)
                     │
                     ▼
  [ Streamlit Visual Interface Layer ] 
  (Tabular Dataframes, Bar Charts, CSV Exports)

---

## 📂 Project Structure

```text
├── app.py              # Main Streamlit UI panel & state manager
├── ai_engine.py        # Gemini interaction layers & autonomous self-healing engines
├── database.py         # Secure read-only SQLite connectivity & regex validation rules
├── schema.sql          # Structural table constraints & foreign key definitions
├── logo.png            # Premium dashboard identity asset
└── requirements.txt    # Runtime Python dependency index

