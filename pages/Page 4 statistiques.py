import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np


st.set_page_config(page_title="Auchan", page_icon="🌋", layout="wide")
st.header("🔔DASHBORD DE SUIVI DES PRIX DE AUCHAN SENEGAL")

st.sidebar.image(
    "images/Auchan-Logo.png",
    caption="Dashbord Auchan",
    use_column_width=True
)

@st.cache_data
def load_data():
    with open("out_of_stck.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    df["price"] = df["price"].str.replace("\u202f", "").str.replace("\xa0CFA", "")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    
    df["is_out_of_stock"] = df["is_out_of_stock"].fillna(False)
    
    df["category"] = pd.Categorical(df["category"])
    df["subcategory"] = pd.Categorical(df["subcategory"])
    
    return df

df = load_data()


st.markdown("<div class='title'> Statistiques</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2: st.sidebar.markdown("# Page des statistiques")

col1, col2 = st.columns([2, 2])

with col1: st.markdown(
    "<div class='subtitle'>Moyenne des prix par catégorie</div>",
    unsafe_allow_html=True,
)
avg_price = df.groupby("category")["price"].mean().reset_index()
with col1: st.dataframe(avg_price, height=300)

with col2: st.markdown(
    "<div class='subtitle'>Répartition des prix des produits</div>",
    unsafe_allow_html=True,
)
fig = px.histogram(df, x="price", nbins=20, title="Histogramme des prix")
fig.update_layout(title_font_size=24, legend_font_size=16)
with col2: st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "<div class='subtitle'>Nuage de points : Prix vs Catégorie</div>",
    unsafe_allow_html=True,
)
fig = px.scatter(
    df, x="category", y="price", color="category", title="Prix vs Catégorie"
)
fig.update_layout(title_font_size=24, legend_font_size=16)
st.plotly_chart(fig, use_container_width=True)
