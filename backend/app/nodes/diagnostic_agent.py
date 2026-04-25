import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.state import MedicalState

# Section 6 : Chargement de l'environnement
load_dotenv()

# Section 4.1 : Température à 0.7 pour éviter la répétition monotone
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

def diagnostic_node(state: MedicalState):
    """
    Pose 5 questions successives et variées (Section 4.3 & 5).
    """
    current_count = state.get("question_count", 0)
    messages = state.get("messages", [])
    
    print(f"--- DIAGNOSTIC AGENT: Question {current_count + 1}/5 ---")

    if current_count < 5:
        # PROMPT DE DIVERSITÉ : On interdit la répétition
        system_instructions = (
            f"Vous êtes un assistant médical professionnel. C'est la question n°{current_count + 1} sur 5. "
            "INSTRUCTION CRITIQUE : Lisez attentivement l'historique des messages ci-dessous. "
            "NE POSEZ PAS une question sur un sujet déjà abordé. "
            "Variez impérativement vos questions parmi ces thèmes : "
            "1. Durée et début des symptômes. "
            "2. Intensité de la douleur/gêne (échelle 1-10). "
            "3. Signes associés (fièvre, nausées, vertiges). "
            "4. Antécédents médicaux ou allergies. "
            "5. Facteurs déclenchants ou aggravants. "
            "Posez UNE seule question courte, claire et pertinente."
        )
        
        # On passe TOUT l'historique pour que le LLM voit ses propres questions précédentes
        response = llm.invoke([("system", system_instructions)] + messages)
        
        return {
            "messages": [response],
            "question_count": current_count + 1,
            "next": "supervisor"
        }
    else:
        # Section 4.1 & 4.4 : Phase de synthèse clinique et recommandation intermédiaire
        print("--- DIAGNOSTIC AGENT: Phase de synthèse ---")
        summary_prompt = (
            "En vous basant sur l'échange précédent, produisez une synthèse clinique préliminaire "
            "et proposez une recommandation intermédiaire prudente (repos, hydratation, etc.)."
        )
        response = llm.invoke(messages + [("system", summary_prompt)])
        
        return {
            "diagnostic_summary": response.content,
            "interim_care": "Repos, surveillance de la température et hydratation.",
            "next": "supervisor"
        }