import os
import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="F1 Telemetry Dashboard", layout="wide")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "f1_demo"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
}


@st.cache_data(ttl=10)
def load_data():
    query = """
    SELECT
        time,
        car_id,
        driver_name,
        team_name,
        lap_number,
        speed_kph,
        throttle_percent,
        brake_percent,
        tyre_temp_c,
        engine_temp_c,
        battery_percent,
        gear
    FROM f1_telemetry
    ORDER BY time;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        return pd.read_sql(query, conn)


@st.cache_data(ttl=10)
def load_lap_summary():
    query = """
    SELECT
        lap_number,
        ROUND(AVG(speed_kph)::numeric, 2) AS avg_speed_kph,
        ROUND(MAX(speed_kph)::numeric, 2) AS max_speed_kph,
        ROUND(AVG(tyre_temp_c)::numeric, 2) AS avg_tyre_temp_c,
        ROUND(MAX(engine_temp_c)::numeric, 2) AS max_engine_temp_c,
        ROUND(AVG(throttle_percent)::numeric, 2) AS avg_throttle_percent,
        COUNT(*) FILTER (WHERE brake_percent > 80) AS hard_braking_events
    FROM f1_telemetry
    GROUP BY lap_number
    ORDER BY lap_number;
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        return pd.read_sql(query, conn)


st.title("F1 Telemetry Dashboard")
st.caption("A beginner-friendly Streamlit dashboard powered by TimescaleDB")

df = load_data()
lap_summary = load_lap_summary()

selected_lap = st.sidebar.selectbox(
    "Choose a lap",
    options=["All laps"] + sorted(df["lap_number"].unique().tolist())
)

if selected_lap != "All laps":
    filtered = df[df["lap_number"] == selected_lap]
else:
    filtered = df

col1, col2, col3, col4 = st.columns(4)

col1.metric("Fastest speed", f"{filtered['speed_kph'].max():.1f} kph")
col2.metric("Average speed", f"{filtered['speed_kph'].mean():.1f} kph")
col3.metric("Max tyre temp", f"{filtered['tyre_temp_c'].max():.1f} C")
col4.metric("Max engine temp", f"{filtered['engine_temp_c'].max():.1f} C")

st.subheader("Speed over time")

st.plotly_chart(
    px.line(
        filtered,
        x="time",
        y="speed_kph",
        color="lap_number",
        title="Car speed"
    ),
    use_container_width=True
)

st.subheader("Tyre and engine temperature")

temp_df = filtered[["time", "tyre_temp_c", "engine_temp_c"]].melt(
    id_vars="time",
    var_name="measurement",
    value_name="temperature_c"
)

st.plotly_chart(
    px.line(
        temp_df,
        x="time",
        y="temperature_c",
        color="measurement",
        title="Temperature trend"
    ),
    use_container_width=True
)

st.subheader("Throttle and braking")

pedal_df = filtered[["time", "throttle_percent", "brake_percent"]].melt(
    id_vars="time",
    var_name="pedal",
    value_name="percent"
)

st.plotly_chart(
    px.line(
        pedal_df,
        x="time",
        y="percent",
        color="pedal",
        title="Throttle vs braking"
    ),
    use_container_width=True
)

st.subheader("Lap summary")
st.dataframe(lap_summary, use_container_width=True)

st.subheader("Raw telemetry data")
st.dataframe(filtered.tail(100), use_container_width=True)

st.info("Question to think about: which lap looked fastest, and did the tyres or engine get too hot?")