-- ==============================================================================
-- Pune Vegetation Monitoring and Remote-Sensing Database System
-- Seed & Demo Data Script for MySQL 8.0+
--
-- Notice: Sample records are strictly labelled as DEMO DATA — NOT REAL SATELLITE RESULTS
-- per Section 11 of the project specification.
-- ==============================================================================

USE pune_vegetation_db;

-- ------------------------------------------------------------------------------
-- 1. Seed Satellite Datasets
-- ------------------------------------------------------------------------------
INSERT INTO satellite_datasets (
    dataset_id, provider, collection_id, satellite_name, sensor, band_nir, band_red, processing_notes
) VALUES (
    1,
    'Google Earth Engine',
    'COPERNICUS/S2_SR_HARMONIZED',
    'Sentinel-2',
    'MSI',
    'B8',
    'B4',
    'Surface Reflectance Harmonized collection. B8 (NIR 842nm, 10m) and B4 (Red 665nm, 10m). Cloud masking via SCL QA bands.'
) ON DUPLICATE KEY UPDATE satellite_name = VALUES(satellite_name);

-- ------------------------------------------------------------------------------
-- 2. Seed Users (Analyst Demonstrations)
-- ------------------------------------------------------------------------------
INSERT INTO users (user_id, full_name, email, role)
VALUES
    (1, 'Pune Geoinformatics Analyst', 'analyst@puneveg.org', 'analyst'),
    (2, 'DBMS Course Examiner', 'examiner@college.edu', 'admin')
ON DUPLICATE KEY UPDATE full_name = VALUES(full_name);

-- ------------------------------------------------------------------------------
-- 3. Seed Preset Study Areas (Pune Metropolitan & Surrounding Talukas)
-- Coordinates represent approximate geographic study bounding polygons.
-- ------------------------------------------------------------------------------

-- Area 1: Pune City / Urban Core
INSERT INTO study_areas (
    area_id, area_name, area_type, region_label, centroid_lat, centroid_lon, area_sq_km, boundary_source, geometry_geojson
) VALUES (
    1,
    'Pune City / Urban Core',
    'preset',
    'Pune Urban',
    18.520430,
    73.856744,
    250.000,
    'Approximate study-area bounding polygon for Pune DBMS demonstration',
    '{
        "type": "Polygon",
        "coordinates": [[
            [73.780, 18.450],
            [73.950, 18.450],
            [73.950, 18.590],
            [73.780, 18.590],
            [73.780, 18.450]
        ]]
    }'
) ON DUPLICATE KEY UPDATE area_name = VALUES(area_name);

-- Area 2: Haveli Taluka Area
INSERT INTO study_areas (
    area_id, area_name, area_type, region_label, centroid_lat, centroid_lon, area_sq_km, boundary_source, geometry_geojson
) VALUES (
    2,
    'Haveli Area',
    'preset',
    'Haveli',
    18.480000,
    73.910000,
    580.000,
    'Approximate study-area bounding polygon for Pune DBMS demonstration',
    '{
        "type": "Polygon",
        "coordinates": [[
            [73.750, 18.350],
            [74.050, 18.350],
            [74.050, 18.600],
            [73.750, 18.600],
            [73.750, 18.350]
        ]]
    }'
) ON DUPLICATE KEY UPDATE area_name = VALUES(area_name);

-- Area 3: Mulshi Watershed & Hills
INSERT INTO study_areas (
    area_id, area_name, area_type, region_label, centroid_lat, centroid_lon, area_sq_km, boundary_source, geometry_geojson
) VALUES (
    3,
    'Mulshi Area',
    'preset',
    'Mulshi',
    18.510000,
    73.510000,
    620.000,
    'Approximate study-area bounding polygon for Pune DBMS demonstration',
    '{
        "type": "Polygon",
        "coordinates": [[
            [73.380, 18.380],
            [73.680, 18.380],
            [73.680, 18.640],
            [73.380, 18.640],
            [73.380, 18.380]
        ]]
    }'
) ON DUPLICATE KEY UPDATE area_name = VALUES(area_name);

-- Area 4: Maval Taluka Area
INSERT INTO study_areas (
    area_id, area_name, area_type, region_label, centroid_lat, centroid_lon, area_sq_km, boundary_source, geometry_geojson
) VALUES (
    4,
    'Maval Area',
    'preset',
    'Maval',
    18.750000,
    73.580000,
    540.000,
    'Approximate study-area bounding polygon for Pune DBMS demonstration',
    '{
        "type": "Polygon",
        "coordinates": [[
            [73.450, 18.650],
            [73.750, 18.650],
            [73.750, 18.880],
            [73.450, 18.880],
            [73.450, 18.650]
        ]]
    }'
) ON DUPLICATE KEY UPDATE area_name = VALUES(area_name);

