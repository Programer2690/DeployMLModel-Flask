import pickle
import numpy as np
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)


@pytest.fixture(scope="module")
def feature_names():
    # These match the columns from your hiring.csv
    return ["experience", "test_score", "interview_score"]


def test_model_loads(model):
    assert model is not None


def test_prediction_is_positive_number(model, feature_names):
    # Convert numpy array list to a DataFrame with valid column names
    sample = pd.DataFrame([[2, 9, 6]], columns=feature_names)
    prediction = model.predict(sample)
    salary = float(prediction[0])
    assert salary > 0


def test_prediction_within_realistic_range(model, feature_names):
    # Convert sample to DataFrame to preserve feature names
    sample = pd.DataFrame([[2, 9, 6]], columns=feature_names)
    prediction = model.predict(sample)
    salary = float(prediction[0])
    # Based on hiring.csv's salary scale (roughly 40k-110k range)
    assert 20000 <= salary <= 200000


def test_higher_experience_increases_salary(model, feature_names):
    # Construct both comparisons as DataFrames
    low_sample = pd.DataFrame([[1, 5, 5]], columns=feature_names)
    high_sample = pd.DataFrame([[10, 5, 5]], columns=feature_names)
    
    low = float(model.predict(low_sample)[0])
    high = float(model.predict(high_sample)[0])
    assert high > low