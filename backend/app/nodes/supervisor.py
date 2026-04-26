from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.state import MedicalState
from pydantic import BaseModel
from typing import Literal

class RouteResponse(BaseModel):
    next: Literal["diagnostic_agent", "physician_review", "report_agent", "FINISH"]

def supervisor_router(state: MedicalState) -> dict:
    """
    Orchestrates the workflow deterministically to prevent LLM loops.
    Decides the next node strictly based on the presence of data in the state.
    """
    q_count = state.get("question_count", 0)
    has_summary = bool(state.get("diagnostic_summary"))
    has_physician = bool(state.get("physician_treatment"))
    has_report = bool(state.get("final_report"))

    # 1. If we haven't hit 5 questions, keep interviewing
    if q_count < 5 and not has_summary:
        return {"next": "diagnostic_agent"}
        
    # 2. If the interview is done but the doctor hasn't reviewed it, pause for HITL
    elif has_summary and not has_physician:
        return {"next": "physician_review"}
        
    # 3. If the doctor added a treatment, generate the report
    elif has_physician and not has_report:
        return {"next": "report_agent"}
        
    # 4. If everything is done, end the graph
    return {"next": "FINISH"}