-- Area 5: Bhor Taluka Area
INSERT INTO study_areas (
    area_id, area_name, area_type, region_label, centroid_lat, centroid_lon, area_sq_km, boundary_source, geometry_geojson
) VALUES (
    5,
    'Bhor Area',
    'preset',
    'Bhor',
    18.150000,
    73.840000,
    690.000,
    'Approximate study-area bounding polygon for Pune DBMS demonstration',
    '{
        "type": "Polygon",
        "coordinates": [[
            [73.700, 18.020],
            [74.000, 18.020],
            [74.000, 18.300],
            [73.700, 18.300],
            [73.700, 18.020]
        ]]
    }'
) ON DUPLICATE KEY UPDATE area_name = VALUES(area_name);

-- Area 6: Baramati Agricultural Belt
INSERT INTO study_areas (
    area_id, area_name, area_type, region_label, centroid_lat, centroid_lon, area_sq_km, boundary_source, geometry_geojson
) VALUES (
    6,
    'Baramati Area',
    'preset',
    'Baramati',
    18.150000,
    74.580000,
    810.000,
    'Approximate study-area bounding polygon for Pune DBMS demonstration',
    '{
        "type": "Polygon",
        "coordinates": [[
            [74.400, 18.000],
            [74.780, 18.000],
            [74.780, 18.300],
            [74.400, 18.300],
            [74.400, 18.000]
        ]]
    }'
) ON DUPLICATE KEY UPDATE area_name = VALUES(area_name);

-- Area 7: Shirur Area
INSERT INTO study_areas (
    area_id, area_name, area_type, region_label, centroid_lat, centroid_lon, area_sq_km, boundary_source, geometry_geojson
) VALUES (
    7,
    'Shirur Area',
    'preset',
    'Shirur',
    18.820000,
    74.370000,
    750.000,
    'Approximate study-area bounding polygon for Pune DBMS demonstration',
    '{
        "type": "Polygon",
        "coordinates": [[
            [74.200, 18.680],
            [74.550, 18.680],
            [74.550, 18.980],
            [74.200, 18.980],
            [74.200, 18.680]
        ]]
    }'
) ON DUPLICATE KEY UPDATE area_name = VALUES(area_name);

-- Area 8: Daund Agro-Rural Area
INSERT INTO study_areas (
    area_id, area_name, area_type, region_label, centroid_lat, centroid_lon, area_sq_km, boundary_source, geometry_geojson
) VALUES (
    8,
    'Daund Area',
    'preset',
    'Daund',
    18.460000,
    74.580000,
    720.000,
    'Approximate study-area bounding polygon for Pune DBMS demonstration',
    '{
        "type": "Polygon",
        "coordinates": [[
            [74.420, 18.320],
            [74.760, 18.320],
            [74.760, 18.620],
            [74.420, 18.620],
            [74.420, 18.320]
        ]]
    }'
) ON DUPLICATE KEY UPDATE area_name = VALUES(area_name);

-- ------------------------------------------------------------------------------
-- 4. Seed Demonstrative Analysis Runs (Labelled clearly as DEMO DATA)
-- ------------------------------------------------------------------------------

-- Demo Analysis 1: Mulshi Watershed Post-Monsoon (High vegetation density)
INSERT INTO analysis_runs (
    analysis_id, area_id, dataset_id, start_date, end_date, max_scene_cloud_pct,
    processing_status, analysis_mode, image_count, composite_method, error_message
) VALUES (
    1, 3, 1, '2023-09-01', '2023-11-30', 20.00,
    'completed', 'demo', 14, 'median', NULL
) ON DUPLICATE KEY UPDATE processing_status = VALUES(processing_status);

INSERT INTO ndvi_summaries (
    summary_id, analysis_id, mean_ndvi, median_ndvi, min_ndvi, max_ndvi, valid_pixel_count, vegetation_area_sq_km
) VALUES (
    1, 1, 0.684200, 0.712000, 0.125000, 0.892000, 4850000, 524.350
) ON DUPLICATE KEY UPDATE mean_ndvi = VALUES(mean_ndvi);

