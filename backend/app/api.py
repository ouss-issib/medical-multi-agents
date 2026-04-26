import uuid
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# LangGraph & Core Imports
from app.graph import graph
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="Multi-Agent Medical API")

# --- Configuration CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modèles de Données Pydantic ---
class StartRequest(BaseModel):
    thread_id: str
    initial_symptoms: str

class AnswerRequest(BaseModel):
    thread_id: str
    answer: str

class ResumeRequest(BaseModel):
    thread_id: str
    physician_treatment: str

# --- Endpoints de Consultation ---

@app.post("/sessions/start")
def create_session():
    return {"thread_id": str(uuid.uuid4())}

@app.post("/consultation/start")
def start_consultation(req: StartRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    initial_state = {
        "messages": [HumanMessage(content=req.initial_symptoms)],
        "question_count": 0
    }
    for _ in graph.stream(initial_state, config=config):
        pass 
    state = graph.get_state(config).values
    return {"status": "chatting", "state": state}

@app.post("/consultation/answer")
def submit_answer(req: AnswerRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    new_message = HumanMessage(content=req.answer)
    for _ in graph.stream({"messages": [new_message]}, config=config):
        pass
    state = graph.get_state(config).values
    return {"state": state}

@app.get("/consultation/{thread_id}")
def get_consultation_state(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config).values
    if not state:
        raise HTTPException(status_code=404, detail="Session non trouvée.")
    return {"state": state}
@app.post("/consultation/resume")
def resume_consultation(req: ResumeRequest):
    config = {
        "configurable": {"thread_id": req.thread_id}, 
        "recursion_limit": 25
    }
    
    # We revert the process to a direct stream injection.
    # By passing the dictionary directly into stream(), we wake up the graph.
    # The Supervisor will evaluate the state, see the new treatment, 
    # and immediately route to the Report Agent.
    for _ in graph.stream({"physician_treatment": req.physician_treatment}, config=config):
        pass
        
    # Fetch the state after the Report Agent has done its job
    state_values = graph.get_state(config).values
    
    return {
        "status": "completed", 
        "state": state_values, 
        "final_report": state_values.get("final_report", "")
    }
@app.get("/consultation/{thread_id}/report")
def get_report(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config).values
    if "final_report" not in state or not state["final_report"]:
        raise HTTPException(status_code=404, detail="Rapport non disponible.")
    return {"status": "completed", "state": state, "final_report": state.get("final_report")}

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)