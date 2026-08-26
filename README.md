[Click here for Live Streamlit App demo](https://telecom-ai-agent-ly2ydwxhneuezdr2qoagmu.streamlit.app/)

What is this agent?
An agentic customer intelligence assistant designed to analyze telecom operations data, isolate repeat call drivers, and identify root causes from customer call transcripts.

### Key Features & Architecture

* **Agentic Tool Calling & Orchestration:** Powered by OpenAI GPT models to dynamically evaluate user prompts, select function schemas, and execute tools (`run_sql_query`, `search_call_transcripts`).
* **Conversational Operations Analytics:** Translates natural language business queries into quantitative KPI metrics, First Call Resolution (FCR) indicators, and repeat call rates.
* **Qualitative Transcript Search:** Searches customer call interaction logs to uncover underlying root causes, such as firmware regressions, billing confusion, or router setup issues.
* **Separation of Concerns:** Clean enterprise structure decoupling the UI (`app.py`), agent orchestration logic (`agent.py`), and tool definitions (`agent_tools.py`).

---

### Tech Stack
* **UI/UX:** Streamlit
* **LLM Orchestration:** OpenAI API (`gpt-4o` / `gpt-4o-mini`)
* **Language:** Python 3.10+
* **Environment Management:** `python-dotenv`