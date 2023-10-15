import pandas as pd
import altair as alt
import streamlit as st

st.set_page_config(page_title="Nobel Prizes Dataset",
                   page_icon=":trophy:",
                   layout="wide")

@st.cache_data
def get_data():
    df = pd.read_csv("nobel-prizes.csv")
    df["year"] = pd.to_datetime(df["year"], format="%Y")
    return df

df = get_data()

# ----- SIDEBAR ------
st.sidebar.header("Please Filter Here: ")
gender_filter = st.sidebar.multiselect(
    "Select gender:",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select categories:",
    options=df["category"].unique(),
    default=df["category"].unique()
)

year_from, year_to = st.sidebar.slider(
    "Years from ... to:",
    1900,
    2020,
    (1900,2020)
)

df_selection = df.query(
    "gender == @gender_filter & category == @category_filter & year >= @year_from & year <= @year_to"
)

# ----- MAINPAGE -----
st.title(":trophy: Nobel Prizes Dataset")
st.markdown("""
##

The selection currently includes the following count of award winners:            
""")

col1, col2, col3 = st.columns(3)

col1.metric("Total", len(df_selection.index))
col2.metric("Male", df_selection.value_counts("gender")["male"])
col3.metric("Female", df_selection.value_counts("gender")["female"])

tab1, tab2 = st.tabs(["Visualizations", "Raw Data"])

with tab1: 
    col1, col2 = st.columns(2)

    # First chart
    by_category = pd.DataFrame(df_selection.value_counts("category"))
    by_category = by_category.reset_index()
    by_category.columns = ["category", "value"]

    base = alt.Chart(by_category).mark_arc().encode(
        theta="value",
        color="category"
    )

    col1.altair_chart(base, use_container_width=True)


    # Second chart
    country = col2.selectbox(
        "Select a country:",
        options=df["bornCountryCode"].unique(),
        index=0
    )

    df_country = df_selection[df_selection["bornCountryCode"] == country]
    by_country = pd.DataFrame(df_country.value_counts("year"))
    by_country = by_country.reset_index()
    by_country.columns = ["year", "count"]

    base = alt.Chart(by_country.sort_values(by="year")).mark_line().encode(
        x='year',
        y='count'
    )

    col2.altair_chart(base, use_container_width=True)


with tab2: 
    st.dataframe(df_selection)