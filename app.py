import streamlit as st
from agent_tools import run_sql_query, search_call_transcripts

st.set_page_config(page_title="Telecom AI Agent", layout="wide")
st.title("🤖 Customer Intelligence Agentic Assistant")
st.caption("Powered by RAG, Agentic Tool Routing & Conversational Analytics")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_prompt = st.chat_input("Ask about repeat rates, or transcript root causes...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)
    
    if "repeat" in user_prompt.lower() or "rate" in user_prompt.lower():
        tool_output = run_sql_query("line_drops")
        response = f"**[Agent Executed Tool: SQL Query]**\n\n{tool_output}\n\n**Insight:** Line drops show a critical 24% repeat call rate."
    elif "transcript" in user_prompt.lower() or "cause" in user_prompt.lower():
        tool_output = search_call_transcripts("line drop")
        response = f"**[Agent Executed Tool: Vector RAG Search]**\n\n{tool_output}"
    else:
        response = "I can analyze call KPIs or search transcripts. Ask me about repeat rates or root causes!"
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)