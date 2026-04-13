def build_prompt_output(audit_results):
    """Formats the audit results into a professional SEO performance report."""

    intro = (
        "Based on the analysis of recent Google Search Console data, we have identified several "
        "performance wins and future growth opportunities aligned with our current SEO strategy."
    )

    wins_text = ""
    if audit_results['wins']:
        for win in audit_results['wins']:
            wins_text += (
                f"For the page {win['page']}, we observed a significant performance win in {win['month']}. "
                f"{win['change']} As a direct result, we {win['outcome']}\n\n"
            )
    else:
        wins_text = "No confirmed performance wins matched the deliverables in this period.\n\n"

    opps_text = ""
    if audit_results.get('opportunities'):
        for opp in audit_results['opportunities']:
            opps_text += (
                f"The page {opp['page']} is showing strong growth with {opp['metric']}. "
                f"To further capitalize on this trajectory, we recommend that we {opp['recommendation'].lower()}\n\n"
            )
    else:
        opps_text = "No additional growth opportunities were identified at this scale.\n\n"

    final_output = (
        f"SEO PERFORMANCE REPORT\n\n"
        f"{intro}\n\n"
        f"PERFORMANCE WINS\n\n"
        f"{wins_text}"
        f"GROWTH OPPORTUNITIES\n\n"
        f"{opps_text}"
    )

    return final_output.strip()
