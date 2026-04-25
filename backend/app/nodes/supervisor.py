import os
from typing import Literal
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.state import MedicalState

load_dotenv()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

class Router(BaseModel):
    """Schéma de routage imposé par la Section 8"""
    next_step: Literal["diagnostic_agent", "physician_review", "report_agent", "FINISH"]

def supervisor_node(state: MedicalState):
    """Orchestre le workflow (Section 4.1 et 5)"""
    print(f"--- SUPERVISOR: Décision de l'étape suivante ---")
    
    count = state.get("question_count", 0)
    summary = state.get("diagnostic_summary")
    treatment = state.get("physician_treatment")
    
    # 1. Logique de décision déterministe pour respecter le workflow minimal
    if count < 5:
        return {"next": "diagnostic_agent"}
    
    if summary and not treatment:
        return {"next": "physician_review"}
    
    if treatment and not state.get("final_report"):
        return {"next": "report_agent"}
    
    if state.get("final_report"):
        return {"next": "FINISH"}

    # 2. Secours par LLM si besoin de routage intelligent
    structured_llm = llm.with_structured_output(Router)
    response = structured_llm.invoke(state["messages"] + [("system", "Décidez de la prochaine étape médicale.")])
    
    return {"next": response.next_step}