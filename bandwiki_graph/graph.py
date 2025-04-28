from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Any
from langchain_core.runnables import RunnableWithMessageHistory, RunnableSerializable
import json

def tavily_search(query: str) -> list:
    # Mocked search results
    print(f"[Mock Search] Performing fake Tavily search for query: '{query}'")
    return [
        {"url": f"https://example.com/{query.replace(' ', '_')}_info", "title": f"Info about {query}"},
        {"url": f"https://bandwiki.com/{query.replace(' ', '_')}", "title": f"{query} - BandWiki Entry"},
        {"url": f"https://musicpedia.com/{query.replace(' ', '_')}_history", "title": f"{query} history"}
    ]

def summarize_search_results(search_results: list) -> str:
    # Mocked summary
    print("[Mock Summary] Summarizing fake search results.")
    return f"Summary based on {len(search_results)} mock search results."

def schedule_background_scrape(search_results: list):
    # Mocked background job
    print(f"[Mock Background Scrape] Scheduled scraping for {len(search_results)} URLs.")

def format_tool_calls(intermediate_steps):
    tool_calls = []
    for step, _ in intermediate_steps:
        if hasattr(step, 'tool') and hasattr(step, 'tool_input'):
            tool_calls.append({"tool": step.tool, "tool_input": step.tool_input})
    return tool_calls

# Define your state
class BandWikiState(TypedDict):
    query: str
    final_answer: str
    tool_calls: list[dict[str, Any]]
    chat_history: list
    should_search: bool
    search_results: Optional[str]
    band_agent: RunnableWithMessageHistory
    judge_chain: RunnableSerializable

def build_bandwiki_graph():
    graph = StateGraph(BandWikiState)

    # 1. Try answering
    def answer_agent_node(state: BandWikiState) -> BandWikiState:
        response = state["band_agent"].invoke({"input": state["query"]})
        state["final_answer"] = response['output']
        state["tool_calls"] = format_tool_calls(response['intermediate_steps'])
        return state

    graph.add_node("AnswerAgent", answer_agent_node)

    # 2. Judge if search is needed
    def judge_answer_node(state: BandWikiState) -> BandWikiState:
        judge_response = state["judge_chain"].invoke({
            "query": state["query"],
            "final_answer": state["final_answer"],
            "tool_calls": state["tool_calls"],
            "chat_history": state["chat_history"],
        })

        raw_content = judge_response.content

        # Clean it: remove ```json and ``` if present
        cleaned_content = raw_content.strip()
        if cleaned_content.startswith("```json"):
            cleaned_content = cleaned_content[len("```json"):].strip()
        if cleaned_content.startswith("```"):
            cleaned_content = cleaned_content[len("```"):].strip()
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3].strip()

        judge_decision = json.loads(cleaned_content)
        # print(result['should_search'])

        # judge_decision = json.loads(judge_response.content)
        state["should_search"] = judge_decision.get("should_search", False)
        return state

    graph.add_node("JudgeAnswer", judge_answer_node)

    # 3. Search if needed
    def search_fallback_node(state: BandWikiState) -> BandWikiState:
        search_results = tavily_search(state["query"])  # or your own function
        state["search_results"] = search_results
        state["final_answer"] = summarize_search_results(search_results)
        return state

    graph.add_node("SearchFallback", search_fallback_node)

    # 4. Background scrape
    def background_scrape_node(state: BandWikiState) -> BandWikiState:
        schedule_background_scrape(state["search_results"])
        return state

    graph.add_node("BackgroundScrape", background_scrape_node)

    # 5. Final return
    def return_answer_node(state: BandWikiState) -> BandWikiState:
        return state  # No change needed; just end

    graph.add_node("ReturnFinalAnswer", return_answer_node)

    # Define edges
    graph.set_entry_point("AnswerAgent")
    graph.add_edge("AnswerAgent", "JudgeAnswer")

    # Conditional branching
    graph.add_conditional_edges(
        "JudgeAnswer",
        lambda state: "ReturnFinalAnswer" if not state["should_search"] else "SearchFallback"
    )

    graph.add_edge("SearchFallback", "BackgroundScrape")
    graph.add_edge("BackgroundScrape", "ReturnFinalAnswer")

    return graph.compile()