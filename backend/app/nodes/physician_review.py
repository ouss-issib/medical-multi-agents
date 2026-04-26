from app.state import MedicalState

def physician_node(state: MedicalState) -> dict:
    """
    Cette étape est une interruption Human-in-the-Loop.
    Le médecin reçoit la synthèse et propose un traitement.
    """
    # Ce nœud ne contient pas de logique LLM car c'est l'humain qui saisit la donnée.
    # On s'assure simplement que le 'next' pointe vers le Supervisor pour la suite.
    return {"next": "Supervisor"}