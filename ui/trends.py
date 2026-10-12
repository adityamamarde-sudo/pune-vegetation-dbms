"""
UI Component: Trends and Statistics Screen (Screen 5)
Renders interactive Plotly time-series curves matching project specifications,
multi-region comparison, and export options (CSV, SVG, PNG).
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import io
from db.repositories import AnalysisRepository


def render_trends():
    st.markdown("## 📈 NDVI Trends & Time-Series Analytics")
    st.markdown(
        """
        Analyze vegetation dynamics across satellite observation dates.
        The interactive chart tracks seasonal cycles (e.g., monsoon greening peaks versus dry-season drops).
        """
    )

    # 1. Fetch available runs
    runs = AnalysisRepository.get_recent_runs(limit=30)
    if not runs:
        st.warning("No analysis records found in the database. Run an analysis first!")
        return

    run_options = {
        f"Run #{r['analysis_id']}: {r['area_name']} ({r['start_date']} to {r['end_date']}) [{r['analysis_mode']}]": r["analysis_id"]
        for r in runs
    }
    selected_label = st.selectbox("Select Primary Analysis:", list(run_options.keys()), index=0)
    primary_id = run_options[selected_label]

    primary_detail = AnalysisRepository.get_analysis_detail(primary_id)
    primary_ts = AnalysisRepository.get_time_series(primary_id)

    if not primary_detail:
        st.error("Could not load analysis detail.")
        return

    # 2. Key Statistical Cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean NDVI", f"{float(primary_detail['mean_ndvi']):.4f}" if primary_detail.get("mean_ndvi") is not None else "N/A")
    c2.metric("Median NDVI", f"{float(primary_detail['median_ndvi']):.4f}" if primary_detail.get("median_ndvi") is not None else "N/A")
    c3.metric("Min NDVI", f"{float(primary_detail['min_ndvi']):.4f}" if primary_detail.get("min_ndvi") is not None else "N/A")
    c4.metric("Max NDVI", f"{float(primary_detail['max_ndvi']):.4f}" if primary_detail.get("max_ndvi") is not None else "N/A")

    if primary_detail["analysis_mode"] == "demo":
        st.warning("⚠️ **NOTICE**: DEMO DATA — NOT REAL SATELLITE RESULTS. Values generated for educational evaluation.")

    # 3. Interactive Plotly Time Series Chart (Styled after reference specification)
    st.markdown("---")
    st.markdown("### 📊 NDVI Time Series")

    fig = go.Figure()

    if primary_ts:
        df_primary = pd.DataFrame(primary_ts)
        # Format date for cleaner display
        df_primary["obs_dt"] = pd.to_datetime(df_primary["observation_date"])
        df_primary = df_primary.sort_values("obs_dt")

        fig.add_trace(
            go.Scatter(
                x=df_primary["obs_dt"],
                y=[float(v) for v in df_primary["mean_ndvi"]],
                mode="lines+markers",
                name=f"{primary_detail['area_name']}",
                line=dict(color="#1d4ed8", width=2.5),
                marker=dict(size=7, color="#1e40af"),
                hovertemplate="<b>Date</b>: %{x|%Y-%b-%d}<br><b>NDVI</b>: %{y:.4f}<extra></extra>",
            )
        )

    # 4. Optional Comparison Feature
    compare_checked = st.checkbox("🔍 Compare with a second study area / analysis run")
    if compare_checked:
        other_options = {k: v for k, v in run_options.items() if v != primary_id}
        if other_options:
            second_label = st.selectbox("Select Comparison Run:", list(other_options.keys()))
            second_id = other_options[second_label]
            second_detail = AnalysisRepository.get_analysis_detail(second_id)
            second_ts = AnalysisRepository.get_time_series(second_id)

            if second_ts:
                df_second = pd.DataFrame(second_ts)
                df_second["obs_dt"] = pd.to_datetime(df_second["observation_date"])
                df_second = df_second.sort_values("obs_dt")

                fig.add_trace(
                    go.Scatter(
                        x=df_second["obs_dt"],
                        y=[float(v) for v in df_second["mean_ndvi"]],
                        mode="lines+markers",
                        name=f"{second_detail['area_name']}",
                        line=dict(color="#dc2626", width=2.5, dash="dash"),
                        marker=dict(size=7, color="#b91c1c"),
                        hovertemplate="<b>Date</b>: %{x|%Y-%b-%d}<br><b>NDVI</b>: %{y:.4f}<extra></extra>",
                    )
                )
        else:
            st.info("Run another analysis first to enable comparative trend lines.")

    # Match reference layout from Image 2
    fig.update_layout(
        title=dict(text="NDVI Time Series", x=0.05, font=dict(size=18, family="Arial, sans-serif")),
        xaxis=dict(
            title="Date",
            gridcolor="#e5e7eb",
            showgrid=True,
            linecolor="#9ca3af",
            tickformat="%Y-%b",
            dtick="M1",
        ),
        yaxis=dict(
            title="NDVI",
            range=[0.0, 0.85],
            gridcolor="#e5e7eb",
            showgrid=True,
            linecolor="#9ca3af",
            dtick=0.1,
        ),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=40, t=70, b=50),
        height=480,
    )

    st.plotly_chart(fig, use_container_width=True)

    # 5. Export Actions (Matching reference Image 2 buttons: Download CSV, SVG, PNG)
    st.markdown("#### 📥 Export Data & Figures")
    exp_col1, exp_col2 = st.columns(2)

    if primary_ts:
        df_export = pd.DataFrame(primary_ts)
        df_export["area_name"] = primary_detail["area_name"]
        df_export["region_label"] = primary_detail["region_label"]
        df_export["analysis_mode"] = primary_detail["analysis_mode"]
        df_export["units"] = "NDVI Index [-1.0, 1.0]"

        csv_buf = io.StringIO()
        df_export.to_csv(csv_buf, index=False)

        with exp_col1:
            st.download_button(
                label="📄 Download CSV",
                data=csv_buf.getvalue(),
                file_name=f"ndvi_timeseries_run_{primary_id}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with exp_col2:
            st.caption("💡 Use the camera icon in the top-right corner of the chart to download high-res PNG / SVG.")

        st.markdown("---")
        st.markdown("### 📋 Observation Table")
        st.dataframe(df_export, use_container_width=True)
