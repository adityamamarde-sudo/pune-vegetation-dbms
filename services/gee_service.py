"""
Google Earth Engine (GEE) Service Module
Manages GEE authentication, Sentinel-2 image collection filtering,
cloud masking, and NDVI raster calculations.
Gracefully falls back to Demo mode if unauthenticated.
"""

from typing import Dict, Any, Tuple, Optional, List
import datetime
from config import GEEConfig


class GEEService:
    """Interface to Google Earth Engine and Sentinel-2 Surface Reflectance data."""

    _is_initialized: Optional[bool] = None
    _init_error: Optional[str] = None

    @classmethod
    def initialize(cls) -> Tuple[bool, str]:
        """
        Attempts to initialize Earth Engine.
        Returns:
            (success: bool, message: str)
        """
        if cls._is_initialized is not None:
            return cls._is_initialized, cls._init_error or "GEE initialized successfully."

        try:
            import ee
            if GEEConfig.PROJECT_ID:
                ee.Initialize(project=GEEConfig.PROJECT_ID)
            else:
                ee.Initialize()
            cls._is_initialized = True
            cls._init_error = None
            return True, "Connected to Google Earth Engine."
        except Exception as e:
            cls._is_initialized = False
            cls._init_error = str(e)
            return False, f"GEE not initialized ({e}). Application will use Demo Mode."

    @classmethod
    def is_available(cls) -> bool:
        """Checks if Earth Engine API is ready for real satellite operations."""
        if cls._is_initialized is None:
            cls.initialize()
        return bool(cls._is_initialized)

    @classmethod
    def get_status_info(cls) -> Dict[str, Any]:
        """Returns current GEE configuration and runtime status."""
        available = cls.is_available()
        return {
            "available": available,
            "mode": "real_gee" if available else "demo",
            "project_id": GEEConfig.PROJECT_ID or "(None specified)",
            "collection": GEEConfig.COLLECTION_ID,
            "error": cls._init_error if not available else None,
        }

    @classmethod
    def mask_s2_clouds(cls, image):
        """
        Applies Scene Classification Layer (SCL) mask from Sentinel-2 SR
        to filter out clouds, shadows, and cirrus.
        """
        import ee
        scl = image.select("SCL")
        # SCL classes to keep: 4=Vegetation, 5=Not-vegetated, 6=Water, 7=Unclassified, 11=Snow/Ice
        # Classes to mask: 3=Cloud shadows, 8=Cloud medium, 9=Cloud high, 10=Cirrus
        mask = scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10))
        return image.updateMask(mask)

    @classmethod
    def process_ndvi_sentinel2(
        cls,
        geojson_geometry: Dict[str, Any],
        start_date: str,
        end_date: str,
        max_cloud_pct: float = 20.0,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]], Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Runs real Earth Engine NDVI analysis over Sentinel-2 imagery.
        Returns:
            (success, error_msg, summary_stats, time_series_list, map_tile_url)
        """
        if not cls.is_available():
            return False, "Google Earth Engine credentials are not configured.", None, None, None

        import ee
        try:
            # 1. Convert GeoJSON to Earth Engine Geometry
            ee_geom = ee.Geometry(geojson_geometry)

            # 2. Filter Sentinel-2 collection
            s2 = (
                ee.ImageCollection(GEEConfig.COLLECTION_ID)
                .filterBounds(ee_geom)
                .filterDate(start_date, end_date)
                .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", max_cloud_pct))
                .map(cls.mask_s2_clouds)
            )

            image_count = s2.size().getInfo()
            if image_count == 0:
                return False, f"No Sentinel-2 imagery found between {start_date} and {end_date} with cloud cover <= {max_cloud_pct}%.", None, None, None

            # 3. Compute NDVI: (B8 - B4) / (B8 + B4)
            def add_ndvi(img):
                ndvi = img.normalizedDifference(["B8", "B4"]).rename("NDVI")
                return img.addBands(ndvi)

            s2_ndvi = s2.map(add_ndvi)

            # 4. Temporal Median Composite
            composite = s2_ndvi.select("NDVI").median().clip(ee_geom)

            # 5. Spatial Reduction for overall summary stats
            stats = composite.reduceRegion(
                reducer=ee.Reducer.mean().combine(
                    ee.Reducer.median(), sharedInputs=True
                ).combine(
                    ee.Reducer.minMax(), sharedInputs=True
                ).combine(
                    ee.Reducer.count(), sharedInputs=True
                ),
                geometry=ee_geom,
                scale=20,
                maxPixels=1e8,
            ).getInfo()

            mean_val = stats.get("NDVI_mean")
            med_val = stats.get("NDVI_median")
            min_val = stats.get("NDVI_min")
            max_val = stats.get("NDVI_max")
            count_val = stats.get("NDVI_count", 0)

            summary = {
                "mean_ndvi": round(float(mean_val), 6) if mean_val is not None else None,
                "median_ndvi": round(float(med_val), 6) if med_val is not None else None,
                "min_ndvi": round(float(min_val), 6) if min_val is not None else None,
                "max_ndvi": round(float(max_val), 6) if max_val is not None else None,
                "valid_pixel_count": int(count_val) if count_val else 0,
                "vegetation_area_sq_km": None,
                "image_count": image_count,
            }

            # 6. Generate Tile URL for Folium Map Display
            vis_params = {
                "min": 0.0,
                "max": 0.8,
                "palette": ["#d7191c", "#fdae61", "#ffffbf", "#a6d96a", "#1a9641"],
            }
            map_id = composite.getMapId(vis_params)
            tile_url = map_id["tile_fetcher"].url_format

            # 7. Time series extraction per date
            # Aggregate by distinct observation dates
            time_series = []
            dates_list = s2_ndvi.aggregate_array("system:time_start").getInfo()
            unique_dates = sorted(list(set(
                datetime.datetime.fromtimestamp(ts / 1000.0, tz=datetime.timezone.utc).strftime("%Y-%m-%d")
                for ts in dates_list
            )))

            # Sample up to 8 evenly distributed observation dates for rapid interactive response
            step = max(1, len(unique_dates) // 8)
            sampled_dates = unique_dates[::step][:8]

            for d_str in sampled_dates:
                d_obj = datetime.datetime.strptime(d_str, "%Y-%m-%d").date()
                d_next = (d_obj + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                single_pass = s2_ndvi.filterDate(d_str, d_next).select("NDVI").mean().clip(ee_geom)
                pt_stat = single_pass.reduceRegion(
                    reducer=ee.Reducer.mean(), geometry=ee_geom, scale=30, maxPixels=1e7
                ).getInfo()
                pt_mean = pt_stat.get("NDVI")
                if pt_mean is not None:
                    time_series.append({
                        "observation_date": d_str,
                        "mean_ndvi": round(float(pt_mean), 6),
                        "median_ndvi": round(float(pt_mean), 6),
                        "image_count": 1,
                        "quality_notes": "Sentinel-2 L2A Surface Reflectance",
                    })

            return True, "", summary, time_series, tile_url

        except Exception as e:
            return False, f"GEE Processing Exception: {e}", None, None, None

    @classmethod
    def get_tile_url(
        cls,
        geojson_geometry: Dict[str, Any],
        start_date: str,
        end_date: str,
        max_cloud_pct: float = 20.0,
        min_val: float = 0.0,
        max_val: float = 0.8,
    ) -> Optional[str]:
        """Generates real-time GEE tile fetcher URL for live Folium map display."""
        if not cls.is_available():
            return None
        import ee
        try:
            ee_geom = ee.Geometry(geojson_geometry)
            s2 = (
                ee.ImageCollection(GEEConfig.COLLECTION_ID)
                .filterBounds(ee_geom)
                .filterDate(start_date, end_date)
                .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", max_cloud_pct))
                .map(cls.mask_s2_clouds)
            )
            composite = s2.select(["B8", "B4"]).median()
            ndvi = composite.normalizedDifference(["B8", "B4"]).clip(ee_geom)
            vis_params = {
                "min": min_val,
                "max": max_val,
                "palette": ["#d7191c", "#fdae61", "#ffffbf", "#a6d96a", "#1a9641"],
            }
            map_id = ndvi.getMapId(vis_params)
            return map_id["tile_fetcher"].url_format
        except Exception:
            return None

