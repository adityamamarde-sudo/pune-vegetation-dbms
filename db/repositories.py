"""
Data Access Repository Layer
Encapsulates all SQL interactions using parameterized queries and ACID transactions.
"""

import json
from typing import List, Dict, Any, Optional, Tuple
from db.connection import DatabaseManager


class StudyAreaRepository:
    """Data access methods for study_areas table."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT area_id, area_name, area_type, region_label,
                           geometry_geojson, centroid_lat, centroid_lon,
                           area_sq_km, boundary_source, created_at
                    FROM study_areas
                    ORDER BY area_name ASC;
                    """
                )
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_by_id(area_id: int) -> Optional[Dict[str, Any]]:
        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT area_id, area_name, area_type, region_label,
                           geometry_geojson, centroid_lat, centroid_lon,
                           area_sq_km, boundary_source, created_at
                    FROM study_areas
                    WHERE area_id = %s;
                    """,
                    (area_id,),
                )
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def create(
        area_name: str,
        area_type: str,
        region_label: str,
        geometry_geojson: Any,
        centroid_lat: Optional[float],
        centroid_lon: Optional[float],
        area_sq_km: Optional[float],
        boundary_source: Optional[str] = "User Drawn Custom Polygon",
    ) -> int:
        geojson_str = (
            json.dumps(geometry_geojson)
            if isinstance(geometry_geojson, (dict, list))
            else str(geometry_geojson)
        )

        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO study_areas (
                        area_name, area_type, region_label, geometry_geojson,
                        centroid_lat, centroid_lon, area_sq_km, boundary_source
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        area_name,
                        area_type,
                        region_label,
                        geojson_str,
                        centroid_lat,
                        centroid_lon,
                        area_sq_km,
                        boundary_source,
                    ),
                )
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()


class SatelliteDatasetRepository:
    """Data access methods for satellite_datasets table."""

    @staticmethod
    def get_default() -> Optional[Dict[str, Any]]:
        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT dataset_id, provider, collection_id, satellite_name,
                           sensor, band_nir, band_red, processing_notes
                    FROM satellite_datasets
                    LIMIT 1;
                    """
                )
                return cursor.fetchone()
        finally:
            conn.close()


