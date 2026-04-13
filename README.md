# 📊 E-Commerce Automated ELT Pipeline

This repository contains the end-to-end automation for ingesting daily e-commerce data from Gmail, processing it through a Medallion architecture in BigQuery, and providing an interactive SQL assistant for end-users.

## 🏗 System Architecture



The data flows through four distinct stages:
1.  **Ingestion (MailToGCS):** A Google Apps Script monitors Gmail for daily CSV attachments and streams them to a Google Cloud Storage (GCS) bucket.
2.  **Abstraction (GCSToExternalTable):** A BigQuery External Table acts as a permanent pointer to the GCS file, allowing for instant "loading-free" access to raw data.
3.  **Transformation (Dataform):** 
    * **Bronze:** Incremental upsert of raw data into a persistent history table.
    * **Silver:** Deduplication and cleaning using window functions.
    * **Gold:** Aggregated business metrics (LTV, Order frequency).
4.  **Consumption (ChatApp):** A natural language interface that translates user questions into SQL queries against the **Gold** layer.

---

## 📂 Repository Structure

* **`/MailToGCS`**: Contains `main.gs`. Handles Gmail searching, blob extraction, and GCS upload.
* **`/GCSToExternalTable`**: SQL script to define the BigQuery External Table schema and GCS URI.
* **`/Dataform`**: The Core 3.0.42 project including `definitions/` (Bronze, Silver, Gold SQLX files) and `workflow_settings.yaml`.
* **`/ChatApp`**: Python/Streamlit (or similar) code for the LLM-powered SQL assistant.

---

## 💰 Cost Analysis (Estimated)

Based on standard Google Cloud Tiering (North America/Montreal):

| Component | Service | Cost Factor | Estimated Monthly Cost |
| :--- | :--- | :--- | :--- |
| **Orchestration** | Apps Script | Included with Workspace | $0.00 |
| **Storage** | Cloud Storage | Nearline/Standard | ~$0.02 per GB |
| **Compute** | Dataform | Free for Core | $0.00 |
| **Processing** | BigQuery | Query Scanning | ~$5.00 per TB (Free tier first 1TB) |
| **ChatApp** | Gemini API / Vertex | Token usage | Variable (starts at free/low tier) |

---

## 🚀 Moving to Production

To transition from this "Dev" setup to a Production-grade environment, follow these steps:

### 1. Security & Governance
* **Service Accounts:** Move away from personal `ScriptApp.getOAuthToken()`. Create a dedicated Service Account with `Storage Object Admin` and `Dataform Editor` roles.
* **Secrets Management:** Use **Google Cloud Secret Manager** to store Project IDs or sensitive email filters instead of hardcoding them in scripts.

### 2. CI/CD Pipeline
* **Git Integration:** Connect your Dataform repository to GitHub/GitLab. 
* **Environments:** Use Dataform's **Environments** feature to separate `development` and `production` datasets so you don't break production reports while testing new code.

### 3. Monitoring & Alerts
* **Error Notifications:** Update the Apps Script to send a Slack/Email alert if the `UrlFetch` fails.
* **Dataform Assertions:** Add `assertions` to the Gold layer (e.g., `total_revenue > 0`) to catch data quality issues automatically during the run.

### 4. ChatApp Optimization
* **Metadata Layer:** Provide the ChatApp with the `definitions.sqlx` descriptions so it understands the context of the columns (e.g., "Revenue includes tax").
* **Read-Only Access:** Ensure the ChatApp's database user has **strictly** `DATA_VIEWER` permissions—never `DATA_EDITOR`.

---

## 🛠 Setup Instructions
1.  Deploy `MailToGCS` script and set a time-driven trigger.
2.  Execute the `GCSToExternalTable` script in the BigQuery console.
3.  Initialize the Dataform project and create a **Workflow Configuration** to schedule the daily run.
4.  Configure the ChatApp with your BigQuery project credentials.

---

## 🔮 Future Scope: Scaling

To transition this MVP into a high-availability, enterprise-grade production system, the following architectural upgrades are planned:

### 1. Serverless Ingestion (Cloud Functions)
* **Current:** Google Apps Script (subject to workspace timeouts and 6-minute limits).
* **Future:** Replace Apps Script with a **Python Cloud Function**. 
    * The function will be triggered by a **Pub/Sub** notification or a **Cloud Scheduler** cron job.
    * It will use the Gmail API to securely authenticate and stream large CSV attachments directly to GCS.
    * **Benefit:** Better error handling, higher memory limits, and centralized logging in Cloud Logging.

### 2. Orchestration & Lineage (Cloud Composer / Airflow)
* **Current:** Built-in Dataform scheduling.
* **Future:** Implement **Cloud Composer** (Managed Apache Airflow) to act as the "brain" of the entire pipeline.
    * **DAG Workflow:**
        1. **Sensor:** Wait for the file to land in GCS.
        2. **Ingestion:** Trigger the Cloud Function (if not event-driven).
        3. **Dataform Operator:** Trigger the Dataform compilation and invocation for Bronze, Silver, and Gold layers.
        4. **Quality Check:** Run Dataform assertions and block the pipeline if data quality fails.
        5. **Notification:** Send a Slack/Email alert upon success or failure.
    * **Benefit:** Full visibility into cross-service dependencies and automatic retries.


### 3. Advanced Analytics & Chatbot Evolution
* **Semantic Layer:** Integrate the Chatbot with **Dataform Metadata** so it can "read" column descriptions and table tags to provide more accurate SQL generation.
* **Vector Search:** Implement a RAG (Retrieval-Augmented Generation) pattern using **Vertex AI Vector Search** to allow the chatbot to search through internal company documentation alongside the SQL data.

---
