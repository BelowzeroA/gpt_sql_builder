import streamlit as st

from builder.pipeline import SQLBuilderPipeline

CLICKHOUSE_PASSWORD = st.secrets["CLICKHOUSE_PASSWORD"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
pipeline = SQLBuilderPipeline(OPENAI_API_KEY, CLICKHOUSE_PASSWORD)


def generate(query, placeholder_sql, placeholder_data):
    result = pipeline.run(query)
    placeholder_sql.markdown(f'SQL: {result["sql"]}', unsafe_allow_html=True)
    placeholder_data.markdown(f'Result: {result["description"]}', unsafe_allow_html=True)


# Streamlit app
st.title("GPT SQL Builder")
st.write("Welcome to the GPT SQL Builder. This assistant will help you create SQL queries based on natural language.")

# Replace the print and input statements with Streamlit functions
st.write("Type your query and press the button to get the SQL.")
query = st.text_input("Query:")
generate_button = st.button("Generate SQL and get result")
placeholder_sql = st.empty()
placeholder_data = st.empty()

if generate_button:
    generate(query, placeholder_sql, placeholder_data)



