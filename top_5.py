#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 19:39:55 2023

@author: HaksNSH
"""
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import requests
from concurrent.futures import ThreadPoolExecutor

def open_top5_window():
    # URL de l'API Open Food Facts pour la France
    API_URL = "https://world.openfoodfacts.org/cgi/search.pl"

    # Récupération des vraies catégories contenues dans les catégories simplifiées que nous avons proposés à l'utilisateur
    categories = {
        "Produits laitiers, Desserts, Fromages": [
            "Produits laitiers",
            "Produits fermentés", 
            "Produits laitiers fermentés", 
            "Fromages", 
            "Desserts lactés",
            "Desserts lactés fermentés",
            "Skyrs", 
            "Fromages à la crème",
            "Dairies",
            "Desserts",
            "Cheeses",
        ],
        "Snacks sucrés, Confiseries": [
            "Snacks",
            "Snacks sucrés",
            "Confiseries",
            "Massepain",
            "Pâtes d'amande",
        ],
        "Viandes, Volailles": [
            "Viandes",
            "Volailles",
            "Poulets",
            "Aiguillettes de poulet",
        ],
        "Produits de la mer, Poissons": [
            "Produits de la mer",
            "Poissons",
            "Poissons gras",
            "Saumons",
            "Poissons fumés",
            "Saumons fumés",
            "Pavés de saumon",
            "Pavés de saumon fumé",
        ],
        "Petit-déjeuners": [
            "Petit-déjeuners",
            "Produits à tartiner",
            "Produits à tartiner sucrés",
            "Pâtes à tartiner",
            "Pâtes à tartiner aux noisettes",
        ],
        "Plats préparés": ["Plats préparés", "Plats préparés à réchauffer au micro-ondes"],
        "Boissons": ["Boissons"],
    }

    def produit_est_unique(product, products_list):
        # Vérifie si le produit est déjà dans la liste des produits
        for produit_existant in products_list:
            if product['Produit'] == produit_existant['Produit']:
                return False
        return True

    # Requête pour faire des recherches avancées (ici, par catégories)
    def recup_produit(cat):
        params = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": cat,
            "countries": "France",
            "json": "1",
            "page_size": 20, 
        }

        response = requests.get(API_URL, params=params)

        if response.status_code == 200: # si nous n'avons pas d'erreur
            data = response.json().get("products", [])
            return data
        return []

    def top_food():
        user_category = category_var.get()
        user_goal = goal_var.get()

        products_list = []

        # Utiliser ThreadPoolExecutor pour paralléliser les requêtes API afin d'aller plus vite
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(recup_produit, categories[user_category]))

        for data in results:
            for produit in data:
                product = {
                    'Produit': produit.get('product_name'),
                    'Marque': produit.get('brands',''),
                    'Catégorie': produit.get('categories'),
                    'Sucres': produit.get('nutriments', {}).get('sugars_100g', ''),
                    'Graisses': produit.get('nutriments', {}).get('fat_100g', ''),
                    'Calories': produit.get('nutriments', {}).get('energy-kcal_100g', ''),
                    'Fibres': produit.get('nutriments', {}).get('fiber_100g', ''),
                    'Protéines': produit.get('nutriments', {}).get('proteins_100g', ''),
                }

                # Ajouts des aliments à la liste
                if produit_est_unique(product, products_list) and product['Catégorie'] :
                    products_list.append(product)

        # Création d'un dataframe avec tous les nutriments dont on a besoin
        df = pd.DataFrame(products_list)
        nutrient_column = ''  
        if user_goal == "Moins de sucres":
            nutrient_column = 'Sucres'
        elif user_goal == "Plus de protéines":
            nutrient_column = 'Protéines'
        elif user_goal == "Moins de calories":
            nutrient_column = 'Calories'
        elif user_goal == "Moins de gras":
            nutrient_column = 'Graisses'
        elif user_goal == "Plus de fibres":
            nutrient_column = 'Fibres'
        
        # Traitement des erreurs
        if nutrient_column:
            df[nutrient_column] = pd.to_numeric(df[nutrient_column], errors='coerce')

            df = df.dropna(subset=[nutrient_column])  
            
            # Tris selon les demandes d'utilisateurs
            if user_goal == "Moins de sucres":
                sorted_df = df.sort_values(by=nutrient_column, ascending=True)
            elif user_goal == "Plus de protéines":
                sorted_df = df.sort_values(by=nutrient_column, ascending=False)
            elif user_goal == "Moins de calories":
                sorted_df = df.sort_values(by=nutrient_column, ascending=True)
            elif user_goal == "Moins de gras":
                sorted_df = df.sort_values(by=nutrient_column, ascending=True)
            elif user_goal == "Plus de fibres":
                sorted_df = df.sort_values(by=nutrient_column, ascending=False)

            # Retour du top 5
            top_5_products = sorted_df.head(5)
            advice = f"Voici les cinq meilleurs produits qui correspondent à votre objectif :"
            for i, products in enumerate(top_5_products.iterrows(), start=1):
                advice += f"\n{i}. {products[1]['Produit']} - {products[1]['Marque']} - {products[1][nutrient_column]}g de {nutrient_column}"

            result_label.config(text=advice)
        else:
            result_label.config(text="Objectif invalide")

# Création de la fenêtre
    window = tk.Tk()
    window.title("Recommandation d'aliments")
# Création des options
    category_var = tk.StringVar()
    category_var.set("Produits laitiers, Desserts, Fromages")  
    category_label = tk.Label(window, text="Sélectionnez la catégorie d'aliments que vous recherchez :")
    category_menu = tk.OptionMenu(window, category_var, "Produits laitiers, Desserts, Fromages", "Snacks sucrés, Confiseries", "Viandes, Volailles", "Produits de la mer, Poissons", "Petit-déjeuners", "Plats préparés", "Boissons")

    goal_var = tk.StringVar()
    goal_var.set("Moins de sucres") 
    goal_label = tk.Label(window, text="Sélectionnez votre objectif :")
    goal_menu = tk.OptionMenu(window, goal_var, "Moins de sucres", "Plus de protéines", "Moins de calories", "Moins de gras", "Plus de fibres")
    compare_button = tk.Button(window, text="Chercher", command=top_food)
    result_label = tk.Label(window, text="")

# Lancement des instances
    category_label.pack()
    category_menu.pack()
    goal_label.pack()
    goal_menu.pack()
    compare_button.pack()
    result_label.pack()
    window.mainloop()
    

