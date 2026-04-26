from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from app.state import MedicalState
from app.tools.patient_tools import ask_patient
from app.tools.care_tools import recommend_interim_care

def diagnostic_node(state: MedicalState) -> dict:
    """
    Handles patient Q&A up to 5 questions.
    Executes tools immediately to prevent OpenAI 400 Bad Request errors.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm_with_tools = llm.bind_tools([ask_patient, recommend_interim_care])
    
    messages = state.get("messages", [])
    q_count = state.get("question_count", 0)
    
    if q_count < 5:
        response = llm_with_tools.invoke(messages)
        new_messages = [response]
        
        # CRITICAL FIX: Ensure every tool_call receives a matching ToolMessage
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call["name"] == "ask_patient":
                    tool_result = ask_patient.invoke(tool_call["args"])
                    new_messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))
                elif tool_call["name"] == "recommend_interim_care":
                    tool_result = recommend_interim_care.invoke(tool_call["args"])
                    new_messages.append(ToolMessage(content=tool_result, tool_call_id=tool_call["id"]))

        return {
            "messages": new_messages,
            "question_count": q_count + 1
        }
    else:
        # Generate final diagnostic synthesis
        summary_prompt = "Based on the conversation, provide a preliminary clinical synthesis. Do not diagnose."
        messages.append(AIMessage(content=summary_prompt))
        summary = llm.invoke(messages).content
        
        interim = recommend_interim_care.invoke({"symptoms": summary})
        
        return {
            "diagnostic_summary": summary,
            "interim_care": interim,
            "next": "physician_review" # Routing logic preserved perfectly
        }