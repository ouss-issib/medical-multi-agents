from langchain_core.tools import tool
from app.tools.mcp_client import mcp_client

@tool
def recommend_interim_care(symptoms: str) -> str:
    """
    Use this tool to generate safe, preliminary interim care recommendations 
    (e.g., rest, hydration) based on current symptoms.
    """
    # Extract a simple keyword to query the MCP server based on the summary
    keyword = "fever" if "fièvre" in symptoms.lower() or "fever" in symptoms.lower() else "cough"
    
    # Fetch real data from the MCP microservice!
    guidelines = mcp_client.fetch_clinical_guidelines(keyword)
    
    return f"Recommandation (Source: MCP Server) - {guidelines}"