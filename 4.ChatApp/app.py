import streamlit as st
import os
from dotenv import load_dotenv
from vertexai.generative_models import GenerativeModel
import vertexai
from google.cloud import bigquery

# Load variables from .env
load_dotenv()

# 1. Setup & Configuration
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION")

vertexai.init(project=PROJECT_ID, location=REGION)
bq_client = bigquery.Client(project=PROJECT_ID)

SYSTEM_PROMPT = f"""
You are a SQL expert for a BigQuery dataset named 'ecommerce_dataset'.
The primary table is 'orders_gold' which has the following columns:
- customer_id (STRING)
- customer_first_name (STRING)
- customer_last_name (STRING)
- total_orders (INTEGER)
- total_revenue (FLOAT)
- avg_order_value (FLOAT)

Rules:
1. Only return the SQL code. Do not include markdown formatting.
2. If the user asks for something not in the schema, explain why.
3. Use fully qualified table name: `{PROJECT_ID}.ecommerce_dataset.orders_gold`.
"""

model = GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=[SYSTEM_PROMPT]
)

# 2. Streamlit UI
st.set_page_config(page_title="BigQuery Chatbot", page_icon="💬")
st.title("💬 SQL Assistant")
st.caption(f"Connected to: {PROJECT_ID} | Region: {REGION}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat & Execution Logic
if prompt := st.chat_input("Ex: Top 5 customers by revenue?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Generate SQL
        response = model.generate_content(prompt)
        sql_query = response.text
        st.code(sql_query, language="sql")
        
        # Execute Query Button
        if st.button("🚀 Run Query"):
            try:
                with st.spinner("Querying BigQuery..."):
                    df = bq_client.query(sql_query).to_dataframe()
                    if df.empty:
                        st.warning("No data found.")
                    else:
                        st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"SQL Error: {str(e)}")

        st.session_state.messages.append({"role": "assistant", "content": sql_query})