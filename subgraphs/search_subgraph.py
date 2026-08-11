from langgraph.graph import StateGraph, END
from state import JobSearchState
from nodes import search_jobs_node, score_jobs_node, should_retry

search_graph = StateGraph(JobSearchState)
search_graph.add_node("search_jobs", search_jobs_node)
search_graph.add_node("score_jobs", score_jobs_node)

search_graph.set_entry_point("search_jobs")
search_graph.add_edge("search_jobs", "score_jobs")
search_graph.add_conditional_edges(
    "score_jobs",
    should_retry,
    {"retry": "search_jobs", "done": END}
)

search_subgraph = search_graph.compile()