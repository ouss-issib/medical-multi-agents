# 🩺 Assistant Médical Intelligent - Multi-Agents & HITL

Ce dépôt présente l’implémentation complète d’un **écosystème d'assistance médicale** basé sur une architecture multi-agents utilisant **LangGraph**, **FastAPI**, le protocole **MCP (Model Context Protocol)** et un frontend **Flutter**.

Le système simule un workflow d'orientation clinique intelligent avec une validation humaine stricte (**Human-in-the-loop**).

Projet réalisé dans le cadre du cours **Agentique AI** encadré par **Mr YOUSSFI Mohamed** (ENSET Mohammedia).

---

## 🧩 Architecture du Système

Le projet est découpé en trois piliers technologiques :

1.  **Backend (LangGraph + FastAPI)** : Orchestration agentique via un `Supervisor` pattern.
2.  **MCP Server** : Fournit des outils contextuels et des ressources médicales aux agents.
3.  **Frontend (Flutter)** : Interface utilisateur mobile pour la consultation et le rapport final.

---

## 🧠 1. Workflow LangGraph & Agents

Le cœur du système repose sur un graphe d'état supervisé où chaque transition est contrôlée par un agent central.

- **Supervisor** : Orchestre le flux entre les agents.
- **Diagnostic Agent** : Mène l'interrogatoire (limité à 5 questions) et produit la synthèse.
- **Physician Review (HITL)** : Point d'interruption forcé pour validation médicale.
- **Report Agent** : Génère le compte-rendu final au format Markdown.

### 📸 Visualisation du Graphe (LangGraph Studio)

| Graphe de Consultation | État du Thread (Memory) |
| :--- | :--- |
| ![Consultation Flow](./screenshots/consultation_by_thread.png) | ![Session Start](./screenshots/session_start.png) |

---

## 📚 2. Serveur MCP & API

Le **MCP Server** permet d'étendre les capacités des agents en leur offrant un accès sécurisé à des outils de diagnostic et des bases de connaissances.

### 📸 Backend & Tools

| API Swagger (FastAPI) | MCP Server Response |
| :--- | :--- |
| ![FastAPI Docs](./screenshots/fastapi_swagger_docs.png) | ![MCP Response](./screenshots/mcp_server_response.png) |

| Logs API & MCP | Pytest (Validation) |
| :--- | :--- |
| ![Logs](./screenshots/logs_fastapi_mcpserver.png) | ![Pytest](./screenshots/pytest_consultation.png) |

---

## 💬 3. Interface Frontend Flutter

L'application Flutter assure une communication fluide avec le backend, affichant les questions de l'agent en temps réel et le rapport médical final.

### 📸 Captures UI

| Démarrage Consultation | Chargement Agentique | Rapport Final |
| :--- | :--- | :--- |
| ![Start](./screenshots/consultation_start.png) | ![Loading](./screenshots/loading_consultation_flutter.png) | ![Report](./screenshots/consultation_report.png) |

---

## 🧪 4. Jeux de Tests Validés (Scénarios Cliniques)

Le système a été validé sur trois cas d'études principaux, documentés dans `/screenshots/tests_attendus/`.

### Cas 1 : Syndrome Viral (Standard)
| Étape | Capture d'écran |
| :--- | :--- |
| **Cas Initial** | ![Cas 1 Start](./screenshots/tests_attendus/cas1_syndrome_cas_initial.png) |
| **Questions/Réponses** | ![Cas 1 Q/R](./screenshots/tests_attendus/cas1_syndrome_questions_responses.png) |
| **Revue Médecin (HITL)** | ![Cas 1 HITL](./screenshots/tests_attendus/cas1_syndrome_revue_medecin_HITL.png) |
| **Rapport Final** | ![Cas 1 Final](./screenshots/tests_attendus/cas1_syndrome_rapport_final.png) |

### Cas 2 : Red Flags (Urgence)
| Étape | Capture d'écran |
| :--- | :--- |
| **Détection** | ![Cas 2 Start](./screenshots/tests_attendus/cas2_redflags_cas_initial.png) |
| **Questions/Réponses** | ![Cas 2 Q/R](./screenshots/tests_attendus/cas2_redflags_questions_reponses.png) |
| **Revue Médecin (HITL)** | ![Cas 2 HITL](./screenshots/tests_attendus/cas2_redflags_revue_medecin_HITL.png) |
| **Rapport Urgence** | ![Cas 2 Final](./screenshots/tests_attendus/cas2_redflags_rapport_final.png) |

### Cas 3 : Cas Bénin
| Étape | Capture d'écran |
| :--- | :--- |
| **Synthèse** | ![Cas 3 Resume](./screenshots/tests_attendus/cas3_benin_cas_initial.png) |
| **Questions/Réponses** | ![Cas 3 Q/R](./screenshots/tests_attendus/cas3_benin_questions_responses.png) |
| **Revue Médecin (HITL)** | ![Cas 3 HITL](./screenshots/tests_attendus/cas3_benin_revue_medecin_HITL.png) |
| **Rapport Final** | ![Cas 3 Final](./screenshots/tests_attendus/cas3_benin_rapport_final.png) |

---

## 🛠️ Installation et Exécution

### 1. Backend (LangGraph & FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.api:app --reload --env-file .env --host 0.0.0.0 --port 8000         
```

### 2. Lancement du serveur de développement (LangGraph Dev)
Pour visualiser et tester le workflow dans LangGraph Studio :
```bash
# Nécessite Docker installé et lancé
pip install langgraph-cli
langgraph dev
```
Cette commande démarrera l'API de développement et fournira un lien vers LangGraph Studio local.

### 3. Serveur MCP (Medical Context)
```bash
cd mcp_server
python mcp_server.py
```

### 4. Frontend (Flutter)
```bash
cd frontend
flutter pub get
flutter run
```
👥 Auteur
Oussama Issib

Note : Ce système est une preuve de concept (PoC) et ne remplace en aucun cas une consultation médicale réelle.