INSERT INTO ndvi_time_series (analysis_id, observation_date, mean_ndvi, median_ndvi, image_count, quality_notes)
VALUES
    (1, '2023-09-05', 0.621000, 0.645000, 1, 'DEMO DATA — Clear sky post-monsoon sample'),
    (1, '2023-09-20', 0.665000, 0.690000, 1, 'DEMO DATA — Vigorous foliage peak'),
    (1, '2023-10-05', 0.710000, 0.735000, 1, 'DEMO DATA — Maximum canopy density'),
    (1, '2023-10-25', 0.698000, 0.720000, 1, 'DEMO DATA — Stable vegetative cover'),
    (1, '2023-11-12', 0.672000, 0.701000, 1, 'DEMO DATA — Transition into early dry season'),
    (1, '2023-11-28', 0.640000, 0.665000, 1, 'DEMO DATA — Post-monsoon drying trend')
ON DUPLICATE KEY UPDATE mean_ndvi = VALUES(mean_ndvi);

-- Demo Analysis 2: Pune Urban Core Annual Cycle
INSERT INTO analysis_runs (
    analysis_id, area_id, dataset_id, start_date, end_date, max_scene_cloud_pct,
    processing_status, analysis_mode, image_count, composite_method, error_message
) VALUES (
    2, 1, 1, '2023-01-01', '2023-05-31', 15.00,
    'completed', 'demo', 22, 'median', NULL
) ON DUPLICATE KEY UPDATE processing_status = VALUES(processing_status);

INSERT INTO ndvi_summaries (
    summary_id, analysis_id, mean_ndvi, median_ndvi, min_ndvi, max_ndvi, valid_pixel_count, vegetation_area_sq_km
) VALUES (
    2, 2, 0.312000, 0.298000, -0.082000, 0.645000, 2100000, 68.200
) ON DUPLICATE KEY UPDATE mean_ndvi = VALUES(mean_ndvi);

INSERT INTO ndvi_time_series (analysis_id, observation_date, mean_ndvi, median_ndvi, image_count, quality_notes)
VALUES
    (2, '2023-01-15', 0.385000, 0.370000, 1, 'DEMO DATA — Moderate urban green cover (Winter)'),
    (2, '2023-02-14', 0.342000, 0.330000, 1, 'DEMO DATA — Gradual drying trend'),
    (2, '2023-03-15', 0.298000, 0.285000, 1, 'DEMO DATA — Pre-monsoon dry season bare patches'),
    (2, '2023-04-12', 0.265000, 0.252000, 1, 'DEMO DATA — Summer heat peak low vegetation'),
    (2, '2023-05-20', 0.245000, 0.231000, 1, 'DEMO DATA — Lowest annual baseline before monsoon')
ON DUPLICATE KEY UPDATE mean_ndvi = VALUES(mean_ndvi);

-- Demo Analysis 3: Baramati Agricultural Belt
INSERT INTO analysis_runs (
    analysis_id, area_id, dataset_id, start_date, end_date, max_scene_cloud_pct,
    processing_status, analysis_mode, image_count, composite_method, error_message
) VALUES (
    3, 6, 1, '2023-06-01', '2023-10-31', 25.00,
    'completed', 'demo', 18, 'median', NULL
) ON DUPLICATE KEY UPDATE processing_status = VALUES(processing_status);

INSERT INTO ndvi_summaries (
    summary_id, analysis_id, mean_ndvi, median_ndvi, min_ndvi, max_ndvi, valid_pixel_count, vegetation_area_sq_km
) VALUES (
    3, 3, 0.542000, 0.568000, 0.040000, 0.812000, 6200000, 480.100
) ON DUPLICATE KEY UPDATE mean_ndvi = VALUES(mean_ndvi);

INSERT INTO ndvi_time_series (analysis_id, observation_date, mean_ndvi, median_ndvi, image_count, quality_notes)
VALUES
    (3, '2023-06-15', 0.280000, 0.270000, 1, 'DEMO DATA — Sowing season preparation'),
    (3, '2023-07-20', 0.420000, 0.435000, 1, 'DEMO DATA — Crop germination and early vegetative phase'),
    (3, '2023-08-25', 0.585000, 0.610000, 1, 'DEMO DATA — Peak sugarcane and kharif crop canopy'),
    (3, '2023-09-28', 0.640000, 0.670000, 1, 'DEMO DATA — Maturing crops with high chlorophyll'),
    (3, '2023-10-25', 0.535000, 0.550000, 1, 'DEMO DATA — Early harvest cycle starts')
ON DUPLICATE KEY UPDATE mean_ndvi = VALUES(mean_ndvi);
