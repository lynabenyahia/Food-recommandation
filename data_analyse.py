#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 13:07:04 2023

@author: lyna
"""

from openfoodfacts import ProductDataset
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kendalltau

# =============================================================================
# ANALYSE DE CORRÉLATION NUTRISCORE/ECOSCORE/NOVA GROUPE
# =============================================================================

# création de la base de 15000 produits
count = 0 
data_list = []

for produit in ProductDataset("csv"):
    # Vérifier si le produit est français et a un ecoscore_grade, un nova_group et un nutriscore_grade non nuls
    if (
        produit['ecoscore_grade'] != '' and produit['ecoscore_grade'] != 'unknown' and produit['ecoscore_grade'] != 'not-applicable'
        and produit['nova_group'] != ''
        and produit['nutriscore_grade'] != ''
        and produit['countries'] == 'France'
    ):
        data_list.append([
            produit.get('product_name'),
            produit.get('ecoscore_grade'),
            produit.get('nova_group'),
            produit.get('nutriscore_grade')
        ])
        count += 1
    if count == 15000:
        break

# création d'un DataFrame
df = pd.DataFrame(data_list, columns=['Produit', 'Ecoscore', 'Nova', 'Nutriscore'])

# remplacer les valeurs allant de a à e en valeurs allant de 1 à 5
remplacements = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
df = df.applymap(lambda x: remplacements.get(x, x))

if __name__ == "__main__":
    # Calculer la corrélation de rang de Kendall
    correlation_matrix, _ = kendalltau(df['Nutriscore'], df['Ecoscore'])
    correlation_matrix2, _ = kendalltau(df['Nutriscore'], df['Nova'])
    correlation_matrix3, _ = kendalltau(df['Ecoscore'], df['Nova'])

    # Afficher la matrice de corrélation sous forme de heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap([[1,correlation_matrix, correlation_matrix2],
                  [correlation_matrix, 1, correlation_matrix3],
                  [correlation_matrix2, correlation_matrix3, 1]],
                 annot=True, cmap='coolwarm', linewidths=.5,
                 xticklabels=['nutriscore', 'ecoscore', 'nova group'],
                 yticklabels=['nutriscore', 'ecoscore', 'nova group'])
    plt.title("Matrice de Corrélation (Kendall)")
    plt.show()

# =============================================================================
# ANALYSE DE CORRÉLATION GRAISSES/SUCRES
# =============================================================================
# création de la base de 15000 produits
count = 0 
data_list2 = []

for produit in ProductDataset("csv"):
    # Vérifier si le produit est français a des valeurs pour les sucres et les graisses non nulles
    if (
        produit['sugars_100g'] != ''
        and produit['fat_100g'] != ''
        and produit['countries'] == 'France'
    ):
        data_list2.append([
            produit.get('product_name'),
            produit.get('sugars_100g'),
            produit.get('fat_100g'),
        ])
        count += 1
    if count == 15000:
        break

# création d'un DataFrame
df2 = pd.DataFrame(data_list2, columns=['Produit', 'Sucres', 'Graisses'])

# transition vers des valeurs numériques
df2['Sucres'] = pd.to_numeric(df2['Sucres'], errors='coerce')
df2['Graisses'] = pd.to_numeric(df2['Graisses'], errors='coerce')

if __name__ == "__main__":
    # matrice et graphique de corrélation
    correlation_matrix4 = df2[['Sucres', 'Graisses']].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix4, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Corrélation entre Sucres et Graisses")
    plt.show()
