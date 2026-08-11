from langgraph.graph import StateGraph, END
from state import JobSearchState
from nodes import track_jobs_node

tracking_graph = StateGraph(JobSearchState)
tracking_graph.add_node("track_jobs", track_jobs_node)
tracking_graph.set_entry_point("track_jobs")
tracking_graph.add_edge("track_jobs", END)

tracking_subgraph = tracking_graph.compile()