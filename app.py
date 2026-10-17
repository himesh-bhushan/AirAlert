from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import pydeck as pdk

# ============================================================
# AIRALERT MALAYSIA
# Environmental monitoring and haze early-warning prototype
# ============================================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MY_TZ = ZoneInfo("Asia/Kuala_Lumpur")

st.set_page_config(
    page_title="AirAlert Malaysia",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- STYLING -------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #08111f;
        color: #f5f8fc;
    }
    [data-testid="stSidebar"] {
        background-color: #0d1b2a;
    }
    [data-testid="stMetric"] {
        background-color: #112338;
        border: 1px solid #243752;
        padding: 18px;
        border-radius: 12px;
    }
    h1, h2, h3 {
        color: #f5f8fc;
    }
    .subtitle {
        color: #a8b8cf;
        font-size: 16px;
    }
    .demo-banner {
        background-color: #332811;
        border: 1px solid #80621d;
        color: #ffda85;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 18px;
    }
    .info-card {
        background-color: #112338;
        border: 1px solid #243752;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- DATA LOADING --------------------------

@st.cache_data
def load_csv(filename):
    """Load a CSV file from the project's data directory."""
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception as exc:
        st.warning(f"Could not read {filename}: {exc}")
        return pd.DataFrame()


def prepare_dates(df, column="timestamp"):
    """
    Parse timestamps and convert them to Malaysia time.

    Naive timestamps in the CSV are assumed to be UTC. This changes
    timezone display, not the age or truth of the original observation.
    """
    if df.empty or column not in df.columns:
        return df

    result = df.copy()
    parsed = pd.to_datetime(result[column], errors="coerce", utc=True)
    result[column] = parsed.dt.tz_convert(MY_TZ)
    return result


air = prepare_dates(load_csv("air_quality_sample.csv"))
fires = prepare_dates(load_csv("fire_detections_sample.csv"))
wind = prepare_dates(load_csv("wind_sample.csv"))


def number(value, decimals=1):
    """Format a number safely."""
    try:
        if pd.isna(value):
            return "N/A"
        return f"{float(value):,.{decimals}f}"
    except (ValueError, TypeError):
        return "N/A"


def latest_row(df):
    """Return the most recent valid row, or None."""
    if df.empty or "timestamp" not in df.columns:
        return None

    valid = df.dropna(subset=["timestamp"])
    if valid.empty:
        return None

    return valid.sort_values("timestamp").iloc[-1]


def chart_layout(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=45, b=10),
        legend=dict(orientation="h"),
    )
    return fig


def air_quality_recommendations(pm25):
    """
    Return practical exposure-reduction advice based on a PM2.5 sample.

    These broad demo bands are not an official AQI calculation. The
    dataset is synthetic, and a single sample is not a substitute for
    current official air-quality guidance.
    """
    general = [
        "Check current official air-quality advisories before making outdoor plans.",
        "Keep windows and doors closed when outdoor air is smoky; when outdoor air improves, ventilate briefly if appropriate.",
        "Use a correctly sized portable air cleaner with a true HEPA filter, or effective central HVAC filtration (for example, a compatible high-efficiency filter). Replace filters as directed.",
        "Avoid adding indoor particles: do not smoke indoors, burn candles or incense, or fry food without suitable ventilation.",
        "Give extra protection to children, older adults, pregnant people, and people with asthma, COPD, heart disease, or other cardiopulmonary conditions. Follow their clinician's action plan.",
    ]

    try:
        value = float(pm25)
    except (TypeError, ValueError):
        value = None

    if value is None or pd.isna(value) or value < 0:
        return (
            "Air-quality sample unavailable",
            "Use general haze precautions until current, reliable readings are available.",
            general,
        )

    # Broad demonstration bands only; not official Malaysian API categories.
    if value < 15:
        level = "Lower sample reading"
        summary = (
            f"The latest sample is {value:.1f} µg/m³. Continue checking "
            "current readings because conditions can change."
        )
        actions = [
            "Use official current readings to decide whether outdoor activity is appropriate.",
            "People who are unusually sensitive to haze should monitor symptoms and limit exertion if they feel unwell.",
        ] + general[1:4] + [general[4]]
    elif value < 35:
        level = "Elevated sample reading"
        summary = (
            f"The latest sample is {value:.1f} µg/m³. Consider reducing "
            "prolonged or strenuous outdoor activity, especially if sensitive."
        )
        actions = [
            "Reduce time outdoors and avoid strenuous exercise outside; move exercise indoors to cleaner air.",
            "Keep children’s outdoor play shorter or move it indoors when haze is noticeable or official advice recommends it.",
        ] + general[1:]
    else:
        level = "High sample reading"
        summary = (
            f"The latest sample is {value:.1f} µg/m³. Take extra precautions "
            "and check official local advisories immediately."
        )
        actions = [
            "Stay indoors in a cleaner-air room where possible; postpone outdoor exertion and unnecessary trips.",
            "If going outside is unavoidable, consider a well-fitting, certified particulate respirator such as an N95/KN95. Fit matters; ordinary cloth or surgical masks offer limited protection against fine particles.",
            "Move children, older adults, pregnant people, and people with heart or lung conditions to cleaner indoor air; follow their clinician's advice and prescribed treatment plans.",
        ] + general[1:4]

    return level, summary, actions


