# Pune Vegetation Monitoring & Remote-Sensing Database System

[![MySQL 8](https://img.shields.io/badge/MySQL-8.0-blue.svg)](https://www.mysql.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io/)
[![Google Earth Engine](https://img.shields.io/badge/GEE-Sentinel--2-orange.svg)](https://earthengine.google.com/)

A relational database system and analytical dashboard for monitoring vegetation dynamics (NDVI) across Pune, Maharashtra, using Sentinel-2 optical satellite imagery and MySQL 8. Built for DBMS Course Project evaluation.

**Project Directory**: `D:\DBMS_CP`

---

## 1. Quick Start Guide

### Step 1: Install Python Dependencies
Dependencies are already installed in the local environment, or can be re-verified with:
```bash
python -m pip install -r requirements.txt
```

### Step 2: Configure Environment (`.env`)
Create a `.env` file from the template:
```powershell
Copy-Item .env.example .env
```
Open `.env` and set your MySQL credentials (never committed to git):
```ini
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pune_vegetation_db
DB_USER=root
DB_PASSWORD=your_actual_mysql_password
```

### Step 3: Run Schema in MySQL Workbench
1. Open **MySQL Workbench 8.0**.
2. Connect to your local MySQL 8 Server (`localhost:3306`).
3. In Workbench, go to **File** $\rightarrow$ **Open SQL Script...** (or `Ctrl + Shift + O`).
4. Select `D:\DBMS_CP\db\schema.sql`.
5. Click the **Execute** button (yellow lightning bolt ⚡) or press `Ctrl + Shift + Enter`.
6. Open and execute `D:\DBMS_CP\db\seed_demo_data.sql` to populate Pune study-area presets and sample demo runs.

### Step 4: Verify Tables in MySQL Workbench
In MySQL Workbench, open a new SQL tab and run:
```sql
USE pune_vegetation_db;
SHOW TABLES;
```
You should see 7 tables and 2 views:
- `users`
- `study_areas`
- `satellite_datasets`
- `analysis_runs`
- `ndvi_summaries`
- `ndvi_time_series`
- `audit_logs`
- `v_analysis_complete_summary`
- `v_area_performance_summary`

Check table structure:
```sql
DESCRIBE study_areas;
SELECT area_id, area_name, region_label, area_sq_km FROM study_areas;
```

### Step 5: Test Connection from Python
Run the standalone diagnostic tester:
```bash
python db/test_connection.py
```
This tests TCP connectivity, authentication, database existence, and table count without printing sensitive passwords.

### Step 6: Launch the Streamlit Web Application
In your terminal, run:
```powershell
cd D:\DBMS_CP
python -m streamlit run app.py
```
Open your web browser at: **`http://localhost:8501`**

---

## 2. Step-by-Step Application Walkthrough (Demo & Viva)

1. **Dashboard (`Home`)**:
   - Verify green sidebar status badges: `🟢 MySQL Connected (3306)` and `🟢 Real GEE (Sentinel-2) Active`.
   - View high-level metrics across Pune talukas, recent runs, and summary charts.

2. **Select Study Area**:
   - Inspect preset Pune talukas (Pune City Core, Mulshi Watershed, Bhor, Haveli, Baramati, etc.) on the interactive map.
   - Or draw a custom boundary polygon using the Leaflet drawing toolbar and save it to MySQL.

3. **Run NDVI Analysis**:
   - Select a study area (e.g., **Pune City / Urban Core** or **Mulshi Watershed**).
   - Set observation dates (e.g., `2023-09-01` to `2023-10-31`).
   - Set Cloud Cover threshold (`20%` - `25%`).
   - Leave **Force Demo Mode** unchecked to process real Sentinel-2 satellite imagery via Google Earth Engine.
   - Click **🚀 Execute Analysis & Persist to MySQL**. (Executes in ~3-4 seconds, commits an ACID transaction across `analysis_runs`, `ndvi_summaries`, and `ndvi_time_series`, and triggers the audit log).

4. **NDVI Spatial Map**:
   - Select your analysis run from the dropdown.
   - View the **authentic Google Maps base layer** (Terrain / Roads or Satellite Hybrid).
   - View **real-time Sentinel-2 NDVI raster tiles** streamed live from Google Earth Engine.
   - Interact with the **Earth Engine Visualization Parameters panel** and adjust the **Opacity slider**.

5. **Trends & Statistics**:
   - Inspect interactive Plotly time-series curves showing NDVI vegetation index changes across dates.
   - Compare seasonal differences and download CSV time-series tables.

6. **Database Explorer & DBMS Assessment Queries**:
   - Inspect live MySQL data across all 7 normalized tables (`study_areas`, `analysis_runs`, `ndvi_summaries`, `ndvi_time_series`, `audit_logs`, etc.).
   - Select **DBMS Assessment Queries (1-10)** to demonstrate 4-table JOINs, GROUP BY aggregations, HAVING clauses, Views, and `EXPLAIN` query execution plans.

7. **Download Academic Project Report**:
   - Download the 10-page comprehensive project report PDF from the left sidebar or at `D:\DBMS_CP\Pune_Vegetation_DBMS_Comprehensive_Project_Report.pdf`.

---

## 2. Relational Schema Summary
- **`study_areas`**: Spatial bounding coordinates (GeoJSON), centroids, and computed surface areas ($\text{km}^2$) for Pune regions.
- **`satellite_datasets`**: Metadata on Sentinel-2 collections and multispectral band configurations (`B8`, `B4`).
- **`analysis_runs`**: Execution log of temporal and cloud parameters.
- **`ndvi_summaries`**: Statistical aggregates (mean, median, min, max, pixel count).
- **`ndvi_time_series`**: Periodic NDVI points for interactive trend curves.
- **`audit_logs`**: Trigger-backed audit log capturing analysis insertion events.
- **`v_analysis_complete_summary`**: Relational view combining spatial, satellite, and statistical tables.

---

## 3. DBMS Course Query Demonstrations
Open `db/sample_queries.sql` in MySQL Workbench to run the 10 assessment queries:
1. **Filtering**: Runs for a specific taluka.
2. **Sorting**: Latest analyses first.
3. **Aggregation**: Overall average NDVI across study areas.
4. **4-Table JOIN**: Connecting study areas, runs, datasets, and NDVI summaries.
5. **GROUP BY**: Vegetation comparisons grouped by district zone.
6. **HAVING**: Identifying areas with average NDVI $< 0.45$.
7. **Date Range Filtering**: Temporal query on observation dates.
8. **View Query**: Querying `v_analysis_complete_summary`.
9. **Index Scan**: `EXPLAIN` on `(analysis_id, observation_date)`.
10. **ACID Transaction**: Atomic multi-table insertion test with rollback safety.
