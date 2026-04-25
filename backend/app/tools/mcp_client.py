from langchain_core.tools import tool

@tool
def recommend_interim_care(summary: str):
    """
    Génère des conseils de soins intermédiaires basés sur la synthèse.
    Note : Ces conseils sont préventifs et non définitifs.
    """
    return (
        "Recommandations suggérées : Repos strict, hydratation abondante "
        "et surveillance de la température toutes les 4 heures."
    )