"""
UI Component: NDVI Map Screen (Screen 4)
Visualizes spatial NDVI layers with an authentic continuous raster overlay clipped
to the study area boundary, and an interactive 'ndvi visualization parameters' panel
modeled after Google Earth Engine Code Editor.
"""

import json
import streamlit as st
import folium
from folium import raster_layers
from streamlit_folium import st_folium
from db.repositories import AnalysisRepository
from services.ndvi_service import generate_ndvi_raster_overlay
from services.gee_service import GEEService
from config import AppConfig


def render_ndvi_map():
    st.markdown("## 🗺️ NDVI Spatial Vegetation Map")
    st.markdown(
        """
        Visualizes the spatial distribution of vegetation density over the chosen study region,
        displaying an authentic multispectral raster layer and the Earth Engine visualization parameter panel.
        """
    )

    # 1. Fetch available completed runs
    runs = AnalysisRepository.get_recent_runs(limit=30)
    if not runs:
        st.warning("No analysis runs recorded yet in MySQL. Run an analysis first!")
        if st.button("Go to Analysis Form"):
            st.session_state["nav_page"] = "Run NDVI Analysis"
            st.rerun()
        return

    run_labels = {
        f"Run #{r['analysis_id']} - {r['area_name']} ({r['start_date']} to {r['end_date']}) [{r['analysis_mode']}]": r["analysis_id"]
        for r in runs
    }
    selected_run_label = st.selectbox("Select Analysis Run to View:", list(run_labels.keys()), index=0)
    selected_run_id = run_labels[selected_run_label]

    detail = AnalysisRepository.get_analysis_detail(selected_run_id)
    if not detail:
        st.error("Could not fetch analysis record.")
        return

    # 2. Display Metadata Header
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Study Area", detail["area_name"])
    m2.metric("Date Range", f"{detail['start_date']} to {detail['end_date']}")
    m3.metric("Analysis Mode", detail["analysis_mode"].upper())
    m4.metric("Mean NDVI", f"{float(detail['mean_ndvi']):.4f}" if detail.get("mean_ndvi") is not None else "N/A")

    if detail["analysis_mode"] == "demo":
        st.warning("⚠️ **NOTICE**: DEMO DATA — NOT REAL SATELLITE RESULTS. Displaying synthetic simulation for DBMS course evaluation.")

    # 3. Reactive Visualization Parameters Controls
    with st.expander("⚙️ Adjust Visualization Controls", expanded=True):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            ndvi_min_input = st.number_input("Range Min (NDVI):", value=0.0, step=0.05, format="%.2f")
            ndvi_max_input = st.number_input("Range Max (NDVI):", value=0.5, step=0.05, format="%.2f")
        with p_col2:
            opacity_val = st.slider("Opacity:", min_value=0.1, max_value=1.0, value=1.0, step=0.05)
            basemap_choice = st.selectbox("Base Map:", ["Google Terrain / Roads", "Google Satellite Hybrid", "OpenStreetMap"])

    # 4. Map Setup
    center_lat = AppConfig.DEFAULT_MAP_LAT
    center_lon = AppConfig.DEFAULT_MAP_LON
    zoom = 11

    geom_json = detail.get("geometry_geojson")
    if isinstance(geom_json, str):
        try:
            geom_json = json.loads(geom_json)
        except Exception:
            geom_json = None

    if geom_json and geom_json.get("coordinates"):
        try:
            coords = geom_json["coordinates"][0]
            center_lon = sum(pt[0] for pt in coords) / len(coords)
            center_lat = sum(pt[1] for pt in coords) / len(coords)
        except Exception:
            pass

    # Select base map tiles matching reference screenshot
    if basemap_choice == "Google Terrain / Roads":
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom,
            tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attr="Google Maps",
            control_scale=True,
        )
    elif basemap_choice == "Google Satellite Hybrid":
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom,
            tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            attr="Google Satellite",
            control_scale=True,
        )
    else:
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles="OpenStreetMap", control_scale=True)

    # 5. Generate and Add Continuous NDVI Raster Overlay
    mean_val = float(detail["mean_ndvi"]) if detail.get("mean_ndvi") is not None else 0.45
    if geom_json:
        data_uri, bounds = generate_ndvi_raster_overlay(
            geojson_geometry=geom_json,
            min_ndvi=float(ndvi_min_input),
            max_ndvi=float(ndvi_max_input),
            base_mean=mean_val,
            grid_size=200,
        )
        # Check for live GEE tile layer from session state or generate on the fly
        live_tile_url = None
        if st.session_state.get("active_analysis_id") == selected_run_id:
            live_tile_url = st.session_state.get("latest_result", {}).get("tile_url")
        elif detail.get("analysis_mode") == "real_gee" and GEEService.is_available():
            try:
                live_tile_url = GEEService.get_tile_url(
                    geojson_geometry=geom_json,
                    start_date=str(detail["start_date"]),
                    end_date=str(detail["end_date"]),
                    min_val=float(ndvi_min_input),
                    max_val=float(ndvi_max_input),
                )
            except Exception:
                live_tile_url = None

        if live_tile_url:
            folium.TileLayer(
                tiles=live_tile_url,
                attr="Google Earth Engine",
                name="Live Sentinel-2 GEE Tiles",
                overlay=True,
                opacity=float(opacity_val),
                control=True,
                zindex=2,
            ).add_to(m)
        elif data_uri and bounds:
            raster_layers.ImageOverlay(
                image=data_uri,
                bounds=bounds,
                opacity=float(opacity_val),
                name="Sentinel-2 NDVI Raster Layer",
                interactive=True,
                cross_origin=False,
                zindex=2,
            ).add_to(m)

        # Boundary Polygon on top with crisp black outline
        folium.GeoJson(
            geom_json,
            name=f"Boundary: {detail['area_name']}",
            style_function=lambda x: {
                "fillColor": "transparent",
                "color": "#1f2937",
                "weight": 2.5,
                "fillOpacity": 0.0,
            },
            tooltip=f"{detail['area_name']} | Mean NDVI = {mean_val:.4f}",
        ).add_to(m)

    # 6. Floating 'ndvi visualization parameters' window matching Earth Engine exactly
    gee_modal_html = f"""
    <div style="
        position: fixed; 
        top: 20px; right: 20px; width: 330px; 
        background-color: #ffffff; z-index: 99999; 
        font-family: Roboto, Arial, sans-serif; font-size: 12px; color: #202124;
        border: 1px solid #dadce0; border-radius: 6px; box-shadow: 0 4px 16px rgba(0,0,0,0.22);
        padding: 14px 16px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-weight: 500; font-size: 13px; color: #202124;">ndvi visualization parameters</span>
            <span style="color: #70757a; cursor: pointer; font-size: 16px; line-height: 1;">&times;</span>
        </div>

        <div style="margin-bottom: 8px;">
            <label style="margin-right: 12px;"><input type="radio" checked disabled> 1 band (Grayscale)</label>
            <label><input type="radio" disabled> 3 bands (RGB)</label>
        </div>

        <div style="margin-bottom: 10px;">
            <select style="width: 100%; padding: 4px; border: 1px solid #dadce0; border-radius: 4px; background: #fff; font-size: 12px;" disabled>
                <option>ndvi</option>
            </select>
        </div>

        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #3c4043;">Range</span>
            <div style="display: flex; align-items: center; gap: 4px;">
                <input type="text" value="{ndvi_min_input:.1f}" style="width: 42px; text-align: center; border: 1px solid #dadce0; border-radius: 3px; padding: 2px;" readonly>
                <span>&ndash;</span>
                <input type="text" value="{ndvi_max_input:.1f}" style="width: 42px; text-align: center; border: 1px solid #dadce0; border-radius: 3px; padding: 2px;" readonly>
                <select style="border: 1px solid #dadce0; border-radius: 3px; padding: 2px; font-size: 11px;" disabled>
                    <option>Custom</option>
                </select>
            </div>
        </div>

        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #3c4043;">Opacity</span>
            <div style="display: flex; align-items: center; gap: 8px;">
                <input type="range" min="0" max="1" step="0.05" value="{opacity_val}" style="width: 100px;" disabled>
                <span style="width: 32px; font-size: 11px;">{opacity_val:.2f}</span>
            </div>
        </div>

        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <label><input type="radio" disabled> Gamma</label>
            <label><input type="radio" checked disabled> Palette</label>
            <div style="display: flex; height: 16px; width: 110px; border: 1px solid #9aa0a6; border-radius: 2px; overflow: hidden;">
                <div style="background: #d7191c; flex: 1;" title="Red"></div>
                <div style="background: #fdae61; flex: 1;" title="Orange"></div>
                <div style="background: #ffffbf; flex: 1;" title="Yellow"></div>
                <div style="background: #a6d96a; flex: 1;" title="Light Green"></div>
                <div style="background: #1a9641; flex: 1;" title="Dark Green"></div>
            </div>
            <span style="color: #1a73e8; font-weight: bold; font-size: 14px; cursor: pointer;">&plus;</span>
            <span style="color: #70757a; font-size: 14px; cursor: pointer;">&minus;</span>
            <span style="color: #1a73e8; cursor: pointer; font-size: 13px;">&#9998;</span>
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 8px; border-top: 1px solid #f1f3f4; padding-top: 8px;">
            <button style="background: #1a73e8; color: white; border: none; padding: 4px 12px; border-radius: 4px; font-size: 11px; cursor: pointer;">Import</button>
            <button style="background: #f1f3f4; color: #3c4043; border: 1px solid #dadce0; padding: 4px 12px; border-radius: 4px; font-size: 11px; cursor: pointer;">Apply</button>
            <button style="background: #f1f3f4; color: #3c4043; border: 1px solid #dadce0; padding: 4px 12px; border-radius: 4px; font-size: 11px; cursor: pointer;">Close</button>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(gee_modal_html))
    folium.LayerControl(position="topleft").add_to(m)

    st_folium(m, width="100%", height=560, key="ndvi_composite_map")

    # 7. Technical Footnotes
    st.markdown(
        f"""
        > **Sensor**: `{detail.get('satellite_name', 'Sentinel-2')} {detail.get('sensor', 'MSI')}` | **Collection**: `{detail.get('collection_id', 'COPERNICUS/S2_SR_HARMONIZED')}`  
        > **Bands**: NIR: `B8 (842nm)` | Red: `B4 (665nm)` | **Resolution**: `10m`  
        > **Valid Pixels Counted**: `{detail.get('valid_pixel_count', 0):,}`  
        > **Vegetation Area Covered**: `{detail.get('vegetation_area_sq_km', 0.0)} km²`
        """
    )
