from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.state import MedicalState
from app.tools.care_tools import recommend_interim_care

def diagnostic_node(state: MedicalState) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    messages = state.get("messages", [])
    
    # 1. Calcul dynamique et exact basé sur le patient
    human_messages = [m for m in messages if getattr(m, "type", "") == "human"]
    
    # Le nombre de réponses apportées par le patient (0 au début, 1 au 1er /answer)
    answers_given = len(human_messages) - 1

    # 2. Boucle : on s'arrête strictement après 5 réponses du patient
    if answers_given < 5:
        prompt = [
            SystemMessage(
                content=f"Tu es un assistant médical. Pose une seule question pertinente (Question {answers_given + 1}/5) pour clarifier les symptômes. Sois très bref."
            )
        ] + messages
        
        response = llm.invoke(prompt)
        
        return {
            "messages": [response],
            "question_count": answers_given, # Renvoie 0 au /start, 1 au premier /answer, etc.
            "next": "Supervisor"
        }
    
    else:
        #3. Phase de synthèse
        summary_prompt = messages + [
            HumanMessage(content="""Génère une synthèse clinique courte. 
            CONSIGNE D'ANONYMAT : Ne mentionne JAMAIS 'Patient', 'Nom' ou 'Date'. 
            N'utilise pas de crochets comme [Nom]. Commence directement par 'Synthèse : '.""")
        ]
        
        summary = llm.invoke(summary_prompt).content
        
        # Appel MCP sécurisé
        try:
            care = recommend_interim_care.invoke({"symptoms": summary})
        except Exception as e:
            print(f"Erreur outil MCP : {e}")
            care = "En attente de l'avis du médecin." # Fallback de sécurité
        
        return {
            "diagnostic_summary": summary,
            "interim_care": care,
            "question_count": answers_given, # On bloque le compteur à 5 pour Flutter
            "next": "Supervisor"
        }