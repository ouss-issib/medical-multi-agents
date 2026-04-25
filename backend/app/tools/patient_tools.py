from langchain_core.tools import tool

@tool
def ask_patient(question: str):
    """
    Pose une question spécifique au patient pour affiner le diagnostic.
    Cet outil doit être utilisé exactement 5 fois.
    """
    # Dans une application réelle, cela enverrait une notification au frontend
    return f"Question posée : {question}. En attente de la réponse patient..."