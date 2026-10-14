-- ===================================================================
-- Migration: Prediction Scenarios & Forecast Points
-- Course: Database Management Systems (SPPU)
-- Tables: prediction_scenarios, prediction_forecast_points
-- ===================================================================

USE pune_vegetation_db;

-- 1. Prediction Scenarios Table
CREATE TABLE IF NOT EXISTS prediction_scenarios (
    scenario_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    area_id BIGINT NOT NULL,
    base_analysis_id BIGINT NULL,
    scenario_title VARCHAR(150) NOT NULL,
    scenario_type VARCHAR(50) NOT NULL DEFAULT 'baseline_forecast',
    forecast_horizon_months INT NOT NULL DEFAULT 6,
    projected_mean_ndvi DECIMAL(6,4) NOT NULL,
    vegetation_loss_sq_km DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    vulnerability_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    risk_level VARCHAR(30) NOT NULL DEFAULT 'LOW',
    simulation_parameters JSON NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pred_scenario_area FOREIGN KEY (area_id) 
        REFERENCES study_areas(area_id) ON DELETE CASCADE,
    CONSTRAINT fk_pred_scenario_analysis FOREIGN KEY (base_analysis_id) 
        REFERENCES analysis_runs(analysis_id) ON DELETE SET NULL,
    INDEX idx_pred_area_date (area_id, created_at),
    INDEX idx_pred_risk_level (risk_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Prediction Forecast Points Table
CREATE TABLE IF NOT EXISTS prediction_forecast_points (
    point_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    scenario_id BIGINT NOT NULL,
    forecast_date DATE NOT NULL,
    predicted_ndvi DECIMAL(6,4) NOT NULL,
    lower_confidence_ndvi DECIMAL(6,4) NOT NULL,
    upper_confidence_ndvi DECIMAL(6,4) NOT NULL,
    CONSTRAINT fk_pred_point_scenario FOREIGN KEY (scenario_id) 
        REFERENCES prediction_scenarios(scenario_id) ON DELETE CASCADE,
    INDEX idx_pred_scenario_date (scenario_id, forecast_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. View: v_prediction_risk_overview
CREATE OR REPLACE VIEW v_prediction_risk_overview AS
SELECT 
    ps.scenario_id,
    sa.area_name,
    sa.region_label,
    sa.area_sq_km AS total_area_sq_km,
    ps.scenario_title,
    ps.scenario_type,
    ps.forecast_horizon_months,
    ps.projected_mean_ndvi,
    ps.vegetation_loss_sq_km,
    ps.vulnerability_score,
    ps.risk_level,
    ps.created_at
FROM prediction_scenarios ps
JOIN study_areas sa ON ps.area_id = sa.area_id
ORDER BY ps.created_at DESC;
