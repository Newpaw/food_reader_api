import pytest
from fastapi import HTTPException
from src.response_processor import ResponseProcessor

def test_process_response_valid():
    content = '''
    {
        "certainty": 0.9,
        "food_name": "Apple",
        "calories_Kcal": "52",
        "food_composition": {
            "fat_in_g": "0.2",
            "protein_in_g": "0.3",
            "sugar_in_g": "10.4"
        }
    }
    '''
    result = ResponseProcessor.process_response(content)
    assert result.food_name == "Apple"
    assert result.calories_Kcal == 52
    assert result.certainty == 0.9
    assert result.food_composition.fat_in_g == 0.2
    assert result.food_composition.protein_in_g == 0.3
    assert result.food_composition.sugar_in_g == 10.4

def test_process_response_invalid_json():
    content = '''
    { "food_name": "Apple"
    '''
    with pytest.raises(HTTPException) as excinfo:
        ResponseProcessor.process_response(content)
    assert excinfo.value.status_code == 422
    assert excinfo.value.detail == "Invalid JSON format"

def test_process_response_invalid_value():
    content = '''
    {
        "certainty": 0.9,
        "food_name": "Apple",
        "calories_Kcal": "fifty two",
        "food_composition": {
            "fat_in_g": "0.2",
            "protein_in_g": "0.3",
            "sugar_in_g": "10.4"
        }
    }
    '''
    with pytest.raises(HTTPException) as excinfo:
        ResponseProcessor.process_response(content)
    assert excinfo.value.status_code == 422
    assert "not of type" in excinfo.value.detail

def test_process_response_missing_field():
    content = '''
    {
        "certainty": 0.9,
        "food_name": "Apple",
        "calories_Kcal": 52
    }
    '''
    with pytest.raises(HTTPException) as excinfo:
        ResponseProcessor.process_response(content)
    assert excinfo.value.status_code == 422
    assert "is missing" in excinfo.value.detail
