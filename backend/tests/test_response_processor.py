import pytest
from fastapi import HTTPException
from src.response_processor import ResponseProcessor

def test_process_response_valid():
    content = '''
    {
        "certainty": 0.9,
        "food_name": "Apple",
        "calories_Kcal": 52,
        "fat_in_g": 0.2,
        "protein_in_g": 0.3,
        "sugar_in_g": 10.4
    }
    '''
    result = ResponseProcessor.process_response(content)
    assert result.food_name == "Apple"
    assert result.calories_Kcal == 52
    assert result.certainty == 0.9
    assert result.fat_in_g == 0.2
    assert result.protein_in_g == 0.3
    assert result.sugar_in_g == 10.4

def test_process_response_invalid_json():
    content = '''
    { "food_name": "Apple"
    '''
    with pytest.raises(HTTPException) as excinfo:
        ResponseProcessor.process_response(content)
    assert excinfo.value.status_code == 422
    assert "Invalid JSON format" in excinfo.value.detail

def test_process_response_invalid_value():
    content = '''
    {
        "certainty": 0.9,
        "food_name": "Apple",
        "calories_Kcal": "fifty two",
        "fat_in_g": 0.2,
        "protein_in_g": 0.3,
        "sugar_in_g": 10.4
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
    assert "Field 'fat_in_g' is missing" in excinfo.value.detail

def test_process_response_extra_text():
    content = '''
    ERROR: Some error message
    {
        "certainty": 0.9,
        "food_name": "Apple",
        "calories_Kcal": 52,
        "fat_in_g": 0.2,
        "protein_in_g": 0.3,
        "sugar_in_g": 10.4
    }
    INFO: Some info message
    '''
    result = ResponseProcessor.process_response(content)
    assert result.food_name == "Apple"
    assert result.calories_Kcal == 52
    assert result.certainty == 0.9
    assert result.fat_in_g == 0.2
    assert result.protein_in_g == 0.3
    assert result.sugar_in_g == 10.4
