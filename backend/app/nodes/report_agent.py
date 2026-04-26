from langchain_openai import ChatOpenAI
from app.state import MedicalState

def report_node(state: MedicalState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    prompt = f"""
        Génère un rapport médical final strictement anonyme.
        DONNÉES : Synthèse: {state.get('diagnostic_summary')}, Traitement: {state.get('physician_treatment')}

        RÈGLES DE STYLE :
        - Supprime les en-têtes 'Patient', 'Date', 'Nom'.
        - Ne laisse aucun champ vide ou texte entre crochets.
        - Utilise un ton professionnel et factuel.
        - MENTION OBLIGATOIRE FINALE : "*Ce système ne remplace pas une consultation médicale.*"
        """
    
    try:
        response = llm.invoke(prompt)
        final_text = response.content
    except Exception as e:
        print(f"Erreur GPT Report : {e}")
        final_text = "# Rapport Médical\nErreur de génération."
        
    return {
        "final_report": final_text, 
        "next": "Supervisor"
    }