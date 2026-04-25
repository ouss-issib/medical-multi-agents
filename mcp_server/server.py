# mcp_server/server.py
from mcp.server.fastmcp import FastMCP

# Création du serveur MCP
mcp = FastMCP("MedicalDB")

@mcp.tool()
def check_medical_database(symptoms: str) -> str:
    """Recherche les protocoles cliniques basés sur les symptômes."""
    # Simulation d'une base de données médicale pour le projet
    protocols = {
        "fievre": "Protocole grippal : Hydratation et surveillance température.",
        "toux": "Protocole respiratoire : Vérification de la saturation en oxygène.",
        "douleur": "Protocole antalgique : Évaluation de l'échelle de douleur (1-10)."
    }
    
    for key in protocols:
        if key in symptoms.lower():
            return protocols[key]
            
    return "Aucun protocole spécifique trouvé. Procéder à l'examen général."

if __name__ == "__main__":
    mcp.run()