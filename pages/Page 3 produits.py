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

def display_image(image_url):
    if not image_url or image_url == "NaN":
        st.info("Ce produit n'a pas d'image.")  
    else:
        st.image(image_url, width=300)


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
    st.markdown("---")


st.markdown(
    "<div class='title'>Page des produits</div>", unsafe_allow_html=True
)


col1, col2, col3 = st.columns([1, 2, 1])
with col2: st.sidebar.markdown("# Produits")

st.markdown("<div class='title'>Filtres des Produits</div>", unsafe_allow_html=True)


filter_page = st.radio(
    "Choisir un type de filtre",
    ["Filtre par Catégorie", "Filtre par Nom", "Filtre Combiné"],
)


if filter_page == "Filtre par Catégorie":
    st.markdown("<div class='subtitle'>Produits par Catégorie et Sous-catégorie</div>", unsafe_allow_html=True)
    

    category_options =  df["category"].unique().tolist() + ["Tous"]
    category_filter = st.selectbox(
        "Sélectionnez une catégorie", options=category_options, index=0
    )
    
    if category_filter == "Tous":
        subcategory_options = df["subcategory"].unique().tolist() + ["Tous"]
    else:
        subcategory_options = df[df["category"] == category_filter]["subcategory"].unique().tolist() + ["Tous"]

    subcategory_filter = st.multiselect(
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
        for index, row in filtered_data.iterrows():
            st.session_state["i"] += 1
            if  st.session_state["i"] > x:
                break
            else:
                st.write(st.session_state['i'])
                display_product_info(row)
                
                
    else:
        st.info("Aucun produit trouvé.")



elif filter_page == "Filtre par Nom":
    st.markdown("<div class='subtitle'>Recherche par Nom de Produit</div>", unsafe_allow_html=True)
    
    search_term = st.text_input("Rechercher un produit par nom", value="")
    
    @st.cache_data
    def search_products(search_term):
        return df[df["title"].str.contains(search_term, case=False)]

    filtered_data = search_products(search_term)

    if not filtered_data.empty:
        for index, row in filtered_data.iterrows():
            display_product_info(row)
    else:
        st.info("Aucun produit trouvé pour cette recherche.")

elif filter_page == "Filtre Combiné":
    st.markdown("<div class='subtitle'>Filtre Combiné</div>", unsafe_allow_html=True)
    

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
        for index, row in filtered_data.iterrows():
            st.session_state["i"] += 1
            if  st.session_state["i"] > x:
                break
            else:
                st.write(st.session_state['i'])
                display_product_info(row)
    else:
        st.info("Aucun produit trouvé pour ces filtres combinés.")
