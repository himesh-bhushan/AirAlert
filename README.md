# 🌫️ AirAlert Malaysia
### Python-Based Haze Monitoring and Prediction Platform

## 📌 Overview

**AirAlert Malaysia** is a Python-based environmental monitoring and haze prediction prototype designed to help people understand air quality conditions and make informed decisions to protect their health. The platform brings together air-quality measurements, fire-detection data, and wind observations in an interactive dashboard to improve awareness of haze-related risks across Malaysia.

Haze and air pollution can significantly affect public health, particularly among children, older adults, and individuals with respiratory or cardiovascular conditions. AirAlert aims to make environmental information easier to understand by transforming datasets into visual insights, forecast demonstrations, and practical recommendations that encourage safer everyday decisions.

Built using Python, Streamlit, Pandas, Plotly, and PyDeck, AirAlert provides a user-friendly interface for exploring air-quality trends, visualising environmental observations, and demonstrating how haze-forecasting information can be presented to the public.

The project is designed as a foundation for a more comprehensive haze early-warning system, with potential future integration of real-time environmental data, trained machine-learning models, and advanced predictive analytics.

## 🎯 Project Objectives

AirAlert aims to:

- **Monitor air quality:** Present PM2.5 and PM10 measurements to help users understand particulate pollution levels.
- **Demonstrate haze prediction:** Visualise potential changes in PM2.5 concentrations over different forecast horizons.
- **Visualise environmental activity:** Display fire detections, air-quality locations, and wind observations on an interactive map.
- **Promote public-health awareness:** Provide practical recommendations for reducing exposure to polluted air.
- **Protect vulnerable communities:** Highlight precautions for children, older adults, and people with respiratory or cardiovascular conditions.
- **Make environmental data accessible:** Transform environmental datasets into clear charts, interactive visualisations, and actionable information.
- **Support future innovation:** Establish a foundation for integrating live data feeds and validated machine-learning forecasting models.

## ✨ Key Features

### 📊 1. Air Quality Monitoring and Insights

AirAlert presents air-quality information through interactive charts and summary metrics.

Key capabilities include:

- Displaying PM2.5 and PM10 measurements.
- Visualising air-quality trends over time.
- Exploring observations by Malaysian state when location data is available.
- Displaying the latest available sample measurements.
- Filtering observations by state.
- Exporting filtered air-quality data as a CSV file.

These features help users explore environmental data and understand how particulate pollution can vary across locations and time periods.

### 🗺️ 2. Interactive Fire and Wind Map

The interactive environmental map provides a geographical view of the available sample datasets.

It includes:

- Fire-detection locations.
- Air-quality monitoring locations.
- Wind-observation points.
- Illustrative wind-direction indicators.
- Interactive map layers that users can enable or disable.

The map uses PyDeck to present geographical information in an accessible visual format.

By combining these datasets in one interface, AirAlert demonstrates how fire activity, wind conditions, and air-quality information can be explored together when assessing potential haze risks.

> **Note:** The current map uses sample data and illustrative wind indicators. It does not simulate verified smoke movement or provide live fire tracking.

### ⏳ 3. Haze Prediction and Forecast Visualisation

AirAlert includes forecast visualisations designed to demonstrate how future PM2.5 values could be presented to users.

The dashboard supports multiple forecast horizons:

- 1 hour
- 2 hours
- 5 hours
- 12 hours
- 24 hours
- 7 days
- Monthly projections

Users can select a forecast horizon and view the corresponding illustrative PM2.5 projection.

The five-hour early-warning interface demonstrates how short-term forecasts could support timely decisions, while longer forecast horizons illustrate how future environmental conditions might be presented.

**Current implementation:** Forecast values are generated using a simple illustrative calculation based on the latest available sample PM2.5 value and a fixed hourly change. This is not a trained machine-learning model, a validated prediction model, or a reliable prediction of actual future haze conditions.

Future development can replace this demonstration logic with a trained forecasting model that learns from historical observations and incorporates relevant environmental variables.

### 🛡️ 4. Health and Safety Recommendations

AirAlert connects environmental information with practical actions that users can take to reduce exposure to air pollution.

Recommendations cover:

