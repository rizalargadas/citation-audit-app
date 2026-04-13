import pandas as pd
import re

def get_audit_insights(pages_df, queries_df, sop_text):
    """
    Analyzes GSC data and SOP text to find Performance Wins and Opportunities.
    Matches the "Good Example" format with specific wording.
    """
    if pages_df is None or pages_df.empty or not sop_text:
        return {"wins": [], "opportunities": [], "message": "No data available to perform audit."}

    # 1. Extraction of Year/Month info from SOP text
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    found_month = "Recent Month"
    for month in months:
        if month.lower() in sop_text.lower():
            found_month = month
            break

    # 2. Performance Wins (Top Clicks)
    # Sort and calculate rank
    pages_df_ranked = pages_df.sort_values(by='Clicks', ascending=False).reset_index(drop=True)
    pages_df_ranked['Rank'] = pages_df_ranked.index + 1

    wins = []
    for idx, row in pages_df_ranked.head(30).iterrows(): # Check a larger set to find matching SOP keywords
        page_url = str(row['Page'])
        slug = page_url.rstrip('/').split('/')[-1].replace('-', ' ').replace('_', ' ')

        # Heuristic: Find mention of keywords in SOP
        if any(word.lower() in sop_text.lower() for word in slug.split() if len(word) > 3):
            # Extract Keywords from queries_df if available
            keywords = []
            if 'Page' in queries_df.columns:
                # Assuming queries_df has Page and Query columns matched
                # This is a bit of a placeholder since direct Page-to-Query matching requires specific GSC exports
                pass

            wins.append({
                "page": page_url,
                "month_year": f"{found_month} 2026", # Placeholder for Year
                "rank": f"#{row['Rank']}",
                "slug_clean": slug.title()
            })
        if len(wins) >= 2: break

    # 3. Growth Opportunities (Top Impressions)
    opps_df = pages_df.sort_values(by='Impressions', ascending=False).reset_index(drop=True)
    opportunities = []

    for idx, row in opps_df.head(20).iterrows():
        page_url = str(row['Page'])
        if any(w['page'] == page_url for w in wins): continue

        slug = page_url.rstrip('/').split('/')[-1].replace('-', ' ').replace('_', ' ')

        # Only pick if it's high impressions
        opportunities.append({
            "page": page_url,
            "impressions": f"{int(row['Impressions']):,}",
            "ctr": f"{row['CTR']:.2f}%",
            "slug_clean": slug.title(),
            # Placeholder keywords based on slug parts
            "keywords": f"{slug.title()}, {found_month} Toyota Deals, Specials Near Me"
        })
        if len(opportunities) >= 2: break

    return {"wins": wins, "opportunities": opportunities}
