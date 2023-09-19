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

    for cat_name in cat_names:
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={cat_name}&search_simple=1&action=process&json=1"
        response = requests.get(url)
        data = response.json()

        if user_goal == "Moins de sucres":
            data['products'].sort(key=lambda x: float(x.get('nutriments', {}).get('sugars_value', 0)))
        elif user_goal == "Plus de protéines": 
            data['products'].sort(key=lambda x: float(x.get('nutriments', {}).get('proteins_value', 0)), reverse=True)
        elif user_goal == "Moins de calories":
            data['products'].sort(key=lambda x: float(x.get('nutriments', {}).get('calories_value', 0)))
        elif user_goal == "Moins de gras":
            data['products'].sort(key=lambda x: float(x.get('nutriments', {}).get('fat_value', 0)))
        elif user_goal == "Plus de fibres":
            data['products'].sort(key=lambda x: float(x.get('nutriments', {}).get('fiber_value', 0)), reverse=True)

        products_list.extend(data['products'])

    advice = f"Voici les cinq meilleurs produits qui correspondent à votre objectif :"

    top_5_products = products_list[:5]

    for i, product in enumerate(top_5_products, start=1):
        advice += f"\n{i}. {product.get('product_name', 'Nom du produit inconnu')}"

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

