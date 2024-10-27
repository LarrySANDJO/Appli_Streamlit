import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np


st.set_page_config(page_title="Auchan", page_icon="🌋", layout="wide")
st.header("🔔DASHBORD DE SUIVI DES PRIX DE AUCHAN SENEGAL")
# Création de colonnes pour centrer l'image

st.sidebar.image(
    "images/Auchan-Logo.png",
    caption="Dashbord Auchan",
    use_column_width=True
)

# Charger les données JSON avec mise en cache pour améliorer les performances
@st.cache_data
def load_data():
    with open("out_of_stck.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    # Nettoyer les prix et gérer les erreurs de format
    df["price"] = df["price"].str.replace("\u202f", "").str.replace("\xa0CFA", "")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")  # Convertir en numérique, NaN pour erreurs
    
    # Remplacer les valeurs NaN dans is_out_of_stock par False si manquantes
    df["is_out_of_stock"] = df["is_out_of_stock"].fillna(False)
    
    # Optimiser les colonnes catégorielles
    df["category"] = pd.Categorical(df["category"])
    df["subcategory"] = pd.Categorical(df["subcategory"])
    
    return df

# Charger les données
df = load_data()

st.markdown(
    """
    <style>
        .title {
            font-size: 40px;
            color: blue;
            text-align: center;
            margin-bottom: 20px;
            bold: True;
        }
        .subtitle {
            font-size: 30px;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .product-card {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .dataframe {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Pagination configuration
@st.cache_data
def paginate_data(data, page_size=10):
    page_number = st.number_input("Page", min_value=1, max_value=(len(data) // page_size) + 1, step=1)
    start_idx = (page_number - 1) * page_size
    return data.iloc[start_idx : start_idx + page_size]


# Fonction pour gérer l'affichage des images manquantes
@st.cache_data
def display_image(image_url):
    if not image_url or image_url == "NaN":
        st.info("Ce produit n'a pas d'image.")  # Image par défaut si erreur ou manquante
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
    "<div class='title'>Page des produits</div>", unsafe_allow_html=True
)


col1, col2, col3 = st.columns([1, 2, 1])
with col2: st.sidebar.markdown("# Produits")

st.markdown("<div class='title'>Filtres des Produits</div>", unsafe_allow_html=True)

# Sélectionner une sous-page pour les filtres
filter_page = st.radio(
    "Choisir un type de filtre",
    ["Filtre par Catégorie", "Filtre par Nom", "Filtre Combiné"],
)

# 4.1 Filtre par Catégorie et Sous-catégorie
if filter_page == "Filtre par Catégorie":
    st.markdown("<div class='subtitle'>Produits par Catégorie et Sous-catégorie</div>", unsafe_allow_html=True)
    
    # Filtre de recherche par catégorie avec option "Tous"
    category_options =  df["category"].unique().tolist() + ["Tous"]
    category_filter = st.selectbox(
        "Sélectionnez une catégorie", options=category_options, index=0
    )
    
    # Pré-filtrer les sous-catégories après avoir sélectionné une catégorie avec option "Tous"
    if category_filter == "Tous":
        subcategory_options = df["subcategory"].unique().tolist() + ["Tous"]
    else:
        subcategory_options = df[df["category"] == category_filter]["subcategory"].unique().tolist() + ["Tous"]

    subcategory_filter = st.selectbox(
        "Sélectionnez une sous-catégorie",
        options=subcategory_options,
        index=0,
    )

    # Filtrer les produits selon la catégorie et sous-catégorie
    if category_filter == "Tous" and subcategory_filter == "Tous":
        filtered_data = df  # Affiche tous les produits
    elif category_filter == "Tous":
        filtered_data = df[df["subcategory"] == subcategory_filter]  # Affiche tous les produits de la sous-catégorie sélectionnée
    elif subcategory_filter == "Tous":
        filtered_data = df[df["category"] == category_filter]  # Affiche tous les produits de la catégorie sélectionnée
    else:
        filtered_data = df[
            (df["category"] == category_filter) & 
            (df["subcategory"] == subcategory_filter)
        ]  # Filtre par catégorie et sous-catégorie

    if not filtered_data.empty:
        # Boucle sur les produits filtrés et affichage
        for index, row in filtered_data.iterrows():
            product_name = row["title"]
            product_price = row["price"]
            product_image = row["image_url"]
            product_status = "En rupture de stock" if row["is_out_of_stock"] else "En stock"
            
            col1, col2 = st.columns([1, 3])
            with col1:
                display_image(product_image)
            with col2:
                st.markdown(f"**{product_name}**")
                st.markdown(f"Prix : {product_price} CFA")
                st.markdown(f"Statut : {product_status}")
            st.markdown("---")
    else:
        st.info("Aucun produit trouvé pour cette catégorie.")


# 4.2 Filtre par Nom de produit
elif filter_page == "Filtre par Nom":
    st.markdown("<div class='subtitle'>Recherche par Nom de Produit</div>", unsafe_allow_html=True)
    
    # Barre de recherche par nom de produit
    search_term = st.text_input("Rechercher un produit par nom", value="")
    
    # Ajouter un cache pour cette recherche si elle est volumineuse
    @st.cache_data
    def search_products(search_term):
        return df[df["title"].str.contains(search_term, case=False)]

    filtered_data = search_products(search_term)

    if not filtered_data.empty:
        for index, row in filtered_data.iterrows():
            product_name = row["title"]
            product_price = row["price"]
            product_image = row["image_url"]
            product_status = "En rupture de stock" if row["is_out_of_stock"] else "En stock"
            
            col1, col2 = st.columns([1, 3])
            with col1:
                display_image(product_image)
            with col2:
                st.markdown(f"**{product_name}**")
                st.markdown(f"Prix : {product_price} CFA")
                st.markdown(f"Statut : {product_status}")
            st.markdown("---")
    else:
        st.info("Aucun produit trouvé pour cette recherche.")

# 4.3 Filtre combiné (catégorie, sous-catégorie, et nom)
elif filter_page == "Filtre Combiné":
    st.markdown("<div class='subtitle'>Filtre Combiné</div>", unsafe_allow_html=True)
    
    # Filtre par catégorie et sous-catégorie
    category_filter = st.selectbox("Sélectionnez une catégorie", options=df["category"].unique(), index=0)
    subcategory_filter = st.selectbox(
        "Sélectionnez une sous-catégorie",
        options=df[df["category"] == category_filter]["subcategory"].unique(),
        index=0,
    )

    # Barre de recherche par nom de produit
    search_term = st.text_input("Rechercher un produit par nom", value="")

    # Filtrer les produits selon tous les critères
    filtered_data = df[
        (df["category"] == category_filter)
        & (df["subcategory"] == subcategory_filter)
        & (df["title"].str.contains(search_term, case=False))
    ]

    if not filtered_data.empty:
        for index, row in filtered_data.iterrows():
            product_name = row["title"]
            product_price = row["price"]
            product_image = row["image_url"]
            product_status = "En rupture de stock" if row["is_out_of_stock"] else "En stock"
            
            col1, col2 = st.columns([1, 3])
            with col1:
                display_image(product_image)
            with col2:
                st.markdown(f"**{product_name}**")
                st.markdown(f"Prix : {product_price} CFA")
                st.markdown(f"Statut : {product_status}")
            st.markdown("---")
    else:
        st.info("Aucun produit trouvé pour ces filtres combinés.")
