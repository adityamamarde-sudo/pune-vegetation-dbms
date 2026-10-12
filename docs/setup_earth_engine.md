# Google Earth Engine (GEE) Setup & Authentication Guide

### 1. Prerequisites
To use live Google Earth Engine Sentinel-2 imagery:
1. A Google Account registered with Earth Engine at [earthengine.google.com](https://earthengine.google.com/signup/).
2. A Google Cloud Platform (GCP) project with the Earth Engine API enabled.

### 2. Local Authentication Steps
Run the following command in your terminal:

```bash
earthengine authenticate
```

This will launch your web browser. Log in with your registered Google Account and grant permission.

### 3. Configuring `.env`
Add your Google Cloud Project ID to `.env`:
```ini
GEE_PROJECT_ID=your-gcp-project-id
GEE_AUTH_MODE=local
```

### 4. Running Without GEE (Demo Mode)
If you do not have a GEE account or are evaluating offline:
- The system automatically detects missing credentials and activates **Demo Mode**.
- Synthetic, biologically representative NDVI data for Pune will be generated and persisted in MySQL.
- All demo outputs are explicitly labeled: `DEMO DATA — NOT REAL SATELLITE RESULTS`.
