from app.state import MedicalState

def physician_node(state: MedicalState) -> dict:
    """
    Passive node. Acts as an interrupt boundary for Human-in-the-Loop.
    LangGraph will pause BEFORE this node executes.
    When resumed via API, the state is updated directly.
    """
    # If this executes, it means the physician has reviewed it and the state was updated.
    # We simply route back to the supervisor.
    return {"next": "Supervisor"}