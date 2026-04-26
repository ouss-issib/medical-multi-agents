from langchain_core.tools import tool

@tool
def ask_patient(question: str) -> str:
    """
    Use this tool to ask the patient a clinical question.
    In an API context, this tool pauses the agent and returns the question to the user.
    """
    return f"QUESTION_FOR_PATIENT: {question}"