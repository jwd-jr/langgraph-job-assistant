from langgraph.graph import StateGraph, END
from state import JobSearchState
from nodes import (
    load_resume_node,
    search_jobs_node,
    score_jobs_node,
    should_retry,
    track_jobs_node,
)

graph = StateGraph(JobSearchState)

graph.add_node("load_resume", load_resume_node)
graph.add_node("search_jobs", search_jobs_node)
graph.add_node("score_jobs", score_jobs_node)
graph.add_node("track_jobs", track_jobs_node)

graph.set_entry_point("load_resume")
graph.add_edge("load_resume", "search_jobs")
graph.add_edge("search_jobs", "score_jobs")
graph.add_conditional_edges(
    "score_jobs",
    should_retry,
    {"retry": "search_jobs", "done": "track_jobs"}
)
graph.add_edge("track_jobs", END)

app = graph.compile()