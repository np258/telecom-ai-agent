import streamlit as st
from agent import TelecomAgent

st.set_page_config(page_title="Telecom AI Agent", layout="wide")
st.title("Customer Intelligence Agentic Assistant")
st.caption("Powered by LLM Tool Calling, Vector RAG & Conversational Analytics")

# Initialize Agent
agent = TelecomAgent()

# Chat history initialization (No system prompt needed here, handled inside agent.py)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    if isinstance(msg, dict):
        role = msg.get("role")
        content = msg.get("content")
        if role in ["user", "assistant"] and content:
            st.chat_message(role).write(content)

# Process user interaction
if user_prompt := st.chat_input("Ask about repeat rates, line drops, or transcript root causes..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing telecom data..."):
            final_answer, logs = agent.run(st.session_state.messages)
            
            # Display tool execution details transparently
            for log in logs:
                st.info(log)
            
            st.write(final_answer)
            st.session_state.messages.append({"role": "assistant", "content": final_answer})