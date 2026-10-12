"""
UI Component: Select Study Area Screen (Screen 2)
Provides an interactive Folium map centered on Pune, preset region selection,
custom polygon/rectangle drawing, geodesic area calculation, and database persistence.
"""

import json
import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium

from config import AppConfig
from db.repositories import StudyAreaRepository
from services.geometry_service import GeometryService


def render_area_selector():
    st.markdown("## 🗺️ Select or Define Study Area (Pune Region)")
    st.markdown(
        """
        Choose a predefined study area around Pune (e.g., Haveli, Mulshi, Bhor) or use the drawing tools on the map
        to outline a custom bounding polygon. The calculated geodesic surface area is shown in square kilometres.
        """
    )

    # 1. Fetch existing study areas from database
    try:
        existing_areas = StudyAreaRepository.get_all()
    except Exception as e:
        st.error(f"Failed to query study_areas from MySQL: {e}")
        existing_areas = []

    col_map, col_controls = st.columns([7, 5])

    # Preset selection handling
    preset_names = ["-- Custom Draw Mode --"] + [f"{a['area_name']} ({a['region_label']})" for a in existing_areas]
    
    with col_controls:
        st.markdown("### 📍 Area Selection Controls")
        selected_option = st.selectbox("Choose a Study Area Preset:", preset_names, index=1 if len(preset_names) > 1 else 0)

        selected_area_record = None
        if selected_option != "-- Custom Draw Mode --":
            chosen_name = selected_option.split(" (")[0]
            selected_area_record = next((a for a in existing_areas if a["area_name"] == chosen_name), None)

        if selected_area_record:
            st.info(
                f"**Selected Preset**: {selected_area_record['area_name']}\n"
                f"- **Region**: {selected_area_record['region_label']}\n"
                f"- **Area**: {selected_area_record['area_sq_km']} km²\n"
                f"- **Centroid**: ({selected_area_record['centroid_lat']:.4f}, {selected_area_record['centroid_lon']:.4f})\n"
                f"- **Source**: {selected_area_record['boundary_source']}"
            )
            # Store in session state for analysis form
            st.session_state["active_study_area_id"] = selected_area_record["area_id"]
            st.session_state["active_study_area_name"] = selected_area_record["area_name"]

    # 2. Build Folium Map
    center_lat = AppConfig.DEFAULT_MAP_LAT
    center_lon = AppConfig.DEFAULT_MAP_LON
    zoom = AppConfig.DEFAULT_MAP_ZOOM

    if selected_area_record and selected_area_record.get("centroid_lat"):
        center_lat = float(selected_area_record["centroid_lat"])
        center_lon = float(selected_area_record["centroid_lon"])
        zoom = 11

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    # Add Google Satellite Hybrid layer option
    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attr="Google Satellite",
        name="Satellite Hybrid",
        overlay=False,
        control=True,
    ).add_to(m)

    # Display polygon if preset is active
    if selected_area_record and selected_area_record.get("geometry_geojson"):
        geom = selected_area_record["geometry_geojson"]
        if isinstance(geom, str):
            try:
                geom = json.loads(geom)
            except Exception:
                geom = None
        if geom:
            folium.GeoJson(
                geom,
                name=selected_area_record["area_name"],
                style_function=lambda x: {
                    "fillColor": "#22c55e",
                    "color": "#15803d",
                    "weight": 3,
                    "fillOpacity": 0.35,
                },
                tooltip=f"{selected_area_record['area_name']} ({selected_area_record['area_sq_km']} km²)",
            ).add_to(m)

    # Add Drawing Plugin for Custom Polygons
    draw = Draw(
        export=True,
        filename="custom_study_area.geojson",
        position="topleft",
        draw_options={
            "polyline": False,
            "circle": False,
            "circlemarker": False,
            "marker": False,
            "polygon": True,
            "rectangle": True,
        },
        edit_options={"edit": True, "remove": True},
    )
    draw.add_to(m)
    folium.LayerControl().add_to(m)

    with col_map:
        st.markdown("#### 🗺️ Map Viewer (Pune Centered)")
        map_output = st_folium(m, width="100%", height=520, key="study_area_map")

    # 3. Handle Drawn Polygon Capture
    drawn_geom = None
    if map_output and map_output.get("last_active_drawing"):
        drawn_geom = map_output["last_active_drawing"]

    with col_controls:
        st.markdown("---")
        st.markdown("### ✏️ Save Custom Drawn Polygon")

        if drawn_geom:
            is_valid, err_msg, sanitized_geom, area_km2, centroid = (
                GeometryService.parse_and_validate_geojson(drawn_geom)
            )
            if is_valid:
                st.success(f"✅ Valid Polygon Detected!\n- **Computed Area**: {area_km2} km²\n- **Centroid**: {centroid}")
                custom_name = st.text_input("Area Name:", value="Custom Pune Study Region")
                custom_region = st.text_input("Region Label:", value="Pune Metropolitan")

                if st.button("💾 Save Polygon to Database", type="primary", use_container_width=True):
                    try:
                        new_id = StudyAreaRepository.create(
                            area_name=custom_name.strip(),
                            area_type="custom",
                            region_label=custom_region.strip(),
                            geometry_geojson=sanitized_geom,
                            centroid_lat=centroid[0],
                            centroid_lon=centroid[1],
                            area_sq_km=area_km2,
                            boundary_source="User Drawn via Leaflet in Streamlit",
                        )
                        st.success(f"🎉 Successfully saved study area '{custom_name}' with ID #{new_id} in MySQL!")
                        st.session_state["active_study_area_id"] = new_id
                        st.session_state["active_study_area_name"] = custom_name
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to persist polygon to MySQL: {e}")
            else:
                st.warning(f"⚠️ {err_msg}")
        else:
            if selected_option == "-- Custom Draw Mode --":
                st.caption("Use the polygon or rectangle tool in the top-left of the map to outline an area.")
