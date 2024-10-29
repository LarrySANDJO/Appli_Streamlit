import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
from pages.Load_data_product import load_data_product


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

st.write(load_data_product(125))

