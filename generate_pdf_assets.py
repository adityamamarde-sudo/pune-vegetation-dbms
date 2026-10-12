"""
Script to generate high-resolution diagrams and charts for the DBMS project PDF report.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

ASSETS_DIR = Path("docs/assets")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def generate_architecture_diagram():
    """Generates the 4-tier system architecture diagram."""
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.axis("off")

    # Background
    ax.set_facecolor("#f8fafc")
    fig.patch.set_facecolor("#f8fafc")

    # Layer Boxes
    layers = [
        ("Layer 1: Presentation Tier (Streamlit Web UI)", 
         "Dashboard | Pune Map Selector (Folium) | NDVI Form | Trends (Plotly) | DB Explorer | Literature", 
         "#dbeafe", "#1e40af", 0.78),
        ("Layer 2: Service & Logic Tier (Python 3.11)", 
         "GeometryService (Shapely/pyproj) | NDVIService | GEEService | AnalysisService Orchestrator", 
         "#dcfce7", "#166534", 0.53),
        ("Layer 3: Processing & External Compute Tier", 
         "Google Earth Engine (COPERNICUS/S2_SR_HARMONIZED) | SCL Cloud Masking | Median Compositing", 
         "#ffedd5", "#c2410c", 0.28),
        ("Layer 4: Relational Data Tier (MySQL 8.0 Server)", 
         "InnoDB Engine (3NF Schema) | study_areas, analysis_runs, ndvi_summaries, ndvi_time_series | ACID Transactions", 
         "#ede9fe", "#5b21b6", 0.03),
    ]

    for title, subtitle, bg_color, border_color, y_pos in layers:
        rect = patches.FancyBboxPatch(
            (0.05, y_pos), 0.90, 0.18,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=2,
        )
        ax.add_patch(rect)
        ax.text(0.50, y_pos + 0.11, title, ha="center", va="center", fontsize=11, fontweight="bold", color=border_color)
        ax.text(0.50, y_pos + 0.05, subtitle, ha="center", va="center", fontsize=8.5, color="#334155")

    # Connectors
    for y_arrow in [0.74, 0.49, 0.24]:
        ax.annotate("", xy=(0.50, y_arrow), xytext=(0.50, y_arrow + 0.04),
                    arrowprops=dict(arrowstyle="->", color="#64748b", lw=2.5))

    plt.tight_layout()
    out_path = ASSETS_DIR / "system_architecture.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def generate_er_diagram_graphic():
    """Generates a visual Entity-Relationship schema overview."""
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.axis("off")
    ax.set_facecolor("#ffffff")
    fig.patch.set_facecolor("#ffffff")

    entities = [
        ("study_areas", 0.05, 0.60, "#e0f2fe", "#0369a1", [
            "PK: area_id (BIGINT)",
            "area_name (VARCHAR)",
            "region_label (VARCHAR)",
            "geometry_geojson (JSON)",
            "centroid_lat / lon (DECIMAL)",
            "area_sq_km (DECIMAL)"
        ]),
        ("satellite_datasets", 0.68, 0.60, "#fef3c7", "#b45309", [
            "PK: dataset_id (BIGINT)",
            "collection_id (VARCHAR)",
            "satellite_name (Sentinel-2)",
            "band_nir (B8 - 842nm)",
            "band_red (B4 - 665nm)",
            "sensor (MSI)"
        ]),
        ("analysis_runs", 0.36, 0.52, "#dcfce7", "#15803d", [
            "PK: analysis_id (BIGINT)",
            "FK: area_id -> study_areas",
            "FK: dataset_id -> datasets",
            "start_date / end_date (DATE)",
            "max_scene_cloud_pct (DEC)",
            "processing_status (VARCHAR)",
            "analysis_mode (real/demo)"
        ]),
        ("ndvi_summaries", 0.15, 0.08, "#fae8ff", "#86198f", [
            "PK: summary_id (BIGINT)",
            "FK: analysis_id -> runs",
            "mean_ndvi (DECIMAL 8,6)",
            "median_ndvi (DECIMAL 8,6)",
            "min_ndvi / max_ndvi",
            "valid_pixel_count (BIGINT)",
            "vegetation_area_sq_km"
        ]),
        ("ndvi_time_series", 0.58, 0.08, "#ffe4e6", "#be123c", [
            "PK: point_id (BIGINT)",
            "FK: analysis_id -> runs",
            "observation_date (DATE)",
            "mean_ndvi (DECIMAL 8,6)",
            "median_ndvi (DECIMAL 8,6)",
            "image_count (INT)",
            "INDEX (analysis_id, date)"
        ]),
    ]

    for name, x, y, bg, border, fields in entities:
        rect = patches.FancyBboxPatch(
            (x, y), 0.27, 0.32,
            boxstyle="round,pad=0.015,rounding_size=0.02",
            facecolor=bg, edgecolor=border, linewidth=2
        )
        ax.add_patch(rect)
        ax.text(x + 0.135, y + 0.27, name, ha="center", va="center", fontsize=11, fontweight="bold", color=border)
        ax.plot([x + 0.02, x + 0.25], [y + 0.24, y + 0.24], color=border, lw=1)
        for idx, f in enumerate(fields):
            ax.text(x + 0.02, y + 0.20 - (idx * 0.033), f, ha="left", va="center", fontsize=7.5, color="#1e293b")

    # Arrows for Relationships
    ax.annotate("", xy=(0.36, 0.68), xytext=(0.32, 0.74), arrowprops=dict(arrowstyle="<-", color="#0284c7", lw=2))
    ax.text(0.34, 0.73, "1 : N", fontsize=9, color="#0284c7", fontweight="bold")

    ax.annotate("", xy=(0.63, 0.68), xytext=(0.68, 0.74), arrowprops=dict(arrowstyle="<-", color="#d97706", lw=2))
    ax.text(0.64, 0.73, "1 : N", fontsize=9, color="#d97706", fontweight="bold")

    ax.annotate("", xy=(0.30, 0.40), xytext=(0.45, 0.52), arrowprops=dict(arrowstyle="<-", color="#86198f", lw=2))
    ax.text(0.35, 0.47, "1 : 1..N", fontsize=9, color="#86198f", fontweight="bold")

    ax.annotate("", xy=(0.68, 0.40), xytext=(0.55, 0.52), arrowprops=dict(arrowstyle="<-", color="#be123c", lw=2))
    ax.text(0.61, 0.47, "1 : N", fontsize=9, color="#be123c", fontweight="bold")

    plt.tight_layout()
    out_path = ASSETS_DIR / "database_er_schema.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def generate_spectral_ndvi_graphic():
    """Generates the NDVI spectral formula and leaf reflectance diagram."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), dpi=300)
    fig.patch.set_facecolor("#ffffff")

    # Left: Leaf Reflectance Concept
    wavelengths = [450, 560, 665, 842, 1610]
    healthy_leaf = [0.05, 0.12, 0.06, 0.55, 0.22]
    soil = [0.10, 0.18, 0.25, 0.28, 0.32]

    ax1.plot(wavelengths, healthy_leaf, "o-", color="#16a34a", lw=2.5, label="Healthy Green Foliage")
    ax1.plot(wavelengths, soil, "s--", color="#b45309", lw=2, label="Bare Soil / Urban")
    ax1.axvspan(640, 690, color="#f87171", alpha=0.25, label="Red Band (B4: 665nm)")
    ax1.axvspan(810, 870, color="#86efac", alpha=0.25, label="NIR Band (B8: 842nm)")
    ax1.set_title("Spectral Reflectance Profiles (Sentinel-2)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Wavelength (nm)", fontsize=9)
    ax1.set_ylabel("Reflectance Ratio", fontsize=9)
    ax1.set_ylim(0, 0.65)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(fontsize=8, loc="upper left")

    # Right: Formula & Palette
    ax2.axis("off")
    ax2.text(0.5, 0.85, "NDVI Formula (Rouse et al., 1974)", ha="center", fontsize=11, fontweight="bold")
    ax2.text(0.5, 0.68, r"$\mathrm{NDVI} = \frac{\mathrm{NIR\ (B8)} - \mathrm{Red\ (B4)}}{\mathrm{NIR\ (B8)} + \mathrm{Red\ (B4)}}$",
             ha="center", fontsize=14, color="#1e3a8a")

    # Palette ramp
    palette = [
        ("#d7191c", "< 0.10", "Bare Soil / Urban"),
        ("#fdae61", "0.10 - 0.25", "Built-up / Shrub"),
        ("#ffffbf", "0.25 - 0.40", "Sparse Vegetation"),
        ("#a6d96a", "0.40 - 0.55", "Moderate Canopy"),
        ("#1a9641", "> 0.55", "Dense Green Foliage"),
    ]
    y_start = 0.42
    for color, rng, desc in palette:
        rect = patches.Rectangle((0.15, y_start), 0.12, 0.07, facecolor=color, edgecolor="#475569")
        ax2.add_patch(rect)
        ax2.text(0.32, y_start + 0.035, f"{rng} : {desc}", va="center", fontsize=8.5, color="#1e293b")
        y_start -= 0.085

    plt.tight_layout()
    out_path = ASSETS_DIR / "spectral_ndvi_concept.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def generate_time_series_graphic():
    """Generates the reference NDVI time series plot (matching user Image 2)."""
    fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    months = ["2023-Jan", "2023-Feb", "2023-Mar", "2023-Apr", "2023-May", "2023-Jun",
              "2023-Jul", "2023-Aug", "2023-Sep", "2023-Oct", "2023-Nov", "2023-Dec"]
    x = np.arange(len(months))

    # Mulshi (high rainfall Western Ghats) vs Pune Urban (built-up)
    mulshi_ndvi = [0.48, 0.42, 0.35, 0.28, 0.25, 0.52, 0.68, 0.74, 0.78, 0.72, 0.64, 0.55]
    pune_urban = [0.32, 0.29, 0.26, 0.22, 0.20, 0.28, 0.35, 0.41, 0.43, 0.38, 0.35, 0.33]

    ax.plot(x, mulshi_ndvi, "o-", color="#1d4ed8", lw=2.5, markersize=6, label="Mulshi Watershed (Western Ghats)")
    ax.plot(x, pune_urban, "s--", color="#dc2626", lw=2.0, markersize=5, label="Pune Urban Core (Metropolitan)")

    ax.set_title("NDVI Time Series: Seasonal Trajectory in Pune Region", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("NDVI", fontsize=10, fontweight="bold")
    ax.set_xlabel("Observation Month", fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=35, ha="right", fontsize=8.5)
    ax.set_ylim(0.0, 0.85)
    ax.grid(True, linestyle="-", color="#e5e7eb", alpha=0.8)
    ax.legend(fontsize=9, loc="upper right", framealpha=0.95)

    plt.tight_layout()
    out_path = ASSETS_DIR / "ndvi_time_series_reference.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    generate_architecture_diagram()
    generate_er_diagram_graphic()
    generate_spectral_ndvi_graphic()
    generate_time_series_graphic()
    print("All report assets generated successfully.")
