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

# 🗺️ System Architecture Design | NF QueryGPT

This document outlines the end-to-end structural flow, data boundary routing, and multi-agent loops designed and implemented for **NF QueryGPT** during the *Build With Trae* hackathon.

---

## 🏗️ Architectural Topology Diagram

```text
    ┌────────────────────────────────────────────────────────┐
    │              USER INTERACTION LAYER (UI)               │
    │  [ Streamlit Desktop Console ]                         │
    │   ├── Multi-Turn Chat Console & Search Frame           │
    │   └── Live Executive KPI Cards (Pandas Local Cache)    │
    └───────────────────────────┬────────────────────────────┘
                                │
                        (Natural Input)
                                │
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │               CONTEXT & INFERENCE MESH                 │
    │  [ Gemini 2.5 Flash Generator Node ]                   │
    │   ├── Session State Memory Stack (Last 3 Conversations) │
    │   └── Schema Registry Context Injection (schema.sql)   │
    └───────────────────────────┬────────────────────────────┘
                                │
                        (Compiled SQL String)
                                │
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │              SECURITY & ISOLATION SHIELD               │
    │  [ Native Tokenization Guardrail Interceptor ]         │
    │   └── Regex Scanner (Blocks DROP, ALTER, DELETE, etc.)  │
    └───────────────────────────┬────────────────────────────┘
                                │
                      (Verified Safe Query)
                                │
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │                DATA METRIC COMPUTATION                 │
    │  [ SQLite Core Storage Engine Layer ]                  │
    │   └── Locked Storage Driver URI Connection (mode=ro)   │
    └───────────────────────────┬────────────────────────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
          (On SQL Success)             (On Engine Error)
                  │                           │
                  ▼                           ▼
    ┌───────────────────────────┐ ┌───────────────────────────┐
    │     DATA SHAPE ROUTER     │ │   AGENT SELF-HEALING LOOP │
    │ [ Pandas Matrix Processing│ │ [ ai_engine.py / Trae Map]│
    │   ├── Metric Callout Card │ │  ├── Intercept Error Msg  │
    │   ├── Grouped Bar Chart   │ │  ├── Cross-Reference Schema│
    │   └── Downloadable CSV    │ │  └── Emit Patched Query   │
    └───────────────────────────┘ └─────────────┬─────────────┘
                                                │
                                                └─(Re-inject to Data)──┘
```

---

## 📂 Project Structure

```text
├── app.py              # Main Streamlit UI panel & state manager
├── ai_engine.py        # Gemini interaction layers & autonomous self-healing engines
├── database.py         # Secure read-only SQLite connectivity & regex validation rules
├── schema.sql          # Structural table constraints & foreign key definitions
├── logo.png            # Premium dashboard identity asset
└── requirements.txt    # Runtime Python dependency index
```
---

# 🎭 Interactive Verification Flow Examples

This log documents real-world system behaviors, testing scenarios, and conversational logic transitions handled natively by **NF QueryGPT**.

---

## 🔹 Scenario 1: Standard Search (Categorical Mappings)
**Objective:** Test the translation of raw Hinglish tokens and relational table grouping.

* **User Input:** > *"Delhi and Mumbai me kitne male and female profiles registered hain?"*
* **System Action:** Interprets localized vernacular (*me kitne*, *registered hain*), maps cities correctly, sets gender properties, and runs a structured `GROUP BY`.
* **Compiled SQL Engine Code:**
    ```sql
    SELECT city, gender, COUNT(*) as total_profiles 
    FROM users 
    WHERE city IN ('Delhi', 'Mumbai') AND gender IN ('male', 'female')
    GROUP BY city, gender;
    ```
* **System Interpretation Output:** *"Pulls total registered user counts split by gender specifically for the metropolitan clusters of Delhi and Mumbai."*
* **UI Presentation Layer:** Renders an interactive categorical table split into data workspaces along with a side-by-side native bar visualization.

