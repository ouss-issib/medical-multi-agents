import uuid
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.graph import graph
from langchain_core.messages import HumanMessage

app = FastAPI(title="Multi-Agent Medical API")

# --- MISSING PIECE 1: CORS Middleware ---
# This allows your React/Angular/Flutter frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StartRequest(BaseModel):
    thread_id: str
    initial_symptoms: str

class ResumeRequest(BaseModel):
    thread_id: str
    physician_treatment: str

@app.post("/sessions/start")
def create_session():
    """Generates a new unique thread ID for a consultation."""
    return {"thread_id": str(uuid.uuid4())}

@app.post("/consultation/start")
def start_consultation(req: StartRequest):
    """Starts the workflow with initial symptoms."""
    config = {"configurable": {"thread_id": req.thread_id}}
    initial_state = {
        "messages": [HumanMessage(content=req.initial_symptoms)],
        "question_count": 0
    }
    
    for _ in graph.stream(initial_state, config=config):
        pass 
    
    state = graph.get_state(config).values
    return {"status": "waiting_or_finished", "state": state}

@app.get("/consultation/{thread_id}")
def get_consultation_state(thread_id: str):
    """Retrieves the current state of the consultation."""
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config).values
    if not state:
        raise HTTPException(status_code=404, detail="Consultation thread not found.")
    return {"state": state}

@app.post("/consultation/resume")
def resume_consultation(req: ResumeRequest):
    """Resumes the graph after the physician provides a treatment."""
    config = {"configurable": {"thread_id": req.thread_id}}
    
    # We strictly enforce the state dictionary transition to report_agent
    graph.update_state(
        config, 
        {"physician_treatment": req.physician_treatment, "next": "report_agent"},
        as_node="physician_review"
    )
    
    for _ in graph.stream(None, config=config):
        pass
        
    state = graph.get_state(config).values
    return {"status": "completed", "final_report": state.get("final_report")}

@app.get("/consultation/{thread_id}/report")
def get_report(thread_id: str):
    """Retrieves the final structured report."""
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config).values
    if "final_report" not in state:
        raise HTTPException(status_code=404, detail="Report not generated yet.")
    return {"report": state["final_report"]}

# --- MISSING PIECE 2: Server Execution Block ---
if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)