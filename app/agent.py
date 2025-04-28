from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from .config import LLM_MODEL, OPENAI_API_KEY, OPENAI_API_BASE, TEMPERATURE
from .tools import get_band_information_tool
from prompts import qa_prompt, search_judge_prompt

def build_agent(retriever, get_session_history):
    tool_fn = get_band_information_tool(retriever)
    tools = [tool_fn]

    llm = ChatOpenAI(
        model=LLM_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE,
        temperature=TEMPERATURE
    )

    agent = create_tool_calling_agent(llm, tools, qa_prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

    memory = RunnableWithMessageHistory(
        executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    judge_llm = ChatOpenAI(
        model=LLM_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE,
        temperature=TEMPERATURE
    )

    judge_chain = search_judge_prompt | judge_llm

    return memory, judge_chain
