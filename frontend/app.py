import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="MediGraph AI - Orientation Clinique", layout="wide")
st.title("🏥 MediGraph AI : Système d'Orientation Médicale")

# Initialisation du thread_id pour la session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "step" not in st.session_state:
    st.session_state.step = 1  # Écran 1 par défaut

# --- ÉCRAN 1 : SAISIE DU CAS INITIAL --- [cite: 121-122]
if st.session_state.step == 1:
    st.subheader("Étape 1 : Description de vos symptômes")
    patient_input = st.text_area("Veuillez décrire votre état :", placeholder="Ex: J'ai mal à la gorge et de la fièvre depuis 2 jours...")
    
    if st.button("Démarrer la consultation"):
        res = requests.post(f"{API_URL}/consultation/start", json={"patient_case": patient_input})
        if res.status_code == 200:
            data = res.json()
            st.session_state.thread_id = data["thread_id"]
            st.session_state.step = 2
            st.rerun()

# --- ÉCRAN 2 : QUESTIONS / RÉPONSES PATIENT --- [cite: 121, 123]
elif st.session_state.step == 2:
    st.subheader("Étape 2 : Questionnaire clinique (Boucle de 5 questions)")
    # Note : Dans une version complète, vous boucleriez ici sur l'état du graphe
    # Pour le projet, nous affichons la progression du DiagnosticAgent [cite: 27, 36, 177]
    st.info(f"ID Consultation : {st.session_state.thread_id}")
    
    # Simulation de l'interaction (à lier dynamiquement à votre state['messages'])
    st.write("Le système analyse vos réponses pour produire une synthèse...")
    
    if st.button("Passer à la revue médicale"):
        st.session_state.step = 3
        st.rerun()

# --- ÉCRAN 3 : REVUE MÉDECIN (Human-in-the-Loop) --- [cite: 31-34, 121, 124]
elif st.session_state.step == 3:
    st.subheader("Étape 3 : Espace Médecin Traitant (HITL)")
    st.warning("Interruption du graphe : En attente de validation médicale.")
    
    physician_input = st.text_area("Conduite à tenir / Traitement :", placeholder="Ex: Repos 3 jours, Doliprane 1g si fièvre > 38.5°C")
    
    if st.button("Valider et Générer le Rapport"):
        res = requests.post(f"{API_URL}/consultation/resume", json={
            "thread_id": st.session_state.thread_id,
            "physician_treatment": physician_input
        })
        if res.status_code == 200:
            st.session_state.final_report = res.json()["final_report"]
            st.session_state.step = 4
            st.rerun()

# --- ÉCRAN 4 : RAPPORT FINAL --- [cite: 120-121, 124]
elif st.session_state.step == 4:
    st.subheader("Étape 4 : Rapport Final Structuré")
    st.success("Consultation terminée")
    st.markdown(st.session_state.final_report)
    
    if st.button("Nouvelle consultation"):
        st.session_state.clear()
        st.rerun()