def build_prompt_output(audit_results):
    """Formats the audit results with absolute precision to match real audit standards."""

    intro = (
        "We conduct monthly content performance checks using Google Search Console to evaluate the "
        "effectiveness of our content strategy. This allows us to track key metrics, identify trends, "
        "and make data-driven decisions to optimize our website for better search engine visibility "
        "and user experience, ultimately driving more traffic and conversions."
    )

    # 1. Wins Section
    wins_inner = ""
    if audit_results['wins']:
        for win in audit_results['wins']:
            # Handle Homepage vs specialized SRP naming
            win_name = win['display_name']

            wins_inner += (
                f"The {win_name} ({win['page']}) has demonstrated strong performance following the "
                f"{win['month_year']} {win_name} Content Optimization. Updated content helped "
                f"reinforce the local relevance and authority for searches in the local market. "
                f"The page is currently ranking {win['rank']} by clicks in Google Search Console, "
                f"confirming its position as one of our top organic entry points.\n\n"
            )
    else:
        wins_inner = "No verified performance wins were identified for pages matched in our latest content SOP.\n\n"

    # 2. Opportunities Section
    opps_inner = ""
    if audit_results['opportunities']:
        for opp in audit_results['opportunities']:
            opp_name = opp['display_name']

            opps_inner += (
                f"The {opp_name} ({opp['page']}) is appearing with nearly {opp['impressions']} "
                f"impressions in Google Search Console at a CTR of just {opp['ctr']}, indicating "
                f"strong search exposure with a meaningful opportunity to convert more visibility into clicks. "
                f"This money page has not been part of any recent optimization efforts and aligns directly with "
                f"the current vehicle focus. Recommended improvements include updated meta tags "
                f"targeting shoppers actively looking for incentives, refreshed on-page content, "
                f"and strategic internal linking to drive qualified traffic. Keyword focus: {opp['keywords']}.\n\n"
            )
    else:
        opps_inner = "No additional growth opportunities were identified at this scale.\n\n"

    # Assemble Report
    final_output = (
        f"{intro}\n\n"
        f"Wins:\n\n"
        f"{wins_inner}"
        f"Opportunities:\n\n"
        f"{opps_inner}"
        f"See Google Search Console top performing pages by clicks & impressions attached."
    )

    return final_output.strip()
