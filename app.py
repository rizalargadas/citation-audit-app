import streamlit as st
import pandas as pd

st.title("GSC Citation Audit Tool")
st.write("Upload your Google Search Console exports to generate performance audits.")

# Sidebar for file uploads
st.sidebar.header("Upload Files")
pages_file = st.sidebar.file_uploader("Upload Pages File (CSV or Excel)", type=["csv", "xlsx"])
queries_file = st.sidebar.file_uploader("Upload Queries File (CSV or Excel)", type=["csv", "xlsx"])

sop_text = st.text_area("SOP / Deliverables SOP", height=200, placeholder="Paste your SEO deliverables guidelines here...")

# Previews
if pages_file:
    st.subheader("Pages Data Preview")
    try:
        if pages_file.name.endswith('.csv'):
            df_pages = pd.read_csv(pages_file)
        else:
            df_pages = pd.read_excel(pages_file)
        st.dataframe(df_pages.head())
    except Exception as e:
        st.error(f"Error reading Pages file: {e}")

if queries_file:
    st.subheader("Queries Data Preview")
    try:
        if queries_file.name.endswith('.csv'):
            df_queries = pd.read_csv(queries_file)
        else:
            df_queries = pd.read_excel(queries_file)
        st.dataframe(df_queries.head())
    except Exception as e:
        st.error(f"Error reading Queries file: {e}")

if sop_text:
    st.info("SOP Guidelines loaded.")
