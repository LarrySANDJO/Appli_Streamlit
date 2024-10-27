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
    df["price"] = pd.to_numeric(df["price"], errors="coerce")  # Convertir en numérique, NaN pour erreurs
    
    df["is_out_of_stock"] = df["is_out_of_stock"].fillna(False)
    
    df["category"] = pd.Categorical(df["category"])
    df["subcategory"] = pd.Categorical(df["subcategory"])
    
    return df

df = load_data()

col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2: st.sidebar.markdown("#   Page principale ")

col1, col2, col3 = st.columns([1, 2, 1])
with col1: st.image("images/Photo2.png", width=1000)


@st.cache_data
def display_image(image_url):
    if not image_url or image_url == "NaN":
        st.info("Ce produit n'a pas d'image.") 
    else:
        st.image(image_url, width=100)

@st.cache_data
def display_product_info(product):
    product_name = product.get("title", "Nom non disponible")
    product_price = product.get("price", "Prix non disponible")
    product_image = product.get("image_url", "")
    product_status = "En rupture de stock" if product.get("is_out_of_stock") else "En stock"
    
    col1, col2 = st.columns([1, 3])
    with col1:
        display_image(product_image)
    with col2:
        st.markdown(f"**{product_name}**")
        st.markdown(f"Prix : {product_price} CFA")
        st.markdown(f"Statut : {product_status}")


st.markdown(
        "<div class='title'>Dashboard des Produits</div>", unsafe_allow_html=True
    )
st.markdown("## Vue d'ensemble des produits")

total_products = df["product_id"].nunique()
total_categories = df["category_id"].nunique()
total_subcategories = df["subcategory_id"].nunique()
out_of_stock_products = df[df["is_out_of_stock"] == True].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de produits", total_products)
col2.metric("Catégories", total_categories)
col3.metric("Sous-catégories", total_subcategories)
col4.metric("En rupture de stock", out_of_stock_products)

max_price_product = df.loc[df['price'].idxmax()]
min_price_product = df.loc[df['price'].idxmin()]

st.markdown("### Produit le plus cher")
display_product_info(max_price_product)

st.markdown("### Produit le moins cher")
display_product_info(min_price_product)

st.markdown("---")

col1, col2 = st.columns([2, 2])



category_count = df["category"].value_counts()
fig = px.pie(
    values=category_count,
    names=category_count.index,
    title="Répartition par catégorie",
)
fig.update_layout(title_font_size=24, legend_font_size=16)
with col1: st.plotly_chart(fig, use_container_width=True)


out_of_stock_data = df[df["is_out_of_stock"] == True]
if not out_of_stock_data.empty:
    fig2 = px.bar(
        out_of_stock_data,
        x="category",
        title="Produits en rupture de stock par catégorie",
        labels={"x": "Catégorie", "y": "Nombre de produits"},
    )
    fig2.update_layout(title_font_size=24, legend_font_size=16)
    with col2: st.plotly_chart(fig2, use_container_width=True)
else:
    with col2: st.info("Aucun produit en rupture de stock.")


