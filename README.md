# 🩺 Assistant Médical Intelligent - Multi-Agents & HITL

Ce projet est un système d'assistance à la consultation médicale basé sur une architecture multi-agents utilisant **LangGraph**. Il permet d'automatiser l'interrogatoire patient, de synthétiser les cas cliniques et de générer des rapports médicaux professionnels, tout en garantissant un contrôle humain strict (**Human-in-the-loop**).

## 🚀 Fonctionnalités Clés
- **Orchestration Agentique** : Un `Supervisor` central gérant des agents spécialisés (Diagnostic, Review, Report).
- **Interrogatoire Dynamique** : Cycle de 5 questions adaptatives basées sur les symptômes initiaux du patient.
- **Human-in-the-Loop (HITL)** : Interruption forcée du flux pour validation médicale avant toute conclusion ou génération de rapport.
- **Rapports Anonymisés** : Génération automatique de documents professionnels au format Markdown.
- **Interface Moderne** : Application Flutter suivant une charte graphique médicale soignée (Teal & Slate).

---

## 🛠️ Architecture Technique

Le système repose sur un graphe d'état (`StateGraph`) complexe qui gère la logique métier et la persistance des données :

1. **Supervisor** : Le cerveau central qui analyse l'état et route vers l'agent approprié.
2. **Diagnostic Agent** : Analyse les réponses, pose des questions de suivi et suggère des hypothèses cliniques.
3. **Physician Review** : Nœud de pause critique attendant l'approbation et le traitement du médecin.
4. **Report Agent** : Agent final responsable de la mise en forme du dossier médical.

---

## 📦 Installation et Configuration

### 1. Prérequis
- Flutter & Dart (dernière version stable)
- Python 3.10+
- Clé API OpenAI
- Clé API LangChain (pour le tracing et LangGraph Studio)

### 2. Backend (Python & LangGraph)
```bash
cd backend
python -m venv .venv
# Activation sur Windows
.venv\Scripts\activate
# Installation des dépendances
pip install -r requirements.txt
Créez un fichier .env dans le dossier backend :

Code snippet
OPENAI_API_KEY=votre_cle_openai
LANGCHAIN_API_KEY=votre_cle_langsmith
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="Medical-Assistant-MultiAgents"
3. Frontend (Flutter)
Bash
cd frontend
flutter pub get
🏃 Exécution
Démarrer le Backend (FastAPI)
Bash
cd backend
uvicorn app.main:app --reload
Démarrer le Frontend (Flutter)
Bash
cd frontend
flutter run
Visualisation dans LangGraph Studio
Ouvrez l'application LangGraph Studio.

Sélectionnez le dossier backend.

Le graphe s'affichera automatiquement, vous permettant de tester les interruptions en temps réel.

🧪 Jeux de Tests Validés
Le système a été validé sur trois scénarios critiques :

Cas 1 : Syndrome respiratoire simple (Infection virale classique).

Cas 2 : Red Flags / Urgence (Suspicion de Syndrome Coronarien Aigu).

Cas 3 : Cas Bénin (Céphalée de tension liée à la fatigue).

👥 Auteur
Projet réalisé dans le cadre du TP Multi-Agents - Agentic AI.