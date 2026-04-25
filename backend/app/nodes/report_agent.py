import os
from dotenv import load_dotenv
from app.state import MedicalState

load_dotenv()

def report_node(state: MedicalState):
    """Génère le rapport final structuré (Section 4.1)."""
    print("--- REPORT AGENT: Génération du rapport final ---")
    
    summary = state.get("diagnostic_summary", "Non disponible")
    treatment = state.get("physician_treatment", "Non spécifié par le médecin")
    
    # MENTION LÉGALE STRICTE (Section 2)
    disclaimer = "Ce système ne remplace pas une consultation médicale."
    
    report_content = (
        f"### RAPPORT D'ORIENTATION CLINIQUE\n\n"
        f"**SYNTHÈSE CLINIQUE PRÉLIMINAIRE :**\n{summary}\n\n"
        f"**TRAITEMENT / CONDUITE À TENIR (MÉDECIN) :**\n{treatment}\n\n"
        f"--- \n*Note : {disclaimer}*"
    )
    
    return {
        "final_report": report_content,
        "next": "supervisor"
    }