def generate_demo_forecast(df, hours=5):
    """
    Generate a clearly labelled illustrative PM2.5 projection.

    This is NOT a trained or validated forecast. It uses the latest
    sample value and a small fixed illustrative change only to
    demonstrate future timestamps and dashboard functionality.
    """
    if df.empty or "timestamp" not in df.columns or "pm25_ugm3" not in df.columns:
        return pd.DataFrame()

    valid = df.dropna(subset=["timestamp", "pm25_ugm3"]).copy()
    valid["pm25_ugm3"] = pd.to_numeric(valid["pm25_ugm3"], errors="coerce")
    valid = valid.dropna(subset=["pm25_ugm3"]).sort_values("timestamp")

    if valid.empty or hours < 1:
        return pd.DataFrame()

    latest_pm25 = max(0.0, float(valid.iloc[-1]["pm25_ugm3"]))
    now = pd.Timestamp.now(tz=MY_TZ)

    # First point is one hour from now, followed by hourly points.
    future_times = pd.date_range(
        start=now.floor("h") + pd.Timedelta(hours=1),
        periods=int(hours),
        freq="h",
    )

    # Fixed illustrative change: not inferred from real atmospheric physics.
    hourly_change = 0.5
    predicted_values = [
        max(0.0, latest_pm25 + hourly_change * step)
        for step in range(1, int(hours) + 1)
    ]

    return pd.DataFrame(
        {
            "timestamp": future_times,
            "predicted_pm25": predicted_values,
        }
    )


# -------------------- SIDEBAR -------------------------------

st.sidebar.title("🌫️ AirAlert")
st.sidebar.caption("Malaysia Environmental Intelligence")

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Map & Forecast", "Air Quality & Insights"],
)

st.sidebar.divider()
st.sidebar.markdown("### Data status")
st.sidebar.write(f"Air quality: {'Loaded' if not air.empty else 'Missing'}")
st.sidebar.write(f"Fire detections: {'Loaded' if not fires.empty else 'Missing'}")
st.sidebar.write(f"Wind observations: {'Loaded' if not wind.empty else 'Missing'}")

