from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from app.state import MedicalState
from app.nodes.supervisor import supervisor_router
from app.nodes.diagnostic_agent import diagnostic_node
from app.nodes.physician_review import physician_node
from app.nodes.report_agent import report_node

builder = StateGraph(MedicalState)

# Add Nodes
builder.add_node("Supervisor", supervisor_router)
builder.add_node("diagnostic_agent", diagnostic_node)
builder.add_node("physician_review", physician_node)
builder.add_node("report_agent", report_node)

# Add Edges
builder.add_edge(START, "Supervisor")

# Conditional routing from Supervisor
builder.add_conditional_edges(
    "Supervisor", 
    lambda state: state.get("next", "FINISH"),
    {
        "diagnostic_agent": "diagnostic_agent",
        "physician_review": "physician_review",
        "report_agent": "report_agent",
        "FINISH": END
    }
)

builder.add_edge("diagnostic_agent", "Supervisor")
builder.add_edge("physician_review", "Supervisor")
builder.add_edge("report_agent", "Supervisor")

# Compile with memory for HITL interruption
memory = MemorySaver()
graph = builder.compile(checkpointer=memory, interrupt_before=["physician_review"])