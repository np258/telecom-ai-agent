def run_sql_query(query_type: str) -> str:
    data = {
        "billing_issues": "Total Calls: 4,500 | Repeat Rate: 12%",
        "line_drops": "Total Calls: 2,100 | Repeat Rate: 24% (CRITICAL)",
        "router_setup": "Total Calls: 3,200 | Repeat Rate: 8%"
    }
    return data.get(query_type.lower(), "Data not found.")

def search_call_transcripts(keyword: str) -> str:
    transcripts = {
        "line drop": "Transcript C101: Customer experienced repeated line drops after updating to Router Firmware v2.1. Rollback resolved 80% of test cases.",
        "billing": "Transcript C102: Customer confused by new promo discount line item."
    }
    return transcripts.get(keyword.lower(), "No matching transcripts found.")