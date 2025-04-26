from langchain_core.prompts import ChatPromptTemplate

llm_judge_prompt = ChatPromptTemplate.from_template("""
You are a strict fact-checker and reasoning verifier.

You will be given:
- A user query about a band.
- The final answer produced by the agent.
- The tools that the agent used during reasoning (including tool names and inputs).
- The full chat history with the user.

Your job is to carefully check:
1. **Tool Use**: Did the agent correctly use the `get_band_information` tool to retrieve the answer?
2. **Memory Use**: If the tool wasn't used, was the information already available in the chat history?
3. **Self-Contained Knowledge**: If neither tool nor memory was used, does the final answer still seem factually correct based on context?

If **any** of these are true, output: JSON: {{ "relevant": true }}
Else Output JSON: {{ "relevant": false }}
---
User Query: {query}
Final Answer: {final_answer}
Tool Calls: {tool_calls}
Chat History: {chat_history}
---
ONLY output the JSON object.
""")
