import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="User Analytics", layout="wide")

CSV_URL = "https://docs.google.com/spreadsheets/d/139ZQjKAnmJB_-5qHgfGz4plwKd5suDI86v-SRAPX840/export?format=csv&gid=0"

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_URL)
    
    # Приводим дату
    df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce")
    df["date"] = df["registration_date"].dt.date
    
    return df

df = load_data()

st.title("📊 User Registrations Dashboard")

# --- Фильтры ---
st.sidebar.header("Фильтры")

countries = st.sidebar.multiselect(
    "Страна",
    options=df["country"].dropna().unique(),
    default=df["country"].dropna().unique()
)

industries = st.sidebar.multiselect(
    "Индустрия",
    options=df["industry"].dropna().unique(),
    default=df["industry"].dropna().unique()
)

filtered_df = df[
    (df["country"].isin(countries)) &
    (df["industry"].isin(industries))
]

# --- KPI ---
col1, col2, col3 = st.columns(3)

col1.metric("Всего пользователей", len(filtered_df))
col2.metric("Уникальные компании", filtered_df["company_id"].nunique())
col3.metric("Страны", filtered_df["country"].nunique())

# --- График: регистрации по дням ---
st.subheader("📈 Регистрации по дням")

daily = filtered_df.groupby("date").size().reset_index(name="users")

fig_daily = px.line(
    daily,
    x="date",
    y="users",
    markers=True,
    title="Количество регистраций по дням"
)

st.plotly_chart(fig_daily, use_container_width=True)

# --- Pie: индустрии ---
st.subheader("🧩 Распределение по индустриям")

industry_counts = filtered_df["industry"].value_counts().reset_index()
industry_counts.columns = ["industry", "count"]

fig_pie = px.pie(
    industry_counts,
    names="industry",
    values="count",
    title="Доли индустрий"
)

st.plotly_chart(fig_pie, use_container_width=True)

# --- Топ стран ---
st.subheader("🌍 Топ стран")

country_counts = filtered_df["country"].value_counts().reset_index()
country_counts.columns = ["country", "count"]

fig_country = px.bar(
    country_counts,
    x="country",
    y="count",
    title="Пользователи по странам"
)

st.plotly_chart(fig_country, use_container_width=True)

# --- Источники трафика ---
st.subheader("🚀 Источники")

source_counts = filtered_df["source"].value_counts().reset_index()
source_counts.columns = ["source", "count"]

fig_source = px.bar(
    source_counts,
    x="source",
    y="count",
    title="Источники пользователей"
)

st.plotly_chart(fig_source, use_container_width=True)

# --- Таблица ---
st.subheader("📋 Данные")

st.dataframe(filtered_df)
