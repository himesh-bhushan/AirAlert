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
```

## 1. Ingestion & Schema Normalization

### Tabular Data Parsers

Ingests heterogeneous environmental datasets from CSV files:

- `air_quality_sample.csv` — Air quality measurements, including PM2.5 and PM10.

- `fire_detections_sample.csv` — Geospatial fire detection records.

- `wind_sample.csv` — Wind observation metrics and vectors.

### Temporal Alignment

Processes observation dates and timestamps and uses Python's `zoneinfo` module to support Malaysian Standard Time (UTC+8 / `Asia/Kuala_Lumpur`).

### Fault-Tolerant Fallbacks

Uses defensive data-loading practices and exception handling, including `FileNotFoundError` and `KeyError`, to help the application handle missing files or unexpected data structures gracefully.

## 2. Analytical & Projection Engine

### Vectorized Computations

Uses Pandas and NumPy operations to support data transformation, filtering, summary statistics, and air-quality trend visualization.

> **Implementation note:** The current prototype uses sample datasets and illustrative forecast projections. It does not yet implement a validated machine-learning forecasting model or a complete official Malaysian Air Pollution Index (API) calculation.

### In-Memory Caching

Streamlit's `@st.cache_data` decorator can cache transformed datasets and reduce repeated data processing. Actual performance depends on dataset size, application configuration, and the host environment.

## 3. Geospatial Layer Compilation

### Coordinate Processing

Processes latitude and longitude values for use in PyDeck geospatial visualizations.

### Dynamic Attribute Mapping

Uses map-layer properties such as colors, point sizes, and geographic coordinates to display fire detections and environmental observations.

PyDeck supports interactive, WebGL-based map rendering, allowing users to explore geospatial data through the dashboard.

## 4. Headless Daemon & Process Management

AirAlert can run as a persistent Streamlit application on a Linux server.

Supported process-management options include:

- **tmux:** Keeps a terminal session running after the SSH connection closes.

- **systemd:** Supports service supervision and automatic startup when configured.

- **Streamlit server:** Hosts the dashboard on a configurable network interface and port.

For example, the application can listen on port `8501`.

> **Security note:** Binding to `0.0.0.0` makes the application listen on all available network interfaces. Configure firewall rules, authentication, and network access controls appropriately. For remote access, SSH port forwarding can help avoid exposing the Streamlit port directly to the public internet.

---

# 🏢 Enterprise Hosting: IBM Z & LinuxONE

AirAlert can be deployed on IBM LinuxONE infrastructure, subject to the availability and configuration of the selected hosting environment.

IBM LinuxONE systems use IBM Z architecture and support enterprise workloads, including data processing, application hosting, and analytics.

Deploying an environmental monitoring prototype on IBM LinuxONE provides an opportunity to explore enterprise computing capabilities.

## Why IBM LinuxONE?

### High-Throughput Data Processing

IBM Z systems are designed for enterprise workloads and high-volume transaction processing. With suitable architecture and configuration, these systems can support environmental data ingestion and analytics workloads.

### Enterprise Reliability & Availability

IBM Z platforms provide enterprise reliability features and support highly available system configurations. Actual service availability depends on the infrastructure, deployment architecture, redundancy, and operational practices.

### Virtualization & Security

IBM Z and LinuxONE support virtualization technologies and enterprise security capabilities. Appropriate configuration can provide isolation between workloads and help protect administrative access.

### Sustainable Computing

Consolidating workloads on enterprise infrastructure may improve resource utilization and energy efficiency. Actual sustainability benefits depend on workload characteristics, system utilization, and the hosting environment.

> **Deployment status:** The descriptions above explain the platform's potential benefits. They should not be interpreted as confirmation that AirAlert is currently deployed on IBM LinuxONE Community Cloud unless that deployment has been completed and verified.

## Mainframe Runtime Configuration (s390x)

IBM Z and LinuxONE support the `s390x` architecture. Python applications deployed on this architecture require compatible Python packages and compiled dependencies.

### Native Package Environments

Miniconda or other compatible Python environment managers may be used to install dependencies available for the target architecture.

### Dependency Compatibility

Packages such as NumPy, Pandas, PyArrow, Pillow, Plotly, Streamlit, and PyDeck must be installed in versions compatible with the selected Python version and operating system.

Using compatible precompiled binaries can reduce installation time and avoid unnecessary source compilation. However, package availability varies by version and platform, and some dependencies may still require additional configuration.

### Secure Remote Connectivity

SSH can provide encrypted administrative access and local port forwarding. Public-facing deployments should use suitable access controls and avoid exposing unauthenticated application endpoints.

---

# 🛠️ Technology Stack

| Component | Technology | Purpose |

|---|---|---|

| Host Architecture | IBM LinuxONE / IBM Z (`s390x`) | Potential enterprise hosting platform |

| Operating System | Ubuntu Linux or another compatible distribution | Application runtime environment |

| Runtime Management | Python / Miniconda | Python environment and dependency management |

| Application Framework | Streamlit | Web dashboard, application state, and interactive rendering |

| Data Processing | Pandas and NumPy | Data transformation, filtering, and numerical analysis |

| Data Interchange | PyArrow | Columnar data processing where required by the application |

| Geospatial Mapping | PyDeck | Interactive geospatial map layers |

| Chart Visualizations | Plotly Express and Plotly Graph Objects | Interactive charts and time-series visualizations |

| Data Storage | CSV files | Sample environmental datasets |

| Process Management | tmux / systemd | Persistent sessions and service management |

| Access Security | OpenSSH | Secure remote access and port forwarding |

> **Note:** The table describes the technology stack and potential deployment options. Confirm the installed package versions and actual hosting environment before claiming a particular configuration is operational.

---

# 📁 Project Structure

```text

AirAlert/

├── app.py                         # Main Streamlit dashboard and application logic

├── data/

│   ├── air_quality_sample.csv      # Sample PM2.5 and PM10 measurements

│   ├── fire_detections_sample.csv  # Sample fire detection coordinates

│   └── wind_sample.csv             # Sample wind observation data

├── Dockerfile                      # Optional container configuration

├── Procfile                        # Optional platform process configuration

├── requirements.txt                # Python dependency specifications

└── README.md                       # Project documentation

```

> The `Dockerfile`, `Procfile`, and `requirements.txt` should be included in the repository if the project uses them. Adjust the structure above to match the files actually present in your repository.

---
If a dataset is missing or has a different structure, the corresponding dashboard features may not work as expected.
---


With future integration of verified live data, validated forecasting methods, secure infrastructure, and reliable alerting systems, AirAlert could evolve into a more comprehensive environmental intelligence platform that supports public awareness and climate-resilient communities.

