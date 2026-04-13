def build_prompt_output(audit_results):
    """Formats the audit results to match the 'Good Example' perfectly."""

    # 1. Exact Intro Paragraph from the Example
    intro = (
        "We conduct monthly content performance checks using Google Search Console to evaluate the "
        "effectiveness of our content strategy. This allows us to track key metrics, identify trends, "
        "and make data-driven decisions to optimize our website for better search engine visibility "
        "and user experience, ultimately driving more traffic and conversions."
    )

    # 2. Wins Section
    wins_section_inner = ""
    if audit_results['wins']:
        for win in audit_results['wins']:
            # Construct phrases like "ranking #2 by clicks" and "February 2026 Homepage Content Creation"
            wins_section_inner += (
                f"The {win['slug_clean']} page ({win['page']}) has demonstrated strong performance following the "
                f"{win['month_year']} {win['slug_clean']} Content Creation and Optimization. Updated content "
                f"helped reinforce the local relevance and authority for searches. The page is currently "
                f"ranking {win['rank']} by clicks in Google Search Console, confirming its position as a "
                f"top organic entry point.\n\n"
            )
    else:
        wins_section_inner = "No confirmed performance wins found matching the SOP deliverables.\n\n"

    # 3. Opportunities Section
    opps_section_inner = ""
    if audit_results['opportunities']:
        for opp in audit_results['opportunities']:
            # Construct technical descriptions matching the professional tone
            opps_section_inner += (
                f"The {opp['slug_clean']} page ({opp['page']}) is generating nearly {opp['impressions']} impressions "
                f"in Google Search Console at a CTR of just {opp['ctr']}, indicating strong search exposure with "
                f"a significant opportunity to convert more of that visibility into clicks. This is a strong "
                f"candidate for improvement without requiring a full content overhaul. Recommended improvements "
                f"include meta title and description refreshes, introductory on-page content updates, and "
                f"enhanced internal linking. Keyword focus: {opp['keywords']}.\n\n"
            )
    else:
        opps_section_inner = "No additional growth opportunities were identified at this scale.\n\n"

    # Assemble Final Report
    report = (
        f"{intro}\n\n"
        f"Wins:\n\n"
        f"{wins_section_inner}"
        f"Opportunities:\n\n"
        f"{opps_section_inner}"
        f"See Google Search Console top performing pages by clicks & impressions attached."
    )

    return report.strip()
