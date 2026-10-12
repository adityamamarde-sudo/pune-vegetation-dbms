-- ==============================================================================
-- Pune Vegetation Monitoring and Remote-Sensing Database System
-- Relational Database DDL Schema for MySQL 8.0+
--
-- This script creates the database, normalized tables, primary/foreign keys,
-- check constraints, performance indexes, relational views, and audit triggers.
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS pune_vegetation_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE pune_vegetation_db;

-- ------------------------------------------------------------------------------
-- Table A: users (Analyst & System Operators)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(30) NOT NULL DEFAULT 'analyst',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_user_role CHECK (role IN ('admin', 'analyst', 'researcher', 'viewer'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Table B: study_areas (Predefined Presets & Custom Drawn Polygons)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS study_areas (
    area_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    area_name VARCHAR(150) NOT NULL,
    area_type VARCHAR(40) NOT NULL DEFAULT 'preset',
    region_label VARCHAR(120) NOT NULL,
    geometry_geojson JSON NOT NULL,
    centroid_lat DECIMAL(10, 7) NULL,
    centroid_lon DECIMAL(10, 7) NULL,
    area_sq_km DECIMAL(12, 3) NULL,
    boundary_source VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_area_type CHECK (area_type IN ('preset', 'custom', 'administrative')),
    INDEX idx_study_areas_type (area_type),
    INDEX idx_study_areas_region (region_label)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Table C: satellite_datasets (Satellite Mission & Band Registry)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS satellite_datasets (
    dataset_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    provider VARCHAR(80) NOT NULL DEFAULT 'Google Earth Engine',
    collection_id VARCHAR(160) NOT NULL UNIQUE,
    satellite_name VARCHAR(80) NOT NULL DEFAULT 'Sentinel-2',
    sensor VARCHAR(80) NULL DEFAULT 'MSI',
    band_nir VARCHAR(20) NOT NULL DEFAULT 'B8',
    band_red VARCHAR(20) NOT NULL DEFAULT 'B4',
    processing_notes TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Table D: analysis_runs (Execution Jobs & Parameters)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS analysis_runs (
    analysis_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    area_id BIGINT NOT NULL,
    dataset_id BIGINT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    max_scene_cloud_pct DECIMAL(5, 2) NOT NULL DEFAULT 20.00,
    processing_status VARCHAR(30) NOT NULL DEFAULT 'pending',
    analysis_mode VARCHAR(30) NOT NULL DEFAULT 'real_gee',
    image_count INT NOT NULL DEFAULT 0,
    composite_method VARCHAR(40) NOT NULL DEFAULT 'median',
    error_message TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_runs_area FOREIGN KEY (area_id)
        REFERENCES study_areas(area_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_runs_dataset FOREIGN KEY (dataset_id)
        REFERENCES satellite_datasets(dataset_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_date_order CHECK (start_date <= end_date),
    CONSTRAINT chk_cloud_pct CHECK (max_scene_cloud_pct >= 0.00 AND max_scene_cloud_pct <= 100.00),
    CONSTRAINT chk_processing_status CHECK (processing_status IN ('pending', 'running', 'completed', 'failed')),
    CONSTRAINT chk_analysis_mode CHECK (analysis_mode IN ('real_gee', 'demo')),
    INDEX idx_analysis_runs_area (area_id),
    INDEX idx_analysis_runs_status (processing_status),
    INDEX idx_analysis_runs_dates (start_date, end_date),
    INDEX idx_analysis_runs_mode (analysis_mode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Table E: ndvi_summaries (Aggregate Statistics per Analysis Run)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ndvi_summaries (
    summary_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    analysis_id BIGINT NOT NULL,
    mean_ndvi DECIMAL(8, 6) NULL,
    median_ndvi DECIMAL(8, 6) NULL,
    min_ndvi DECIMAL(8, 6) NULL,
    max_ndvi DECIMAL(8, 6) NULL,
    valid_pixel_count BIGINT NULL,
    vegetation_area_sq_km DECIMAL(12, 3) NULL,
    calculated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_summaries_analysis FOREIGN KEY (analysis_id)
        REFERENCES analysis_runs(analysis_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT chk_summary_mean CHECK (mean_ndvi IS NULL OR (mean_ndvi >= -1.000000 AND mean_ndvi <= 1.000000)),
    CONSTRAINT chk_summary_median CHECK (median_ndvi IS NULL OR (median_ndvi >= -1.000000 AND median_ndvi <= 1.000000)),
    CONSTRAINT chk_summary_min CHECK (min_ndvi IS NULL OR (min_ndvi >= -1.000000 AND min_ndvi <= 1.000000)),
    CONSTRAINT chk_summary_max CHECK (max_ndvi IS NULL OR (max_ndvi >= -1.000000 AND max_ndvi <= 1.000000)),
    INDEX idx_summaries_analysis (analysis_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Table F: ndvi_time_series (Date-by-Date Observations for Charting)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ndvi_time_series (
    point_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    analysis_id BIGINT NOT NULL,
    observation_date DATE NOT NULL,
    mean_ndvi DECIMAL(8, 6) NOT NULL,
    median_ndvi DECIMAL(8, 6) NULL,
    image_count INT NOT NULL DEFAULT 1,
    quality_notes VARCHAR(255) NULL,
    CONSTRAINT fk_time_series_analysis FOREIGN KEY (analysis_id)
        REFERENCES analysis_runs(analysis_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT chk_ts_mean CHECK (mean_ndvi >= -1.000000 AND mean_ndvi <= 1.000000),
    CONSTRAINT chk_ts_median CHECK (median_ndvi IS NULL OR (median_ndvi >= -1.000000 AND median_ndvi <= 1.000000)),
    CONSTRAINT uq_analysis_obs_date UNIQUE (analysis_id, observation_date),
    INDEX idx_time_series_analysis_date (analysis_id, observation_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Table G: audit_logs (DBMS Course Demonstration: Trigger-backed Auditing)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    action_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id BIGINT NULL,
    details VARCHAR(255) NULL,
    logged_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_table_date (table_name, logged_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- Relational View 1: Complete Analysis Overview
-- Joins study_areas, satellite_datasets, analysis_runs, and ndvi_summaries
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_analysis_complete_summary AS
SELECT
    ar.analysis_id,
    sa.area_name,
    sa.region_label,
    sa.area_type,
    sa.area_sq_km,
    sd.satellite_name,
    sd.collection_id,
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
    ns.valid_pixel_count,
    ns.vegetation_area_sq_km,
    ar.created_at AS analysis_created_at
FROM analysis_runs ar
JOIN study_areas sa ON ar.area_id = sa.area_id
JOIN satellite_datasets sd ON ar.dataset_id = sd.dataset_id
LEFT JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id;

-- ------------------------------------------------------------------------------
-- Relational View 2: Area Performance & Vegetation Aggregates
-- Demonstrates SQL Aggregation, GROUP BY, and Multi-run comparison
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_area_performance_summary AS
SELECT
    sa.area_id,
    sa.area_name,
    sa.region_label,
    sa.area_type,
    sa.area_sq_km,
    COUNT(ar.analysis_id) AS total_analyses,
    ROUND(AVG(ns.mean_ndvi), 4) AS overall_avg_mean_ndvi,
    ROUND(MIN(ns.min_ndvi), 4) AS lowest_recorded_ndvi,
    ROUND(MAX(ns.max_ndvi), 4) AS highest_recorded_ndvi,
    MAX(ar.created_at) AS latest_analysis_date
FROM study_areas sa
LEFT JOIN analysis_runs ar ON sa.area_id = ar.area_id AND ar.processing_status = 'completed'
LEFT JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
GROUP BY sa.area_id, sa.area_name, sa.region_label, sa.area_type, sa.area_sq_km;

-- ------------------------------------------------------------------------------
-- DBMS Trigger Demonstration: Automatic Audit Logging on Analysis Creation
-- ------------------------------------------------------------------------------
DROP TRIGGER IF EXISTS trg_audit_analysis_insert;

DELIMITER $$
CREATE TRIGGER trg_audit_analysis_insert
AFTER INSERT ON analysis_runs
FOR EACH ROW
BEGIN
    INSERT INTO audit_logs (action_type, table_name, record_id, details)
    VALUES (
        'INSERT',
        'analysis_runs',
        NEW.analysis_id,
        CONCAT('Analysis created for Area ID: ', NEW.area_id, ' Mode: ', NEW.analysis_mode, ' Status: ', NEW.processing_status)
    );
END$$
DELIMITER ;
