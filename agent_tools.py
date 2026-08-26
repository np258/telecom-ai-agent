import json

def run_sql_query(query_type: str) -> str:
    q = query_type.lower().replace(" ", "_")
    
    data = {
        "billing_issues": "Total Calls: 4,500 | Repeat Rate: 12%",
        "billing": "Total Calls: 4,500 | Repeat Rate: 12%",
        "line_drops": "Total Calls: 2,100 | Repeat Rate: 24% (CRITICAL)",
        "line_drop": "Total Calls: 2,100 | Repeat Rate: 24% (CRITICAL)",
        "router_setup": "Total Calls: 3,200 | Repeat Rate: 8%",
        "router": "Total Calls: 3,200 | Repeat Rate: 8%"
    }
    return data.get(q, "Total Calls: 9,800 across all categories | Average Repeat Rate: 14.6%")

def search_call_transcripts(keyword: str) -> str:
    k = keyword.lower()
    transcripts = {
        "line drop": "Transcript C101: Customer experienced repeated line drops after updating to Router Firmware v2.1. Rollback resolved 80% of test cases.",
        "line_drops": "Transcript C101: Customer experienced repeated line drops after updating to Router Firmware v2.1. Rollback resolved 80% of test cases.",
        "billing": "Transcript C102: Customer confused by new promo discount line item."
    }
    
    for key, val in transcripts.items():
        if key in k or k in key:
            return val
            
    return "Transcript C103: General inquiry regarding monthly statement charges."

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_sql_query",
            "description": "Fetch structured KPI metrics and repeat rates. REQUIRES a specific category like 'line_drops', 'billing_issues', or 'router_setup'. Do NOT call if the user prompt is ambiguous or incomplete (e.g. 'line' or 'root').",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_type": {
                        "type": "string",
                        "description": "The exact call driver category: 'line_drops', 'billing_issues', or 'router_setup'."
                    }
                },
                "required": ["query_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_call_transcripts",
            "description": "Search raw call transcripts for qualitative root cause analysis. REQUIRES a clear search topic. Do NOT call for single vague words.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "The specific keyword or topic to search."
                    }
                },
                "required": ["keyword"]
            }
        }
    }
]

def execute_tool_call(tool_name: str, arguments: dict) -> str:
    # Clean namespace prefixes if added by LLM (e.g. 'repo_browser.run_sql_query' -> 'run_sql_query')
    clean_name = tool_name.split(".")[-1]
    
    if clean_name == "run_sql_query":
        # Handle fallback keys if LLM used 'query' or 'topic' instead of 'query_type'
        val = arguments.get("query_type") or arguments.get("query") or arguments.get("topic") or ""
        return run_sql_query(str(val))
    elif clean_name == "search_call_transcripts":
        val = arguments.get("keyword") or arguments.get("topic") or arguments.get("query") or ""
        return search_call_transcripts(str(val))
        
    return "Unknown tool called."