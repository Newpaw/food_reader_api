import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from run import backend as app  
from src.database import get_db, Base

# Testovací databáze
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Příprava testovací databáze
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_calculate_intake():
    user_info = {
        "user_id": 1,
        "height_cm": 180,
        "weight_kg": 75,
        "age": 25,
        "gender": "male",
        "activity_level": "low"
    }
    response = client.post("/calculate-intake", json=user_info)
    assert response.status_code == 200
    response_json = response.json()
    assert "calories" in response_json
    assert "fat_g" in response_json
    assert "protein_g" in response_json
    assert "sugar_g" in response_json
    assert response_json["calories"] > 0
    assert response_json["fat_g"] >= 0
    assert response_json["protein_g"] >= 0
    assert response_json["sugar_g"] >= 0

def test_analyze_image(mocker):
    mock_openai_client = mocker.patch("src.routes.OpenAIClient")
    mock_openai_client.return_value.create_thread.return_value.id = "test_thread_id"
    mock_openai_client.return_value.upload_file.return_value = "test_file_id"
    mock_openai_client.return_value.create_message.return_value = None
    mock_openai_client.return_value.create_and_poll_run.return_value.status = "completed"
    mock_openai_client.return_value.list_messages.return_value.data[0].content[0].text.value = '''
    {
        "certainty": 0.9,
        "food_name": "Apple",
        "calories_Kcal": 52,
        "fat_in_g": 0.2,
        "protein_in_g": 0.3,
        "sugar_in_g": 10.4
    }
    '''

    file_path = "test_image.jpg"
    with open(file_path, "wb") as f:
        f.write(os.urandom(1024))  # Vytvoříme náhodný soubor pro testování

    with open(file_path, "rb") as f:
        response = client.post("/analyze-image", files={"file": f})

    os.remove(file_path)  # Uklidíme po sobě

    assert response.status_code == 200
    json_response = response.json()
    assert json_response["food_name"] == "Apple"
    assert json_response["calories_Kcal"] == 52
    assert json_response["certainty"] == 0.9

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Příprava před spuštěním testů
    Base.metadata.create_all(bind=engine)
    yield
    # Úklid po testech
    Base.metadata.drop_all(bind=engine)
