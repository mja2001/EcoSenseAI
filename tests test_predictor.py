import pytest
from backend.models.predictor import predict_co2_spike

def test_normal_prediction():
    prediction, value = predict_co2_spike(500)
    assert prediction == "Normal"
    assert value < 600

def test_spike_prediction():
    prediction, value = predict_co2_spike(700)
    assert prediction == "Spike likely"
    assert value > 600