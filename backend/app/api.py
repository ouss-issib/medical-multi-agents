import os
import uuid
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. Chargement de l'environnement (Section 6)
load_dotenv()

# 2. Import du graphe et du state (Section 7 & 8)
from app.graph import graph

app = FastAPI(
    title="MediGraph AI API",
    description="Système d'orientation clinique préliminaire - Pr. Mohamed YOUSSFI"
)

# --- Modèles de Données (Pydantic - Section 16) ---

class ConsultationStart(BaseModel):
    patient_case: str

class ConsultationResume(BaseModel):
    thread_id: str
    physician_treatment: str

# --- Endpoints Obligatoires (Section 10) ---

# 1. Initialiser une session
@app.post("/sessions/start")
async def start_session():
    """Initialise un nouvel identifiant de session (thread_id)."""
    thread_id = str(uuid.uuid4())
    return {"thread_id": thread_id, "status": "session_initialized"}

# 2. Démarrer une consultation
@app.post("/consultation/start")
async def start_consultation(data: ConsultationStart):
    """Lance le workflow d'orientation clinique (Section 4.3)."""
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # État initial conforme à la Section 8
    initial_input = {
        "messages": [("user", data.patient_case)],
        "question_count": 0
    }
    
    # Exécution jusqu'à l'interruption PhysicianReview (Section 12)
    result = graph.invoke(initial_input, config)
    
    # Vérification du prochain nœud pour le status
    state = graph.get_state(config)
    
    return {
        "thread_id": thread_id,
        "status": "interrupted_for_physician" if "physician_review" in state.next else "in_progress",
        "diagnostic_summary": result.get("diagnostic_summary"),
        "interim_care": result.get("interim_care"),
        "messages": [m.content if hasattr(m, 'content') else m for m in result.get("messages", [])]
    }

# 3. Reprendre après l'avis du médecin (Human-in-the-Loop)
@app.post("/consultation/resume")
async def resume_consultation(data: ConsultationResume):
    """Injecte l'avis du médecin et finalise le rapport (Section 4.2)."""
    config = {"configurable": {"thread_id": data.thread_id}}
    
    # Vérifier si la consultation existe
    current_state = graph.get_state(config)
    if not current_state.next:
        raise HTTPException(status_code=404, detail="Consultation introuvable ou terminée.")

    # Mise à jour de l'état (Section 3 : Human-in-the-Loop)
    graph.update_state(config, {"physician_treatment": data.physician_treatment})
    
    # Reprise de l'exécution
    result = graph.invoke(None, config)
    
    return {
        "thread_id": data.thread_id,
        "status": "completed",
        "final_report": result.get("final_report")
    }

# 4. Récupérer l'état complet d'une consultation
@app.get("/consultation/{thread_id}")
async def get_consultation_status(thread_id: str):
    """Récupère les valeurs et les transitions (Section 12)."""
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config)
    
    if not state.values:
        raise HTTPException(status_code=404, detail="Thread ID non trouvé.")
        
    return {
        "values": state.values,
        "next": state.next,
        "metadata": state.metadata
    }

# 5. Récupérer spécifiquement le rapport final
@app.get("/consultation/{thread_id}/report")
async def get_consultation_report(thread_id: str):
    """Extrait le rapport final structuré (Section 4.1)."""
    config = {"configurable": {"thread_id": thread_id}}
    state = graph.get_state(config)
    
    report = state.values.get("final_report")
    if not report:
        raise HTTPException(status_code=404, detail="Le rapport n'est pas encore généré.")
        
    return {
        "thread_id": thread_id,
        "final_report": report
    }

if __name__ == "__main__":
    import uvicorn
    # Configuration standard pour le test local
    uvicorn.run(app, host="127.0.0.1", port=8000)