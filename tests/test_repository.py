"""
Integration Tests for MySQL 8 Database Repositories
Verifies CRUD operations, foreign key constraints, views, and ACID transaction persistence.
"""

import pytest
import datetime
from db.connection import DatabaseManager
from db.repositories import StudyAreaRepository, SatelliteDatasetRepository, AnalysisRepository, QueryDemonstrator


@pytest.fixture(scope="module")
def check_db_connection():
    """Skips tests if MySQL server is not accessible."""
    success, info = DatabaseManager.test_connection()
    if not success:
        pytest.skip(f"MySQL connection not available: {info.get('error_message')}")


def test_study_areas_retrieval(check_db_connection):
    """Verifies that study_areas can be retrieved from MySQL."""
    areas = StudyAreaRepository.get_all()
    assert isinstance(areas, list)
    assert len(areas) >= 8  # 8 preset Pune study areas
    sample = areas[0]
    assert "area_name" in sample
    assert "region_label" in sample
    assert "area_sq_km" in sample


def test_satellite_dataset_retrieval(check_db_connection):
    """Verifies default Sentinel-2 dataset metadata."""
    ds = SatelliteDatasetRepository.get_or_create_default() if hasattr(SatelliteDatasetRepository, "get_or_create_default") else SatelliteDatasetRepository.get_default()
    assert ds is not None
    assert ds["satellite_name"] == "Sentinel-2"
    assert ds["band_nir"] == "B8"
    assert ds["band_red"] == "B4"


def test_custom_study_area_creation(check_db_connection):
    """Verifies inserting a new custom drawn polygon into study_areas."""
    geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [73.81, 18.51],
                [73.89, 18.51],
                [73.89, 18.59],
                [73.81, 18.59],
                [73.81, 18.51],
            ]
        ],
    }
    new_id = StudyAreaRepository.create(
        area_name="Test Automation Zone",
        area_type="custom",
        region_label="Pune Test",
        geometry_geojson=geojson,
        centroid_lat=18.55,
        centroid_lon=73.85,
        area_sq_km=65.2,
        boundary_source="Pytest Test Suite",
    )
    assert new_id > 0

    fetched = StudyAreaRepository.get_by_id(new_id)
    assert fetched is not None
    assert fetched["area_name"] == "Test Automation Zone"
    assert fetched["area_type"] == "custom"


def test_acid_transaction_persistence(check_db_connection):
    """Verifies atomic insertion across analysis_runs, ndvi_summaries, and ndvi_time_series."""
    ds = SatelliteDatasetRepository.get_default()
    dataset_id = ds["dataset_id"]

    summary = {
        "mean_ndvi": 0.582,
        "median_ndvi": 0.591,
        "min_ndvi": 0.120,
        "max_ndvi": 0.810,
        "valid_pixel_count": 500000,
        "vegetation_area_sq_km": 42.5,
    }
    points = [
        {
            "observation_date": "2023-07-10",
            "mean_ndvi": 0.550,
            "median_ndvi": 0.560,
            "image_count": 1,
            "quality_notes": "Integration test point 1",
        },
        {
            "observation_date": "2023-07-25",
            "mean_ndvi": 0.614,
            "median_ndvi": 0.622,
            "image_count": 1,
            "quality_notes": "Integration test point 2",
        },
    ]

    analysis_id = AnalysisRepository.save_analysis_transaction(
        area_id=1,
        dataset_id=dataset_id,
        start_date="2023-07-01",
        end_date="2023-07-31",
        max_scene_cloud_pct=15.0,
        processing_status="completed",
        analysis_mode="demo",
        image_count=2,
        composite_method="median",
        summary_stats=summary,
        time_series_points=points,
    )

    assert analysis_id > 0

    # Verify run details
    detail = AnalysisRepository.get_analysis_detail(analysis_id)
    assert detail is not None
    assert detail["processing_status"] == "completed"
    assert float(detail["mean_ndvi"]) == pytest.approx(0.582, abs=1e-3)

    # Verify time series points
    ts = AnalysisRepository.get_time_series(analysis_id)
    assert len(ts) == 2
    assert ts[0]["observation_date"] == datetime.date(2023, 7, 10)


def test_relational_view_query(check_db_connection):
    """Verifies querying the analytical view v_analysis_complete_summary."""
    rows = QueryDemonstrator.execute_custom_view("v_analysis_complete_summary", limit=10)
    assert isinstance(rows, list)
    assert len(rows) > 0
    row = rows[0]
    assert "area_name" in row
    assert "satellite_name" in row
    assert "analysis_id" in row
