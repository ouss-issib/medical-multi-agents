import streamlit as st
import requests
import time

# Configuration de l'URL de ton API FastAPI
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="MediGraph AI", page_icon="🏥")

# Initialisation des variables de session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "step" not in st.session_state:
    st.session_state.step = 1
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🏥 MediGraph AI : Orientation Clinique")

# --- ÉCRAN 1 : SAISIE DU CAS INITIAL ---
if st.session_state.step == 1:
    st.subheader("Étape 1 : Description de votre situation")
    case_input = st.text_area("Expliquez vos symptômes :", placeholder="Ex: J'ai une forte fièvre et une toux sèche...")
    
    if st.button("Démarrer la consultation"):
        if case_input:
            with st.spinner("Initialisation..."):
                response = requests.post(f"{API_URL}/consultation/start", json={"patient_case": case_input})
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.thread_id = data["thread_id"]
                    st.session_state.messages = data["messages"]
                    st.session_state.step = 2
                    st.rerun()
        else:
            st.error("Veuillez décrire votre cas.")

# --- ÉCRAN 2 : QUESTIONS/RÉPONSES PATIENT ---
elif st.session_state.step == 2:
    st.subheader("Étape 2 : Questionnaire Médical")
    
    # On affiche l'historique (les questions de l'IA)
    for msg in st.session_state.messages:
        role = "Patient" if st.session_state.messages.index(msg) == 0 else "IA Médicale"
        st.write(f"**{role}** : {msg}")
    
    st.divider()
    
    # Note : Dans une version réelle, on répondrait à chaque question. 
    # Pour la démo, on simule la progression vers l'étape médecin une fois les 5 questions posées par le backend.
    st.info("Le Diagnostic Agent a terminé son analyse préliminaire.")
    
    if st.button("Transmettre au Médecin Traitant"):
        st.session_state.step = 3
        st.rerun()

# --- ÉCRAN 3 : REVUE MÉDECIN (HITL) ---
elif st.session_state.step == 3:
    st.subheader("Étape 3 : Espace Médecin (Validation)")
    st.warning("Interruption du système : En attente de l'expertise humaine.")
    
    # Le médecin saisit son traitement
    treatment = st.text_area("Avis médical et traitement préconisé :", placeholder="Ex: Prescription de paracétamol, repos 48h...")
    
    if st.button("Valider et Générer le Rapport"):
        if treatment:
            with st.spinner("Génération du rapport final..."):
                payload = {
                    "thread_id": st.session_state.thread_id,
                    "physician_treatment": treatment
                }
                res = requests.post(f"{API_URL}/consultation/resume", json=payload)
                if res.status_code == 200:
                    st.session_state.final_report = res.json()["final_report"]
                    st.session_state.step = 4
                    st.rerun()
        else:
            st.error("L'avis du médecin est obligatoire.")

# --- ÉCRAN 4 : RAPPORT FINAL ---
elif st.session_state.step == 4:
    st.subheader("Étape 4 : Rapport de Synthèse Final")
    st.success("La consultation est terminée.")
    
    st.markdown(st.session_state.final_report)
    
    if st.button("Nouvelle Consultation"):
        st.session_state.clear()
        st.rerun()