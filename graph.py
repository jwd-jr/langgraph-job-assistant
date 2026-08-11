from langgraph.graph import StateGraph, END
from state import JobSearchState
from subgraphs.resume_subgraph import resume_subgraph
from subgraphs.search_subgraph import search_subgraph
from subgraphs.tracking_subgraph import tracking_subgraph

graph = StateGraph(JobSearchState)

graph.add_node("resume_stage", resume_subgraph)
graph.add_node("search_stage", search_subgraph)
graph.add_node("tracking_stage", tracking_subgraph)

graph.set_entry_point("resume_stage")
graph.add_edge("resume_stage", "search_stage")
graph.add_edge("search_stage", "tracking_stage")
graph.add_edge("tracking_stage", END)

app = graph.compile()