#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 19:59:53 2023

@author: HaksNSH
"""

import openfoodfacts
import tkinter as tk
from tkinter import messagebox
from openfoodfacts import API, APIVersion, Country, Environment, Flavor

# connexion api open food facts
api = API(
    username='lyna-hakim',
    password='ds2e67lyna',
    country=Country.world,
    flavor=Flavor.off,
    version=APIVersion.v2,
    environment=Environment.org,
)

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


import requests
from bs4 import BeautifulSoup



def top_food():
    user_category = category_var.get()
    user_goal = goal_var.get()
    
    if user_category not in categories:
        messagebox.showerror("Erreur", "Catégorie non prise en charge.")
        return
    
    cat_names = categories[user_category]
    products_list = []
    if user_category == "Produits laitiers, Desserts, Fromages":
        cat = "Produits laitiers, Desserts, Produits fermentés, Produits laitiers fermentés, Fromages, Desserts lactés, Desserts lactés fermentés, Skyrs, Fromages à la crème"
    elif user_category == "Snacks sucrés, Confiseries":
        cat = "Snacks, Snacks sucrés, Confiseries, Massepain, Pâtes d'amande"
    elif user_category == "Viandes, Volailles":
        cat = "Viandes, Volailles, Poulets, Aiguillettes de poulet"
    elif user_category == "Produits de la mer, Poissons":
        cat = "Produits de la mer, Poissons, Poissons gras, Saumons, Poissons fumés, Saumons fumés, Pavés de saumon, Pavés de saumon fumé"
    elif user_category == "Petit-déjeuners":
        cat = "Petit-déjeuners, Produits à tartiner, Produits à tartiner sucrés, Pâtes à tartiner, Pâtes à tartiner aux noisettes"
    elif user_category == "Plats préparés":
        cat = "Plats préparés, Plats préparés à réchauffer au micro-ondes"
    elif user_category == "Boissons":
        cat = "Boissons"

    
    
    for cat in cat_names:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={cat}&search_simple=1&action=process&json=1"
        response = requests.get(url)
        data = response.json()

        # Vérifiez que chaque produit appartient à la catégorie sélectionnée par l'utilisateur
        for product in data['products']:
            if cat in product.get('categories', []):
                products_list.append(product)

    # Triez la liste de produits en fonction du contenu nutritionnel
    if user_goal == "Moins de sucres":
        products_list.sort(key=lambda x: float(x.get('nutriments', {}).get('sugars_100g', 0)))
    elif user_goal == "Plus de protéines":
        products_list.sort(key=lambda x: -float(x.get('nutriments', {}).get('proteins_100g', 0)))
    elif user_goal == "Moins de calories":
        products_list.sort(key=lambda x: float(x.get('nutriments', {}).get('energy-kcal_100g', 0)))
    elif user_goal == "Moins de gras":
        products_list.sort(key=lambda x: float(x.get('nutriments', {}).get('fat_100g', 0)))
    elif user_goal == "Plus de fibres":
        products_list.sort(key=lambda x: -float(x.get('nutriments', {}).get('fiber_100g', 0)))
    

    advice = f"Voici les cinq meilleurs produits qui correspondent à votre objectif :"

    unique_products_set = set()
    for i, product in enumerate(products_list[:5], start=1):
        product_name = product.get('product_name', 'Nom du produit inconnu')
        if product_name not in unique_products_set:
            advice += f"\n{i}. {product_name}"
            unique_products_set.add(product_name)

    result_label.config(text=advice)






window = tk.Tk()
window.title("Recommandation d'aliments")

category_var = tk.StringVar()
category_var.set("Produits laitiers, Desserts, Fromages")  
category_label = tk.Label(window, text="Sélectionnez la catégorie d'aliments que vous recherchez':")
category_menu = tk.OptionMenu(window, category_var, "Produits laitiers, Desserts, Fromages", "Snacks sucrés, Confiseries", "Viandes, Volailles", "Produits de la mer, Poissons", "Petit-déjeuners", "Plats préparés", "Boissons")

goal_var = tk.StringVar()
goal_var.set("Moins de sucres") 
goal_label = tk.Label(window, text="Sélectionnez votre objectif:")
goal_menu = tk.OptionMenu(window, goal_var, "Moins de sucres", "Plus de protéines", "Moins de calories", "Moins de gras", "Plus de fibres")
compare_button = tk.Button(window, text="Chercher", command=top_food)
result_label = tk.Label(window, text="")

category_label.pack()
category_menu.pack()
goal_label.pack()
goal_menu.pack()
compare_button.pack()
result_label.pack()
window.mainloop()

