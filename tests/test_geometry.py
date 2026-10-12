"""
Unit Tests for Polygon Geometry Validation and Geodesic Area Calculations
"""

import pytest
from services.geometry_service import GeometryService


def test_valid_polygon_geometry():
    """Tests standard rectangular polygon bounding box."""
    geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [73.80, 18.50],
                [73.90, 18.50],
                [73.90, 18.60],
                [73.80, 18.60],
                [73.80, 18.50],
            ]
        ],
    }
    is_valid, err, geom, area_km2, centroid = GeometryService.parse_and_validate_geojson(geojson)
    assert is_valid is True
    assert err == ""
    assert area_km2 > 0.0
    # Approximate ~10km x ~11km ~ 110-120 km²
    assert 90.0 < area_km2 < 140.0
    assert centroid is not None
    assert 18.50 <= centroid[0] <= 18.60
    assert 73.80 <= centroid[1] <= 73.90


def test_empty_or_null_geometry():
    """Empty or None geometry must be rejected with helpful message."""
    is_valid, err, _, _, _ = GeometryService.parse_and_validate_geojson(None)
    assert is_valid is False
    assert "empty" in err.lower()

    is_valid, err, _, _, _ = GeometryService.parse_and_validate_geojson({})
    assert is_valid is False


def test_non_polygon_geometry_rejection():
    """Points and LineStrings should be rejected."""
    point_geojson = {
        "type": "Point",
        "coordinates": [73.8567, 18.5204],
    }
    is_valid, err, _, _, _ = GeometryService.parse_and_validate_geojson(point_geojson)
    assert is_valid is False
    assert "polygon" in err.lower()


def test_area_exceeds_maximum_threshold():
    """Gigantic polygons exceeding configured threshold (5000 km²) must be rejected."""
    # State-level polygon spanning many degrees (> 100,000 km²)
    huge_geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [70.0, 15.0],
                [80.0, 15.0],
                [80.0, 25.0],
                [70.0, 25.0],
                [70.0, 15.0],
            ]
        ],
    }
    is_valid, err, _, _, _ = GeometryService.parse_and_validate_geojson(huge_geojson)
    assert is_valid is False
    assert "exceeds maximum allowed limit" in err
