import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np


# Page d'acceuil

# Configuration de la page
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

def display_image(image_url):
    if not image_url or image_url == "NaN":
        st.info("Ce produit n'a pas d'image.")  
    else:
        st.image(image_url, width=300)

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


st.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h2 style = "text-align: center;font-weight: bold;">Page des produits</h2>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h2 style = "text-align: center;font-weight: bold;">Produits</h2>
        </div>
    """, unsafe_allow_html=True)


filter_page = st.sidebar.radio(
    "Choisir un type de filtre",
    ["Filtre par Catégorie", "Filtre par Nom", "Filtre Combiné"],
)

cols_per_row = 6

if filter_page == "Filtre par Catégorie":
        
    category_options =  df["category"].unique().tolist() + ["Tous"]
    category_filter = st.sidebar.selectbox(
        "Sélectionnez une catégorie", options=category_options, index=0
    )
    
    if category_filter == "Tous":
        subcategory_options = df["subcategory"].unique().tolist() + ["Tous"]
    else:
        subcategory_options = df[df["category"] == category_filter]["subcategory"].unique().tolist() + ["Tous"]

    subcategory_filter = st.sidebar.multiselect(
        "Sélectionnez une sous-catégorie",
        options=subcategory_options
    )

    
    if category_filter == "Tous" and subcategory_filter == "Tous":
        filtered_data = df 
    elif category_filter == "Tous":
        filtered_data = df[df["subcategory"] == subcategory_filter]  
    elif subcategory_filter == "Tous":
        filtered_data = df[df["category"] == category_filter]  
    else:
        filtered_data = df[
            (df["category"] == category_filter) & 
            (df["subcategory"].isin(subcategory_filter))
        ] 

    
    if not filtered_data.empty:
        x = st.slider("Nombre maximum de produits", value = 15)
        if "i" not in st.session_state:
            st.session_state['i'] = 0
        st.session_state['i'] = 0
        cols = st.columns(cols_per_row)
        for index, row in filtered_data.iterrows():
            if  st.session_state["i"] > x:
                break
            if st.session_state["i"] % cols_per_row == 0:
                cols = st.columns(cols_per_row)
            col_idx = st.session_state["i"] % cols_per_row
            with cols[col_idx]:
                st.write(st.session_state['i'])
                display_product_info(row)
            st.session_state["i"] += 1
    else:
        st.info("Aucun produit trouvé.")



elif filter_page == "Filtre par Nom": 
    search_term = st.text_input("Rechercher un produit par nom", value="")
    
    @st.cache_data
    def search_products(search_term):
        return df[df["title"].str.contains(search_term, case=False)]

    filtered_data = search_products(search_term)

    if not filtered_data.empty:
        x = st.slider("Nombre maximum de produits", value = 15)
        if "i" not in st.session_state:
            st.session_state['i'] = 0
        st.session_state['i'] = 0
        cols = st.columns(cols_per_row)
        for index, row in filtered_data.iterrows():
            if  st.session_state["i"] > x:
                break
            if st.session_state["i"] % cols_per_row == 0:
                cols = st.columns(cols_per_row)
            col_idx = st.session_state["i"] % cols_per_row
            with cols[col_idx]:
                st.write(st.session_state['i'])
                display_product_info(row)
            st.session_state["i"] += 1
    else:
        st.info("Aucun produit trouvé pour cette recherche.")

elif filter_page == "Filtre Combiné":
    
    category_filter = st.selectbox("Sélectionnez une catégorie", options=df["category"].unique(), index=0)
    subcategory_filter = st.multiselect(
        "Sélectionnez une sous-catégorie",
        options=df[df["category"] == category_filter]["subcategory"].unique(),

    )

    search_term = st.text_input("Rechercher un produit par nom", value="")

    filtered_data = df[
        (df["category"] == category_filter)
        & (df["subcategory"].isin(subcategory_filter))
        & (df["title"].str.contains(search_term, case=False))
    ]

    if not filtered_data.empty:
        x = st.slider("Nombre maximum de produits", value = 15)
        if "i" not in st.session_state:
            st.session_state['i'] = 0
        st.session_state['i'] = 0
        cols = st.columns(cols_per_row)
        for index, row in filtered_data.iterrows():
            if  st.session_state["i"] > x:
                break
            if st.session_state["i"] % cols_per_row == 0:
                cols = st.columns(cols_per_row)
            col_idx = st.session_state["i"] % cols_per_row
            with cols[col_idx]:
                st.write(st.session_state['i'])
                display_product_info(row)
            st.session_state["i"] += 1
    else:
        st.info("Aucun produit trouvé pour ces filtres combinés.")

st.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h3 style = "text-align: center;font-weight: bold;">Produits en promotion</h3>
        </div>
    """, unsafe_allow_html=True)

on_promotion = df[df["old_price"] != "Not concerned"]
if not on_promotion.empty:
        if "i" not in st.session_state:
            st.session_state['i'] = 0
        st.session_state['i'] = 0
        cols = st.columns(cols_per_row)
        for index, row in on_promotion.iterrows():
            if st.session_state["i"] % cols_per_row == 0:
                cols = st.columns(cols_per_row)
            col_idx = st.session_state["i"] % cols_per_row
            with cols[col_idx]:
                st.write(st.session_state['i'])
                display_product_info(row)
            st.session_state["i"] += 1

st.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h3 style = "text-align: center;font-weight: bold;">Produits en rupture de stock</h3>
        </div>
    """, unsafe_allow_html=True)
out_of_stock_products = df[df["is_out_of_stock"] == True]
if not out_of_stock_products.empty:
        if "i" not in st.session_state:
            st.session_state['i'] = 0
        st.session_state['i'] = 0
        cols = st.columns(cols_per_row)
        for index, row in out_of_stock_products.iterrows():
            if st.session_state["i"] % cols_per_row == 0:
                cols = st.columns(cols_per_row)
            col_idx = st.session_state["i"] % cols_per_row
            with cols[col_idx]:
                st.write(st.session_state['i'])
                display_product_info(row)
            st.session_state["i"] += 1

