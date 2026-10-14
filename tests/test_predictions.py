"""
Unit and Integration Tests for PredictionService and PredictionRepository
"""

import datetime
import pytest
from services.prediction_service import PredictionService
from db.repositories import PredictionRepository, StudyAreaRepository
from db.connection import DatabaseManager


@pytest.fixture(scope="module")
def check_db_connection():
    success, info = DatabaseManager.test_connection()
    if not success:
        pytest.skip(f"MySQL connection not available: {info.get('error_message')}")


def test_historical_insights_analysis():
    sample_series = [
        {"observation_date": "2023-06-01", "mean_ndvi": 0.28},
        {"observation_date": "2023-07-15", "mean_ndvi": 0.52},  # Big surge (+0.24)
        {"observation_date": "2023-09-15", "mean_ndvi": 0.78},  # Peak
        {"observation_date": "2023-11-15", "mean_ndvi": 0.44},  # Big drop (-0.34)
    ]

    res = PredictionService.analyze_historical_insights(sample_series, area_name="Pune Test Area")
    assert "events" in res
    assert "anomalies" in res
    assert "summary" in res

    summary = res["summary"]
    assert summary["historical_peak_ndvi"] == 0.78
    assert summary["historical_peak_date"] == "2023-09-15"
    assert summary["historical_trough_ndvi"] == 0.28
    assert summary["historical_trough_date"] == "2023-06-01"

    # Verify at least one surge event and one drop event were detected
    event_types = [e["event_type"] for e in res["events"]]
    assert any("Surge" in et for et in event_types)
    assert any("Drop" in et for et in event_types)


def test_ml_forecast_generation():
    sample_series = [
        {"observation_date": "2023-06-01", "mean_ndvi": 0.30},
        {"observation_date": "2023-07-15", "mean_ndvi": 0.50},
        {"observation_date": "2023-09-15", "mean_ndvi": 0.75},
        {"observation_date": "2023-11-15", "mean_ndvi": 0.45},
    ]

    fc = PredictionService.generate_ml_forecast(sample_series, horizon_months=6, base_mean=0.50)
    assert "forecast_points" in fc
    assert len(fc["forecast_points"]) > 0
    assert "projected_mean_ndvi" in fc
    assert "rmse" in fc

    for pt in fc["forecast_points"]:
        assert "forecast_date" in pt
        assert "predicted_ndvi" in pt
        assert "lower_confidence_ndvi" in pt
        assert "upper_confidence_ndvi" in pt
        assert pt["lower_confidence_ndvi"] <= pt["predicted_ndvi"] <= pt["upper_confidence_ndvi"]
        assert 0.0 <= pt["predicted_ndvi"] <= 1.0


def test_climate_stress_simulation():
    sample_forecast = [
        {"forecast_date": "2024-06-15", "predicted_ndvi": 0.45, "month_name": "June 2024"},
        {"forecast_date": "2024-07-15", "predicted_ndvi": 0.65, "month_name": "July 2024"},
        {"forecast_date": "2024-08-15", "predicted_ndvi": 0.75, "month_name": "August 2024"},
        {"forecast_date": "2024-09-15", "predicted_ndvi": 0.70, "month_name": "September 2024"},
    ]

    sim = PredictionService.simulate_climate_stress(
        baseline_forecast=sample_forecast,
        total_area_sq_km=250.0,
        drought_deficit_pct=35.0,
        temp_anomaly_deg_c=2.5,
        extreme_rainfall_pct=0.0,
    )

    metrics = sim["metrics"]
    assert metrics["mean_stressed_ndvi"] < metrics["mean_baseline_ndvi"]
    assert metrics["net_ndvi_drop"] > 0
    assert metrics["projected_lost_area_km2"] > 0
    assert metrics["vulnerability_score"] > 0
    assert metrics["risk_tier"] in ("MODERATE", "SEVERE", "CRITICAL")


def test_prediction_repository_persistence(check_db_connection):
    areas = StudyAreaRepository.get_all()
    assert len(areas) > 0
    area_id = areas[0]["area_id"]

    sim_pts = [
        {"forecast_date": "2024-06-15", "stressed_ndvi": 0.35, "lower_confidence_ndvi": 0.25, "upper_confidence_ndvi": 0.45},
        {"forecast_date": "2024-07-15", "stressed_ndvi": 0.48, "lower_confidence_ndvi": 0.38, "upper_confidence_ndvi": 0.58},
    ]

    scenario_id = PredictionRepository.save_scenario(
        area_id=area_id,
        base_analysis_id=None,
        scenario_title="Automated PyTest Severe Drought Simulation",
        scenario_type="drought_stress",
        forecast_horizon_months=6,
        projected_mean_ndvi=0.4150,
        vegetation_loss_sq_km=45.20,
        vulnerability_score=62.5,
        risk_level="SEVERE",
        simulation_parameters={"drought_deficit_pct": 35.0},
        forecast_points=sim_pts,
    )

    assert scenario_id > 0

    # Retrieve and verify detail
    detail = PredictionRepository.get_scenario_detail(scenario_id)
    assert detail is not None
    assert detail["scenario_id"] == scenario_id
    assert detail["risk_level"] == "SEVERE"
    assert len(detail["points"]) == 2
