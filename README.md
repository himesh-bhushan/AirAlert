# 🌫️ AirAlert 

**AirAlert** is a Python-based environmental monitoring and haze prediction prototype designed to help people understand air quality conditions and make informed decisions to protect their health. The platform brings together air-quality measurements, fire-detection data, and wind observations in an interactive dashboard to improve awareness of haze-related risks across Malaysia.

Haze and air pollution can significantly affect public health, particularly among children, older adults, and individuals with respiratory or cardiovascular conditions. AirAlert aims to make environmental information easier to understand by transforming datasets into visual insights, forecast demonstrations, and practical recommendations that encourage safer everyday decisions.

Built using Python, Streamlit, Pandas, Plotly, and PyDeck, AirAlert is hosted on enterprise-grade **IBM LinuxONE (s390x)** mainframe infrastructure. It provides a reliable interface for exploring air-quality trends, visualising environmental observations, and demonstrating how haze-forecasting information can be presented to the public.

The project is designed as a foundation for a more comprehensive haze early-warning system, with potential future integration of real-time environmental data, trained machine-learning models, and advanced predictive analytics.

---

## 🎯 Project Objectives

AirAlert aims to:

- **Monitor air quality:** Present PM2.5 and PM10 measurements to help users understand particulate pollution levels.
- **Demonstrate haze prediction:** Visualise potential changes in PM2.5 concentrations over different forecast horizons.
- **Visualise environmental activity:** Display fire detections, air-quality locations, and wind observations on an interactive map.
- **Promote public-health awareness:** Provide practical recommendations for reducing exposure to polluted air.
- **Protect vulnerable communities:** Highlight precautions for children, older adults, and people with respiratory or cardiovascular conditions.
- **Make environmental data accessible:** Transform environmental datasets into clear charts, interactive visualisations, and actionable information.
- **Support future innovation:** Establish a foundation for integrating live data feeds and validated machine-learning forecasting models.

---

## ✨ Key Features

### 📊 1. Air Quality Monitoring and Insights
AirAlert presents air-quality information through interactive charts and summary metrics:
- Displaying PM2.5 and PM10 measurements.
- Visualising air-quality trends over time.
- Exploring observations by Malaysian state when location data is available.
- Displaying the latest available sample measurements.
- Filtering observations by state.
- Exporting filtered air-quality data as a CSV file.

### 🗺️ 2. Interactive Fire and Wind Map
The interactive environmental map provides a geographical view of the available sample datasets:
- Fire-detection locations.
- Air-quality monitoring locations.
- Wind-observation points.
- Illustrative wind-direction indicators.
- Interactive map layers that users can enable or disable.

The map uses PyDeck to present geographical information in an accessible visual format.

> **Note:** The current map uses sample data and illustrative wind indicators. It does not simulate verified smoke movement or provide live fire tracking.

### ⏳ 3. Haze Prediction and Forecast Visualisation
AirAlert includes forecast visualisations designed to demonstrate how future PM2.5 values could be presented across multiple horizons:
- Short-term: 1 hour, 2 hours, 5 hours, 12 hours, 24 hours
- Extended: 7 days, Monthly outlook

**Current implementation:** Forecast values are generated using a demonstration calculation based on the latest available sample PM2.5 value and a fixed hourly delta. This is not a trained machine-learning model, a validated prediction model, or a reliable prediction of actual future haze conditions.

### 🛡️ 4. Health and Safety Recommendations
AirAlert connects environmental information with practical actions that users can take to reduce exposure:
- Limiting strenuous outdoor activity when air quality is unhealthy.
- Improving indoor air quality with HEPA filtration.
- Protecting vulnerable demographics (children, elderly, respiratory/cardiovascular patients).
- Using particulate respirators (N95/KN95) during severe conditions.
- Adhering to official Malaysian APIMS guidance.

---

## ⚙️ Backend Architecture & Data Processing

The AirAlert backend is designed around an asynchronous, memory-efficient data-processing pipeline tailored for high throughput and rapid interactive rendering:

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                     IBM LinuxONE (s390x)                    │
 │                                                             │
 │  ┌─────────────────┐       ┌─────────────────────────────┐  │
 │  │ Demonstration   │       │   Data Processing Pipeline  │  │
 │  │ Datasets (CSV)  │ ────> │  - Schema validation        │  │
 │  └─────────────────┘       │  - Timezone parsing (UTC+8) │  │
 │                            │  - Outlier filtering        │  │
 │                            └──────────────┬──────────────┘  │
 │                                           │                 │
 │                                           ▼                 │
 │  ┌─────────────────┐       ┌─────────────────────────────┐  │
 │  │  Process Daemon │       │  Vector & Analytical Engine │  │
 │  │  (tmux / systemd│ <───> │  - Pandas / NumPy arrays    │  │
 │  │   port 8501)    │       │  - Caching (@st.cache_data) │  │
 │  └────────┬────────┘       │  - Horizon projection math  │  │
 │           │                └──────────────┬──────────────┘  │
 └───────────┼───────────────────────────────┼─────────────────┘
             │ Secure Encrypted Tunnel       │ Interactive Visuals
             ▼ (OpenSSH / Port 8501)         ▼ (JSON Payloads)
 ┌─────────────────────────────────────────────────────────────┐
 │                      Client Web Browser                     │
 └─────────────────────────────────────────────────────────────┘
