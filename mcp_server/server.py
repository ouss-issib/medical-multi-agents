# # mcp_server/server.py
# from mcp.server.fastmcp import FastMCP

# # Création du serveur MCP nommé "MedicalDB"
# mcp = FastMCP("MedicalDB")

# @mcp.tool()
# def get_medical_guidelines(condition: str) -> str:
#     """Récupère les recommandations de soins pour une condition donnée."""
#     guidelines = {
#         "fievre": "Hydratation abondante, repos et surveillance de la température toutes les 4h.",
#         "toux": "Si sèche : hydratation. Si grasse : ne pas couper la toux. Consulter si essoufflement.",
#         "douleur": "Évaluer l'échelle de douleur. Repos de la zone concernée.",
#         "grippe": "Repos strict, isolation, paracétamol si fièvre mal tolérée."
#     }
#     # Recherche simple par mot-clé
#     for key in guidelines:
#         if key in condition.lower():
#             return guidelines[key]
#     return "Recommandations générales : Repos, hydratation et surveillance des symptômes."

# if __name__ == "__main__":
#     mcp.run()

from fastapi import FastAPI
import uvicorn

mcp_app = FastAPI(title="MCP Data Server")

@mcp_app.get("/guidelines")
def get_guidelines(query: str):
    """
    Mock MCP Server endpoint to provide external clinical guidelines.
    """
    # In reality, this queries an external database or standard protocol system
    guidelines_db = {
        "fever": "Protocole: Paracétamol 1g/8h si fièvre > 38.5°C.",
        "cough": "Protocole: Sirop antitussif, hydratation."
    }
    
    data = guidelines_db.get(query.lower(), "Standard care applies. Monitor vitals.")
    return {"status": "success", "data": data}

if __name__ == "__main__":
    uvicorn.run(mcp_app, host="0.0.0.0", port=8080)