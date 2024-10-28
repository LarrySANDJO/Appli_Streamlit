import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(page_title="Auchan", page_icon="♨️", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2: st.header("🔔DASHBORD DE SUIVI DES PRIX DE AUCHAN SENEGAL🔔")

# pas de theme par defaut
theme_plotly = None 

# chargement du style css pour les graphiques
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Chargement du css pour les textes
with open("bootstrap_style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Chargement des composantes bootstrap
st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    """, unsafe_allow_html=True)

# Logo
st.sidebar.image(
    "images/Auchan-Logo.png",
    caption="Dashbord Auchan",
    use_column_width=True
)

# Fonction pour transformer la base json en dataframe
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

# chargement des donnees
df = load_data()

# Etiquette de page
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2: 
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h1 style = "text-align: center;font-weight: bold;">Page principale</h1>
        </div>
    """, unsafe_allow_html=True)

# Photo de Auchan
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
        </div>
    """, unsafe_allow_html=True)
with col2: 
    st.image("images/Photo2.png", width=1000)
with col3:
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
        </div>
    """, unsafe_allow_html=True)
    
st.markdown("---")

# Fonction pour afficher les images
@st.cache_data
def display_image(image_url):
    if not image_url or image_url == "NaN":
        st.info("Ce produit n'a pas d'image.") 
    else:
        st.image(image_url, width=200)

# Fonction pour afficher un produit
@st.cache_data
def display_product_info(product):
    product_name = product.get("title", "Nom non disponible")
    product_price = product.get("price", "Prix non disponible")
    product_image = product.get("image_url", "")
    product_status = "En rupture de stock" if product.get("is_out_of_stock") else "En stock"
    st.markdown(
        """
        <style>
        .product-card {
            border: 1px solid #d1d1d1;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 16px;
            background-color: #f9f9f9;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f"""
    <div class="product-card">
        <img src="{product_image}" alt="Image du produit" style="width:100%; height:auto; border-radius: 8px;">
        <h4>{product_name}</h4>
        <p style = "font-weight: bold;font-size: 24px;">Prix : {product_price} CFA</p>
        <p>Statut : {product_status}</p>
    </div>
    """, unsafe_allow_html=True)


# Affichage des donnees cles
total_products = df["product_id"].nunique()
total_categories = df["category_id"].nunique()
total_subcategories = df["subcategory_id"].nunique()
out_of_stock_products = df[df["is_out_of_stock"] == True].shape[0]
on_promotion = df[df["old_price"] != "Not concerned"].shape[0]

def display_custom_metric(label, value, color):
    st.markdown(
        f"""
        <div style="background-color: {color}; padding: 20px; border-radius: 10px; margin: 5px 0;">
            <p style="font-size: 9px; margin: 0; color: white;">{label}</p>
            <h2 style="margin: 0; color: white; font-weight: bold">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.info('Total de produits',icon="📌")
    display_custom_metric("Total de produits", total_products, "#0000FF")
with col2:
    st.info('Catégories',icon="📌")
    display_custom_metric("Catégories", total_categories, "#228B22")
with col3:
    st.info('Sous-catégories',icon="📌")
    display_custom_metric("Sous-catégories", total_subcategories, "#FF0000")
with col4:
    st.info('En rupture de stock',icon="⚠️")
    display_custom_metric("En rupture de stock", out_of_stock_products, "#FE9900")
with col5:
    st.info('En promotion',icon="💯")
    display_custom_metric("En promotio", on_promotion, "#582698")



# style_metric_cards(background_color="#F5F5DC",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")

st.markdown("---")

# Affichage du produit le plus cher et le moins 
max_price_product = df.loc[df['price'].idxmax()]
min_price_product = df.loc[df['price'].idxmin()]

col1, col2 = st.columns([2, 2])

with col1: 
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h3 style = "text-align: center;font-weight: bold;">Produit le plus cher</h3>
        </div>
    """, unsafe_allow_html=True)
    display_product_info(max_price_product)

with col2: 
    st.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h3 style = "text-align: center; font-weight: bold;">Produit le moins cher</h3>
        </div>
    """, unsafe_allow_html=True)
    display_product_info(min_price_product)

st.markdown("---")


# Graphique de repartition par categorie
col1, col2 = st.columns([2, 2])

category_count = df["category"].value_counts()
fig = px.pie(
    values=category_count,
    names=category_count.index,
    title="Répartition par catégorie",
)
fig.update_layout(title_font_size=24, legend_font_size=16)
with col1: st.plotly_chart(fig, use_container_width=True)

# Affichage des produits en rupture de stock par categorie
out_of_stock_data = df[df["is_out_of_stock"] == True]

if not out_of_stock_data.empty:
    fig2 = px.pie(
        out_of_stock_data,
        names="category",      
        title="Produits en rupture de stock par catégorie",
        hole=0.3               
    )
    
    fig2.update_traces(textinfo="label+value", textfont_size=10) 
    fig2.update_layout(title_font_size=24, legend_font_size=16)
    
    with col2: 
        st.plotly_chart(fig2, use_container_width=True)

else:
    with col2: 
        st.info("Aucun produit en rupture de stock.")

# Fin de la page d'acceuil