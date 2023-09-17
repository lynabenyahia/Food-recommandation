#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 18:51:47 2023

@author: lyna
"""

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
    
# Fonction pour recommander des aliments en fonction de l'objectif de l'utilisateur
def top_food():
    user_category = category_var.get()
    user_goal = goal_var.get()
    
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
    
    advice = ""
    
    if user_goal == "Moins de sucres":
        advice = "Voici les cinq meilleurs produits qui correspondent à votre objectif"
    elif user_goal == "Plus de protéines": 
        advice = "Voici les cinq meilleurs produits qui correspondent à votre objectif"
    elif user_goal == "Moins de calories":
        advice = "Voici les cinq meilleurs produits qui correspondent à votre objectif"
    elif user_goal == "Moins de gras":
        advice = "Voici les cinq meilleurs produits qui correspondent à votre objectif"
    elif user_goal == "Plus de fibres":
        advice = "Voici les cinq meilleurs produits qui correspondent à votre objectif"
    

    result_label.config(text=advice)

# Création fenêtre Tkinter
window = tk.Tk()
window.title("Recommandation d'aliments")

# Options pour l'objectif de l'utilisateur
category_var = tk.StringVar()
category_var.set("Produits laitiers, Desserts, Fromages")  # on doit sélectionner une valeur par défaut
category_label = tk.Label(window, text="Sélectionnez la catégorie d'aliments que vous recherchez':")
category_menu = tk.OptionMenu(window, category_var, "Produits laitiers, Desserts, Fromages", "Snacks sucrés, Confiseries", "Viandes, Volailles", "Produits de la mer, Poissons", "Petit-déjeuners", "Plats préparés", "Boissons")

goal_var = tk.StringVar()
goal_var.set("Moins de sucres")  # on doit sélectionner une valeur par défaut
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


# Lancer la boucle
window.mainloop()