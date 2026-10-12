"""
Analysis Orchestration Service
Coordinates execution between GEE/Demo pipelines and handles ACID persistence in MySQL.
"""

from typing import Dict, Any, Tuple, Optional
import datetime

from services.gee_service import GEEService
from services.ndvi_service import generate_demo_dataset
from services.geometry_service import GeometryService
from db.repositories import AnalysisRepository, StudyAreaRepository, SatelliteDatasetRepository


class AnalysisService:
    """Orchestrates vegetation analysis workflows."""

    @staticmethod
    def execute_and_persist_analysis(
        area_id: int,
        start_date: str,
        end_date: str,
        max_scene_cloud_pct: float = 20.0,
        force_demo: bool = False,
    ) -> Tuple[bool, str, Optional[int], Optional[Dict[str, Any]]]:
        """
        Validates, executes (real GEE or Demo Mode), and commits analysis to MySQL.
        Returns:
            (success: bool, message: str, analysis_id: Optional[int], result_bundle: Optional[dict])
        """
        # 1. Fetch study area from MySQL
        area = StudyAreaRepository.get_by_id(area_id)
        if not area:
            return False, f"Study area ID {area_id} does not exist in the database.", None, None

        # 2. Date validation
        try:
            d_start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            d_end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return False, "Dates must follow the YYYY-MM-DD format.", None, None

        if d_start >= d_end:
            return False, "Start date must be strictly earlier than end date.", None, None

        if d_start < datetime.date(2015, 6, 23):
            return False, "Sentinel-2 imagery is available only from June 23, 2015 onward.", None, None

        # 3. Geometry parsing
        geom_json = area["geometry_geojson"]
        is_valid, geom_err, geom_dict, area_sq_km, _ = GeometryService.parse_and_validate_geojson(geom_json)
        if not is_valid:
            return False, f"Invalid study area geometry: {geom_err}", None, None

        # 4. Get default satellite dataset record
        default_ds = SatelliteDatasetRepository.get_default()
        dataset_id = default_ds["dataset_id"] if default_ds else 1

        # 5. Decide processing mode (Real GEE vs Demo)
        gee_available = GEEService.is_available() and not force_demo
        tile_url = None

        if gee_available:
            analysis_mode = "real_gee"
            success, err_msg, summary_stats, time_series, tile_url = GEEService.process_ndvi_sentinel2(
                geojson_geometry=geom_dict,
                start_date=start_date,
                end_date=end_date,
                max_cloud_pct=max_scene_cloud_pct,
            )
            if not success:
                # Log failed run in MySQL for DBMS auditing
                AnalysisRepository.save_analysis_transaction(
                    area_id=area_id,
                    dataset_id=dataset_id,
                    start_date=start_date,
                    end_date=end_date,
                    max_scene_cloud_pct=max_scene_cloud_pct,
                    processing_status="failed",
                    analysis_mode=analysis_mode,
                    image_count=0,
                    composite_method="median",
                    summary_stats=None,
                    time_series_points=[],
                    error_message=err_msg,
                )
                return False, f"GEE analysis failed: {err_msg}", None, None

            image_count = summary_stats.get("image_count", 1)
        else:
            # Clean Demo Mode execution
            analysis_mode = "demo"
            summary_stats, time_series = generate_demo_dataset(
                area_name=area["area_name"],
                start_date=start_date,
                end_date=end_date,
                area_sq_km=float(area.get("area_sq_km") or 250.0),
            )
            image_count = len(time_series)

        # 6. Atomic Transaction Persistence in MySQL 8
        analysis_id = AnalysisRepository.save_analysis_transaction(
            area_id=area_id,
            dataset_id=dataset_id,
            start_date=start_date,
            end_date=end_date,
            max_scene_cloud_pct=max_scene_cloud_pct,
            processing_status="completed",
            analysis_mode=analysis_mode,
            image_count=image_count,
            composite_method="median",
            summary_stats=summary_stats,
            time_series_points=time_series,
            error_message=None,
        )

        result_bundle = {
            "analysis_id": analysis_id,
            "area_name": area["area_name"],
            "region_label": area["region_label"],
            "analysis_mode": analysis_mode,
            "summary_stats": summary_stats,
            "time_series": time_series,
            "tile_url": tile_url,
            "image_count": image_count,
        }

        return True, "Analysis completed and saved successfully.", analysis_id, result_bundle
