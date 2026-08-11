from langgraph.graph import StateGraph, END
from state import JobSearchState
from nodes import load_resume_node

resume_graph = StateGraph(JobSearchState)
resume_graph.add_node("load_resume", load_resume_node)
resume_graph.set_entry_point("load_resume")
resume_graph.add_edge("load_resume", END)

resume_subgraph = resume_graph.compile()