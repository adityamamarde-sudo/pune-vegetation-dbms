"""
UI Component: Vegetation Anomaly Insights & Future Predictions (Screen 8)
Provides:
1. Historical event attribution (explaining WHY NDVI graph fluctuated on specific dates).
2. Seasonal harmonic machine learning time-series forecasting (next 3 to 12 months).
3. Climate disaster & stress simulation ("What-If" drought, extreme rain, heatwave scenarios).
4. Relational database persistence of simulation scenarios to MySQL 8.
"""

import json
import datetime
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from db.repositories import StudyAreaRepository, AnalysisRepository, PredictionRepository
from services.prediction_service import PredictionService


def render_predictions():
    st.markdown("## 🔮 Vegetation Insights & Future Predictions")
    st.markdown(
        """
        Integrates statistical anomaly detection, seasonal harmonic machine learning,
        and natural disaster stress simulations to explain past vegetation fluctuations
        and project future ecological risks across Pune and surrounding Western Ghats talukas.
        """
    )

    # 1. Fetch available study areas
    areas = StudyAreaRepository.get_all()
    if not areas:
        st.warning("No study areas available. Please initialize the database.")
        return

    area_dict = {f"{a['area_name']} ({a['region_label']} - {a['area_sq_km']} km²)": a for a in areas}
    selected_label = st.selectbox("Select Study Area for Predictive Modeling:", list(area_dict.keys()), index=0)
    selected_area = area_dict[selected_label]
    area_id = selected_area["area_id"]
    area_name = selected_area["area_name"]
    total_area_sq_km = float(selected_area.get("area_sq_km") or 250.0)

    # 2. Fetch analysis runs for this area
    runs = AnalysisRepository.get_runs_by_area(area_id, limit=10)

    # Get time series from selected run or default
    time_series = []
    base_run_id = None
    if runs:
        run_options = {
            f"Run #{r['analysis_id']} ({r['start_date']} to {r['end_date']}) [{r['analysis_mode'].upper()}]": r["analysis_id"]
            for r in runs
        }
        chosen_run_label = st.selectbox("Reference Observation Dataset:", list(run_options.keys()), index=0)
        base_run_id = run_options[chosen_run_label]
        detail = AnalysisRepository.get_analysis_detail(base_run_id)
        if detail and "time_series" in detail:
            time_series = detail["time_series"]

    # Tabs for the feature
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Historical Insights & Event Attribution",
        "📈 Machine Learning Future Forecast",
        "🌪️ Climate Disaster & 'What-If' Simulator",
        "💾 Database Scenario Vault",
    ])

    # =========================================================================
    # TAB 1: HISTORICAL INSIGHTS & ATTRIBUTION
    # =========================================================================
    with tab1:
        st.markdown(f"### 🔍 Historical Vegetation Insights: {area_name}")
        st.caption("Pinpoints inflection dates and attributes shifts to seasonal monsoon, harvest, or environmental drivers.")

        insights = PredictionService.analyze_historical_insights(time_series, area_name=area_name)
        summary = insights.get("summary", {})

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Historical Mean NDVI", f"{summary.get('overall_mean_ndvi', 0.45):.4f}")
        m2.metric("Observed Peak NDVI", f"{summary.get('historical_peak_ndvi', 'N/A')}", help=f"Recorded on {summary.get('historical_peak_date', 'N/A')}")
        m3.metric("Observed Trough NDVI", f"{summary.get('historical_trough_ndvi', 'N/A')}", help=f"Recorded on {summary.get('historical_trough_date', 'N/A')}")
        m4.metric("Observations Analyzed", summary.get("total_observations_analyzed", len(time_series)))

        st.markdown("---")

        # Events breakdown
        events = insights.get("events", [])
        anomalies = insights.get("anomalies", [])

        c_ev, c_an = st.columns([3, 2])
        with c_ev:
            st.markdown("#### 📅 Key Date-by-Date Inflections")
            if events:
                for ev in events[:6]:
                    with st.expander(f"{ev['event_type']} — {ev['date']} (NDVI: {ev['ndvi']:.4f})", expanded=True):
                        st.markdown(f"**Season Phase**: `{ev['season']}`")
                        st.markdown(f"**Observed Change**: `Δ {ev['delta']:+.4f}`")
                        st.write(ev["cause"])
            else:
                st.info("Vegetation values across the selected temporal window remained stable within nominal bounds.")

        with c_an:
            st.markdown("#### ⚠️ Statistical Anomalies (Z-Score > 1.8σ)")
            if anomalies:
                for an in anomalies:
                    st.warning(f"**{an['title']}** ({an['date']})\n- NDVI: `{an['ndvi']:.4f}` ({an['z_score']:+.1f}σ)\n- {an['description']}")
            else:
                st.success("✅ **No extreme statistical anomalies detected.** Canopy evolution matched standard seasonal climatology.")

    # =========================================================================
    # TAB 2: ML FUTURE FORECAST
    # =========================================================================
    with tab2:
        st.markdown(f"### 📈 Seasonal Machine Learning Forecast: {area_name}")
        st.caption("Extrapolates 3 to 12 months ahead using seasonal harmonic autoregression with 95% confidence bounds.")

        c_hz1, c_hz2 = st.columns([2, 3])
        with c_hz1:
            horizon = st.slider("Forecast Horizon (Months Ahead):", min_value=3, max_value=12, value=6, step=3)
        with c_hz2:
            st.info("Model: **Seasonal Harmonic Autoregressive Model (SHAM-2)** trained on Sentinel-2 optical historical passes.")

        forecast_res = PredictionService.generate_ml_forecast(
            time_series=time_series,
            horizon_months=horizon,
            base_mean=float(summary.get("overall_mean_ndvi", 0.45)),
        )

        f_pts = forecast_res["forecast_points"]

        # Plotly chart combining history + forecast + confidence corridor
        fig = go.Figure()

        # 1. Historical observations
        if time_series:
            hist_dates = [pt.get("observation_date") for pt in time_series]
            hist_ndvis = [float(pt.get("mean_ndvi") or pt.get("ndvi") or 0.0) for pt in time_series]
            fig.add_trace(go.Scatter(
                x=hist_dates,
                y=hist_ndvis,
                mode="lines+markers",
                name="Historical Sentinel-2 NDVI",
                line=dict(color="#10b981", width=2.5),
                marker=dict(size=7, color="#059669"),
            ))

        # 2. Forecast Confidence Corridor (Upper & Lower)
        fc_dates = [p["forecast_date"] for p in f_pts]
        fc_ndvis = [p["predicted_ndvi"] for p in f_pts]
        fc_lower = [p["lower_confidence_ndvi"] for p in f_pts]
        fc_upper = [p["upper_confidence_ndvi"] for p in f_pts]

        fig.add_trace(go.Scatter(
            x=fc_dates,
            y=fc_upper,
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            name="Upper 95% CI",
        ))
        fig.add_trace(go.Scatter(
            x=fc_dates,
            y=fc_lower,
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(147, 51, 234, 0.15)",
            name="95% Confidence Corridor",
        ))

        # 3. Forecast Line
        fig.add_trace(go.Scatter(
            x=fc_dates,
            y=fc_ndvis,
            mode="lines+markers",
            name=f"Projected Baseline Forecast (+{horizon} mo)",
            line=dict(color="#9333ea", width=3, dash="dash"),
            marker=dict(size=8, color="#7e22ce", symbol="diamond"),
        ))

        fig.update_layout(
            title=f"Vegetation Health Trajectory & Future Projection — {area_name}",
            xaxis_title="Timeline",
            yaxis_title="NDVI Index (-0.1 to +1.0)",
            yaxis=dict(range=[0.0, 0.95]),
            template="plotly_white",
            hovermode="x unified",
            margin=dict(l=40, r=40, t=50, b=40),
            height=460,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Forecast Summary Cards
        f_m1, f_m2, f_m3, f_m4 = st.columns(4)
        f_m1.metric("Projected Mean NDVI", f"{forecast_res['projected_mean_ndvi']:.4f}")
        f_m2.metric("Projected Peak", f"{forecast_res['projected_peak_ndvi']:.4f}", help=f"Expected: {forecast_res['projected_peak_date']}")
        f_m3.metric("Projected Trough", f"{forecast_res['projected_trough_ndvi']:.4f}", help=f"Expected: {forecast_res['projected_trough_date']}")
        f_m4.metric("Model RMSE", f"±{forecast_res['rmse']:.4f}")

    # =========================================================================
    # TAB 3: DISASTER & WHAT-IF STRESS SIMULATOR
    # =========================================================================
    with tab3:
        st.markdown(f"### 🌪️ Natural Disaster & Climate Stress Simulator: {area_name}")
        st.markdown(
            """
            Simulate the ecological impact of climatic shocks (such as severe monsoon failure or heatwaves).
            The simulation recalculates the vegetation loss curve and estimates the **impacted surface area in km²**.
            """
        )

        with st.expander("⚙️ Configure Disaster Simulation Parameters", expanded=True):
            col_sc1, col_sc2, col_sc3 = st.columns(3)
            with col_sc1:
                st.markdown("##### ☀️ Drought / Monsoon Deficit")
                drought_pct = st.slider("Rainfall Deficit (%):", min_value=0, max_value=60, value=30, step=5)
                st.caption("30% deficit corresponds to severe meteorological drought in Maharashtra.")

            with col_sc2:
                st.markdown("##### 🌡️ Pre-Monsoon Heatwave")
                temp_anomaly = st.slider("Temperature Anomaly (°C):", min_value=0.0, max_value=5.0, value=2.0, step=0.5)
                st.caption("+2°C elevates soil evapotranspiration and accelerates canopy browning.")

            with col_sc3:
                st.markdown("##### 🌧️ Extreme Precipitation")
                extreme_rain = st.slider("Excess Rainfall (%):", min_value=0, max_value=50, value=0, step=5)
                st.caption("Excess rain causes initial waterlogging followed by late-season vegetative rebound.")

        # Run stress simulation
        sim_res = PredictionService.simulate_climate_stress(
            baseline_forecast=f_pts,
            total_area_sq_km=total_area_sq_km,
            drought_deficit_pct=float(drought_pct),
            temp_anomaly_deg_c=float(temp_anomaly),
            extreme_rainfall_pct=float(extreme_rain),
        )

        s_pts = sim_res["stressed_points"]
        metrics = sim_res["metrics"]

        # Results Overview
        st.markdown("#### 🚨 Simulated Disaster Impact Assessment")
        sc_m1, sc_m2, sc_m3, sc_m4 = st.columns(4)
        sc_m1.metric("Baseline Mean NDVI", f"{metrics.get('mean_baseline_ndvi', 0.0):.4f}")
        sc_m2.metric(
            "Stressed Mean NDVI",
            f"{metrics.get('mean_stressed_ndvi', 0.0):.4f}",
            delta=f"-{metrics.get('net_ndvi_drop', 0.0):.4f}",
            delta_color="inverse",
        )
        sc_m3.metric("Projected Lost Veg. Area", f"{metrics.get('projected_lost_area_km2', 0.0)} km²", help=f"Out of {total_area_sq_km} km² total area")
        sc_m4.metric("Vulnerability Score", f"{metrics.get('vulnerability_score', 0.0)} / 100", delta=metrics.get("risk_tier"))

        # Risk Banner
        tier = metrics.get("risk_tier", "LOW")
        color = metrics.get("badge_color", "#10b981")
        st.markdown(
            f"""
            <div style="background-color: {color}22; border-left: 5px solid {color}; padding: 12px 16px; border-radius: 4px; margin: 12px 0;">
                <h4 style="margin: 0; color: {color};">Disaster Severity Level: {tier} RISK</h4>
                <p style="margin: 4px 0 0 0; color: #1e293b;">{metrics.get('risk_description')}</p>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: #475569;"><strong>Recommended Mitigation:</strong> {metrics.get('recommended_mitigation')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Plot Comparative Trajectory
        fig_sim = go.Figure()

        # Baseline
        fig_sim.add_trace(go.Scatter(
            x=[p["forecast_date"] for p in s_pts],
            y=[p["baseline_ndvi"] for p in s_pts],
            mode="lines+markers",
            name="Normal Climatological Baseline",
            line=dict(color="#3b82f6", width=2.5),
        ))

        # Stressed
        fig_sim.add_trace(go.Scatter(
            x=[p["forecast_date"] for p in s_pts],
            y=[p["stressed_ndvi"] for p in s_pts],
            mode="lines+markers",
            name=f"Stressed Simulation ({tier} Risk)",
            line=dict(color=color, width=3, dash="dot"),
            fill="tonexty",
            fillcolor=f"{color}18",
        ))

        fig_sim.update_layout(
            title=f"Disaster Stress Impact on Vegetation Curve — {area_name}",
            xaxis_title="Forecast Date",
            yaxis_title="Predicted NDVI",
            template="plotly_white",
            hovermode="x unified",
            height=400,
        )
        st.plotly_chart(fig_sim, use_container_width=True)

        # Save to MySQL form
        st.markdown("#### 💾 Persist Simulation Scenario to MySQL 8")
        with st.form("save_scenario_form"):
            default_title = f"{area_name} {drought_pct}% Drought & +{temp_anomaly}°C Heatwave Simulation"
            scenario_title = st.text_input("Scenario Title:", value=default_title)
            scenario_type = "drought_stress" if drought_pct > 0 else ("extreme_rainfall" if extreme_rain > 0 else "baseline_forecast")

            save_btn = st.form_submit_button("🚀 Persist Simulation Scenario to MySQL 8", type="primary", use_container_width=True)

        if save_btn:
            try:
                sc_id = PredictionRepository.save_scenario(
                    area_id=area_id,
                    base_analysis_id=base_run_id,
                    scenario_title=scenario_title,
                    scenario_type=scenario_type,
                    forecast_horizon_months=horizon,
                    projected_mean_ndvi=float(metrics.get("mean_stressed_ndvi", 0.0)),
                    vegetation_loss_sq_km=float(metrics.get("projected_lost_area_km2", 0.0)),
                    vulnerability_score=float(metrics.get("vulnerability_score", 0.0)),
                    risk_level=tier,
                    simulation_parameters=metrics.get("parameters", {}),
                    forecast_points=s_pts,
                )
                st.success(f"🎉 **Scenario #{sc_id} successfully persisted in MySQL 8!** Stored in `prediction_scenarios` and `prediction_forecast_points` tables.")
            except Exception as e:
                st.error(f"Failed to persist scenario: {e}")

    # =========================================================================
    # TAB 4: DATABASE SCENARIO VAULT
    # =========================================================================
    with tab4:
        st.markdown("### 💾 Database Scenario Vault (MySQL 8 Records)")
        st.caption("Inspect persisted climate scenarios and multi-table prediction records stored in MySQL.")

        scenarios = PredictionRepository.get_recent_scenarios(limit=30)
        if not scenarios:
            st.info("No prediction scenarios saved yet in MySQL. Run a simulation in Tab 3 and click 'Persist Simulation Scenario'!")
        else:
            df_sc = pd.DataFrame(scenarios)
            st.dataframe(
                df_sc[[
                    "scenario_id", "area_name", "scenario_title", "scenario_type",
                    "forecast_horizon_months", "projected_mean_ndvi",
                    "vegetation_loss_sq_km", "risk_level", "created_at"
                ]],
                use_container_width=True,
                column_config={
                    "scenario_id": st.column_config.NumberColumn("ID", width="small"),
                    "area_name": "Study Area",
                    "scenario_title": "Scenario Name",
                    "scenario_type": "Type",
                    "forecast_horizon_months": "Horizon (Mo)",
                    "projected_mean_ndvi": st.column_config.NumberColumn("Projected NDVI", format="%.4f"),
                    "vegetation_loss_sq_km": st.column_config.NumberColumn("Loss (km²)", format="%.2f"),
                    "risk_level": "Risk Tier",
                    "created_at": "Timestamp",
                },
            )

            st.markdown("---")
            st.markdown("#### 🔍 Inspect Specific Stored Scenario Trajectory")
            sc_dict = {f"Scenario #{s['scenario_id']}: {s['scenario_title']} ({s['risk_level']})": s["scenario_id"] for s in scenarios}
            chosen_sc_id = st.selectbox("Select Stored Scenario to Inspect:", list(sc_dict.keys()), index=0)
            chosen_id = sc_dict[chosen_sc_id]

            sc_detail = PredictionRepository.get_scenario_detail(chosen_id)
            if sc_detail and "points" in sc_detail:
                st.markdown(f"**Parameters**: `{sc_detail.get('simulation_parameters')}`")
                df_pts = pd.DataFrame(sc_detail["points"])
                fig_stored = go.Figure()
                fig_stored.add_trace(go.Scatter(
                    x=df_pts["forecast_date"],
                    y=df_pts["predicted_ndvi"],
                    mode="lines+markers",
                    name="Stored Predicted NDVI",
                    line=dict(color="#ea580c", width=3),
                ))
                fig_stored.add_trace(go.Scatter(
                    x=df_pts["forecast_date"],
                    y=df_pts["upper_confidence_ndvi"],
                    mode="lines",
                    line=dict(width=0),
                    showlegend=False,
                ))
                fig_stored.add_trace(go.Scatter(
                    x=df_pts["forecast_date"],
                    y=df_pts["lower_confidence_ndvi"],
                    mode="lines",
                    line=dict(width=0),
                    fill="tonexty",
                    fillcolor="rgba(234, 88, 12, 0.15)",
                    name="Stored Confidence Band",
                ))
                fig_stored.update_layout(
                    title=f"Stored Trajectory — {sc_detail['scenario_title']}",
                    xaxis_title="Date",
                    yaxis_title="NDVI",
                    template="plotly_white",
                    height=350,
                )
                st.plotly_chart(fig_stored, use_container_width=True)