- **Reducing outdoor exposure:** Limiting prolonged outdoor activities and strenuous exercise when air quality is poor.
- **Improving indoor air quality:** Using appropriately sized air purifiers with HEPA filters or compatible high-efficiency HVAC filtration.
- **Maintaining cleaner indoor environments:** Reducing indoor sources of airborne particles and keeping windows and doors closed when outdoor air is smoky.
- **Protecting vulnerable individuals:** Taking additional precautions for children, older adults, pregnant people, and people with respiratory or cardiovascular conditions.
- **Using respiratory protection:** Considering well-fitting particulate respirators, such as N95 or KN95 respirators, when outdoor exposure cannot be avoided during poor air quality.
- **Following official guidance:** Checking current air-quality advisories and following appropriate medical advice.

The application can display different precautionary recommendations according to the available PM2.5 sample value.

> These demonstration thresholds are not official Malaysian air-quality categories. Recommendations should not be interpreted as personalised medical advice.

### 📍 5. Malaysia-Focused Environmental Dashboard

AirAlert is designed with Malaysian environmental awareness in mind.

Its dashboard combines:

- National-level air-quality summaries.
- State-based observations where available.
- Fire-detection visualisations.
- Wind-observation data.
- Air-quality trends.
- Forecast demonstrations.
- Public-health recommendations.

This integrated interface provides a starting point for developing a more comprehensive environmental intelligence platform for Malaysian communities.

### 🔄 6. Data Management and Visualisation

AirAlert uses CSV files to store and load its demonstration datasets.

The application includes:

- Automatic loading of available datasets.
- Timestamp parsing and conversion to Malaysia time.
- Basic handling of missing or invalid data.
- Interactive charts and data tables.
- A data-refresh control.
- CSV export functionality for filtered observations.

This approach makes the prototype straightforward to run and modify while allowing future integration with APIs, databases, and automated data-collection pipelines.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language and application logic |
| **Streamlit** | Interactive web dashboard and user interface |
| **Pandas** | Data loading, processing, filtering, and analysis |
| **Plotly Express** | Interactive charts and air-quality trend visualisations |
| **PyDeck** | Interactive geographical maps and environmental layers |
| **CSV** | Storage format for demonstration datasets |
| **ZoneInfo** | Malaysia timezone handling |

The application uses a modular structure that separates data loading, timestamp preparation, forecasting demonstrations, chart formatting, and dashboard pages.

## 📁 Project Structure

```text
AirAlert/
├── app.py
├── data/
│   ├── air_quality_sample.csv
│   ├── fire_detections_sample.csv
│   └── wind_sample.csv
└── README.md
```

### File Descriptions

- **`app.py`** — Main Streamlit application containing the dashboard, data-processing functions, forecast demonstrations, interactive maps, and recommendations.
- **`air_quality_sample.csv`** — Sample air-quality measurements, including PM2.5 and PM10 values.
- **`fire_detections_sample.csv`** — Sample fire-detection records and geographical coordinates.
- **`wind_sample.csv`** — Sample wind observations and directional information.
- **`README.md`** — Project documentation, setup instructions, features, and limitations.

