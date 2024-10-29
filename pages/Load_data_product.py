from typing import List
from datetime import date
import pymysql
import pandas as pd

def load_data_product(product: int):
    # Connexion à la base de données
    conn = pymysql.connect(
        host="db-auchan.c5esoc4g6qck.eu-west-3.rds.amazonaws.com",
        user="admin",
        password="MNdione2024",# Utilisation de DictCursor pour des résultats sous forme de dictionnaire
        database="bdccAuchan"
    )

    cursor = conn.cursor()
    
    # Exécuter une requête pour récupérer les informations de produits correspondant à l'ID de sous-catégorie
    query = """
    SELECT * FROM suivi
    WHERE idProduit = %s 
            """
    cursor.execute(query, (product))
    
    # Récupérer les résultats
    result = cursor.fetchall()
            
    # Fermer la connexion
    conn.close()
    # Convertir les résultats en DataFrame
    df = pd.DataFrame(result)
    
    return df
    
print("Début")
data=load_data_product(product=125)
print(data.head())
# print(data.columns)
print("Fin")