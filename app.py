import streamlit as st
import pandas as pd
from parser import parse_gsc_combined_excel
from audit_logic import get_audit_insights
from prompt_builder import build_prompt_output

# Set Page Config for professional feel
st.set_page_config(page_title="GSC Citation Audit Tool", page_icon="📈", layout="wide")

st.title("📈 GSC Citation Audit Tool")
st.markdown("""
Use this tool to analyze a Google Search Console Excel export (the one with 'Pages' and 'Queries' tabs)
and generate a professional SEO audit.
""")

# Initialize session state to store dataframes
if 'df_pages' not in st.session_state:
    st.session_state['df_pages'] = None
if 'df_queries' not in st.session_state:
    st.session_state['df_queries'] = None

# Create Layout Columns
upload_col, input_col = st.columns([1, 1], gap="large")

with upload_col:
    st.subheader("1. Load GSC Export")
    st.sidebar.header("Data Uploads")
    gsc_file = st.sidebar.file_uploader("Upload GSC Excel Export", type=["xlsx"])

    if gsc_file:
        try:
            # Parse both sheets from one file
            df_pages, df_queries = parse_gsc_combined_excel(gsc_file)
            st.session_state['df_pages'] = df_pages
            st.session_state['df_queries'] = df_queries

            with st.expander("✅ Data Successfully Loaded", expanded=True):
                st.write(f"**Pages Detected:** {len(df_pages)} rows")
                st.write(f"**Queries Detected:** {len(df_queries)} rows")
                st.info("Both 'Pages' and 'Queries' tabs identified and processed.")
                st.dataframe(df_pages.head(5))
        except Exception as e:
            st.error(f"Error parsing GSC file: {e}")
            st.info("Make sure your Excel file has 'Pages' and 'Queries' tabs.")
    else:
        st.info("Upload your GSC Excel export in the sidebar to begin.")

with input_col:
    st.subheader("2. Audit Guidelines")
    sop_text = st.text_area(
        "Paste Deliverables SOP / Strategy Text",
        height=300,
        placeholder="Example: Optimized title tags for 'best cat food' in January...",
        help="Paste your full list of SEO optimizations here. There is no hard limit, but keep it relevant to the period."
    )
    if sop_text:
        st.success(f"Strategy keywords recognized ({len(sop_text)} characters).")
    else:
        st.warning("Please provide your SOP text to match against performance wins.")

st.divider()

# Audit Action
st.subheader("3. Finalize Audit")
if st.button("🚀 Generate Audit Report", use_container_width=True):
    # Validation check
    if st.session_state['df_pages'] is None or st.session_state['df_queries'] is None:
        st.error("Missing GSC Data! Please upload your Excel report in the sidebar.")
    elif not sop_text:
        st.error("Missing SOP! Please paste your strategy text in the box above.")
    else:
        # Visual loading spinner
        with st.spinner("Analyzing metrics and locating wins based on SOP..."):
            # Trigger analysis
            audit_results = get_audit_insights(
                st.session_state['df_pages'],
                st.session_state['df_queries'],
                sop_text
            )

            # Assemble report
            final_report = build_prompt_output(audit_results)

            # Success message
            st.success("Audit Generated Successfully!")

        # Results Display
        res_col1, res_col2 = st.columns([2, 1])
        with res_col1:
            st.header("Final Audit Output")
            st.markdown("Copy the text below for your SEO report:")
            # Use st.code for built-in clipboard copy button
            st.code(final_report, language="text")

        with res_col2:
            st.info("💡 **Next Steps:** Review the output for tone and accuracy before sending to the client.")
            st.write(f"**Wins found:** {len(audit_results.get('wins', []))}")
            st.write(f"**Opportunities found:** {len(audit_results.get('opportunities', []))}")

            with st.expander("View Raw JSON Data"):
                st.json(audit_results)
