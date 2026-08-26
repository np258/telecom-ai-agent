import os
import json
from dotenv import load_dotenv
import streamlit as st
from groq import Groq
from agent_tools import TOOLS, execute_tool_call

load_dotenv()

TELECOM_SYSTEM_PROMPT = """You are a Principal Telecom Operations & Customer Intelligence Analyst.

CRITICAL GUARDRAIL - CLARIFICATION REQUIRED:
- If the user provides a single-word query, partial phrase, or ambiguous term (e.g., "line", "drop", "root", "billing", "router"), DO NOT CALL ANY TOOLS.
- Immediately ask a polite, concise clarifying question listing 2-3 specific topics they might mean.
- Example: If the user types "line", reply: "Did you mean line drop KPIs, line drop call transcripts, or line activation issues?"

CORE RESPONSIBILITIES:
1. Domain Expertise: Frame analysis around core telecom operational metrics (e.g., FCR, repeat call rates, firmware regressions).
2. Data Integrity: Only when the request is clear and specific, use `run_sql_query` for quantitative metrics and `search_call_transcripts` for qualitative root causes.
3. Structured Output: Summarize insights clearly using bullet points and bold metrics."""

class TelecomAgent:
    def __init__(self):
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except (KeyError, FileNotFoundError, Exception):
            api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def get_active_model(self):
        preferred_models = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.6-27b"]
        try:
            available_models = [m.id for m in self.client.models.list().data]
            for model in preferred_models:
                if model in available_models:
                    return model
            return available_models[0]
        except Exception:
            return "openai/gpt-oss-120b"

    def run(self, history: list):
        logs = []
        active_model = self.get_active_model()
        
        # 1. Primary context setup
        clean_messages = [{"role": "system", "content": TELECOM_SYSTEM_PROMPT}]
        
        for msg in history:
            if isinstance(msg, dict) and msg.get("role") in ["user", "assistant"]:
                if msg.get("content"):
                    clean_messages.append({
                        "role": msg["role"],
                        "content": str(msg["content"])
                    })

        # 2. First LLM Call with Tool Definitions
        response = self.client.chat.completions.create(
            model=active_model,
            messages=clean_messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        response_msg = response.choices[0].message

        # 3. Handle Tool Execution
        if response_msg.tool_calls:
            tool_results_summary = []

            for tool_call in response_msg.tool_calls:
                fn_name = tool_call.function.name
                
                # Parse function arguments safely
                try:
                    fn_args = json.loads(tool_call.function.arguments) if isinstance(tool_call.function.arguments, str) else tool_call.function.arguments
                except Exception:
                    fn_args = {}

                logs.append(f"🔧 Executing `{fn_name}` with arguments `{fn_args}`")

                tool_result = execute_tool_call(fn_name, fn_args)
                tool_results_summary.append(f"Output from `{fn_name}`:\n{tool_result}")

            # 4. Inject execution results as plain text instruction
            synthesis_prompt = (
                "DATA RETRIEVED FROM TOOLS:\n"
                + "\n\n".join(tool_results_summary)
                + "\n\nINSTRUCTION: Synthesize the above data into a clear analytical response in plain text. "
                "Do NOT output JSON or attempt to call any further functions."
            )
            
            clean_messages.append({"role": "user", "content": synthesis_prompt})

            # 5. Second Pass: Pure text response without sending `tools` payload
            second_resp = self.client.chat.completions.create(
                model=active_model,
                messages=clean_messages
            )
            return second_resp.choices[0].message.content, logs

        return response_msg.content, logs