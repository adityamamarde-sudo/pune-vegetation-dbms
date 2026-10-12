"""
UI Component: Dashboard Screen (Screen 1)
Displays project summary, MySQL database health, analysis statistics, and GEE mode badge.
"""

import streamlit as st
from db.connection import DatabaseManager
from db.repositories import QueryDemonstrator
from services.gee_service import GEEService


def render_dashboard():
    st.markdown("## 🌿 Pune Vegetation Monitoring & Remote-Sensing Database")
    st.markdown(
        """
        An enterprise-grade relational database management system tracking **vegetation dynamics and NDVI trends**
        across the Pune metropolitan region and Western Ghats foothills using **Sentinel-2 multispectral satellite imagery** and **MySQL 8.0**.
        """
    )

    # 1. System Status & Runtime Badges
    gee_info = GEEService.get_status_info()
    db_success, db_info = DatabaseManager.test_connection()

    col1, col2, col3 = st.columns(3)
    with col1:
        if db_success:
            st.success(f"🗄️ **MySQL 8 Server**: Connected\n- Host: `{db_info['host']}:{db_info['port']}`\n- DB: `{db_info['database']}`")
        else:
            st.error(f"❌ **MySQL 8 Server**: Disconnected\n- Error: {db_info.get('error_message')}")

    with col2:
        if gee_info["available"]:
            st.success("🛰️ **Satellite Engine**: Real GEE (Sentinel-2 SR)\n- Status: Authenticated\n- Collection: Harmonized L2A")
        else:
            st.warning("🧪 **Satellite Engine**: Demo Mode\n- Status: Synthetic verified datasets\n- Note: DEMO DATA — NOT REAL GEE")

    with col3:
        if db_success:
            st.info(f"⚡ **Connection Health**\n- Version: `{db_info['version']}`\n- Latency: `{db_info['latency_ms']} ms`\n- Total Tables: `{db_info['table_count']}`")
        else:
            st.info("⚡ **Connection Health**\n- Status: Inactive")

    st.markdown("---")

    # 2. Database Key Metrics
    if db_success:
        try:
            stats = QueryDemonstrator.get_dashboard_counts()
            c1, c2, c3 = st.columns(3)
            c1.metric("📍 Saved Study Areas", stats["total_areas"])
            c2.metric("🚀 Total Analysis Runs", stats["total_runs"])

            latest = stats["latest_run"]
            if latest:
                c3.metric(
                    "📅 Latest Completed Analysis",
                    f"Run #{latest['analysis_id']} ({latest['area_name']})",
                    delta=f"NDVI: {latest['mean_ndvi']:.3f}" if latest.get("mean_ndvi") is not None else None,
                )
            else:
                c3.metric("📅 Latest Completed Analysis", "No runs recorded yet")
        except Exception as e:
            st.warning(f"Could not load database counts: {e}")

    # 3. Quick Actions & Guidance
    st.markdown("### ⚡ Quick Actions")
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("🗺️ Explore & Select Study Area", use_container_width=True):
            st.session_state["nav_page"] = "Select Study Area"
            st.rerun()
    with qa2:
        if st.button("🛰️ Run NDVI Analysis", use_container_width=True):
            st.session_state["nav_page"] = "Run NDVI Analysis"
            st.rerun()
    with qa3:
        if st.button("🔍 Explore Database & SQL Lab", use_container_width=True):
            st.session_state["nav_page"] = "Database Explorer"
            st.rerun()

    st.markdown("---")
    st.markdown(
        """
        > **Academic Note**: This system stores spatial bounding definitions, sensor parameters,
        > and calculated aggregate metrics inside a normalized **MySQL 8** schema. High-resolution multi-gigabyte
        > satellite rasters remain in Google Earth Engine or cloud storage, maintaining database scalability.
        """
    )
