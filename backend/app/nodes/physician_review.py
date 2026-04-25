import os
from dotenv import load_dotenv
from app.state import MedicalState

load_dotenv()

def physician_node(state: MedicalState):
    """
    Étape Human-in-the-Loop (Section 4.2).
    Le médecin reçoit la synthèse et propose un traitement.
    """
    print("--- PHYSICIAN REVIEW: Interruption pour le médecin traitant ---")
    
    # On récupère les données pour affichage médecin (Section 4.2)
    summary = state.get("diagnostic_summary", "Synthèse en attente...")
    interim = state.get("interim_care", "Recommandation générale en attente...")
    
    # Si le traitement est injecté via l'API resume, on avance
    if state.get("physician_treatment"):
        print("--- PHYSICIAN REVIEW: Traitement reçu, retour au Superviseur ---")
        return {"next": "supervisor"}
        
    # Sinon, on reste bloqué ici (attente du signal externe)
    return {"next": "physician_review"}