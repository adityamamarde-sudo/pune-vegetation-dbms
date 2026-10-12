-- ==============================================================================
-- Pune Vegetation Monitoring & Remote-Sensing Database System
-- Required SQL Query Demonstrations for DBMS Course Assessment
--
-- Each query corresponds to a required DBMS category (Section 8 of Specification)
-- and can be executed directly in MySQL Workbench.
-- ==============================================================================

USE pune_vegetation_db;

-- ------------------------------------------------------------------------------
-- 1. FILTERING: Retrieve all analysis runs for a specific study area
-- ------------------------------------------------------------------------------
SELECT
    ar.analysis_id,
    sa.area_name,
    ar.start_date,
    ar.end_date,
    ar.processing_status,
    ar.analysis_mode,
    ar.image_count
FROM analysis_runs ar
JOIN study_areas sa ON ar.area_id = sa.area_id
WHERE sa.region_label = 'Mulshi';

-- ------------------------------------------------------------------------------
-- 2. SORTING: Retrieve latest analysis runs ordered chronologically
-- ------------------------------------------------------------------------------
SELECT
    analysis_id,
    area_id,
    start_date,
    end_date,
    processing_status,
    created_at
FROM analysis_runs
ORDER BY created_at DESC, analysis_id DESC;

-- ------------------------------------------------------------------------------
-- 3. AGGREGATION: Overall aggregate NDVI across all completed analyses
-- ------------------------------------------------------------------------------
SELECT
    COUNT(ns.summary_id) AS total_summaries_evaluated,
    ROUND(AVG(ns.mean_ndvi), 4) AS overall_average_ndvi,
    ROUND(MIN(ns.min_ndvi), 4) AS absolute_minimum_ndvi,
    ROUND(MAX(ns.max_ndvi), 4) AS absolute_maximum_ndvi,
    SUM(ns.valid_pixel_count) AS total_valid_pixels_computed
FROM ndvi_summaries ns
JOIN analysis_runs ar ON ns.analysis_id = ar.analysis_id
WHERE ar.processing_status = 'completed';

-- ------------------------------------------------------------------------------
-- 4. MULTI-TABLE JOIN: Comprehensive relation joining 4 tables
-- (study_areas, analysis_runs, satellite_datasets, ndvi_summaries)
-- ------------------------------------------------------------------------------
SELECT
    ar.analysis_id,
    sa.area_name,
    sa.area_type,
    sd.satellite_name,
    sd.collection_id,
    ar.start_date,
    ar.end_date,
    ns.mean_ndvi,
    ns.median_ndvi,
    ns.vegetation_area_sq_km
FROM analysis_runs ar
INNER JOIN study_areas sa ON ar.area_id = sa.area_id
INNER JOIN satellite_datasets sd ON ar.dataset_id = sd.dataset_id
INNER JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
ORDER BY ns.mean_ndvi DESC;

-- ------------------------------------------------------------------------------
-- 5. GROUP BY: Compare average NDVI across study areas
-- ------------------------------------------------------------------------------
SELECT
    sa.area_name,
    sa.region_label,
    COUNT(ar.analysis_id) AS runs_count,
    ROUND(AVG(ns.mean_ndvi), 4) AS avg_area_ndvi,
    ROUND(AVG(ns.vegetation_area_sq_km), 2) AS avg_veg_area_km2
FROM study_areas sa
JOIN analysis_runs ar ON sa.area_id = ar.area_id
JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
WHERE ar.processing_status = 'completed'
GROUP BY sa.area_id, sa.area_name, sa.region_label
ORDER BY avg_area_ndvi DESC;

-- ------------------------------------------------------------------------------
-- 6. HAVING: Filter aggregated regions whose average NDVI is below a threshold
-- (e.g., Identifying stressed or highly urbanized/low-canopy regions < 0.40)
-- ------------------------------------------------------------------------------
SELECT
    sa.area_name,
    COUNT(ar.analysis_id) AS completed_analyses,
    ROUND(AVG(ns.mean_ndvi), 4) AS avg_vegetation_index
FROM study_areas sa
JOIN analysis_runs ar ON sa.area_id = ar.area_id
JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
WHERE ar.processing_status = 'completed'
GROUP BY sa.area_id, sa.area_name
HAVING AVG(ns.mean_ndvi) < 0.4500
ORDER BY avg_vegetation_index ASC;

-- ------------------------------------------------------------------------------
-- 7. DATE FILTERING: Temporal range filtering on satellite observation dates
-- ------------------------------------------------------------------------------
SELECT
    ts.point_id,
    ar.analysis_id,
    sa.area_name,
    ts.observation_date,
    ts.mean_ndvi,
    ts.quality_notes
FROM ndvi_time_series ts
JOIN analysis_runs ar ON ts.analysis_id = ar.analysis_id
JOIN study_areas sa ON ar.area_id = sa.area_id
WHERE ts.observation_date BETWEEN '2023-08-01' AND '2023-10-31'
ORDER BY ts.observation_date ASC;

-- ------------------------------------------------------------------------------
-- 8. RELATIONAL VIEW: Querying the pre-compiled analytical view
-- ------------------------------------------------------------------------------
SELECT
    analysis_id,
    area_name,
    region_label,
    start_date,
    end_date,
    mean_ndvi,
    valid_pixel_count,
    analysis_mode
FROM v_analysis_complete_summary
WHERE processing_status = 'completed';

-- ------------------------------------------------------------------------------
-- 9. INDEX VERIFICATION: EXPLAIN query demonstrating index scan on time series
-- ------------------------------------------------------------------------------
EXPLAIN
SELECT observation_date, mean_ndvi
FROM ndvi_time_series
WHERE analysis_id = 1 AND observation_date >= '2023-09-01';

-- ------------------------------------------------------------------------------
-- 10. TRANSACTION (ACID): Demonstrating consistent multi-table insertion
-- ------------------------------------------------------------------------------
START TRANSACTION;

-- Step 1: Insert Run Record
INSERT INTO analysis_runs (
    area_id, dataset_id, start_date, end_date, max_scene_cloud_pct,
    processing_status, analysis_mode, image_count, composite_method
) VALUES (
    1, 1, '2023-12-01', '2023-12-31', 10.00,
    'completed', 'demo', 4, 'median'
);

-- Retrieve generated ID
SET @new_analysis_id = LAST_INSERT_ID();

-- Step 2: Insert Summary Record
INSERT INTO ndvi_summaries (
    analysis_id, mean_ndvi, median_ndvi, min_ndvi, max_ndvi, valid_pixel_count, vegetation_area_sq_km
) VALUES (
    @new_analysis_id, 0.355000, 0.342000, -0.050000, 0.620000, 2150000, 72.500
);

-- Step 3: Insert Time Series Record
INSERT INTO ndvi_time_series (
    analysis_id, observation_date, mean_ndvi, median_ndvi, image_count, quality_notes
) VALUES
    (@new_analysis_id, '2023-12-05', 0.370000, 0.360000, 1, 'DEMO DATA — Early December snapshot'),
    (@new_analysis_id, '2023-12-20', 0.340000, 0.330000, 1, 'DEMO DATA — Late December snapshot');

-- Commit all changes together ensuring consistency
COMMIT;
