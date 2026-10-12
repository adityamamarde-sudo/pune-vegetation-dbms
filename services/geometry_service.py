"""
Geospatial Geometry Service
Provides polygon validation, centroid calculation, and geodesic area computation.
"""

from typing import Dict, Any, Tuple, Optional
import json
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import transform
import pyproj

from config import AppConfig


class GeometryService:
    """Methods for spatial analysis and validation of study area polygons."""

    # Geodesic WGS84 area calculation setup
    _GEOD = pyproj.Geod(ellps="WGS84")

    @classmethod
    def parse_and_validate_geojson(
        cls, geojson_data: Any
    ) -> Tuple[bool, str, Optional[Dict[str, Any]], Optional[float], Optional[Tuple[float, float]]]:
        """
        Validates GeoJSON structure, topology, and size limits.
        Returns:
            (is_valid: bool, error_msg: str, sanitized_geojson: dict, area_sq_km: float, centroid: (lat, lon))
        """
        if not geojson_data:
            return False, "Geometry cannot be empty.", None, None, None

        if isinstance(geojson_data, str):
            try:
                geojson_data = json.loads(geojson_data)
            except Exception as e:
                return False, f"Invalid JSON string: {e}", None, None, None

        # Extract geometry object if passed a Feature or FeatureCollection
        if isinstance(geojson_data, dict):
            if geojson_data.get("type") == "FeatureCollection":
                features = geojson_data.get("features", [])
                if not features:
                    return False, "FeatureCollection is empty.", None, None, None
                geom_dict = features[0].get("geometry", {})
            elif geojson_data.get("type") == "Feature":
                geom_dict = geojson_data.get("geometry", {})
            else:
                geom_dict = geojson_data
        else:
            return False, "Unsupported GeoJSON object type.", None, None, None

        try:
            geom = shape(geom_dict)
        except Exception as e:
            return False, f"Failed to parse geometric shape: {e}", None, None, None

        if not isinstance(geom, (Polygon, MultiPolygon)):
            return False, "Only Polygon and MultiPolygon geometries are supported.", None, None, None

        if geom.is_empty:
            return False, "Geometry is empty.", None, None, None

        if not geom.is_valid:
            return False, "Polygon geometry is topologically invalid (e.g., self-intersecting).", None, None, None

        # Compute geodesic area in square kilometers
        area_sq_m, _ = cls._GEOD.geometry_area_perimeter(geom)
        area_sq_km = round(abs(area_sq_m) / 1e6, 3)

        if area_sq_km < 0.01:
            return False, "Selected area is too small (< 0.01 km²).", None, None, None

        if area_sq_km > AppConfig.MAX_STUDY_AREA_SQ_KM:
            return (
                False,
                f"Selected area ({area_sq_km} km²) exceeds maximum allowed limit ({AppConfig.MAX_STUDY_AREA_SQ_KM} km²).",
                None,
                None,
                None,
            )

        # Centroid (lat, lon)
        centroid = geom.centroid
        centroid_lat = round(centroid.y, 7)
        centroid_lon = round(centroid.x, 7)

        return True, "", geom_dict, area_sq_km, (centroid_lat, centroid_lon)

    @classmethod
    def compute_polygon_area_sq_km(cls, geom_dict: Dict[str, Any]) -> float:
        """Computes approximate area in km² for a valid GeoJSON geometry."""
        geom = shape(geom_dict)
        area_sq_m, _ = cls._GEOD.geometry_area_perimeter(geom)
        return round(abs(area_sq_m) / 1e6, 3)
