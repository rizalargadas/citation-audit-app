import pandas as pd
import re

def get_audit_insights(pages_df, queries_df, sop_text):
    """
    Analyzes GSC data and SOP text to find Performance Wins.
    Rules:
    - Sort pages by clicks descending
    - Take top 15 pages
    - Check if any keywords from the page URL (slug) match the deliverables SOP
    - Return max 2 wins
    """
    if pages_df is None or pages_df.empty or not sop_text:
        return {"wins": [], "message": "No data available to perform audit."}

    # 1. Sort by Clicks and get Top 15
    top_15 = pages_df.sort_values(by='Clicks', ascending=False).head(15)

    wins = []

    # 2. Extract potential "Month" from SOP text (e.g., "January", "February", etc.)
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    found_month = "Latest Period"
    for month in months:
        if month.lower() in sop_text.lower():
            found_month = month
            break

    # 3. Simple Keyword Matching
    for _, row in top_15.iterrows():
        page_url = str(row['Page'])

        # Extract the slug (last part of the URL) for simpler keyword matching
        slug = page_url.rstrip('/').split('/')[-1].replace('-', ' ').replace('_', ' ')

        # If the slug contains keywords found in the SOP text, it's a win!
        # (This is a simplified "did we work on this page?" check)
        keywords = slug.split()
        is_match = any(word.lower() in sop_text.lower() for word in keywords if len(word) > 3)

        if is_match:
            win = {
                "page": page_url,
                "month": found_month,
                "change": f"Applied SEO optimizations based on {found_month} deliverables.",
                "outcome": f"Achieved {int(row['Clicks']):,} clicks and {int(row['Impressions']):,} impressions."
            }
            wins.append(win)

        # Max 2 wins as per SOP
        if len(wins) >= 2:
            break

    # 4. Fallback if no matches found
    if not wins:
        return {
            "wins": [],
            "message": "No confirmed performance wins found matching the SOP deliverables for the top 15 pages."
        }

    return {"wins": wins, "message": "Audit completed successfully."}
