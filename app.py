"""
Main Application Entrypoint
Streamlit Web UI for Pune Vegetation Monitoring and Remote-Sensing Database System.
"""

import streamlit as st

# Configure wide layout and page title
st.set_page_config(
    page_title="Pune Vegetation Monitoring DBMS",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for polished aesthetics
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
    }
    .badge-demo {
        background-color: #fef3c7;
        color: #92400e;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
    .badge-gee {
        background-color: #d1fae5;
        color: #065f46;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

from db.connection import DatabaseManager
from services.gee_service import GEEService
from ui.dashboard import render_dashboard
from ui.area_selector import render_area_selector
from ui.analysis_form import render_analysis_form
from ui.ndvi_map import render_ndvi_map
from ui.trends import render_trends
from ui.predictions import render_predictions
from ui.database_explorer import render_database_explorer
from ui.about import render_about


def main():
    # Session state for page navigation
    if "nav_page" not in st.session_state:
        st.session_state["nav_page"] = "Dashboard"

    # Sidebar Navigation & System Monitor
    with st.sidebar:
        st.markdown("## 🌿 Pune Vegetation DBMS")
        st.caption("Remote-Sensing & MySQL 8.0 System")
        st.markdown("---")

        # Database Health Badge
        db_connected, db_info = DatabaseManager.test_connection()
        if db_connected:
            st.success(f"🟢 **MySQL 8**: Online\n- Host: `{db_info['host']}`\n- DB: `{db_info['database']}`")
        else:
            st.error(f"🔴 **MySQL 8**: Offline\n- {db_info.get('error_message', 'Check .env')}")

        # Earth Engine Badge
        gee_status = GEEService.get_status_info()
        if gee_status["available"]:
            st.markdown('<span class="badge-gee">🛰️ Real GEE (Sentinel-2)</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge-demo">🧪 Demo Mode Active</span>', unsafe_allow_html=True)
            st.caption("Showing verified synthetic datasets for course evaluation.")

        st.markdown("---")
        st.markdown("### Navigation")

        nav_options = [
            "Dashboard",
            "Select Study Area",
            "Run NDVI Analysis",
            "NDVI Map",
            "Trends & Statistics",
            "Key Insights & Predictions",
            "Database Explorer",
            "Literature & Methodology",
        ]

        # Sync selection with session state
        current_idx = nav_options.index(st.session_state["nav_page"]) if st.session_state["nav_page"] in nav_options else 0
        selected = st.radio("Go to:", nav_options, index=current_idx)

        if selected != st.session_state["nav_page"]:
            st.session_state["nav_page"] = selected
            st.rerun()

        st.markdown("---")
        # PDF Report Download Button
        from pathlib import Path
        pdf_path = Path("Pune_Vegetation_DBMS_Comprehensive_Project_Report.pdf")
        if pdf_path.exists():
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="📥 Download Project Report (PDF)",
                data=pdf_bytes,
                file_name="Pune_Vegetation_DBMS_Comprehensive_Project_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        st.caption("DBMS Course Project • SPPU / Pune")

    # Render selected screen
    page = st.session_state["nav_page"]

    if page == "Dashboard":
        render_dashboard()
    elif page == "Select Study Area":
        render_area_selector()
    elif page == "Run NDVI Analysis":
        render_analysis_form()
    elif page == "NDVI Map":
        render_ndvi_map()
    elif page == "Trends & Statistics":
        render_trends()
    elif page == "Key Insights & Predictions":
        render_predictions()
    elif page == "Database Explorer":
        render_database_explorer()
    elif page == "Literature & Methodology":
        render_about()


if __name__ == "__main__":
    main()