class AnalysisRepository:
    """Data access methods for analysis_runs, summaries, and time series."""

    @staticmethod
    def get_recent_runs(limit: int = 20) -> List[Dict[str, Any]]:
        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        ar.analysis_id,
                        sa.area_name,
                        sa.region_label,
                        ar.start_date,
                        ar.end_date,
                        ar.max_scene_cloud_pct,
                        ar.processing_status,
                        ar.analysis_mode,
                        ar.image_count,
                        ar.composite_method,
                        ns.mean_ndvi,
                        ns.median_ndvi,
                        ns.min_ndvi,
                        ns.max_ndvi,
                        ar.created_at
                    FROM analysis_runs ar
                    JOIN study_areas sa ON ar.area_id = sa.area_id
                    LEFT JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
                    ORDER BY ar.created_at DESC, ar.analysis_id DESC
                    LIMIT %s;
                    """,
                    (limit,),
                )
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_analysis_detail(analysis_id: int) -> Optional[Dict[str, Any]]:
        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        ar.analysis_id,
                        ar.area_id,
                        sa.area_name,
                        sa.region_label,
                        sa.area_sq_km,
                        sa.geometry_geojson,
                        sd.satellite_name,
                        sd.collection_id,
                        ar.start_date,
                        ar.end_date,
                        ar.max_scene_cloud_pct,
                        ar.processing_status,
                        ar.analysis_mode,
                        ar.image_count,
                        ar.composite_method,
                        ar.error_message,
                        ar.created_at,
                        ns.mean_ndvi,
                        ns.median_ndvi,
                        ns.min_ndvi,
                        ns.max_ndvi,
                        ns.valid_pixel_count,
                        ns.vegetation_area_sq_km
                    FROM analysis_runs ar
                    JOIN study_areas sa ON ar.area_id = sa.area_id
                    JOIN satellite_datasets sd ON ar.dataset_id = sd.dataset_id
                    LEFT JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
                    WHERE ar.analysis_id = %s;
                    """,
                    (analysis_id,),
                )
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_time_series(analysis_id: int) -> List[Dict[str, Any]]:
        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT point_id, observation_date, mean_ndvi, median_ndvi,
                           image_count, quality_notes
                    FROM ndvi_time_series
                    WHERE analysis_id = %s
                    ORDER BY observation_date ASC;
                    """,
                    (analysis_id,),
                )
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def save_analysis_transaction(
        area_id: int,
        dataset_id: int,
        start_date: str,
        end_date: str,
        max_scene_cloud_pct: float,
        processing_status: str,
        analysis_mode: str,
        image_count: int,
        composite_method: str,
        summary_stats: Optional[Dict[str, Any]],
        time_series_points: List[Dict[str, Any]],
        error_message: Optional[str] = None,
    ) -> int:
        """
        Demonstrates a complete ACID Transaction:
        Inserts into analysis_runs, ndvi_summaries, and ndvi_time_series atomically.
        """
        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                # 1. Insert analysis run
                cursor.execute(
                    """
                    INSERT INTO analysis_runs (
                        area_id, dataset_id, start_date, end_date, max_scene_cloud_pct,
                        processing_status, analysis_mode, image_count, composite_method, error_message
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        area_id,
                        dataset_id,
                        start_date,
                        end_date,
                        max_scene_cloud_pct,
                        processing_status,
                        analysis_mode,
                        image_count,
                        composite_method,
                        error_message,
                    ),
                )
                analysis_id = cursor.lastrowid

                # 2. Insert summary stats if available
                if summary_stats and processing_status == "completed":
                    cursor.execute(
                        """
                        INSERT INTO ndvi_summaries (
                            analysis_id, mean_ndvi, median_ndvi, min_ndvi, max_ndvi,
                            valid_pixel_count, vegetation_area_sq_km
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s);
                        """,
                        (
                            analysis_id,
                            summary_stats.get("mean_ndvi"),
                            summary_stats.get("median_ndvi"),
                            summary_stats.get("min_ndvi"),
                            summary_stats.get("max_ndvi"),
                            summary_stats.get("valid_pixel_count"),
                            summary_stats.get("vegetation_area_sq_km"),
                        ),
                    )

                # 3. Insert time series records
                if time_series_points and processing_status == "completed":
                    ts_sql = """
                        INSERT INTO ndvi_time_series (
                            analysis_id, observation_date, mean_ndvi, median_ndvi, image_count, quality_notes
                        ) VALUES (%s, %s, %s, %s, %s, %s);
                    """
                    ts_params = [
                        (
                            analysis_id,
                            pt["observation_date"],
                            pt["mean_ndvi"],
                            pt.get("median_ndvi"),
                            pt.get("image_count", 1),
                            pt.get("quality_notes"),
                        )
                        for pt in time_series_points
                    ]
                    cursor.executemany(ts_sql, ts_params)

                # Commit transaction
                conn.commit()
                return analysis_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


class QueryDemonstrator:
    """Executes the pre-defined course SQL queries for UI and report demonstration."""

    @staticmethod
    def execute_custom_view(view_name: str = "v_analysis_complete_summary", limit: int = 50) -> List[Dict[str, Any]]:
        # Safe parameterized view query
        allowed_views = ["v_analysis_complete_summary", "v_area_performance_summary"]
        if view_name not in allowed_views:
            raise ValueError(f"Unauthorized view: {view_name}")

        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {view_name} LIMIT %s;", (limit,))
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_dashboard_counts() -> Dict[str, Any]:
        """Fetches total counts for the main dashboard cards."""
        conn = DatabaseManager.get_raw_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) AS total_areas FROM study_areas;")
                total_areas = cursor.fetchone()["total_areas"]

                cursor.execute("SELECT COUNT(*) AS total_runs FROM analysis_runs;")
                total_runs = cursor.fetchone()["total_runs"]

                cursor.execute(
                    """
                    SELECT ar.analysis_id, sa.area_name, ar.analysis_mode, ar.created_at, ns.mean_ndvi
                    FROM analysis_runs ar
                    JOIN study_areas sa ON ar.area_id = sa.area_id
                    LEFT JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
                    WHERE ar.processing_status = 'completed'
                    ORDER BY ar.created_at DESC
                    LIMIT 1;
                    """
                )
                latest_run = cursor.fetchone()

                return {
                    "total_areas": total_areas,
                    "total_runs": total_runs,
                    "latest_run": latest_run,
                }
        finally:
            conn.close()
