from langchain_openai import ChatOpenAI
from app.state import MedicalState

def report_node(state: MedicalState) -> dict:
    """
    Generates the final structured report and appends the mandatory ethical disclaimer.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    summary = state.get("diagnostic_summary", "N/A")
    care = state.get("interim_care", "N/A")
    treatment = state.get("physician_treatment", "N/A")
    
    prompt = f"""
    Generate a highly structured medical report in Markdown based on:
    - Clinical Synthesis: {summary}
    - Interim Care: {care}
    - Physician Treatment Plan: {treatment}
    
    You MUST end the report with this exact phrasing:
    "Ce système ne remplace pas une consultation médicale."
    """
    
    response = llm.invoke(prompt)
    
    return {
        "final_report": response.content,
        "next": "FINISH"
    }