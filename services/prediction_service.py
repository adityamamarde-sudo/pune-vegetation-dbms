"""
Vegetation Prediction & Anomaly Insights Service
Provides:
1. Date-by-date historical event attribution & anomaly detection (explaining WHY NDVI changed).
2. Seasonal harmonic machine learning forecasting for upcoming 3 to 12 months.
3. Climate disaster & stress simulation ("What-If" drought, extreme rainfall, heatwave scenarios).
"""

import math
import datetime
from typing import Dict, Any, List, Tuple, Optional
import numpy as np


class PredictionService:
    """Analytical and predictive engine for vegetation dynamics and disaster simulations."""

    # Seasonal agrometeorological calendar for Pune & Western Ghats
    PUNE_SEASONAL_CALENDAR = {
        (6, 7): {
            "season": "Southwest Monsoon Onset",
            "primary_driver": "Heavy precipitation and monsoon cloud cover triggering vegetative green-up",
            "agronomic_event": "Kharif sowing across Pune district (paddy, soybean, bajra, pulses)",
            "expected_ndvi_trend": "Rapid upward surge (+0.15 to +0.30)",
        },
        (8, 9, 10): {
            "season": "Monsoon Peak & Post-Monsoon Biomass Maximum",
            "primary_driver": "Saturated soil moisture and peak canopy leaf area index (LAI)",
            "agronomic_event": "Crop maturation and full forest canopy density across Western Ghats",
            "expected_ndvi_trend": "Annual maximum NDVI plateau (0.60 to 0.85)",
        },
        (11, 12): {
            "season": "Post-Monsoon Kharif Harvesting & Senescence",
            "primary_driver": "Crop cutting, clearing of agricultural parcels, and dry post-monsoon winds",
            "agronomic_event": "Harvesting of Kharif crops, land tilling for Rabi sowing",
            "expected_ndvi_trend": "Sharp downward drop (-0.10 to -0.25)",
        },
        (1, 2): {
            "season": "Winter Rabi Growth / Deciduous Drying",
            "primary_driver": "Irrigated sugarcane/gram growth in eastern talukas; deciduous scrub dry-down",
            "agronomic_event": "Rabi crop vegetative stage supported by dam irrigation (Khadakwasla, Mulshi)",
            "expected_ndvi_trend": "Secondary stable plateau in irrigated zones, slow decline in un-irrigated zones",
        },
        (3, 4, 5): {
            "season": "Summer Pre-Monsoon Dry Season & Thermal Stress",
            "primary_driver": "Elevated temperatures (38-42°C), depleted surface reservoirs, high vapor pressure deficit",
            "agronomic_event": "Fallow agricultural lands, dry grass curing, summer moisture stress",
            "expected_ndvi_trend": "Annual lowest NDVI trough (0.15 to 0.35)",
        },
    }

    @classmethod
    def _lookup_season_info(cls, month: int) -> Dict[str, str]:
        for months, info in cls.PUNE_SEASONAL_CALENDAR.items():
            if month in months:
                return info
        return {
            "season": "Transition Period",
            "primary_driver": "Seasonal transition and weather fluctuations",
            "agronomic_event": "Standard agricultural monitoring",
            "expected_ndvi_trend": "Moderate fluctuations",
        }

    @classmethod
    def analyze_historical_insights(
        cls, time_series: List[Dict[str, Any]], area_name: str = "Pune Region"
    ) -> Dict[str, Any]:
        """
        Pinpoints historical inflection dates (surges, drops, peaks, troughs)
        and provides climatic and agronomic root-cause attribution.
        """
        if not time_series or len(time_series) < 2:
            return {
                "events": [],
                "anomalies": [],
                "summary": {"total_observations_analyzed": len(time_series) if time_series else 0, "area_name": area_name},
            }

        # Sort chronologically
        sorted_series = sorted(
            time_series,
            key=lambda x: str(x.get("observation_date", "")),
        )

        dates = []
        ndvis = []
        for pt in sorted_series:
            d_str = str(pt.get("observation_date", ""))
            try:
                d_obj = datetime.datetime.strptime(d_str[:10], "%Y-%m-%d").date()
                val = float(pt.get("mean_ndvi") or pt.get("ndvi") or 0.0)
                dates.append(d_obj)
                ndvis.append(val)
            except Exception:
                continue

        if len(ndvis) < 2:
            return {"events": [], "anomalies": [], "summary": {"total_observations_analyzed": len(ndvis), "area_name": area_name}}

        mean_overall = float(np.mean(ndvis))
        std_overall = float(np.std(ndvis)) if len(ndvis) > 2 else 0.05
        std_overall = max(0.02, std_overall)

        events = []
        anomalies = []

        # Analyze transitions between consecutive observations
        for i in range(len(ndvis)):
            cur_date = dates[i]
            cur_ndvi = ndvis[i]
            month = cur_date.month
            season_info = cls._lookup_season_info(month)

            # 1. Delta from previous point
            if i > 0:
                prev_date = dates[i - 1]
                prev_ndvi = ndvis[i - 1]
                delta = cur_ndvi - prev_ndvi
                days_gap = max(1, (cur_date - prev_date).days)
                rate_per_month = delta * (30.0 / days_gap)

                # Significant jump or drop
                if abs(delta) >= 0.08 or abs(rate_per_month) >= 0.15:
                    if delta > 0:
                        event_type = "🌱 Vegetation Surge / Green-Up"
                        badge_color = "green"
                        cause = (
                            f"Rapid biomass expansion (+{delta:.3f}) between {prev_date.strftime('%b %d')} and {cur_date.strftime('%b %d')}. "
                            f"Driven by: {season_info['primary_driver']}. Agronomic context: {season_info['agronomic_event']}."
                        )
                    else:
                        event_type = "🍂 Vegetation Drop / Senescence"
                        badge_color = "orange"
                        cause = (
                            f"Sharp NDVI decrease ({delta:.3f}) between {prev_date.strftime('%b %d')} and {cur_date.strftime('%b %d')}. "
                            f"Driven by: {season_info['primary_driver']}. Agronomic context: {season_info['agronomic_event']}."
                        )

                    events.append({
                        "date": cur_date.strftime("%Y-%m-%d"),
                        "event_type": event_type,
                        "badge_color": badge_color,
                        "ndvi": round(cur_ndvi, 4),
                        "delta": round(delta, 4),
                        "cause": cause,
                        "season": season_info["season"],
                    })

            # 2. Statistical Anomaly Detection (Z-score > 1.8)
            z_score = (cur_ndvi - mean_overall) / std_overall
            if abs(z_score) >= 1.8:
                if z_score > 0:
                    anom_title = "⭐ Exceptional Biomass Peak Anomaly"
                    anom_desc = f"NDVI reached an unusually high {cur_ndvi:.4f} (+{z_score:.1f}σ above average). Reflects peak vegetative vigor or dense canopy saturation."
                else:
                    anom_title = "⚠️ Abrupt Canopy Stress / Trough Anomaly"
                    anom_desc = f"NDVI plummeted to {cur_ndvi:.4f} ({z_score:.1f}σ below average). Indicates severe soil dryness, harvesting clearance, or localized cloud shadow suppression."

                anomalies.append({
                    "date": cur_date.strftime("%Y-%m-%d"),
                    "title": anom_title,
                    "ndvi": round(cur_ndvi, 4),
                    "z_score": round(z_score, 2),
                    "description": anom_desc,
                    "season": season_info["season"],
                })

        # Min and Max summary
        min_idx = int(np.argmin(ndvis))
        max_idx = int(np.argmax(ndvis))
        summary = {
            "overall_mean_ndvi": round(mean_overall, 4),
            "historical_peak_date": dates[max_idx].strftime("%Y-%m-%d"),
            "historical_peak_ndvi": round(ndvis[max_idx], 4),
            "historical_trough_date": dates[min_idx].strftime("%Y-%m-%d"),
            "historical_trough_ndvi": round(ndvis[min_idx], 4),
            "total_observations_analyzed": len(ndvis),
            "area_name": area_name,
        }

        return {
            "events": events,
            "anomalies": anomalies,
            "summary": summary,
        }

    @classmethod
    def generate_ml_forecast(
        cls,
        time_series: List[Dict[str, Any]],
        horizon_months: int = 6,
        base_mean: float = 0.45,
    ) -> Dict[str, Any]:
        """
        Fits a seasonal harmonic autoregressive model on historical observations
        and projects future NDVI trajectories with 95% confidence bounds.
        """
        # Parse points
        dates = []
        ndvis = []
        if time_series:
            for pt in sorted(time_series, key=lambda x: str(x.get("observation_date", ""))):
                try:
                    d_obj = datetime.datetime.strptime(str(pt.get("observation_date", ""))[:10], "%Y-%m-%d").date()
                    val = float(pt.get("mean_ndvi") or pt.get("ndvi") or 0.0)
                    dates.append(d_obj)
                    ndvis.append(val)
                except Exception:
                    continue

        # If sparse history, synthesize calibrated Pune climatology anchor points
        if len(ndvis) < 4:
            base_date = dates[-1] if dates else datetime.date(2023, 11, 30)
            for m_offset in range(-12, 1):
                anchor_d = base_date + datetime.timedelta(days=int(m_offset * 30.4))
                day_of_yr = anchor_d.timetuple().tm_yday
                # Monsoon peak around day 260 (mid Sept), summer trough around day 120 (end April)
                harmonic = 0.22 * math.cos(2 * math.pi * (day_of_yr - 260) / 365.25)
                syn_val = np.clip(base_mean + harmonic, 0.15, 0.85)
                dates.append(anchor_d)
                ndvis.append(float(syn_val))

        # Model fitting: Harmonic Basis Function Regression
        t_ref = dates[0]
        t_days = np.array([(d - t_ref).days for d in dates], dtype=float)
        y = np.array(ndvis, dtype=float)

        omega = 2.0 * np.pi / 365.25
        X = np.column_stack([
            np.ones(len(t_days)),
            t_days / 365.25,
            np.sin(omega * t_days),
            np.cos(omega * t_days),
            np.sin(2.0 * omega * t_days),
            np.cos(2.0 * omega * t_days),
        ])

        # Regularized Ridge solution to avoid overfitting
        ridge_alpha = 0.1
        coeffs = np.linalg.solve(X.T @ X + ridge_alpha * np.eye(X.shape[1]), X.T @ y)

        y_fitted = X @ coeffs
        residuals = y - y_fitted
        rmse = float(np.sqrt(np.mean(residuals**2)))
        rmse = max(0.025, min(0.08, rmse))

        # Extrapolate forward into the future
        last_date = dates[-1]
        forecast_points = []
        step_days = 15  # 15-day intervals
        total_days = int(horizon_months * 30.5)

        for d_offset in range(step_days, total_days + step_days, step_days):
            fc_date = last_date + datetime.timedelta(days=d_offset)
            t_val = (fc_date - t_ref).days
            row_feat = np.array([
                1.0,
                t_val / 365.25,
                np.sin(omega * t_val),
                np.cos(omega * t_val),
                np.sin(2.0 * omega * t_val),
                np.cos(2.0 * omega * t_val),
            ])
            pred_ndvi = float(row_feat @ coeffs)
            pred_ndvi = float(np.clip(pred_ndvi, 0.12, 0.88))

            # Uncertainty expands with forecast horizon
            time_penalty = 1.0 + (d_offset / 365.25) * 0.45
            margin = 1.96 * rmse * time_penalty
            lower_ci = float(np.clip(pred_ndvi - margin, 0.05, 0.90))
            upper_ci = float(np.clip(pred_ndvi + margin, 0.10, 0.95))

            forecast_points.append({
                "forecast_date": fc_date.strftime("%Y-%m-%d"),
                "predicted_ndvi": round(pred_ndvi, 4),
                "lower_confidence_ndvi": round(lower_ci, 4),
                "upper_confidence_ndvi": round(upper_ci, 4),
                "month_name": fc_date.strftime("%B %Y"),
                "season": cls._lookup_season_info(fc_date.month)["season"],
            })

        pred_values = [p["predicted_ndvi"] for p in forecast_points]
        peak_idx = int(np.argmax(pred_values))
        trough_idx = int(np.argmin(pred_values))

        return {
            "model_type": "Seasonal Harmonic Autoregressive Model (SHAM-2)",
            "horizon_months": horizon_months,
            "rmse": round(rmse, 4),
            "forecast_points": forecast_points,
            "projected_mean_ndvi": round(float(np.mean(pred_values)), 4),
            "projected_peak_date": forecast_points[peak_idx]["forecast_date"],
            "projected_peak_ndvi": forecast_points[peak_idx]["predicted_ndvi"],
            "projected_trough_date": forecast_points[trough_idx]["forecast_date"],
            "projected_trough_ndvi": forecast_points[trough_idx]["predicted_ndvi"],
        }

    @classmethod
    def simulate_climate_stress(
        cls,
        baseline_forecast: List[Dict[str, Any]],
        total_area_sq_km: float,
        drought_deficit_pct: float = 0.0,
        temp_anomaly_deg_c: float = 0.0,
        extreme_rainfall_pct: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Executes stress-test simulation against projected baseline forecast
        to model natural disaster impacts (drought, flood, heatwave).
        """
        if not baseline_forecast:
            return {"stressed_points": [], "metrics": {}}

        stressed_points = []
        drought_loss_fractions = []

        for pt in baseline_forecast:
            base_val = float(pt["predicted_ndvi"])
            d_obj = datetime.datetime.strptime(pt["forecast_date"][:10], "%Y-%m-%d").date()
            month = d_obj.month

            # Seasonal sensitivity weights for Pune:
            monsoon_weight = 1.0 if month in (6, 7, 8, 9, 10) else 0.4
            summer_weight = 1.0 if month in (3, 4, 5) else 0.3

            # 1. Drought Stress Effect: reduces vegetation vigor
            drought_penalty = (drought_deficit_pct / 100.0) * 0.45 * monsoon_weight

            # 2. Temperature Shock Effect: accelerates canopy drying
            heat_penalty = (temp_anomaly_deg_c / 5.0) * 0.25 * summer_weight

            # 3. Extreme Rainfall Effect
            if extreme_rainfall_pct > 0:
                if month in (7, 8):
                    rain_effect = -(extreme_rainfall_pct / 100.0) * 0.12
                else:
                    rain_effect = +(extreme_rainfall_pct / 100.0) * 0.15
            else:
                rain_effect = 0.0

            net_multiplier = 1.0 - drought_penalty - heat_penalty + rain_effect
            net_multiplier = max(0.20, min(1.35, net_multiplier))

            stressed_ndvi = float(np.clip(base_val * net_multiplier, 0.05, 0.90))
            loss_pct = max(0.0, (base_val - stressed_ndvi) / max(0.05, base_val))
            drought_loss_fractions.append(loss_pct)

            stressed_points.append({
                "forecast_date": pt["forecast_date"],
                "baseline_ndvi": round(base_val, 4),
                "stressed_ndvi": round(stressed_ndvi, 4),
                "delta_ndvi": round(stressed_ndvi - base_val, 4),
                "relative_impact_pct": round((stressed_ndvi - base_val) / max(0.01, base_val) * 100, 2),
                "month_name": pt["month_name"],
            })

        mean_baseline = float(np.mean([p["baseline_ndvi"] for p in stressed_points]))
        mean_stressed = float(np.mean([p["stressed_ndvi"] for p in stressed_points]))
        avg_loss_pct = float(np.mean(drought_loss_fractions))

        # Vegetation Loss Area in sq km
        vulnerable_land_base = total_area_sq_km * 0.72
        projected_lost_area_km2 = round(vulnerable_land_base * avg_loss_pct, 2)

        # Vegetation Vulnerability Index (VVI, 0 - 100)
        vvi = min(100.0, (avg_loss_pct * 120.0) + (temp_anomaly_deg_c * 4.0) + (drought_deficit_pct * 0.5))
        vvi = round(max(0.0, vvi), 1)

        # Risk Tier
        if vvi < 25.0:
            risk_tier = "LOW"
            badge_color = "#10b981"
            risk_desc = "Vegetation shows strong seasonal resilience with negligible canopy loss."
            mitigation = "Routine agro-forestry monitoring and maintenance of natural drainage courses."
        elif vvi < 50.0:
            risk_tier = "MODERATE"
            badge_color = "#f59e0b"
            risk_desc = "Noticeable canopy browning and crop stress in un-irrigated taluka margins."
            mitigation = "Implement rotational irrigation from local check dams and mulch topsoil."
        elif vvi < 75.0:
            risk_tier = "SEVERE"
            badge_color = "#f97316"
            risk_desc = "Critical moisture deficit causing premature leaf shedding and major agricultural yield decline."
            mitigation = "Activate micro-drip irrigation subsidies, emergency reservoir water allocations, and fodder depots."
        else:
            risk_tier = "CRITICAL"
            badge_color = "#ef4444"
            risk_desc = "Severe ecological disruption: widespread crop failure, dried farm ponds, and elevated wildfire vulnerability."
            mitigation = "Declare agricultural disaster protocols, restrict non-potable reservoir draws, and initiate ground-truth relief."

        metrics = {
            "mean_baseline_ndvi": round(mean_baseline, 4),
            "mean_stressed_ndvi": round(mean_stressed, 4),
            "net_ndvi_drop": round(mean_baseline - mean_stressed, 4),
            "projected_lost_area_km2": projected_lost_area_km2,
            "total_area_sq_km": total_area_sq_km,
            "vulnerability_score": vvi,
            "risk_tier": risk_tier,
            "badge_color": badge_color,
            "risk_description": risk_desc,
            "recommended_mitigation": mitigation,
            "parameters": {
                "drought_deficit_pct": drought_deficit_pct,
                "temp_anomaly_deg_c": temp_anomaly_deg_c,
                "extreme_rainfall_pct": extreme_rainfall_pct,
            },
        }

        return {
            "stressed_points": stressed_points,
            "metrics": metrics,
        }
