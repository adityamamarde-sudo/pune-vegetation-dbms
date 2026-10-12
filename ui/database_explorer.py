"""
UI Component: Database Explorer & SQL Demonstration Screen (Screen 6)
Allows safe inspection of MySQL tables, parameterized filtering, CSV export,
and live execution of the 10 required DBMS course assessment queries.
"""

import streamlit as st
import pandas as pd
import io
from db.connection import DatabaseManager


def run_safe_query(sql: str, params=None):
    """Executes a safe parameterized read-only query and returns a pandas DataFrame."""
    conn = DatabaseManager.get_raw_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            rows = cursor.fetchall()
            return pd.DataFrame(rows)
    finally:
        conn.close()


def render_database_explorer():
    st.markdown("## 🔍 MySQL Database Explorer & SQL Demonstration Lab")
    st.markdown(
        """
        Inspect live tables in your **MySQL 8.0** database, export CSV reports, and execute
        the **10 course-mandated relational SQL queries** (Filtering, Aggregation, JOINs, GROUP BY, HAVING, Views, and Transactions).
        """
    )

    tab_tables, tab_sql_demo = st.tabs(["🗄️ Relational Tables & Views", "⚡ DBMS Assessment Queries (1-10)"])

    # TAB 1: Relational Tables & Views
    with tab_tables:
        table_options = [
            "v_analysis_complete_summary (Unified View)",
            "v_area_performance_summary (Aggregates View)",
            "study_areas",
            "analysis_runs",
            "ndvi_summaries",
            "ndvi_time_series",
            "audit_logs",
            "satellite_datasets",
        ]
        selected_tbl = st.selectbox("Select Table or Relational View:", table_options)
        clean_tbl_name = selected_tbl.split(" ")[0]

        try:
            df = run_safe_query(f"SELECT * FROM {clean_tbl_name} LIMIT 100;")
            st.markdown(f"**Showing up to 100 records from `{clean_tbl_name}`** ({len(df)} rows found)")
            st.dataframe(df, use_container_width=True)

            csv_buf = io.StringIO()
            df.to_csv(csv_buf, index=False)
            st.download_button(
                label=f"📥 Download {clean_tbl_name} as CSV",
                data=csv_buf.getvalue(),
                file_name=f"{clean_tbl_name}_export.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.error(f"Failed to query {clean_tbl_name}: {e}")

    # TAB 2: DBMS Course SQL Demonstration Queries
    with tab_sql_demo:
        st.markdown("### 🎓 10 Required DBMS Demonstration Queries")
        st.caption("These queries run live against your local MySQL 8 database to prove relational database competencies.")

        demo_queries = {
            "1. Filtering: Retrieve analyses for a specific region": (
                """
                SELECT ar.analysis_id, sa.area_name, sa.region_label, ar.start_date, ar.end_date, ar.analysis_mode
                FROM analysis_runs ar
                JOIN study_areas sa ON ar.area_id = sa.area_id
                WHERE sa.region_label = %s;
                """,
                ("Mulshi",),
                "Filters runs specifically located in the 'Mulshi' region using an indexed join predicate.",
            ),
            "2. Sorting: Retrieve latest completed analyses first": (
                """
                SELECT analysis_id, area_id, start_date, end_date, processing_status, created_at
                FROM analysis_runs
                ORDER BY created_at DESC, analysis_id DESC
                LIMIT 5;
                """,
                (),
                "Chronological reverse-order sort for the analyst dashboard feed.",
            ),
            "3. Aggregation: Overall statistical NDVI across completed analyses": (
                """
                SELECT
                    COUNT(ns.summary_id) AS total_analyses,
                    ROUND(AVG(ns.mean_ndvi), 4) AS overall_avg_ndvi,
                    ROUND(MIN(ns.min_ndvi), 4) AS min_ndvi,
                    ROUND(MAX(ns.max_ndvi), 4) AS max_ndvi,
                    SUM(ns.valid_pixel_count) AS total_pixels
                FROM ndvi_summaries ns
                JOIN analysis_runs ar ON ns.analysis_id = ar.analysis_id
                WHERE ar.processing_status = 'completed';
                """,
                (),
                "Aggregate functions (COUNT, AVG, MIN, MAX, SUM) over all runs.",
            ),
            "4. Multi-Table JOIN: Join study_areas, runs, datasets, and summaries": (
                """
                SELECT
                    ar.analysis_id, sa.area_name, sd.satellite_name, ar.start_date, ar.end_date,
                    ns.mean_ndvi, ns.vegetation_area_sq_km
                FROM analysis_runs ar
                INNER JOIN study_areas sa ON ar.area_id = sa.area_id
                INNER JOIN satellite_datasets sd ON ar.dataset_id = sd.dataset_id
                INNER JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
                ORDER BY ns.mean_ndvi DESC;
                """,
                (),
                "4-table equi-join demonstrating 3NF relational reconstruction.",
            ),
            "5. GROUP BY: Compare average NDVI across study areas": (
                """
                SELECT
                    sa.area_name, sa.region_label,
                    COUNT(ar.analysis_id) AS runs_count,
                    ROUND(AVG(ns.mean_ndvi), 4) AS avg_area_ndvi
                FROM study_areas sa
                JOIN analysis_runs ar ON sa.area_id = ar.area_id
                JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
                WHERE ar.processing_status = 'completed'
                GROUP BY sa.area_id, sa.area_name, sa.region_label
                ORDER BY avg_area_ndvi DESC;
                """,
                (),
                "Spatial grouping to compare agricultural vs urban vegetative health.",
            ),
            "6. HAVING: Identify regions with average NDVI below critical cutoff": (
                """
                SELECT sa.area_name, COUNT(ar.analysis_id) AS completed_runs, ROUND(AVG(ns.mean_ndvi), 4) AS avg_ndvi
                FROM study_areas sa
                JOIN analysis_runs ar ON sa.area_id = ar.area_id
                JOIN ndvi_summaries ns ON ar.analysis_id = ns.analysis_id
                WHERE ar.processing_status = 'completed'
                GROUP BY sa.area_id, sa.area_name
                HAVING AVG(ns.mean_ndvi) < 0.4500
                ORDER BY avg_ndvi ASC;
                """,
                (),
                "Post-aggregation filtering (HAVING) to isolate degraded or low-canopy zones.",
            ),
            "7. Date Filtering: Temporal query on observation timestamps": (
                """
                SELECT ts.point_id, sa.area_name, ts.observation_date, ts.mean_ndvi, ts.quality_notes
                FROM ndvi_time_series ts
                JOIN analysis_runs ar ON ts.analysis_id = ar.analysis_id
                JOIN study_areas sa ON ar.area_id = sa.area_id
                WHERE ts.observation_date BETWEEN '2023-08-01' AND '2023-11-30'
                ORDER BY ts.observation_date ASC;
                """,
                (),
                "Index-assisted range query over the observation_date dimension.",
            ),
            "8. Relational View: Query pre-compiled view v_analysis_complete_summary": (
                """
                SELECT analysis_id, area_name, region_label, start_date, end_date, mean_ndvi, analysis_mode
                FROM v_analysis_complete_summary
                WHERE processing_status = 'completed';
                """,
                (),
                "Encapsulates join logic into a standardized relational abstraction.",
            ),
            "9. Index Optimization: EXPLAIN plan for composite index verification": (
                """
                EXPLAIN
                SELECT observation_date, mean_ndvi
                FROM ndvi_time_series
                WHERE analysis_id = 1 AND observation_date >= '2023-09-01';
                """,
                (),
                "Proves query optimizer utilizes idx_time_series_analysis_date for O(log N) lookups.",
            ),
            "10. Audit Log Trigger: Inspect automated trigger activity": (
                """
                SELECT log_id, action_type, table_name, record_id, details, logged_at
                FROM audit_logs
                ORDER BY logged_at DESC
                LIMIT 10;
                """,
                (),
                "Demonstrates trigger trg_audit_analysis_insert logging insertion operations.",
            ),
        }

        query_choice = st.selectbox("Select Query Demonstration:", list(demo_queries.keys()))
        sql_template, params, explanation = demo_queries[query_choice]

        st.info(f"💡 **DBMS Concept**: {explanation}")
        st.code(sql_template.strip(), language="sql")

        if st.button("▶️ Execute Query in MySQL 8", key="btn_run_sql"):
            try:
                res_df = run_safe_query(sql_template, params)
                st.success(f"Execution Succeeded! Returned {len(res_df)} rows.")
                st.dataframe(res_df, use_container_width=True)
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
