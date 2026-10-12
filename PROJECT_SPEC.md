# Pune Vegetation Monitoring & Remote-Sensing Database System
## DBMS Course Project Specification & Implementation Plan

> **Course Focus**: Relational Database Management Systems (MySQL 8)  
> **Application Domain**: Environmental Informatics & Satellite Remote Sensing  
> **Study Region**: Pune, Maharashtra, India (18.5204° N, 73.8567° E) and surrounding talukas/regions  
> **Primary Technology Stack**: Python 3.11+, Streamlit, MySQL 8, MySQL Workbench, Folium, Plotly, Google Earth Engine (GEE) Python API

---

## 1. Project Overview & Objectives

This project builds a full-stack, database-centric system for monitoring vegetation health (Normalized Difference Vegetation Index — NDVI) across the Pune metropolitan and surrounding rural regions using Sentinel-2 optical satellite imagery.

### Core Philosophy & Constraints
- **Relational Integrity First**: The system must use a real **MySQL 8** server database managed independently through **MySQL Workbench**. No SQLite or MongoDB.
- **Role of Satellite Engine**: Google Earth Engine (GEE) serves purely as the satellite-data processing backend. MySQL 8 is the project's permanent relational store for study areas, analysis runs, sensor metadata, derived NDVI aggregations, and time-series records. Large rasters remain in the cloud or compute engine; relational metadata and numerical metrics live in MySQL.
- **Dual Operating Mode (Real GEE & Demo Mode)**:
  - When GEE credentials and Google Cloud project access are configured, analyses execute live against Sentinel-2 surface reflectance datasets.
  - When credentials are not yet configured or quota is exhausted, the application provides a clearly labeled **Demo Mode** with verified synthetic presets. Every demo page, chart, and export must explicitly state: `DEMO DATA — NOT REAL SATELLITE RESULTS`.

---

## 2. System Architecture & Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Relational Database** | **MySQL 8.0+** | Normalized schema, foreign keys, constraints, indexes, views, transactions |
| **DB Administration** | **MySQL Workbench 8.0** | Independent schema management, query testing, inspection, ER visualizer |
| **Python DB Driver** | `mysql-connector-python` / `SQLAlchemy` + `PyMySQL` | Parameterized SQL execution, connection pooling, connection health checks |
| **Web UI / Frontend** | **Streamlit** | Multi-screen responsive dashboard, interactive controls, data tables |
| **Interactive Map** | **Folium** + `streamlit-folium` | Pune area centering, preset selection, custom polygon drawing (`Leaflet-Geoman` / `Draw`) |
| **Charts & Visualizations** | **Plotly Graph Objects / Express** | Interactive NDVI time-series trends, comparative area plots, distribution bands |
| **Remote Sensing Compute** | **Google Earth Engine API** (`earthengine-api`) | Sentinel-2 SR Harmonized imagery filtering, QA cloud-masking, NDVI raster generation |
| **Geospatial Utilities** | `shapely`, `pyproj`, `geopandas` | Polygon validation, centroid extraction, spherical/geodesic area calculation (km²) |
| **Tabular Data & CSV** | `pandas` | Aggregations, safe SQL result transformations, CSV report export |
| **Configuration** | `python-dotenv` | Secret isolation (`.env`), zero hardcoded credentials |
| **Testing** | `pytest` | Unit tests for NDVI formulas, geometry validation, date checks, database transactions |

---

## 3. Study Area & Geographic Boundaries

- **Center Point**: Pune City (~`18.5204° N, 73.8567° E`).
- **Preset Study Areas** (Approximate regional bounding geometries with clear provenance):
  1. *Pune City / Urban Core*
  2. *Haveli Taluka Area*
  3. *Mulshi Watershed & Western Ghats Foothills*
  4. *Maval Taluka Area*
  5. *Bhor Taluka Area*
  6. *Baramati Agricultural Area*
  7. *Shirur Agricultural Belt*
  8. *Daund Agro-Rural Area*
- **Custom Area Drawing**:
  - Interactive polygon and rectangle drawing via Leaflet/Folium.
  - Validation: Non-empty, closed polygon, valid topology (no self-intersections), maximum area restriction (e.g. $\le 2500 \text{ km}^2$ to avoid timeouts).
  - Computed approximate area displayed in $\text{km}^2$ and centroid coordinates.

---

## 4. Satellite Processing Workflow (Sentinel-2 & NDVI)

1. **Dataset**: `COPERNICUS/S2_SR_HARMONIZED` (Sentinel-2 Surface Reflectance).
2. **Spectral Index Calculation**:
   $$\text{NDVI} = \frac{\text{NIR (B8)} - \text{Red (B4)}}{\text{NIR (B8)} + \text{Red (B4)}}$$
   - Valid range: $[-1.0, +1.0]$.
   - Palette: Brown/Orange (bare/low NDVI) $\rightarrow$ Yellow (moderate) $\rightarrow$ Light Green (healthy) $\rightarrow$ Deep Green (dense canopy).
