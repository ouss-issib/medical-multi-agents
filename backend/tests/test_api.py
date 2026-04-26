import sys
import os
import pytest
from fastapi.testclient import TestClient

# 1. Add the parent directory (backend) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. Now the import will work regardless of where you run pytest
from app.api import app

client = TestClient(app)

# ... (rest of your test code)


def test_full_consultation_workflow():
    # 1. POST /sessions/start
    response = client.post("/sessions/start")
    assert response.status_code == 200
    thread_id = response.json()["thread_id"]
    assert thread_id is not None

    # 2. POST /consultation/start
    start_payload = {
        "thread_id": thread_id,
        "initial_symptoms": "J'ai une forte fièvre et une toux sèche depuis 3 jours."
    }
    response = client.post("/consultation/start", json=start_payload)
    assert response.status_code == 200
    
    # 3. GET /consultation/{thread_id}
    response = client.get(f"/consultation/{thread_id}")
    assert response.status_code == 200
    state = response.json()["state"]
    
    # Check that we are either looping questions or paused at physician_review
    assert "messages" in state
    assert "question_count" in state
    
    # (Optional Mock) If we assume the graph paused at physician_review for this test:
    # 4. POST /consultation/resume
    resume_payload = {
        "thread_id": thread_id,
        "physician_treatment": "Prescrire du paracétamol et un sirop antitussif. Repos."
    }
    response = client.post("/consultation/resume", json=resume_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

    # 5. GET /consultation/{thread_id}/report
    response = client.get(f"/consultation/{thread_id}/report")
    assert response.status_code == 200
    report_data = response.json()
    assert "report" in report_data
    
    # Verify the mandatory ethical disclaimer is present
    assert "Ce système ne remplace pas une consultation médicale." in report_data["report"]