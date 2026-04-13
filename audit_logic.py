import pandas as pd
import re

def get_audit_insights(pages_df, queries_df, sop_text):
    """
    Analyzes GSC data and SOP text to find Performance Wins and Opportunities.
    Rules:
    - Sort pages by clicks descending for Wins
    - Sort pages by impressions descending for Opportunities
    - Take top 15 pages for each
    - Check if any keywords from the page URL (slug) match the deliverables SOP
    - Return max 2 wins and max 2 opportunities
    """
    if pages_df is None or pages_df.empty or not sop_text:
        return {"wins": [], "opportunities": [], "message": "No data available to perform audit."}

    # 1. Extraction of potential "Month" from SOP text
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    found_month = "Latest Month"
    for month in months:
        if month.lower() in sop_text.lower():
            found_month = month
            break

    # 2. Performance Wins (Top 15 by Clicks)
    top_15_wins = pages_df.sort_values(by='Clicks', ascending=False).head(15)
    wins = []

    for _, row in top_15_wins.iterrows():
        page_url = str(row['Page'])
        slug = page_url.rstrip('/').split('/')[-1].replace('-', ' ').replace('_', ' ')
        keywords = slug.split()

        # Match if a significant word from slug is in SOP
        if any(word.lower() in sop_text.lower() for word in keywords if len(word) > 3):
            wins.append({
                "page": page_url,
                "month": found_month,
                "change": f"Applied SEO optimizations based on {found_month} deliverables.",
                "outcome": f"Achieved {int(row['Clicks']):,} clicks and {int(row['Impressions']):,} impressions."
            })
        if len(wins) >= 2: break

    # 3. Growth Opportunities (Top 15 by Impressions, but lower CTR)
    # Target high-reach pages that haven't converted as well yet
    top_15_opps = pages_df.sort_values(by='Impressions', ascending=False).head(15)
    opportunities = []

    for _, row in top_15_opps.iterrows():
        page_url = str(row['Page'])

        # Don't pick a page that is already a win
        if any(w['page'] == page_url for w in wins): continue

        slug = page_url.rstrip('/').split('/')[-1].replace('-', ' ').replace('_', ' ')
        keywords = slug.split()

        if any(word.lower() in sop_text.lower() for word in keywords if len(word) > 3):
            opportunities.append({
                "page": page_url,
                "metric": f"{int(row['Impressions']):,} impressions",
                "recommendation": f"Optimize title tags and meta descriptions to improve CTR beyond the current {row['CTR']:.2f}%."
            })
        if len(opportunities) >= 2: break

    results = {
        "wins": wins,
        "opportunities": opportunities,
        "message": "Audit completed successfully."
    }
    return results
