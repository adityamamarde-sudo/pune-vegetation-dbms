"""
Unit Tests for NDVI Computation & Summary Statistics
Verifies mathematical correctness, zero-division safety, and edge cases.
"""

import pytest
import math
from services.ndvi_service import compute_pixel_ndvi, compute_summary_statistics, generate_demo_dataset


def test_ndvi_formula_known_values():
    """Requirement: NIR=0.8 and Red=0.2 should yield 0.6."""
    nir = 0.8
    red = 0.2
    expected = (0.8 - 0.2) / (0.8 + 0.2)  # 0.6 / 1.0 = 0.6
    result = compute_pixel_ndvi(nir, red)
    assert result is not None
    assert math.isclose(result, 0.6, abs_tol=1e-5)


def test_ndvi_formula_edge_bounds():
    """Tests extreme values and boundaries [-1, +1]."""
    # Pure green vegetation: high NIR, zero Red -> NDVI = 1.0
    assert math.isclose(compute_pixel_ndvi(1.0, 0.0), 1.0, abs_tol=1e-5)

    # Water body absorption: low NIR, high Red -> NDVI = -1.0
    assert math.isclose(compute_pixel_ndvi(0.0, 1.0), -1.0, abs_tol=1e-5)

    # Neutral bare soil / concrete: equal reflectance -> NDVI = 0.0
    assert math.isclose(compute_pixel_ndvi(0.4, 0.4), 0.0, abs_tol=1e-5)


def test_ndvi_division_by_zero_and_none():
    """Denominator zero or missing input should safely return None."""
    assert compute_pixel_ndvi(0.0, 0.0) is None
    assert compute_pixel_ndvi(None, 0.5) is None
    assert compute_pixel_ndvi(0.5, None) is None
    assert compute_pixel_ndvi(None, None) is None


def test_summary_statistics_calculation():
    """Tests mean, median, min, max, pixel count, and vegetation area calculation."""
    values = [0.2, 0.4, 0.6, 0.8]
    stats = compute_summary_statistics(values, total_area_sq_km=100.0, vegetation_threshold=0.4)

    assert stats["valid_pixel_count"] == 4
    assert math.isclose(stats["mean_ndvi"], 0.5, abs_tol=1e-5)
    assert math.isclose(stats["median_ndvi"], 0.5, abs_tol=1e-5)
    assert math.isclose(stats["min_ndvi"], 0.2, abs_tol=1e-5)
    assert math.isclose(stats["max_ndvi"], 0.8, abs_tol=1e-5)
    # Values >= 0.4 are [0.4, 0.6, 0.8] -> 3/4 = 75% of 100 km² = 75 km²
    assert math.isclose(stats["vegetation_area_sq_km"], 75.0, abs_tol=1e-2)


def test_summary_empty_values():
    """Empty list returns None values without raising exceptions."""
    stats = compute_summary_statistics([])
    assert stats["mean_ndvi"] is None
    assert stats["valid_pixel_count"] == 0


def test_demo_dataset_generation_labelling():
    """Verifies that demo dataset points are explicitly labelled DEMO DATA."""
    summary, time_series = generate_demo_dataset(
        area_name="Pune Urban",
        start_date="2023-01-01",
        end_date="2023-06-01",
        area_sq_km=250.0,
    )
    assert summary["valid_pixel_count"] > 0
    assert len(time_series) > 0
    for pt in time_series:
        assert "DEMO DATA" in pt["quality_notes"]
        assert -1.0 <= pt["mean_ndvi"] <= 1.0
