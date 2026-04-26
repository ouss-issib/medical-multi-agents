from app.state import MedicalState

def supervisor_node(state: MedicalState) -> dict:
    q_count = state.get("question_count", 0)
    summary = state.get("diagnostic_summary", "")
    treatment = state.get("physician_treatment", "")
    report = state.get("final_report", "")

    # 1. Si le rapport existe déjà, c'est fini.
    if report:
        return {"next": "FINISH"}

    # 2. Si le médecin a donné son traitement mais qu'il n'y a pas de rapport
    if treatment and not report:
        return {"next": "report_agent"} # <--- C'est CETTE ligne qui doit s'exécuter

    # 3. Si on a fini les questions mais que le médecin n'a pas répondu
    if q_count >= 5 and summary and not treatment:
        return {"next": "physician_review"}

    # 4. Si on n'a pas fini les questions
    if q_count < 5 or not summary:
         return {"next": "diagnostic_agent"}

    return {"next": "FINISH"}