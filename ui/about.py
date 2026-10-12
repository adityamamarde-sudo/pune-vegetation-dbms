"""
UI Component: Literature & About Screen (Screen 7)
Provides scientific background, remote-sensing methodology, system limitations,
and verified academic literature citations for DBMS project review.
"""

import streamlit as st


def render_about():
    st.markdown("## 📚 Literature Review & Scientific Methodology")
    st.markdown(
        """
        This remote-sensing database project addresses environmental monitoring across Pune and surrounding talukas
        by bridging spatial satellite processing with normalized relational database management.
        """
    )

    st.markdown("### 1. The Environmental Problem in Pune")
    st.markdown(
        """
        Pune district sits at the intersection of the biologically diverse Western Ghats (Mulshi, Maval, Bhor)
        and semi-arid agricultural plains (Baramati, Daund, Shirur). Rapid urban expansion, land-use conversion,
        and changing rainfall patterns have altered canopy cover.
        Relational persistence of vegetation indexes enables longitudinal ecological assessment, seasonal baseline tracking,
        and comparative taluka-level environmental auditing.
        """
    )

    st.markdown("### 2. Sentinel-2 and NDVI Explained")
    st.markdown(
        """
        - **Sentinel-2 Mission**: Operated by the European Space Agency (ESA), featuring twin satellites (Sentinel-2A and 2B) carrying the MultiSpectral Instrument (MSI) with a 5-day revisit cycle.
        - **Normalized Difference Vegetation Index (NDVI)**:
          $$\\text{NDVI} = \\frac{\\text{B8 (Near-Infrared)} - \\text{B4 (Red)}}{\\text{B8 (Near-Infrared)} + \\text{B4 (Red)}}$$
          - **Why NIR?** Mesophyll cell walls in healthy green leaves strongly scatter and reflect Near-Infrared light ($842\\text{ nm}$).
          - **Why Red?** Chlorophyll pigments strongly absorb Red light ($665\\text{ nm}$) for photosynthesis.
          - High values ($> 0.6$) denote dense, vigorous foliage. Low values ($< 0.2$) represent built-up surfaces, exposed rock, or bare soil.
        """
    )

    st.markdown("### 3. Data Provenance & Limitations")
    st.warning(
        """
        **System Limitations & Scientific Context**:
        - **NDVI is an Indicator, Not a Diagnosis**: NDVI does not measure crop yield, identify specific plant diseases, or evaluate soil nutrients.
        - **Atmospheric & Cloud Interference**: Heavy monsoon cloud cover during June–August can obscure optical observations. Cloud masks via Sentinel-2 Scene Classification Layer (SCL) are applied to remove corrupted pixels.
        - **Spatial Resolution**: Sentinel-2 optical bands B4 and B8 provide a 10-meter ground sampling distance. Sub-pixel mixed surfaces can affect readings in dense urban pockets.
        """
    )

    st.markdown("### 4. Verified Literature References")
    st.markdown(
        """
        1. **Rouse, J. W., Haas, R. H., Schell, J. A., & Deering, D. W. (1974)**. *Monitoring the vernal advancement and retrogradation (Greenwave effect) of natural vegetation*. NASA/GSFC Final Report.
        2. **Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., ... & Bargellini, P. (2012)**. *Sentinel-2: ESA's optical high-resolution mission for GMES operational services*. Remote Sensing of Environment, 120, 25-36.
        3. **Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017)**. *Google Earth Engine: Planetary-scale geospatial analysis for everyone*. Remote Sensing of Environment, 202, 18-27.
        4. **Gadgil, S., & Joshi, N. V. (1983)**. *Climatic clusters of the Indian region*. Journal of Climatology, 3(1), 47-63. (Focusing on Maharashtra leeward precipitation gradients).
        """
    )
