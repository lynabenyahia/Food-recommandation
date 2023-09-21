#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 09:29:21 2023

@author: lyna
"""

import tkinter as tk
from openfoodfacts import ProductDataset
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
from tkinter import messagebox
from openfoodfacts import API, APIVersion, Country, Environment, Flavor
from tkinter import PhotoImage
import cv2
from PIL import Image, ImageTk

# Fonction pour ouvrir la fenêtre de comparaison d'aliments
def open_food_comparison_window():

    # connexion api open food facts
    api = API(
        username='lyna-hakim',
        password='ds2e67lyna',
        country=Country.world,
        flavor=Flavor.off,
        version=APIVersion.v2,
        environment=Environment.org,
    )

    # Fonction pour obtenir les détails d'un aliment à partir de son code barre
    def get_food_details(barcode):
            product = api.product.get(barcode)
            return product
        
    # Fonction pour recommander un aliment en fonction de l'objectif de l'utilisateur
    def recommend_food():
        barcode1 = entry1.get()
        barcode2 = entry2.get()
        user_goal = goal_var.get()

        product1 = get_food_details(barcode1)
        product2 = get_food_details(barcode2)

        # Obtenez les caractéristiques des aliments
        sugar1 = float(product1['product']['nutriments'].get('sugars_100g', 0))
        sugar2 = float(product2['product']['nutriments'].get('sugars_100g', 0))
        protein1 = float(product1['product']['nutriments'].get('proteins_100g', 0))
        protein2 = float(product2['product']['nutriments'].get('proteins_100g', 0))
        energy1 = float(product1['product']['nutriments'].get('energy-kcal_100g', 0))
        energy2 = float(product2['product']['nutriments'].get('energy-kcal_100g', 0))
        fat1 = float(product1['product']['nutriments'].get('fat_100g', 0))
        fat2 = float(product2['product']['nutriments'].get('fat_100g', 0))
        fiber1 = float(product1['product']['nutriments'].get('fiber_100g', 0))
        fiber2 = float(product2['product']['nutriments'].get('fiber_100g', 0))

        recommendation = ""
        
        
        if user_goal == "Moins de sucres":
            if sugar1 < sugar2:
                recommendation = f"Choisissez le produit {product1['product']['product_name_fr']} - {product1['product']['brands']} qui contient {sugar2-sugar1}g moins de sucre que le produit {product2['product']['product_name_fr']} - {product2['product']['brands']}."
            elif sugar2 < sugar1:
                recommendation = f"Choisissez le produit {product2['product']['product_name_fr']} - {product2['product']['brands']} qui contient {sugar1-sugar2}g moins de sucre que le produit {product1['product']['product_name_fr']} - {product1['product']['brands']}."
            else:
                recommendation = "Les deux produits ont la même teneur en sucres."
        elif user_goal == "Plus de protéines":
            if protein1 > protein2:
                recommendation = f"Choisissez le produit {product1['product']['product_name_fr']} - {product1['product']['brands']} qui contient {protein1-protein2}g plus de protéines que le produit {product2['product']['product_name_fr']} - {product2['product']['brands']}."
            elif protein2 > protein1:
                recommendation = f"Choisissez le produit {product2['product']['product_name_fr']} - {product2['product']['brands']} qui contient {protein2-protein1}g plus de protéines que le produit {product1['product']['product_name_fr']} - {product1['product']['brands']}."
            else:
                recommendation = "Les deux produits ont la même teneur en protéines."
        elif user_goal == "Moins de calories":
            if energy1 > energy2 :
                recommendation = f"Choisissez le produit {product1['product']['product_name_fr']} - {product1['product']['brands']} qui contient {energy1-energy2}g Moins de calories que le produit {product2['product']['product_name_fr']} - {product2['product']['brands']}."
            elif energy2 > energy1 :
                recommendation = f"Choisissez le produit {product2['product']['product_name_fr']} - {product2['product']['brands']} qui contient {energy2-energy1}g Moins de calories que le produit {product1['product']['product_name_fr']} - {product1['product']['brands']}."
            else:
                recommendation = "Les deux produits ont la même teneur en calories."
        elif user_goal == "Moins de gras":
            if fat2 > fat1 :
                recommendation = f"Choisissez le produit {product1['product']['product_name_fr']} - {product1['product']['brands']} qui contient {fat2-fat1}g moins de gras que le produit {product2['product']['product_name_fr']} - {product2['product']['brands']}."
            elif fat1 > fat2 :
                recommendation = f"Choisissez le produit {product2['product']['product_name_fr']} - {product2['product']['brands']} qui contient {fat1-fat2}g moins de gras que le produit {product1['product']['product_name_fr']} - {product1['product']['brands']}."
            else:
                recommendation = "Les deux produits ont la même teneur en gras."
        elif user_goal == "Plus de fibres":
            if fiber1 > fiber2:
                recommendation = f"Choisissez le produit {product1['product']['product_name_fr']} - {product1['product']['brands']} qui contient {fiber1-fiber2}g plus de fibres que le produit {product2['product']['product_name_fr']} - {product2['product']['brands']}."
            elif fiber2 > fiber1:
                recommendation = f"Choisissez le produit {product2['product']['product_name_fr']} - {product2['product']['brands']} qui contient {fiber2-fiber1}g plus de fibres que le produit {product1['product']['product_name_fr']} - {product1['product']['brands']}."
            else:
                recommendation = "Les deux produits ont la même teneur en fibres."

        result_label.config(text=recommendation)

    # Création fenêtre Tkinter
    window = tk.Tk()
    window.title("Comparaison d'aliments")


    # Création des étiquettes et des champs de texte
    label1 = tk.Label(window, text="Code-barres du produit 1:")
    label2 = tk.Label(window, text="Code-barres du produit 2:")
    entry1 = tk.Entry(window)
    entry2 = tk.Entry(window)
    label1.pack()
    entry1.pack()
    label2.pack()
    entry2.pack()

    # Options pour l'objectif de l'utilisateur
    goal_var = tk.StringVar()
    goal_var.set("Moins de sucres")  # on doit sélectionner une valeur par défaut
    #réduire les calories/augmenter la teneur en fibres/réduire les Matières grasses
    goal_label = tk.Label(window, text="Sélectionnez votre objectif:")
    goal_menu = tk.OptionMenu(window, goal_var, "Moins de sucres", "Plus de protéines", "Moins de calories", "Moins de gras", "Plus de fibres")
    compare_button = tk.Button(window, text="Comparer", command=recommend_food)
    result_label = tk.Label(window, text="")
    goal_label.pack()
    goal_menu.pack()
    compare_button.pack()
    result_label.pack()

# Fonction pour ouvrir la fenêtre d'analyse de données
def open_data_analysis_window():
    data_analysis_window = tk.Toplevel(root)
    data_analysis_window.title("Analyse de données")

    # Titre de la première image
    title1 = tk.Label(data_analysis_window, text="Analyse de corrélation entre Nutriscore, Ecoscore et Nova Group")
    title1.pack()

    # Charger l'image 1
    image1 = Image.open("Corr_nutri_eco_nova.png")
    image1 = ImageTk.PhotoImage(image1)
    label1 = tk.Label(data_analysis_window, image=image1)
    label1.image = image1  # Conserver une référence
    label1.pack()

    # Titre de la deuxième image
    title2 = tk.Label(data_analysis_window, text="Analyse de corrélation entre Sucre et Gras")
    title2.pack()

    # Charger l'image 2
    image2 = Image.open("Corr_sucres_gras.png")
    image2 = ImageTk.PhotoImage(image2)
    label2 = tk.Label(data_analysis_window, image=image2)
    label2.image = image2  # Conserver une référence
    label2.pack()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Menu Principal")

# Création du bouton pour ouvrir la fenêtre d'analyse de données
button_data_analysis = tk.Button(root, text="Analyse de données", command=open_data_analysis_window)
button_food_comparison = tk.Button(root, text="Comparaison d'aliments", command=open_food_comparison_window)
button_data_analysis.pack()
button_food_comparison.pack()
button_data_analysis.pack()

# Lancer la boucle
root.mainloop()