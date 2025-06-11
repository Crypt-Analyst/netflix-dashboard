import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

st.set_page_config(page_title="Netflix EDA Dashboard", layout="wide")

st.title("📺 Netflix Titles - EDA Dashboard")

# Load data
df = pd.read_csv("netflix_titles.csv")

# Fill missing non-essential fields
for col in ['director', 'cast', 'country', 'date_added']:
    df[col].fillna('Unknown', inplace=True)

# Drop rows with missing key values
df.dropna(subset=['rating', 'duration'], inplace=True)

# Convert 'date_added' to datetime (handling 'Unknown')
df['date_added'] = df['date_added'].replace('Unknown', pd.NA)
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Extract year from date_added
df['year_added'] = df['date_added'].dt.year

st.sidebar.header("📌 Filters")

selected_type = st.sidebar.selectbox("Select Type", options=['All'] + list(df['type'].unique()))
if selected_type != 'All':
    df = df[df['type'] == selected_type]

# ----- Plot 1: Type count -----
st.subheader("Content Type Distribution")
fig1, ax1 = plt.subplots(figsize=(6, 4))
sns.countplot(data=df, x='type', palette='Set2', ax=ax1)
ax1.set_title("Movies vs TV Shows")
st.pyplot(fig1)

# ----- Plot 2: Content added over time -----
if 'year_added' in df.columns:
    st.subheader("Content Added Over Time")
    df_year = df.dropna(subset=['year_added'])
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df_year, x='year_added', hue='type', palette='Set1', ax=ax2)
    ax2.set_title("Titles Added by Year")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# ----- Plot 3: Top Countries -----
st.subheader("Top 10 Countries")
country_series = df['country'].dropna().apply(lambda x: [i.strip() for i in x.split(',')])
flat_countries = [country for sublist in country_series for country in sublist]
country_counts = Counter(flat_countries)
top_countries = pd.DataFrame(country_counts.most_common(10), columns=['Country', 'Count'])
fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.barplot(data=top_countries, x='Count', y='Country', palette='viridis', ax=ax3)
ax3.set_title("Top Countries by Content")
st.pyplot(fig3)

# ----- Plot 4: Top Genres -----
st.subheader("Top 10 Genres")
genre_series = df['listed_in'].dropna().apply(lambda x: [i.strip() for i in x.split(',')])
flat_genres = [genre for sublist in genre_series for genre in sublist]
genre_counts = Counter(flat_genres)
top_genres = pd.DataFrame(genre_counts.most_common(10), columns=['Genre', 'Count'])
fig4, ax4 = plt.subplots(figsize=(8, 5))
sns.barplot(data=top_genres, x='Count', y='Genre', palette='coolwarm', ax=ax4)
ax4.set_title("Most Common Netflix Genres")
st.pyplot(fig4)

# ----- Plot 5: Top Directors -----
st.subheader("Top 10 Directors")
top_directors = df[df['director'] != 'Unknown']['director'].value_counts().head(10).reset_index()
top_directors.columns = ['Director', 'Count']
fig5, ax5 = plt.subplots(figsize=(8, 5))
sns.barplot(data=top_directors, x='Count', y='Director', palette='magma', ax=ax5)
ax5.set_title("Directors with Most Titles")
st.pyplot(fig5)

# ----- Plot 6: Duration Distributions -----
st.subheader("Movie Durations vs TV Show Seasons")
movies = df[df['type'] == 'Movie'].copy()
tv_shows = df[df['type'] == 'TV Show'].copy()
movies['duration_int'] = movies['duration'].str.extract('(\\d+)').astype(float)
tv_shows['duration_int'] = tv_shows['duration'].str.extract('(\\d+)').astype(float)

fig6, (ax6a, ax6b) = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(movies['duration_int'], bins=30, color='skyblue', kde=True, ax=ax6a)
ax6a.set_title("Movie Durations")
ax6a.set_xlabel("Minutes")
sns.countplot(x=tv_shows['duration_int'], color='salmon', ax=ax6b)
ax6b.set_title("TV Show Seasons")
ax6b.set_xlabel("Seasons")
ax6b.set_ylabel("Number of Shows")
plt.tight_layout()
st.pyplot(fig6)

# Save cleaned data
cleaned_file = "netflix_titles_cleaned.csv"
df.to_csv(cleaned_file, index=False)
st.success(f"✅ Cleaned data saved as {cleaned_file}")
