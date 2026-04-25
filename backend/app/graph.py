import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.state import MedicalState
from app.nodes.supervisor import supervisor_node
from app.nodes.diagnostic_agent import diagnostic_node
from app.nodes.physician_review import physician_node
from app.nodes.report_agent import report_node

load_dotenv()

# 1. Initialisation du graphe avec l'état partagé (Section 8)
builder = StateGraph(MedicalState)

# 2. Ajout des nœuds obligatoires (Section 4.1)
builder.add_node("supervisor", supervisor_node)
builder.add_node("diagnostic_agent", diagnostic_node)
builder.add_node("physician_review", physician_node)
builder.add_node("report_agent", report_node)

# 3. Définition des relations (Section 5)
builder.add_edge(START, "supervisor")

# Routing conditionnel depuis le Superviseur
builder.add_conditional_edges(
    "supervisor",
    lambda x: x["next"],
    {
        "diagnostic_agent": "diagnostic_agent",
        "physician_review": "physician_review",
        "report_agent": "report_agent",
        "FINISH": END
    }
)

# Retours systématiques au superviseur
builder.add_edge("diagnostic_agent", "supervisor")
builder.add_edge("physician_review", "supervisor")
builder.add_edge("report_agent", "supervisor")

# 4. CONFIGURATION CRUCIALE (Section 4.2 & 12)
# On utilise MemorySaver pour la persistance (thread_id)
# On ajoute une interruption AVANT le médecin
memory = MemorySaver()
graph = builder.compile(
    checkpointer=memory, 
    interrupt_before=["physician_review"] 
)