if st.sidebar.button("Refresh data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.divider()
st.sidebar.caption(
    "Prototype version. Included CSV data is synthetic and must not "
    "be treated as live environmental information."
)

# -------------------- HEADER ---------------------------------

st.title("🌫️ AirAlert Malaysia")
now_myt = datetime.now(MY_TZ)
st.caption(f"Current Malaysia time: {now_myt:%d %b %Y, %I:%M %p} MYT")

st.markdown(
    '<p class="subtitle">Environmental intelligence for a haze-resilient Malaysia</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="demo-banner">
    DEMONSTRATION MODE — The included datasets are synthetic sample data.
    Live environmental feeds and a validated prediction model have not been connected.
    Forecast charts below are illustrative demonstrations, not real predictions.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# PAGE 1: OVERVIEW
# ============================================================

if page == "Overview":
    st.header("National Overview")

    latest_air = latest_row(air)
    latest_wind = latest_row(wind)

    if latest_air is not None:
        pm25 = latest_air.get("pm25_ugm3")
        pm10 = latest_air.get("pm10_ugm3")
        state = latest_air.get("state", "Unknown")
        timestamp = latest_air.get("timestamp")
    else:
        pm25 = pm10 = timestamp = None
        state = "No data"

    if latest_wind is not None:
        wind_speed = latest_wind.get("wind_speed_ms")
    else:
        wind_speed = None

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sample PM2.5", f"{number(pm25)} µg/m³")
    col2.metric("Sample PM10", f"{number(pm10)} µg/m³")
    col3.metric("Fire detections in sample", str(len(fires)))
    col4.metric("Sample wind speed", f"{number(wind_speed)} m/s")

    if timestamp is not None:
        st.caption(
            f"Latest air-quality sample timestamp: {timestamp} | Location: {state}. "
            "This is the timestamp in the sample file, not necessarily a current observation."
        )

    st.divider()
    left, right = st.columns([1.6, 1])

    with left:
        st.subheader("PM2.5 Trends")
        if not air.empty and "pm25_ugm3" in air.columns and "timestamp" in air.columns:
            trend = air.copy()
            trend["pm25_ugm3"] = pd.to_numeric(trend["pm25_ugm3"], errors="coerce")
            trend = trend.dropna(subset=["timestamp", "pm25_ugm3"])

            if not trend.empty:
                fig = px.line(
                    trend,
                    x="timestamp",
                    y="pm25_ugm3",
                    color="state" if "state" in trend.columns else None,
                    markers=True,
                    title="Sample PM2.5 measurements over time",
                    labels={
                        "timestamp": "Time (Malaysia time)",
                        "pm25_ugm3": "PM2.5 (µg/m³)",
                        "state": "State",
                    },
                )
                st.plotly_chart(chart_layout(fig), use_container_width=True)
            else:
                st.info("No valid PM2.5 observations are available.")
        else:
            st.info("Add a valid data/air_quality_sample.csv file to display trends.")

    with right:
        st.subheader("Five-Hour Early Warning")
        forecast = generate_demo_forecast(air, hours=5)

        if not forecast.empty:
            st.metric(
                "Illustrative PM2.5 in 1 hour",
                f"{number(forecast.iloc[0]['predicted_pm25'])} µg/m³",
            )
            fig = px.line(
                forecast,
                x="timestamp",
                y="predicted_pm25",
                markers=True,
                title="Illustrative PM2.5 projection — next 5 hours",
                labels={
                    "timestamp": "Future time (Malaysia time)",
                    "predicted_pm25": "Illustrative PM2.5 (µg/m³)",
                },
            )
            st.plotly_chart(chart_layout(fig), use_container_width=True)

            # Practical actions based on the latest available sample.
            # Sample data may be synthetic/stale; this is not live medical advice.
            st.subheader("Practical Actions to Reduce Haze Exposure")
            if latest_air is not None:
                recommendation_pm25 = latest_air.get("pm25_ugm3")
            else:
                recommendation_pm25 = None

            level, summary, actions = air_quality_recommendations(recommendation_pm25)
            st.markdown(f"**{level}**")
            st.write(summary)
            for action in actions:
                st.markdown(f"- {action}")

            st.caption(
                "These recommendations are general precautions. The dataset is synthetic, "
                "and the sample value may be stale; check current official Malaysian air-quality "
                "advisories. Seek urgent medical care for severe breathing difficulty or chest pain."
            )

            st.warning(
                "DEMO ONLY: This uses a fixed illustrative change, not a trained or "
                "validated model. Do not use it for health or operational decisions."
            )
        else:
            st.info("No forecast can be displayed because valid PM2.5 sample data is unavailable.")

        st.subheader("Health Guidance")
        st.write("• Follow official air-quality advisories.")
        st.write("• Reduce strenuous outdoor activity during unhealthy air-quality conditions.")
        st.write("• Seek medical advice if experiencing breathing difficulties.")
        st.write("• Vulnerable populations should follow local health recommendations.")

    st.divider()
    st.subheader("Sample Fire Activity")
    if not fires.empty:
        display_columns = [
            col for col in [
                "timestamp", "region", "latitude", "longitude",
                "confidence", "frp_mw", "data_status",
            ] if col in fires.columns
        ]
        st.dataframe(fires[display_columns], use_container_width=True, hide_index=True)
    else:
        st.info("No fire data available.")

# ============================================================
# PAGE 2: MAP & FORECAST
# ============================================================

elif page == "Map & Forecast":
    st.header("Interactive Fire & Wind Map")
    st.write("Explore sample fire detections, air-quality locations and wind observations.")

    horizon = st.selectbox(
        "Select analysis horizon",
        ["1 hour", "2 hours", "5 hours", "12 hours", "24 hours", "7 days", "Monthly"],
        index=2,
    )

    horizon_hours = {
        "1 hour": 1,
        "2 hours": 2,
        "5 hours": 5,
        "12 hours": 12,
        "24 hours": 24,
        "7 days": 24 * 7,
        "Monthly": 24 * 30,
    }
    forecast_hours = horizon_hours[horizon]
    forecast = generate_demo_forecast(air, hours=forecast_hours)

    st.subheader(f"Illustrative PM2.5 Projection — {horizon}")
    if not forecast.empty:
        fig = px.line(
            forecast,
            x="timestamp",
            y="predicted_pm25",
            markers=(forecast_hours <= 24),
            title=f"Illustrative PM2.5 projection for {horizon}",
            labels={
                "timestamp": "Future time (Malaysia time)",
                "predicted_pm25": "Illustrative PM2.5 (µg/m³)",
            },
        )
        st.plotly_chart(chart_layout(fig), use_container_width=True)
        st.warning(
            "DEMO ONLY: This projection uses a fixed illustrative change. "
            "It is not a validated haze forecast."
        )
    else:
        st.info("Forecast unavailable because valid PM2.5 sample data could not be loaded.")

    st.divider()
    show_fires = st.checkbox("Show fire detections", value=True)
    show_air = st.checkbox("Show air-quality locations", value=True)
    show_wind = st.checkbox("Show wind observations", value=True)

    layers = []

    # Fire layer
    if show_fires and not fires.empty and {"longitude", "latitude"}.issubset(fires.columns):
        fire_data = fires.copy()
        fire_data["longitude"] = pd.to_numeric(fire_data["longitude"], errors="coerce")
        fire_data["latitude"] = pd.to_numeric(fire_data["latitude"], errors="coerce")
        fire_data = fire_data.dropna(subset=["longitude", "latitude"])
        if not fire_data.empty:
            layers.append(
                pdk.Layer(
                    "ScatterplotLayer",
                    data=fire_data,
                    get_position="[longitude, latitude]",
                    get_radius=9000,
                    get_fill_color=[255, 90, 60, 200],
                    get_line_color=[255, 180, 100, 220],
                    pickable=True,
                    auto_highlight=True,
                )
            )

    # Air-quality layer
    if show_air and not air.empty and {"longitude", "latitude"}.issubset(air.columns):
        air_data = air.copy()
        air_data["longitude"] = pd.to_numeric(air_data["longitude"], errors="coerce")
        air_data["latitude"] = pd.to_numeric(air_data["latitude"], errors="coerce")
        air_data = air_data.dropna(subset=["longitude", "latitude"])
        if not air_data.empty:
            layers.append(
                pdk.Layer(
                    "ScatterplotLayer",
                    data=air_data,
                    get_position="[longitude, latitude]",
                    get_radius=5000,
                    get_fill_color=[50, 220, 160, 180],
                    pickable=True,
                    auto_highlight=True,
                )
            )

    # Wind layer
    required_wind = {
        "longitude", "latitude", "wind_speed_ms",
        "direction_east_component", "direction_north_component",
    }
    if show_wind and not wind.empty and required_wind.issubset(wind.columns):
        wind_data = wind.copy()
        for col in required_wind:
            wind_data[col] = pd.to_numeric(wind_data[col], errors="coerce")
        wind_data = wind_data.dropna(subset=list(required_wind))

        if not wind_data.empty:
            wind_data["end_lon"] = (
                wind_data["longitude"]
                + 0.12 * wind_data["wind_speed_ms"] * wind_data["direction_east_component"]
            )
            wind_data["end_lat"] = (
                wind_data["latitude"]
                + 0.12 * wind_data["wind_speed_ms"] * wind_data["direction_north_component"]
            )
            line_data = [
                {
                    "start": [row["longitude"], row["latitude"]],
                    "end": [row["end_lon"], row["end_lat"]],
                }
                for _, row in wind_data.iterrows()
            ]
            if line_data:
                layers.append(
                    pdk.Layer(
                        "LineLayer",
                        data=line_data,
                        get_source_position="start",
                        get_target_position="end",
                        get_color=[60, 190, 255, 220],
                        get_width=3,
                        width_min_pixels=2,
                        pickable=True,
                    )
                )

    if layers:
        deck = pdk.Deck(
            layers=layers,
            initial_view_state=pdk.ViewState(
                latitude=2.5,
                longitude=105.0,
                zoom=4.2,
                pitch=0,
            ),
            tooltip={
                "text": (
                    "Region: {region}\nState: {state}\n"
                    "Confidence: {confidence}\nPM2.5: {pm25_ugm3}"
                )
            },
        )
        st.pydeck_chart(deck, use_container_width=True)
        st.caption(
            "Orange = sample fires | Green = sample air-quality locations | "
            "Blue = illustrative wind direction. These are not live feeds."
        )
    else:
        st.warning("No map layers are available. Check CSV files and coordinate columns.")

    left, right = st.columns(2)
    with left:
        st.subheader("Fire Detections")
        if not fires.empty:
            st.dataframe(fires, use_container_width=True, hide_index=True)
        else:
            st.info("No fire detections loaded.")

    with right:
        st.subheader("Wind Observations")
        if not wind.empty:
            st.dataframe(wind, use_container_width=True, hide_index=True)
        else:
            st.info("No wind observations loaded.")

# ============================================================
# PAGE 3: AIR QUALITY & INSIGHTS
# ============================================================

elif page == "Air Quality & Insights":
    st.header("Air Quality & Insights")

    if air.empty:
        st.warning("The air-quality dataset is missing. Check data/air_quality_sample.csv.")
    else:
        if "state" in air.columns:
            states = sorted(air["state"].dropna().astype(str).unique().tolist())
            selected_states = st.multiselect("Select states", states, default=states)
            filtered = air[air["state"].astype(str).isin(selected_states)].copy()
        else:
            filtered = air.copy()

        pollutant = st.radio("Select pollutant", ["PM2.5", "PM10"], horizontal=True)
        column = "pm25_ugm3" if pollutant == "PM2.5" else "pm10_ugm3"

        if column in filtered.columns and "timestamp" in filtered.columns:
            filtered[column] = pd.to_numeric(filtered[column], errors="coerce")
            chart_data = filtered.dropna(subset=["timestamp", column])

            if not chart_data.empty:
                fig = px.line(
                    chart_data,
                    x="timestamp",
                    y=column,
                    color="state" if "state" in chart_data.columns else None,
                    markers=True,
                    title=f"{pollutant} over time",
                    labels={
                        "timestamp": "Time (Malaysia time)",
                        column: f"{pollutant} (µg/m³)",
                        "state": "State",
                    },
                )
                st.plotly_chart(chart_layout(fig), use_container_width=True)
            else:
                st.info("No observations match your filters.")
        else:
            st.info(f"The data needs timestamp and {column} columns to draw this chart.")

        st.divider()
        st.subheader("Latest Sample by State")

        if not filtered.empty and "state" in filtered.columns and "timestamp" in filtered.columns:
            latest_by_state = (
                filtered.sort_values("timestamp")
                .groupby("state", as_index=False)
                .tail(1)
                .sort_values("state")
            )
            columns_to_show = [
                col for col in [
                    "timestamp", "state", "pm25_ugm3", "pm10_ugm3",
                    "api_sample", "data_status",
                ] if col in latest_by_state.columns
            ]
            st.dataframe(
                latest_by_state[columns_to_show],
                use_container_width=True,
                hide_index=True,
            )
            csv_data = latest_by_state[columns_to_show].to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download filtered data as CSV",
                data=csv_data,
                file_name="airalert_air_quality.csv",
                mime="text/csv",
            )

        st.divider()
        st.subheader("Fire Activity")

        if not fires.empty and "region" in fires.columns:
            region_counts = (
                fires["region"].fillna("Unknown")
                .value_counts()
                .rename_axis("region")
                .reset_index(name="detections")
            )
            fig = px.bar(
                region_counts,
                x="region",
                y="detections",
                title="Sample detections by region",
                labels={"region": "Region", "detections": "Detections"},
            )
            st.plotly_chart(chart_layout(fig), use_container_width=True)
            st.caption(
                "Fire counts describe the included sample dataset, not current satellite observations."
            )

        st.divider()
        st.subheader("Data Limitations")
        st.write(
            "These sample measurements are synthetic. They demonstrate charts and filters only."
        )
        st.write(
            "Real-world comparisons require verified sources, consistent units, suitable timestamps, "
            "and appropriate measurement methods."
        )

# -------------------- FOOTER ---------------------------------

st.divider()
st.caption(
    "AirAlert Malaysia | Environmental monitoring prototype | "
    "Synthetic data must not be used for operational decisions."
)
