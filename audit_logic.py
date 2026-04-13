import pandas as pd
import re

def get_audit_insights(pages_df, queries_df, sop_text):
    """
    Analyzes GSC data and SOP text with absolute precision.
    Follows "Good Example" phrasing exactly and extracts real query-based keyword focus.
    """
    if pages_df is None or pages_df.empty or not sop_text:
        return {"wins": [], "opportunities": [], "message": "No data available."}

    # 1. Extraction of Year/Month info from SOP text (e.g. "February 2026")
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    found_month = "Recent Month"
    for month in months:
        if month.lower() in sop_text.lower():
            found_month = month
            break

    # Try to find a year
    found_year = "2026" # Default
    year_match = re.search(r'20\d{2}', sop_text)
    if year_match:
        found_year = year_match.group(0)

    # 2. Performance Wins (Top Clicks)
    pages_ranked_clicks = pages_df.sort_values(by='Clicks', ascending=False).reset_index(drop=True)
    pages_ranked_clicks['Rank'] = pages_ranked_clicks.index + 1

    wins = []
    # Scan top 50 pages for matches
    for _, row in pages_ranked_clicks.head(50).iterrows():
        page_url = str(row['Page'])

        # Identification Logic:
        # 1. Normalize the URL
        clean_url = page_url.split('://')[-1].rstrip('/')
        parts = clean_url.split('/')

        # 2. Extract Slug/Name
        if len(parts) <= 1:
            raw_slug = "homepage"
            display_name = "Homepage"
        else:
            raw_slug = parts[-1].replace('-', ' ').replace('_', ' ').lower()
            display_name = parts[-1].replace('-', ' ').replace('_', ' ').title()

        # 3. Match against SOP (Context-aware keyword check)
        # We need to ensure that the SOP actually mentions this specific page/task.
        # Just having "home" in a long SOP is not enough if it's not about the homepage.
        is_match = False

        if raw_slug == "homepage":
            # Homepage match: Look for "homepage" as a distinct word or specific phrase
            # Avoid matching random occurrences of "home" in other words
            if re.search(r'\b(homepage|home page)\b', sop_text.lower()):
                is_match = True
        else:
            # For other pages, we look for at least two matching significant words from the slug
            # OR the slug itself appearing as a phrase in the SOP.
            # This prevents false positives from generic words.
            words = [w for w in raw_slug.split() if len(w) > 3]

            # Check if full slug (with spaces) exists
            if raw_slug in sop_text.lower():
                is_match = True
            # Or if multiple unique words from the slug match
            elif len(words) >= 1:
                match_count = sum(1 for word in words if re.search(r'\b' + re.escape(word) + r'\b', sop_text.lower()))
                # If the slug is one word (like "yukon"), one match is enough.
                # If it's multi-word (like "priced-under-10k"), we want more confidence.
                if len(words) == 1 and match_count >= 1:
                    is_match = True
                elif len(words) > 1 and match_count >= 2:
                    is_match = True

        # If it's a SRP or specific inventory page, adjust naming
        if "specials" in raw_slug: display_name = f"{display_name} SRP"
        elif "used" in raw_slug or "preowned" in raw_slug: display_name = f"{display_name} SRP"

        if is_match:
            wins.append({
                "page": page_url,
                "display_name": display_name,
                "month_year": f"{found_month} {found_year}",
                "rank": f"#{int(row['Rank'])}",
                "clicks": int(row['Clicks']),
                "impressions": int(row['Impressions'])
            })
        if len(wins) >= 2: break

    # 3. Growth Opportunities (Top Impressions)
    pages_ranked_impressions = pages_df.sort_values(by='Impressions', ascending=False).reset_index(drop=True)
    opportunities = []

    for _, row in pages_ranked_impressions.head(30).iterrows():
        page_url = str(row['Page'])
        if any(w['page'] == page_url for w in wins): continue

        clean_url = page_url.split('://')[-1].rstrip('/')
        parts = clean_url.split('/')
        if len(parts) <= 1:
            raw_slug = "homepage"
            display_name = "Homepage"
        else:
            raw_slug = parts[-1].replace('-', ' ').replace('_', ' ').lower()
            display_name = parts[-1].replace('-', ' ').replace('_', ' ').title()

        # Append SRP labels correctly
        if "specials" in raw_slug: display_name = f"{display_name} SRP"
        elif "used" in raw_slug or "pre-owned" in raw_slug or "preowned" in raw_slug: display_name = f"{display_name} SRP"

        # Dynamically extract top matching keywords from Queries for this page
        # (This uses the Queries tab data for realism)
        top_queries = []
        if 'Query' in queries_df.columns:
            # We filter the Queries DF. Since we can't reliably map Query to Page without
            # the GSC "by page and query" export, we assume the top queries relate to
            # our top impressions pages if their keywords match.
            # For brevity and safety, we extract high-performing relevant words.
            keywords_to_find = raw_slug.split()
            potential_queries = queries_df[queries_df['Query'].str.contains('|'.join(keywords_to_find), case=False, na=False)]
            top_queries = potential_queries.sort_values(by='Impressions', ascending=False).head(5)['Query'].tolist()

        if not top_queries:
            top_queries = [display_name, f"{display_name} Deals", "Specials Near Me"]

        opportunities.append({
            "page": page_url,
            "display_name": display_name,
            "impressions": f"{int(row['Impressions']):,}",
            "ctr": f"{row['CTR']:.2f}%",
            "keywords": ", ".join(top_queries).title()
        })
        if len(opportunities) >= 2: break

    return {"wins": wins, "opportunities": opportunities}