3. **Cloud & Shadow Filtering**:
   - Filter image collection by date range and scene-level cloud percentage threshold (`CLOUDY_PIXEL_PERCENTAGE`).
   - SCL (Scene Classification Layer) / QA mask to filter out clouds, cloud shadows, and invalid pixels.
4. **Compositing & Statistics**:
   - Temporal median compositing over selected intervals.
   - Spatial reduction: Mean, Median, Min, Max NDVI, valid pixel counts.
   - Time-series generation: Aggregated observations per satellite pass across the requested timeframe.

---

## 5. MySQL Relational Database Schema Design

The schema follows third normal form (3NF), enforces referential integrity via Foreign Keys, and uses strict constraints and indexes:

### Tables Summary
1. `users` *(Optional / Demonstrative)*: Analyst details and audit identity.
2. `study_areas`: Predefined presets and user-saved custom drawn polygons with GeoJSON, centroid, and area in $\text{km}^2$.
3. `satellite_datasets`: Registry of satellite collections, sensor specifications, and active bands (`B8`, `B4`).
4. `analysis_runs`: Executed analysis jobs capturing parameters (date range, cloud cutoff, mode, status, image count).
5. `ndvi_summaries`: Aggregate statistical summary metrics per analysis run.
6. `ndvi_time_series`: Temporal observations per date for time-series charts.
7. `audit_logs` / `saved_queries` *(Optional)*: DBMS demonstration table for logging query and transaction events.

### Views & DBMS Academic Criteria
- `v_analysis_complete_summary`: Unified relational view joining `analysis_runs`, `study_areas`, `satellite_datasets`, and `ndvi_summaries`.
- **Composite Indexes**: `(analysis_id, observation_date)` for high-performance time-series retrieval.
- **Constraints**: Check constraints on date ranges (`start_date <= end_date`), cloud threshold ($0 \le \text{cloud} \le 100$), and NDVI range ($ -1.0 \le \text{NDVI} \le 1.0 $).
- **Transactions**: Atomic persistence of `analysis_runs` + `ndvi_summaries` + `ndvi_time_series` within a single `START TRANSACTION ... COMMIT / ROLLBACK` block.

---

## 6. Required Application Screens

1. **Dashboard / Overview**: Key metrics (total areas, total runs, recent runs, system health, active database connection status, GEE/Demo badge).
2. **Select Study Area (Map)**: Interactive Folium map centered on Pune, preset selector, custom polygon drawing, geometry summary, save to database.
3. **Run NDVI Analysis**: Date selection, cloud percentage slider, computation trigger, input validation, progress indicators.
4. **NDVI Map Visualizer**: Interactive tile visualization or color-coded choropleth/raster composite with legend.
5. **Trends & Statistical Insights**: Plotly time-series curves, statistical summary cards (Mean, Median, Min, Max), comparative run viewer.
6. **Database Explorer & SQL Lab**: Interactive query table viewers, parameter filters, CSV data exporter, and demonstrator for the 10+ required DBMS queries.
7. **Literature & Methodology**: Scientific background, Sentinel-2 specifications, NDVI formulas, references, and system limitations.

---

## 7. Required DBMS SQL Demonstrations

The application and project documentation include 10 real SQL demonstrations tested against MySQL 8:
1. **Filtering**: Retrieve all analysis runs for a selected area.
2. **Sorting**: Retrieve analysis runs ordered chronologically (latest first).
3. **Aggregation**: Calculate average NDVI across all runs or by area.
4. **Multi-table JOIN**: Inner join of `study_areas`, `analysis_runs`, and `ndvi_summaries`.
5. **GROUP BY**: Group mean NDVI by study area or calendar month.
6. **HAVING**: Find regions where average NDVI drops below a critical threshold.
7. **Date Filtering**: Temporal range queries on observation timestamps.
8. **Relational View**: Querying `v_analysis_complete_summary`.
9. **Index Optimization**: Explain plan showing index scan on `(analysis_id, observation_date)`.
10. **ACID Transaction**: Transaction saving analysis run and batch time-series points atomically.

---

## 8. Development & Implementation Plan

- **Stage 1 (Current Stage)**:
  - Project scaffolding and directory structure setup.
  - Configuration (`.env.example`, `config.py`) and dependencies (`requirements.txt`).
  - MySQL 8 Relational Schema (`db/schema.sql`) and Demo Seed Data (`db/seed_demo_data.sql`).
  - Python database connection module (`db/connection.py`) and standalone CLI tester.
  - Step-by-step guidance for MySQL Workbench connection and schema execution.
- **Stage 2**:
  - Geospatial service (`services/geometry_service.py`) and Pune presets data.
  - Interactive Pune map selection UI with Folium polygon drawing.
- **Stage 3**:
  - GEE service interface (`services/gee_service.py`), authentication helper, and fallback Demo generator (`services/ndvi_service.py`).
- **Stage 4**:
  - Analysis execution pipeline, transaction-based persistence in MySQL (`services/analysis_service.py`).
  - Plotly interactive time-series and comparative charts.
- **Stage 5**:
  - Database Explorer, SQL demo console, CSV exporter, unit tests (`pytest`), documentation, and screenshots.
