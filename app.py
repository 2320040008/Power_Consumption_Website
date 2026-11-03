
import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="Power Consumption Analytics",
    page_icon="⚡",
    layout="wide"
)

# Custom website design
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #172554;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #38bdf8 !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="radiogroup"] p {
    color: white !important;
}

[data-testid="stSidebar"] [role="radiogroup"] {
    color: white !important;
}

.hero {
    background: linear-gradient(120deg, #2563eb, #7c3aed);
    padding: 35px;
    border-radius: 20px;
    text-align: center;
}

.hero h1 {
    color: white !important;
    font-size: 36px;
}

div[data-testid="stMetric"] {
    background: #1e3a6d;
    padding: 18px;
    border-radius: 12px;
}
/* Prediction button styling */
.stButton > button {
    background-color: #2563eb !important;
    color: white !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: bold !important;
}

.stButton > button:hover {
    background-color: #7c3aed !important;
    color: white !important;
    border-color: #a78bfa !important;
}
</style>
""", unsafe_allow_html=True)


# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("energy_website.csv")

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )

    df["active_power_kw"] = pd.to_numeric(
        df["active_power_kw"], errors="coerce"
    )

    return df

@st.cache_resource
def load_model():
    model = joblib.load("improved_model.pkl")
    return model




try:
    data = load_data()
    model = load_model()

    # Website heading
    st.markdown("""
    <div class="hero">
        <h1>⚡ Electronic Device Power Consumption</h1>
        <h2>Analysis and Forecasting</h2>
        <p>Explore energy usage and understand power consumption patterns.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Sidebar navigation
    st.sidebar.title("⚡ Project Navigation")

    page = st.sidebar.radio(
        "Choose a section",
        ["Home", "Dataset Overview", "Power Analysis", "Data Preview", "Power Prediction"]
    )

    # HOME PAGE
    if page == "Home":
        st.title("Welcome to Our Project")

        st.write(
            "This website analyses household energy consumption "
            "data and explores power usage patterns."
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("📊 Data Analysis\n\nExplore energy data.")

        with col2:
            st.info("📈 Interactive Dashboard\n\nView consumption trends.")

        with col3:
            st.info("🔮 Forecasting\n\nExplore power prediction.")

        st.subheader("Project Highlights")

        st.write("- Analysis of energy consumption")
        st.write("- Study of power usage patterns")
        st.write("- Weather and environmental information")
        st.write("- Machine learning-based forecasting")

    # DATASET OVERVIEW PAGE
    elif page == "Dataset Overview":
        st.title("📊 Dataset Overview")

        st.write("A summary of the energy consumption dataset.")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Records", f"{len(data):,}")
        col2.metric("Total Columns", len(data.columns))

        col3.metric(
            "Average Power",
            f"{data['active_power_kw'].mean():.2f} kW"
        )

        st.subheader("Dataset Information")

        st.write("Number of rows:", len(data))
        st.write("Number of columns:", len(data.columns))
        st.write("Missing values:", int(data.isnull().sum().sum()))

        st.subheader("Available Features")
        st.write(", ".join(data.columns))

    # POWER ANALYSIS PAGE
    elif page == "Power Analysis":
        st.title("📈 Power Consumption Analysis")

        # DATE FILTER
        st.subheader("Power Consumption Over Time")

        valid_timestamps = data["timestamp"].dropna()

        if not valid_timestamps.empty:

            min_date = valid_timestamps.min().date()
            max_date = valid_timestamps.max().date()

            selected_dates = st.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            if len(selected_dates) == 2:
                start_date, end_date = selected_dates

                filtered_data = data[
                    (data["timestamp"].dt.date >= start_date) &
                    (data["timestamp"].dt.date <= end_date)
                ]
            else:
                filtered_data = data

        else:
            filtered_data = data
            st.warning("No valid timestamp data is available.")

        # WEATHER FILTER
        st.subheader("Weather Filter")

        weather_options = sorted(
            filtered_data["weather_condition"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_weather = st.selectbox(
            "Select Weather Condition",
            ["All"] + weather_options
        )

        if selected_weather == "All":
            weather_filtered_data = filtered_data
        else:
            weather_filtered_data = filtered_data[
                filtered_data["weather_condition"] == selected_weather
            ]

        # LINE CHART
        st.subheader("Power Consumption Over Time")

        chart_data = weather_filtered_data[
            ["timestamp", "active_power_kw"]
        ].dropna()

        chart_data = (
            chart_data
            .set_index("timestamp")
            .resample("D")
            .mean()
            .dropna()
        )

        if not chart_data.empty:
            st.line_chart(chart_data)
        else:
            st.warning("No data available for the selected filters.")

        # HOURLY POWER CHART
        st.subheader("Average Power by Hour")

        hourly_data = (
            weather_filtered_data
            .groupby("hour")["active_power_kw"]
            .mean()
            .dropna()
        )

        if not hourly_data.empty:
            st.bar_chart(hourly_data)
        else:
            st.warning("No hourly data available.")

        # WEATHER CHART
        st.subheader("Weather and Power Consumption")

        weather_data = (
            weather_filtered_data
            .groupby("weather_condition")["active_power_kw"]
            .mean()
            .dropna()
        )

        if not weather_data.empty:
            st.bar_chart(weather_data)
        else:
            st.warning("No weather data available.")

    # DATA PREVIEW PAGE
    elif page == "Data Preview":
        st.title("📋 Dataset Preview")

        st.write("Explore the first 100 records.")

        st.dataframe(
            data.head(100),
            use_container_width=True
        )
    elif page == "Power Prediction":
        st.title("🔮 Power Consumption Prediction")
        st.write("Predict the next recorded power consumption using the trained machine learning model.")

        prediction_features = [
            "power_lag_1",
            "power_lag_2",
            "power_lag_4",
            "power_lag_48",
            "power_lag_336",
            "temperature_c",
            "humidity_pct",
            "solar_generation_kw",
            "occupants",
            "hour",
            "day_of_week",
            "month",
            "weather_condition",
            "holiday_flag",
            "school_holiday_flag",
            "active_power_kw"
        ]

        latest_data = data.sort_values("timestamp").tail(1)
        prediction_input = latest_data[prediction_features]

        st.subheader("Latest Available Data")
        st.write("The model will use the latest available dataset record.")

        if st.button("Predict Power Consumption"):
            prediction = model.predict(prediction_input)[0]
            st.success(f"Predicted Power Consumption: {prediction:.2f} kW")


except Exception as e:
    st.error("Unable to load the dataset.")
    st.write("Error details:", str(e))

    st.info(
        "Check that energy_website.csv is in the same folder as app.py."
    )
