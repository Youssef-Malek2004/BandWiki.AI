from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from .config import LLM_MODEL, OPENAI_API_KEY, OPENAI_API_BASE, TEMPERATURE
from .tools import get_acdc_information_tool
from prompts import qa_prompt

def build_agent(retriever, get_session_history):
    tool_fn = get_acdc_information_tool(retriever)
    tools = [tool_fn]

    llm = ChatOpenAI(
        model=LLM_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE,
        temperature=TEMPERATURE
    )

    agent = create_tool_calling_agent(llm, tools, qa_prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    memory = RunnableWithMessageHistory(
        executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )
    return memory