The application expects the CSV files to be located in the `data/` directory relative to `app.py`.

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd AirAlert
```

Replace `<your-repository-url>` with the actual repository URL.

### 2. Install Dependencies

Ensure Python is installed, then install the required libraries:

```bash
pip install streamlit pandas plotly pydeck
```

### 3. Check the Project Files

Ensure that `app.py` and the `data/` directory are present. The data directory should contain the three CSV files listed in the project structure above.

The CSV files should include the columns required by the application. For example, the air-quality dataset should contain a timestamp and a PM2.5 measurement column named `pm25_ugm3`.

### 4. Run the Application

From the project directory, execute:

```bash
streamlit run app.py
```

Streamlit will start the application and provide a local URL that you can open in your browser.

### 5. Explore the Dashboard

Use the sidebar to navigate between the three main sections:

1. **Overview** — View summary metrics, air-quality trends, the five-hour forecast demonstration, and health recommendations.
2. **Map & Forecast** — Explore the environmental map and select different forecast horizons.
3. **Air Quality & Insights** — Filter measurements, examine pollutant trends, explore fire activity, and download filtered data.

## 🔬 Future Development

AirAlert is intended to evolve from a demonstration dashboard into a more capable environmental monitoring and early-warning platform.

### 1. Real-Time Environmental Data Integration

Integrate verified environmental data sources to obtain current air-quality measurements, fire detections, and meteorological observations. Automated data updates would reduce reliance on manually maintained CSV files and improve the timeliness of dashboard information.

### 2. Machine-Learning-Based Haze Prediction

Develop a trained forecasting model using suitable historical air-quality and meteorological datasets.

Potential input variables include:

- Historical PM2.5 and PM10 concentrations.
- Wind speed and direction.
- Temperature and humidity.
- Rainfall and other relevant meteorological factors.
- Fire activity and verified hotspot observations.
- Temporal patterns and geographical information.

Candidate approaches could include time-series forecasting, gradient boosting, and other suitable machine-learning methods. Models should be evaluated against held-out observations using appropriate forecasting metrics and baselines before being used for operational warnings.

### 3. Improved Haze-Risk Assessment

Develop a more comprehensive assessment framework that combines air-quality measurements, meteorological conditions, and verified fire activity. Such a system could help identify areas requiring closer monitoring, provided its outputs are properly validated and uncertainty is communicated clearly.

### 4. Location-Specific Alerts

Introduce configurable notifications when verified measurements or validated forecasts indicate that air quality may deteriorate. Potential notification channels include email, mobile notifications, and dashboard alerts.

### 5. Enhanced Geospatial Analysis

Extend the interactive map with additional geographical datasets, improved wind visualisation, and validated atmospheric transport modelling where suitable data is available.

### 6. Improved User Experience

Future enhancements could include:

- Mobile-friendly layouts.
- More detailed historical analysis.
- Downloadable environmental reports.
- Location-specific dashboards.
- Additional languages.
- Improved accessibility.
- More detailed explanations of forecast uncertainty.

## ⚠️ Current Limitations

AirAlert is currently a **prototype for environmental monitoring and haze forecast visualisation**.

- **Synthetic data:** The included CSV datasets are demonstration data and do not necessarily represent actual Malaysian environmental conditions.
- **No live monitoring:** Live environmental feeds have not been integrated into the current implementation.
- **Illustrative forecasts:** The current forecast uses a fixed hourly change rather than a trained predictive model.
- **No validated prediction accuracy:** The forecast has not been evaluated as a reliable predictor of future haze conditions.
- **Simplified environmental analysis:** Fire and wind observations are displayed separately; the current implementation does not calculate verified smoke transport or atmospheric haze dispersion.
- **General health recommendations:** Guidance is intended for public awareness and does not replace official advisories or professional medical advice.

The displayed current Malaysia time is generated from the system clock, while observation timestamps originate from the loaded datasets. A current clock does not mean the underlying environmental observations are current.

**AirAlert should not be used for operational emergency decisions or as a substitute for official air-quality information.** Before real-world deployment, the platform requires verified data sources, robust data-quality checks, and a properly developed and validated forecasting system.

## 🌍 Project Vision

Air pollution and haze can affect communities, public health, and everyday activities. Understanding these conditions requires more than raw measurements: environmental information must also be presented in a way that people can interpret and use responsibly.

AirAlert aims to bridge this gap by combining environmental data visualisation, haze forecast demonstrations, and practical exposure-reduction guidance in one accessible platform.

By providing a foundation for future real-time monitoring and validated predictive analytics, the project seeks to demonstrate how software and environmental data science can contribute to greater public awareness and preparedness.

## 🤝 Contributions

Contributions and suggestions for improving AirAlert are welcome.

Potential areas for contribution include:

- Integrating verified environmental data sources.
- Developing and evaluating forecasting models.
- Improving data quality and processing.
- Enhancing visualisations and map functionality.
- Expanding health guidance and accessibility.
- Improving documentation, testing, and deployment.

When contributing forecasting or environmental-analysis features, please document the data sources, assumptions, limitations, and validation methods.

## 📄 License

Add a suitable open-source license to the repository if you intend to distribute the project publicly. The license should reflect how you want others to use, modify, and redistribute the code.

## 💚 Conclusion

**AirAlert Malaysia is a Python-based environmental monitoring and haze prediction prototype that combines air-quality insights, interactive environmental maps, forecast visualisations, and practical health recommendations in a single dashboard.**

Built with Python, Streamlit, Pandas, Plotly, and PyDeck, it demonstrates how environmental information can be transformed into accessible visual insights to support public awareness and safer decision-making.

With future integration of verified real-time data and validated forecasting models, AirAlert has the potential to develop into a more comprehensive platform for haze monitoring, early warning, and environmental awareness in Malaysia.

**AirAlert — Breathe Smarter. Stay Informed. Stay Protected.**
