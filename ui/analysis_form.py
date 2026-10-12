"""
UI Component: Run NDVI Analysis Form (Screen 3)
Allows users to configure satellite date ranges, cloud cover thresholds,
and trigger GEE or Demo computations with transaction-based MySQL persistence.
"""

import datetime
import streamlit as st
from db.repositories import StudyAreaRepository
from services.analysis_service import AnalysisService
from services.gee_service import GEEService


def render_analysis_form():
    st.markdown("## 🛰️ Run NDVI Vegetation Analysis")
    st.markdown(
        """
        Configure satellite imagery filters (temporal window and cloud threshold) and compute the
        **Normalized Difference Vegetation Index (NDVI)** using Sentinel-2 B8 (Near-Infrared) and B4 (Red) bands.
        """
    )

    # 1. Fetch study areas
    try:
        areas = StudyAreaRepository.get_all()
    except Exception as e:
        st.error(f"Failed to fetch study areas: {e}")
        return

    if not areas:
        st.warning("No study areas found in the database. Please select or draw a study area first.")
        if st.button("Go to Study Area Selector"):
            st.session_state["nav_page"] = "Select Study Area"
            st.rerun()
        return

    area_dict = {f"{a['area_name']} ({a['region_label']} - {a['area_sq_km']} km²)": a["area_id"] for a in areas}
    area_labels = list(area_dict.keys())

    # Pre-select if passed from map selector
    default_index = 0
    if "active_study_area_id" in st.session_state:
        for idx, (label, aid) in enumerate(area_dict.items()):
            if aid == st.session_state["active_study_area_id"]:
                default_index = idx
                break

    # 2. Form Layout
    with st.form("ndvi_analysis_form"):
        st.markdown("### 1. Select Study Region")
        selected_label = st.selectbox("Study Area:", area_labels, index=default_index)
        chosen_area_id = area_dict[selected_label]

        st.markdown("### 2. Temporal & Cloud Parameters")
        c1, c2 = st.columns(2)
        with c1:
            start_date = st.date_input("Start Date:", value=datetime.date(2023, 6, 1), min_value=datetime.date(2015, 6, 23))
        with c2:
            end_date = st.date_input("End Date:", value=datetime.date(2023, 11, 30), max_value=datetime.date.today())

        c_cloud, c_mode = st.columns(2)
        with c_cloud:
            max_cloud = st.slider("Maximum Scene Cloud Cover (%):", min_value=0, max_value=100, value=20, step=5)

        with c_mode:
            gee_avail = GEEService.is_available()
            if gee_avail:
                force_demo = st.checkbox("Force Demo Mode (for offline testing)", value=False)
                mode_str = "Demo Mode (Manual Override)" if force_demo else "Real Google Earth Engine"
            else:
                force_demo = True
                mode_str = "Demo Mode (GEE unauthenticated)"
            st.info(f"**Execution Engine**: {mode_str}")

        submit_btn = st.form_submit_button("🚀 Execute Analysis & Persist to MySQL", type="primary", use_container_width=True)

    # 3. Execution Handler
    if submit_btn:
        s_date_str = start_date.strftime("%Y-%m-%d")
        e_date_str = end_date.strftime("%Y-%m-%d")

        if start_date >= end_date:
            st.error("Validation Error: Start Date must be earlier than End Date.")
            return

        with st.spinner("Processing multispectral satellite imagery and saving records to MySQL 8..."):
            success, msg, analysis_id, result_bundle = AnalysisService.execute_and_persist_analysis(
                area_id=chosen_area_id,
                start_date=s_date_str,
                end_date=e_date_str,
                max_scene_cloud_pct=float(max_cloud),
                force_demo=force_demo,
            )

        if success:
            st.success(f"🎉 **Analysis #{analysis_id} Completed Successfully!**\n- {msg}")
            st.session_state["active_analysis_id"] = analysis_id
            st.session_state["latest_result"] = result_bundle

            summary = result_bundle.get("summary_stats", {})
            st.markdown("#### 📊 Summary Metrics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Mean NDVI", f"{summary.get('mean_ndvi', 0.0):.4f}")
            m2.metric("Median NDVI", f"{summary.get('median_ndvi', 0.0):.4f}")
            m3.metric("Min NDVI", f"{summary.get('min_ndvi', 0.0):.4f}")
            m4.metric("Max NDVI", f"{summary.get('max_ndvi', 0.0):.4f}")

            if result_bundle.get("analysis_mode") == "demo":
                st.warning("⚠️ **NOTICE**: DEMO DATA — NOT REAL SATELLITE RESULTS. Synthetic observations generated for DBMS assessment.")

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🗺️ View NDVI Map", use_container_width=True):
                    st.session_state["nav_page"] = "NDVI Map"
                    st.rerun()
            with col_btn2:
                if st.button("📈 View Trends & Plots", use_container_width=True):
                    st.session_state["nav_page"] = "Trends & Statistics"
                    st.rerun()
        else:
            st.error(f"Analysis Execution Failed: {msg}")
