# Project: GSC Citation Audit Tool

## Description
A simple Streamlit app that analyzes Google Search Console exports and generates SEO content performance audits (Wins + Opportunities) based on a strict SOP.

## Tech Stack
- Python
- Streamlit
- Pandas

## How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Run the app:
   streamlit run app.py

## Code Style
- Keep functions small and readable
- Add comments explaining logic in plain English
- Avoid complex abstractions
- Prioritize clarity over cleverness

## Git Rules
- Never commit directly to main
- Always create a feature branch
- Commit after every working feature

## File Structure
- app.py → UI and user inputs
- parser.py → handles CSV/Excel parsing
- audit_logic.py → determines wins + opportunities
- prompt_builder.py → formats final output

## Gotchas
- GSC exports sometimes have different column names → normalize them
- CTR may come as percentage or decimal → standardize to %
- Pages vs Queries must be matched by URL
- Do NOT exceed 2 wins or 2 opportunities
- Follow SOP strictly (no guessing wins)
