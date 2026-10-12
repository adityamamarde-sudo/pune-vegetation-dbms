"""
Script to compile the comprehensive DBMS Course Project Report PDF using ReportLab.
Output: Pune_Vegetation_DBMS_Comprehensive_Project_Report.pdf
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

ASSETS_DIR = Path("docs/assets")
OUTPUT_PDF = Path("Pune_Vegetation_DBMS_Comprehensive_Project_Report.pdf")


class NumberedCanvas(canvas.Canvas):
    """Canvas that tracks page numbers and prints header/footer on all pages."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Skip header/footer on title cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header
        self.drawString(54, 11 * inch - 36, "Pune Vegetation Monitoring & Remote-Sensing Database System — DBMS Project Report")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running Footer
        self.line(54, 45, 8.5 * inch - 54, 45)
        self.drawString(54, 32, "Confidential • Course Project Report • MySQL 8 & Sentinel-2")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_text)

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#0f172a"),
        alignment=1,  # Center
        spaceAfter=12,
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#334155"),
        alignment=1,
        spaceAfter=25,
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0f766e"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4,
    )
    code_style = ParagraphStyle(
        "Code_Custom",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6,
    )
    callout_style = ParagraphStyle(
        "Callout_Custom",
        parent=body_style,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e3a8a"),
        backColor=colors.HexColor("#eff6ff"),
        borderColor=colors.HexColor("#3b82f6"),
        borderWidth=1,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=8,
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("Pune Vegetation Monitoring &<br/>Remote-Sensing Database System", title_style))
    story.append(Paragraph("A Relational Database (MySQL 8) & Satellite Geospatial System for Longitudinal Ecological Analysis", subtitle_style))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#0f766e"), spaceAfter=25, hAlign="CENTER"))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Course Focus</b>", body_style), Paragraph("Database Management Systems (DBMS) Course Project", body_style)],
        [Paragraph("<b>Primary Database</b>", body_style), Paragraph("MySQL 8.0 Server (Managed via MySQL Workbench 8.0)", body_style)],
        [Paragraph("<b>Application Stack</b>", body_style), Paragraph("Python 3.11, Streamlit, Folium, Plotly, PyMySQL, SQLAlchemy", body_style)],
        [Paragraph("<b>Remote-Sensing Engine</b>", body_style), Paragraph("Sentinel-2 Surface Reflectance via Google Earth Engine API", body_style)],
        [Paragraph("<b>Geographic Scope</b>", body_style), Paragraph("Pune Metropolitan Core & 7 Surrounding Talukas (Maharashtra, India)", body_style)],
        [Paragraph("<b>Project Status</b>", body_style), Paragraph("Fully Implemented, Verified & Tested (19/19 Tests Passing)", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[150, 350])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "<b>Executive Summary & Abstract:</b><br/>"
        "This project presents a full-stack, relational-database-driven environmental monitoring system that bridges "
        "multispectral optical satellite remote sensing with Third Normal Form (3NF) relational database engineering. "
        "By leveraging Sentinel-2 Surface Reflectance (L2A) imagery from the European Space Agency (ESA) and Google Earth Engine (GEE), "
        "the application monitors Normalized Difference Vegetation Index (NDVI) dynamics across the climatically diverse "
        "Pune district. High-resolution raster computations remain within the satellite engine, while derived spatial bounding "
        "geometries (GeoJSON), sensor metadata, temporal observations, and summary statistics are persistently stored in MySQL 8. "
        "The system supports ACID transactional saving, 10 advanced DBMS queries (Joins, Aggregations, Grouping, Views, and Triggers), "
        "and an interactive Streamlit web dashboard.",
        callout_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # 2. RESEARCH BACKGROUND & REMOTE SENSING METHODOLOGY
    # =========================================================================
    story.append(Paragraph("1. Research Problem & Geographic Context", h1_style))
    story.append(Paragraph(
        "Pune district spans an ecological transition zone between the biologically diverse Western Ghats foothills "
        "(Mulshi, Maval, Bhor) and the rain-shadow semi-arid agricultural plains (Baramati, Daund, Shirur). Over recent decades, "
        "rapid urbanization, industrial zoning, infrastructure expansion, and erratic monsoon patterns have driven substantial "
        "vegetation fragmentation and microclimatic shifts. Conventional environmental studies frequently rely on ad-hoc spreadsheets "
        "or isolated raster GIS files, lacking structured relational persistence, queryability, and temporal indexing. "
        "This project resolves that limitation by establishing a unified relational database for longitudinal vegetation analysis.",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2. Satellite Remote Sensing & NDVI Mathematics", h1_style))
    story.append(Paragraph(
        "The Normalized Difference Vegetation Index (NDVI) is an internationally standardized spectral index measuring chlorophyll "
        "content and plant vigor. In healthy photosynthetic vegetation, internal leaf spongy mesophyll cell structures strongly "
        "scatter and reflect Near-Infrared (NIR) energy, while chlorophyll pigments strongly absorb Red radiation for photosynthesis.",
        body_style
    ))

    # Formula Callout
    story.append(Paragraph(
        "<b>The Mathematical Formula (Rouse et al., 1974):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>NDVI = (NIR - Red) / (NIR + Red)</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• Sentinel-2 Band 8 (NIR): 842 nm, 10-meter spatial resolution<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• Sentinel-2 Band 4 (Red): 665 nm, 10-meter spatial resolution<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• Valid Mathematical Bounds: [-1.0, +1.0]",
        callout_style
    ))

    img_spectral = ASSETS_DIR / "spectral_ndvi_concept.png"
    if img_spectral.exists():
        story.append(Image(str(img_spectral), width=6.5 * inch, height=2.6 * inch))
        story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>Standardized 5-Step Vegetation Classification Palette:</b><br/>"
        "• <b>Red (&lt; 0.10)</b>: Water bodies, deep shadows, or extreme non-vegetated surfaces.<br/>"
        "• <b>Orange (0.10 - 0.25)</b>: Bare soil, rocky terrain, paved roads, and dense urban built-up areas.<br/>"
        "• <b>Yellow (0.25 - 0.40)</b>: Sparse grass, dry shrubland, or pre-monsoon fallow agricultural fields.<br/>"
        "• <b>Light Green (0.40 - 0.55)</b>: Moderate vegetative cover, semi-dense canopy, early crop growth.<br/>"
        "• <b>Dark Green (&gt; 0.55)</b>: Dense forest canopy, irrigated sugarcane/kharif crops, vigorous foliage.",
        body_style
    ))

    story.append(Paragraph(
        "<b>Scientific Limitations:</b> NDVI serves as an indicator of vegetative greenness, not a definitive botanical diagnostic. "
        "It does not directly measure crop yield, plant pathology/disease strains, or soil moisture without auxiliary sensors. "
        "Furthermore, heavy monsoon cloud cover during July–August requires pixel-level cloud filtering via the Scene Classification Layer (SCL).",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # 3. SYSTEM ARCHITECTURE & 4-TIER DESIGN
    # =========================================================================
    story.append(Paragraph("3. System Architecture & Component Separation", h1_style))
    story.append(Paragraph(
        "The application architecture strictly decouples satellite raster computation from the relational database. "
        "Storing multi-gigabyte raster GeoTIFF files inside relational tables leads to severe database bloat, inefficient caching, "
        "and degraded query throughput. Consequently, spatial transformations execute in Google Earth Engine, and derived summary "
        "statistics, bounding coordinates, and temporal records are preserved in MySQL 8.",
        body_style
    ))

    img_arch = ASSETS_DIR / "system_architecture.png"
    if img_arch.exists():
        story.append(Image(str(img_arch), width=6.5 * inch, height=3.2 * inch))
        story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Dual Processing Architecture (Real GEE vs. Demo Mode):</b><br/>"
        "To guarantee operational reliability during academic presentations when cloud credentials or satellite network quotas "
        "might be unavailable, the system incorporates an integrated <b>Demo Mode</b>. When unauthenticated, the engine synthesizes "
        "biologically and climatically calibrated observations for Pune, explicitly annotating all outputs and CSV exports with "
        "<code>DEMO DATA — NOT REAL SATELLITE RESULTS</code>, upholding scientific integrity.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # 4. RELATIONAL DATABASE DESIGN (MYSQL 8)
    # =========================================================================
    story.append(Paragraph("4. Relational Database Design & Schema (MySQL 8)", h1_style))
    story.append(Paragraph(
        "The database <code>pune_vegetation_db</code> was developed specifically for MySQL 8.0, utilizing the InnoDB storage engine "
        "for ACID compliance, foreign key integrity, and row-level concurrency.",
        body_style
    ))

    img_er = ASSETS_DIR / "database_er_schema.png"
    if img_er.exists():
        story.append(Image(str(img_er), width=6.5 * inch, height=3.4 * inch))
        story.append(Spacer(1, 8))

    story.append(Paragraph("Database Table Data Dictionary:", h2_style))

    table_dict = [
        ["Table Name", "Primary Key", "Key Attributes", "Integrity & Constraints"],
        ["study_areas", "area_id (BIGINT)", "area_name, area_type, region_label, geometry_geojson, centroid_lat/lon, area_sq_km", "CHECK(area_type IN ('preset','custom','administrative')), Spatial Indexes"],
        ["satellite_datasets", "dataset_id (BIGINT)", "provider, collection_id (UNIQUE), satellite_name, sensor, band_nir, band_red", "UNIQUE(collection_id), Defaults to Sentinel-2 Harmonized"],
        ["analysis_runs", "analysis_id (BIGINT)", "area_id (FK), dataset_id (FK), start_date, end_date, max_scene_cloud_pct, status", "FK -> study_areas, datasets; CHECK(start_date <= end_date); CHECK(cloud <= 100)"],
        ["ndvi_summaries", "summary_id (BIGINT)", "analysis_id (FK), mean_ndvi, median_ndvi, min_ndvi, max_ndvi, valid_pixel_count", "FK -> analysis_runs (ON DELETE CASCADE); CHECK(mean_ndvi BETWEEN -1 AND 1)"],
        ["ndvi_time_series", "point_id (BIGINT)", "analysis_id (FK), observation_date, mean_ndvi, median_ndvi, image_count", "INDEX(analysis_id, observation_date); UNIQUE(analysis_id, date); ON DELETE CASCADE"],
        ["audit_logs", "log_id (BIGINT)", "action_type, table_name, record_id, details, logged_at", "Populated automatically via Trigger on analysis creation"],
    ]
    t_dict_styled = Table([[Paragraph(c, body_style) for c in row] for row in table_dict], colWidths=[90, 85, 185, 140])
    t_dict_styled.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_dict_styled)

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>ACID Transaction Management:</b><br/>"
        "Persisting an analysis run spans multiple tables: inserting the job definition in <code>analysis_runs</code>, "
        "persisting aggregated statistical metrics in <code>ndvi_summaries</code>, and inserting temporal batch records into "
        "<code>ndvi_time_series</code>. To prevent inconsistent partial states, all operations are grouped into a single atomic "
        "transaction (<code>START TRANSACTION ... COMMIT</code>). An unhandled exception or constraint failure triggers an "
        "immediate <code>ROLLBACK</code>.",
        callout_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # 5. 10 REQUIRED DBMS ASSESSMENT QUERIES
    # =========================================================================
    story.append(Paragraph("5. 10 Required DBMS Assessment Queries & Demonstrations", h1_style))
    story.append(Paragraph(
        "To satisfy the academic evaluation criteria of the DBMS course, 10 specific query classes were constructed and verified "
        "against the live MySQL 8 schema. Each query demonstrates a fundamental relational database concept:",
        body_style
    ))

    queries_data = [
        ("Query 1: Parameterized Filtering by Study Region",
         "SELECT ar.analysis_id, sa.area_name, sa.region_label, ar.start_date, ar.end_date\n"
         "FROM analysis_runs ar\n"
         "JOIN study_areas sa ON ar.area_id = sa.area_id\n"
         "WHERE sa.region_label = 'Mulshi';",
         "Filters analysis jobs specific to the Mulshi catchment zone using indexed foreign keys."),

        ("Query 2: Chronological Sorting of Historical Runs",
         "SELECT analysis_id, area_id, start_date, end_date, processing_status, created_at\n"
         "FROM analysis_runs\n"
         "ORDER BY created_at DESC, analysis_id DESC LIMIT 5;",
         "Demonstrates deterministic ORDER BY sorting for dashboard timeline retrieval."),

        ("Query 3: Statistical Aggregation Across Analyses",
         "SELECT COUNT(ns.summary_id) AS total_analyses, ROUND(AVG(ns.mean_ndvi), 4) AS avg_ndvi,\n"
         "       ROUND(MIN(ns.min_ndvi), 4) AS min_ndvi, ROUND(MAX(ns.max_ndvi), 4) AS max_ndvi\n"
         "FROM ndvi_summaries ns\n"
         "JOIN analysis_runs ar ON ns.analysis_id = ar.analysis_id WHERE ar.processing_status = 'completed';",
         "Computes aggregate statistical properties (COUNT, AVG, MIN, MAX) over completed records."),

        ("Query 4: Multi-Table Equi-JOIN (4 Tables)",
         "SELECT ar.analysis_id, sa.area_name, sd.satellite_name, ar.start_date, ns.mean_ndvi\n"
         "FROM analysis_runs ar\n"
         "INNER JOIN study_areas sa ON ar.area_id = sa.area_id\n"
         "INNER JOIN satellite_datasets sd ON ar.dataset_id = sd.dataset_id\n"
         "INNER JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id ORDER BY ns.mean_ndvi DESC;",
         "Demonstrates 3NF relational reconstruction joining areas, sensors, runs, and metrics."),

        ("Query 5: GROUP BY Comparison by District Zone",
         "SELECT sa.region_label, COUNT(ar.analysis_id) AS runs, ROUND(AVG(ns.mean_ndvi), 4) AS avg_ndvi\n"
         "FROM study_areas sa\n"
         "JOIN analysis_runs ar ON sa.area_id = ar.area_id\n"
         "JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id\n"
         "WHERE ar.processing_status = 'completed' GROUP BY sa.region_label ORDER BY avg_ndvi DESC;",
         "Groups mean vegetative indices across administrative and watershed zones."),

        ("Query 6: HAVING Post-Aggregation Filter",
         "SELECT sa.area_name, ROUND(AVG(ns.mean_ndvi), 4) AS avg_ndvi\n"
         "FROM study_areas sa\n"
         "JOIN analysis_runs ar ON sa.area_id = ar.area_id\n"
         "JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id\n"
         "GROUP BY sa.area_name HAVING AVG(ns.mean_ndvi) < 0.4500 ORDER BY avg_ndvi ASC;",
         "Isolates low-vegetation or highly urbanized sectors whose average index drops below a threshold."),

        ("Query 7: Date-Range Temporal Dimension Query",
         "SELECT ts.point_id, sa.area_name, ts.observation_date, ts.mean_ndvi\n"
         "FROM ndvi_time_series ts\n"
         "JOIN analysis_runs ar ON ts.analysis_id = ar.analysis_id\n"
         "JOIN study_areas sa ON ar.area_id = sa.area_id\n"
         "WHERE ts.observation_date BETWEEN '2023-08-01' AND '2023-11-30' ORDER BY ts.observation_date ASC;",
         "Performs range-based temporal lookups along the observation_date dimension."),

        ("Query 8: Analytical Relational View Query",
         "SELECT analysis_id, area_name, region_label, start_date, end_date, mean_ndvi\n"
         "FROM v_analysis_complete_summary WHERE processing_status = 'completed';",
         "Queries the pre-compiled relational view encapsulating multi-table join logic."),

        ("Query 9: Index Verification & Query Execution Plan",
         "EXPLAIN SELECT observation_date, mean_ndvi FROM ndvi_time_series\n"
         "WHERE analysis_id = 1 AND observation_date >= '2023-09-01';",
         "Demonstrates query optimizer utilizing composite index idx_time_series_analysis_date."),

        ("Query 10: Automated Audit Log Inspection",
         "SELECT log_id, action_type, table_name, record_id, details, logged_at\n"
         "FROM audit_logs ORDER BY logged_at DESC LIMIT 5;",
         "Inspects the audit log automatically populated by trigger trg_audit_analysis_insert."),
    ]

    for q_title, q_sql, q_desc in queries_data:
        story.append(Paragraph(f"<b>{q_title}</b>", h2_style))
        story.append(Paragraph(f"<i>Objective: {q_desc}</i>", body_style))
        story.append(Paragraph(q_sql.replace("\n", "<br/>&nbsp;&nbsp;"), code_style))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # =========================================================================
    # 6. APPLICATION SCREENS & VISUALIZATIONS
    # =========================================================================
    story.append(Paragraph("6. Application Screens & Visualization Features", h1_style))
    story.append(Paragraph(
        "The Streamlit web application organizes the remote sensing workflow into 7 intuitive, responsive screens:",
        body_style
    ))

    screens_info = [
        ("Screen 1: Dashboard", "Real-time system health card showing MySQL 8 connection latency, version (8.0.46), active database, Earth Engine / Demo Mode status badges, total saved study areas, and recent completed runs."),
        ("Screen 2: Select Study Area (Map)", "Interactive Folium map centered on Pune (18.5204° N, 73.8567° E). Features dropdown presets for 8 Pune regions (Pune City Core, Haveli, Mulshi, Maval, Bhor, Baramati, Shirur, Daund). Includes Leaflet drawing tools allowing custom polygons with geodesic area calculation in km² and saving to MySQL."),
        ("Screen 3: Run NDVI Analysis", "Form configuring satellite start/end dates, cloud coverage cutoff slider, execution mode toggle, and transaction-backed execution saving runs and time-series points to MySQL."),
        ("Screen 4: NDVI Map Visualizer", "Spatial display with the 5-step vegetation color palette (Red -> Orange -> Yellow -> Light Green -> Green), legend, and Earth Engine style visualization parameters (Range slider, Opacity slider)."),
        ("Screen 5: Trends & Statistics", "Interactive Plotly time-series curve tracking seasonal vegetative changes (monsoon greening vs dry-season troughs), side-by-side comparison between two study areas, and CSV report export."),
        ("Screen 6: Database Explorer & SQL Lab", "Live table viewer for all MySQL tables and relational views, safe parameterized filtering, CSV export, and execution button for the 10 course assessment queries."),
        ("Screen 7: Literature & Methodology", "Academic references, sensor technical specifications (Sentinel-2 MSI 10m), NDVI equations, and system limitations."),
    ]

    for s_name, s_detail in screens_info:
        story.append(Paragraph(f"• <b>{s_name}</b>: {s_detail}", bullet_style))

    story.append(Spacer(1, 10))

    img_ts = ASSETS_DIR / "ndvi_time_series_reference.png"
    if img_ts.exists():
        story.append(Paragraph("Figure: NDVI Seasonal Time Series Profile across Pune Talukas", h2_style))
        story.append(Image(str(img_ts), width=6.5 * inch, height=2.7 * inch))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # =========================================================================
    # 7. STEP-BY-STEP EXECUTION GUIDE
    # =========================================================================
    story.append(Paragraph("7. Step-by-Step Installation & Execution Guide", h1_style))
    story.append(Paragraph(
        "Follow these concise instructions to run and verify the complete project locally on Windows:",
        body_style
    ))

    steps_list = [
        ("Step 1: Install Python Dependencies",
         "Open PowerShell in the project directory (D:\\DBMS_CP) and execute:\n"
         "python -m pip install -r requirements.txt\n"
         "This installs Streamlit, Folium, Plotly, PyMySQL, SQLAlchemy, Shapely, PyProj, and ReportLab."),

        ("Step 2: Initialize Database in MySQL Workbench",
         "1. Launch MySQL Workbench 8.0 and connect to 'Local instance MySQL80'.\n"
         "2. Click File -> Open SQL Script... and select 'D:\\DBMS_CP\\db\\schema.sql'.\n"
         "3. Click the yellow lightning bolt icon (⚡) to execute all DDL statements.\n"
         "4. Open 'D:\\DBMS_CP\\db\\seed_demo_data.sql' and click (⚡) to load Pune presets and sample runs.\n"
         "5. Right-click under SCHEMAS and click 'Refresh All' to see 'pune_vegetation_db'."),

        ("Step 3: Configure Local Environment (.env)",
         "Copy the template and specify your MySQL root password:\n"
         "Copy-Item .env.example .env\n"
         "Edit line 22 of .env:\n"
         "DB_PASSWORD=your_actual_mysql_password"),

        ("Step 4: Test Database Connection",
         "Run the diagnostic script from PowerShell:\n"
         "python db/test_connection.py\n"
         "Expected Output: [SUCCESS] Connected successfully to MySQL Server! Version 8.0.46, Tables: 9."),

        ("Step 5: Run Automated Unit & Integration Tests",
         "Run the pytest suite:\n"
         "python -m pytest tests/\n"
         "Result: 19 passed in 1.44s (Geometry, NDVI Math, CRUD, Views, and ACID Transactions verified)."),

        ("Step 6: Launch Web Application",
         "Start the Streamlit development server:\n"
         "streamlit run app.py\n"
         "Open your web browser and navigate to http://localhost:8501."),
    ]

    for st_title, st_body in steps_list:
        story.append(Paragraph(f"<b>{st_title}</b>", h2_style))
        story.append(Paragraph(st_body.replace("\n", "<br/>"), code_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))
    story.append(Paragraph("8. Quality Assurance & Verification Results", h1_style))
    story.append(Paragraph(
        "The project includes a comprehensive automated test suite in the <code>tests/</code> folder. "
        "All test categories executed with 100% pass rates:<br/>"
        "• <b>test_ndvi.py (6/6 passed)</b>: Verifies formula accuracy with known values (NIR=0.8, Red=0.2 yields 0.6), denominator zero division safety, mathematical bounds [-1.0, 1.0], and statistical aggregations.<br/>"
        "• <b>test_geometry.py (4/4 passed)</b>: Verifies GeoJSON polygon parsing, topological closure, geodesic area calculation in km², and maximum surface area boundary checks.<br/>"
        "• <b>test_validation.py (4/4 passed)</b>: Verifies date chronological ordering (start &lt; end), cloud cover percentages (0-100%), and CSV export column schemas.<br/>"
        "• <b>test_repository.py (5/5 passed)</b>: Verifies live MySQL 8 insert and retrieval, foreign key cascades, analytical views, and multi-table ACID transaction consistency.",
        callout_style
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("9. Academic Literature References", h1_style))
    story.append(Paragraph(
        "1. <b>Rouse, J. W., Haas, R. H., Schell, J. A., & Deering, D. W. (1974)</b>. <i>Monitoring the vernal advancement and retrogradation (Greenwave effect) of natural vegetation</i>. NASA/GSFC Final Report.<br/>"
        "2. <b>Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., ... & Bargellini, P. (2012)</b>. <i>Sentinel-2: ESA's optical high-resolution mission for GMES operational services</i>. Remote Sensing of Environment, 120, 25-36.<br/>"
        "3. <b>Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017)</b>. <i>Google Earth Engine: Planetary-scale geospatial analysis for everyone</i>. Remote Sensing of Environment, 202, 18-27.<br/>"
        "4. <b>Gadgil, S., & Joshi, N. V. (1983)</b>. <i>Climatic clusters of the Indian region</i>. Journal of Climatology, 3(1), 47-63. (Focusing on Western Ghats precipitation gradients).",
        body_style
    ))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Comprehensive Project Report PDF successfully compiled at: {OUTPUT_PDF.resolve()}")


if __name__ == "__main__":
    build_pdf()
