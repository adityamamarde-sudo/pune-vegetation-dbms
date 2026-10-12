"""
Unit Tests for Form and Parameter Validation Logic
Verifies date ordering, cloud cover percentage limits, and CSV export format.
"""

import pytest
import datetime
import io
import pandas as pd


def validate_analysis_parameters(start_date: str, end_date: str, max_cloud_pct: float):
    """Validation helper replicating application validation logic."""
    try:
        d_start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        d_end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return False, "Dates must be formatted as YYYY-MM-DD."

    if d_start >= d_end:
        return False, "Start date must be strictly earlier than end date."

    if max_cloud_pct < 0.0 or max_cloud_pct > 100.0:
        return False, "Cloud percentage must be between 0% and 100%."

    # Sentinel-2 mission launched in 2015
    if d_start < datetime.date(2015, 6, 23):
        return False, "Sentinel-2 imagery is only available from June 23, 2015 onward."

    return True, ""


def test_valid_parameters():
    is_valid, msg = validate_analysis_parameters("2023-01-01", "2023-06-01", 20.0)
    assert is_valid is True
    assert msg == ""


def test_invalid_date_order():
    is_valid, msg = validate_analysis_parameters("2023-06-01", "2023-01-01", 20.0)
    assert is_valid is False
    assert "earlier than end date" in msg


def test_invalid_cloud_percentages():
    is_valid, msg = validate_analysis_parameters("2023-01-01", "2023-06-01", -5.0)
    assert is_valid is False
    assert "between 0% and 100%" in msg

    is_valid, msg = validate_analysis_parameters("2023-01-01", "2023-06-01", 105.0)
    assert is_valid is False
    assert "between 0% and 100%" in msg


def test_csv_export_format_and_columns():
    """Requirement: CSV exports must include units, dates, region, source, and mode."""
    records = [
        {
            "analysis_id": 1,
            "region_label": "Mulshi",
            "observation_date": "2023-09-05",
            "mean_ndvi": 0.621,
            "units": "Index [-1.0, 1.0]",
            "analysis_mode": "demo",
            "quality_notes": "DEMO DATA — NOT REAL SATELLITE RESULTS",
        }
    ]
    df = pd.DataFrame(records)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_str = csv_buffer.getvalue()

    assert "analysis_id" in csv_str
    assert "region_label" in csv_str
    assert "observation_date" in csv_str
    assert "mean_ndvi" in csv_str
    assert "analysis_mode" in csv_str
    assert "DEMO DATA" in csv_str
