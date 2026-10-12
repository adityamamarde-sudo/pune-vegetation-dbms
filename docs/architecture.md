# System Architecture & Component Design
## Pune Vegetation Monitoring & Remote-Sensing Database System

### 1. Conceptual Architecture

The application is structured into four decoupled layers:

```
+------------------------------------------------------------------------+
|                           Streamlit Web UI                             |
|  - Dashboard       - Area Selector Map     - NDVI Run Form             |
|  - Trends & Plots  - DB Explorer & SQL Lab - Literature Review         |
+------------------------------------------------------------------------+
                                  |
                                  v
+------------------------------------------------------------------------+
|                            Service Layer                               |
|  - geometry_service (Shapely, pyproj area & polygon validation)        |
|  - ndvi_service     (Mathematical NDVI formula & statistical summary) |
|  - gee_service      (Sentinel-2 Earth Engine API & Cloud Masking)      |
|  - analysis_service (Orchestrator, dispatching GEE or Demo generator)  |
+------------------------------------------------------------------------+
           |                                              |
           v                                              v
+------------------------+             +---------------------------------+
|  Google Earth Engine   |             |   MySQL 8 Relational Database   |
|  - COPERNICUS/S2_SR    |             |   - study_areas                 |
|  - Cloud reduction     |             |   - analysis_runs               |
|  - Raster NDVI tiles   |             |   - ndvi_summaries              |
|                        |             |   - ndvi_time_series            |
|                        |             |   - audit_logs / views          |
+------------------------+             +---------------------------------+
```

### 2. Design Decisions
1. **Raster vs. Relational Separation**:
   Large satellite raster files (gigabytes of optical multispectral data) are not stored as BLOBs in MySQL. Instead, spatial algorithms execute in Earth Engine, and derived tabular metadata, spatial bounding geometries, and aggregate statistics are stored in MySQL 8.
2. **Graceful Demo Fallback**:
   If GEE credentials or internet connections fail, the application gracefully provides verified, clearly labelled demo data to allow database and UI evaluations without blocking development.
