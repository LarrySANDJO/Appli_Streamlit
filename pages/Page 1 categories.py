
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np

st.set_page_config(page_title="Auchan", page_icon="🌋", layout="wide")
st.header("🔔DASHBORD DE SUIVI DES PRIX DE AUCHAN SENEGAL")

#all graphs we use custom css not streamlit 
theme_plotly = None 

# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

st.sidebar.image(
    "images/Auchan-Logo.png",
    caption="Dashbord Auchan",
    use_column_width=True
)

st.markdown(
    """
    <style>
    .text-card {
        border: 2px solid #4CAF50;  /* Couleur de la bordure */
        border-radius: 10px;        /* Coins arrondis */
        padding: 20px;              /* Espacement interne */
        margin: 20px 0;             /* Espacement externe */
        background-color: #f1f1f1;  /* Couleur de fond */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Ombre */
        text-align: center;           /* Alignement du texte */
    }
    h4 {
        color: #4CAF50;  /* Couleur du titre */
    }
    </style>
    """,
    unsafe_allow_html=True
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


st.markdown(
    """
    <div class="text-card">
        <h1>Catégories de Produits</h1>
    </div>
    """,
    unsafe_allow_html=True
    )

col1, col2, col3 = st.columns([1, 2, 1])
with col2: st.sidebar.markdown("# Categories")

col1, col2 = st.columns([2, 2])

with col1: 
    st.markdown(
    """
    <div class="text-card">
        <h3>Liste des Catégories</h3>
    </div>
    """,
    unsafe_allow_html=True
    )
with col1: st.dataframe(df[["category_id", "category"]].drop_duplicates(), height=300)

with col2: 
    st.markdown(
    """
    <div class="text-card">
        <h3>Répartition des Produits par Catégorie</h3>
    </div>
    """,
    unsafe_allow_html=True
    )
fig = px.pie(
    df, names="category", title="Répartition des produits dans les catégories"
)
fig.update_layout(title_font_size=24, legend_font_size=16)
with col2: st.plotly_chart(fig, use_container_width=True)
