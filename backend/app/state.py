from typing import Annotated, Literal, List
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class MedicalState(TypedDict, total=False):
    # Liste des messages échangés (historique) 
    messages: Annotated[list, add_messages]
    # Prochain agent à appeler (décidé par le Supervisor) 
    next: Literal["diagnostic_agent", "physician_review", "report_agent", "FINISH"]
    # Compteur pour les 5 questions obligatoires 
    question_count: int
    # Résultats des étapes 
    interim_care: str
    diagnostic_summary: str
    physician_treatment: str
    final_report: str