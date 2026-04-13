import streamlit as st
import pandas as pd
from parser import parse_gsc_export

st.title("GSC Citation Audit Tool")
st.write("Upload your Google Search Console exports to generate performance audits.")

# Initialize session state to store dataframes
if 'df_pages' not in st.session_state:
    st.session_state['df_pages'] = None
if 'df_queries' not in st.session_state:
    st.session_state['df_queries'] = None

# Sidebar for file uploads
st.sidebar.header("Upload Files")
pages_file = st.sidebar.file_uploader("Upload Pages File (CSV or Excel)", type=["csv", "xlsx"])
queries_file = st.sidebar.file_uploader("Upload Queries File (CSV or Excel)", type=["csv", "xlsx"])

sop_text = st.text_area("SOP / Deliverables SOP", height=200, placeholder="Paste your SEO deliverables guidelines here...")

# Previews and Data Storage
if pages_file:
    st.subheader("Cleaned Pages Data Preview")
    try:
        # Use our parser to clean/normalize data
        df_pages = parse_gsc_export(pages_file)
        st.session_state['df_pages'] = df_pages
        st.dataframe(df_pages.head())
        st.success(f"Successfully processed {len(df_pages)} rows from Pages file.")
    except Exception as e:
        st.error(f"Error reading Pages file: {e}")

if queries_file:
    st.subheader("Cleaned Queries Data Preview")
    try:
        # Use our parser to clean/normalize data
        df_queries = parse_gsc_export(queries_file)
        st.session_state['df_queries'] = df_queries
        st.dataframe(df_queries.head())
        st.success(f"Successfully processed {len(df_queries)} rows from Queries file.")
    except Exception as e:
        st.error(f"Error reading Queries file: {e}")

if sop_text:
    st.info("SOP Guidelines loaded.")
