import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Netflix Dashboard",
    layout="wide"
)

st.title("Netflix Movies and TV Shows Dashboard")

uploaded_file = st.file_uploader(
    "Upload Netflix CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # Data Cleaning
    df.drop_duplicates(inplace=True)

    df['country'].fillna("Unknown", inplace=True)
    df['rating'].fillna("Unknown", inplace=True)

    df['date_added'] = pd.to_datetime(
        df['date_added'],
        errors='coerce'
    )

    # Dataset Preview
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # KPI Metrics
    total_titles = df.shape[0]
    total_movies = df[df['type'] == 'Movie'].shape[0]
    total_tvshows = df[df['type'] == 'TV Show'].shape[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Titles", total_titles)
    col2.metric("Movies", total_movies)
    col3.metric("TV Shows", total_tvshows)

    # Sidebar Filters
    st.sidebar.header("Filters")

    selected_type = st.sidebar.multiselect(
        "Select Type",
        options=df['type'].unique(),
        default=df['type'].unique()
    )

    selected_rating = st.sidebar.multiselect(
        "Select Rating",
        options=df['rating'].unique(),
        default=df['rating'].unique()
    )

    filtered_df = df[
        (df['type'].isin(selected_type)) &
        (df['rating'].isin(selected_rating))
    ]

    # Movies vs TV Shows
    st.subheader("Movies vs TV Shows")

    type_counts = filtered_df['type'].value_counts()

    fig1, ax1 = plt.subplots()
    type_counts.plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

    # Top Countries
    st.subheader("Top 10 Countries")

    top_countries = (
        filtered_df['country']
        .value_counts()
        .head(10)
    )

    fig2, ax2 = plt.subplots(figsize=(10,5))
    top_countries.plot(kind='bar', ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # Release Year Trend
    st.subheader("Release Year Trend")

    release_year = (
        filtered_df['release_year']
        .value_counts()
        .sort_index()
    )

    fig3, ax3 = plt.subplots(figsize=(12,5))
    release_year.plot(ax=ax3)
    st.pyplot(fig3)

else:
    st.info("Please upload the Netflix dataset CSV file")