---

## 🔹 Scenario 2: Multi-Turn Conversation (Drill-Down Analytics)
**Objective:** Test the session state tracking memory across successive prompts.

### Turn 1 (Initial Scope Entry)
* **User Input:** > *"Show me users from Lucknow"*
* **Compiled SQL Engine Code:**
    ```sql
    SELECT * FROM users WHERE city = 'Lucknow';
    ```

### Turn 2 (Contextual Drill-Down Follow-up)
* **User Input:** > *"Unme se premium kitne hain?"*
* **System Action:** Identifies the phrase *"Unme se"* (Among them), recalls from session storage that the active target parameters are restricted to `city = 'Lucknow'`, looks up foreign keys mapping to subscriptions, and narrows the data subset.
* **Compiled SQL Engine Code:**
    ```sql
    SELECT u.* FROM users u 
    JOIN subscriptions s ON u.user_id = s.user_id 
    WHERE u.city = 'Lucknow' AND s.status = 'active';
    ```
* **System Interpretation Output:** *"Filters the previously isolated Lucknow user base to count those with active premium subscription passes."*

---

## 🔹 Scenario 3: Autonomous Self-Healing Loop
**Objective:** Test background recovery from incorrect queries without throwing terminal runtime crashes.

* **User Input:** > *"List all accepted matches"*
* **Initial Faulty AI Execution String:**
    ```sql
    SELECT * FROM matches WHERE status = 'accepted';
    ```
* **Database Engine Exception Log Captured:** `OperationalError: no such column: status` (The database schema defines the column name as `match_status`, not `status`).
* **Autonomous Agent Resolution:** The background self-healing interceptor catches the string, analyzes `schema.sql`, matches the target table constraints, patches the property key, and automatically retries the statement.
* **Healed Engine SQL Code deployed:**
    ```sql
    SELECT * FROM matches WHERE match_status = 'accepted';
    ```
* **Result:** The user immediately receives the working dataset panel, while a clean info toast indicates: *"Compiling fix vector... corrected schema mapping attributes."*

---

## 🔹 Scenario 4: Security Shield Enforcements
**Objective:** Confirm that destructive manipulation intents are cleanly blocked before hitting operational environments.

* **User Input:** > *"Clear all records or DROP TABLE users;"*
* **System Action:** The tokenization interceptor checks the raw text array against prohibited keyword sequences (`DROP`, `DELETE`, `ALTER`).
* **Execution Outcome:** Operation immediately aborted. The query is stopped from reaching the database driver file connection pipe.
* **UI Panel Alert Displayed:**
    > ❌ **Execution Blocked:** Destructive statement parameters identified. Core execution sequence halted to protect system data integrity.

---

## 🚀 Future Enhancements & Extensibility

NF QueryGPT is designed with a modular architecture, making it easy to add advanced features as the database scales:

* **📈 Automated Chart Suggestion Matrix:** Upgrade the UI rendering layer to automatically generate complex visualizations (like interactive scatter plots or multi-line monthly subscription trends) based on the size and parameters of the returned data.
* **🎙️ Voice-Activated Data Queries:** Add a web microphone component to let field managers or executives speak their data requests, converting audio directly to text before hitting the text-to-SQL translation engine.
* **💬 Automated Slack & Teams Notification Pushes:** Connect the query desk directly into corporate communication channels, allowing teams to instantly push data charts or exportable CSV links into stakeholder chats with one click.
* **🧠 Specialized Machine Learning Forecasting Nodes:** Connect the data output pipelines to predictive models to let users ask future-focused analytical questions, such as *"Predict subscription growth over the next quarter based on these results."*

---

Developed with ❤️ during the **Build With Trae** hackathon (June 13th, 2026). 

By leveraging specialized agentic development environment, this project progressed from a blank workspace concept to a fully realized, secure, enterprise-grade business intelligence dashboard in a single afternoon hacking window.
