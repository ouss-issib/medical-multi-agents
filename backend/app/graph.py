import os
from langgraph.graph import StateGraph, START, END
from app.state import MedicalState
from app.nodes.supervisor import supervisor_node
from app.nodes.diagnostic_agent import diagnostic_node
from app.nodes.physician_review import physician_node
from app.nodes.report_agent import report_node
from langgraph.checkpoint.memory import MemorySaver

# On initialise le constructeur
builder = StateGraph(MedicalState)

# 1. Ajout des Noeuds
builder.add_node("Supervisor", supervisor_node)
builder.add_node("diagnostic_agent", diagnostic_node)
builder.add_node("physician_review", physician_node)
builder.add_node("report_agent", report_node)

# 2. Edges de base
builder.add_edge(START, "Supervisor")

# 3. Routage conditionnel du Superviseur
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

# 4. Retour systématique au Superviseur
builder.add_edge("diagnostic_agent", "Supervisor")
builder.add_edge("physician_review", "Supervisor")
builder.add_edge("report_agent", "Supervisor")

# 5. Compilation adaptée (Studio vs Local)
# Note: On garde les interruptions pour que Studio sache où s'arrêter

# ... tout ton code builder.add_node et builder.add_edge ...

# 1. Configuration des interruptions (Obligatoire pour ton TP)
interrupt_config = {
    "interrupt_after": ["diagnostic_agent"], 
    "interrupt_before": ["physician_review"]
}

# 2. Détection de l'environnement LangGraph Studio / API
# Ces variables sont injectées automatiquement par la plateforme
is_studio = os.getenv("LANGGRAPH_API_KEY") or os.getenv("LANGCHAIN_API_KEY") or os.getenv("JETBRAINS_IDE")

if is_studio:
    # Pour Studio : ON NE MET PAS de checkpointer du tout.
    # La plateforme s'en occupe toute seule.
    graph = builder.compile(**interrupt_config)
else:
    # Pour ton serveur FastAPI local uniquement
    memory = MemorySaver()
    graph = builder.compile(
        checkpointer=memory,
        **interrupt_config
    )

# # 5. Compile with HITL requirements (Section 4.2 & 12)
# memory = MemorySaver()
# # We interrupt AFTER the diagnostic to wait for patient answers, 
# # and BEFORE physician_review for the doctor's manual input.
# graph = builder.compile(
#     checkpointer=memory, 
#     interrupt_after=["diagnostic_agent"], 
#     interrupt_before=["physician_review"]
# )


