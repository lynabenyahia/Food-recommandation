#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 16:38:33 2023

@author: HaksNSH
"""
from pyzbar.pyzbar import decode
import tkinter as tk
import pandas as pd
from tkinter import messagebox
from openfoodfacts import API, APIVersion, Country, Environment, Flavor
from tkinter import PhotoImage
from comparaison import open_food_comparison_window
from top_5 import open_top5_window
from PIL import Image, ImageTk
#from data_analyse import *


# Fonction pour ouvrir la fenêtre de comparaison d'aliments

#open_food_comparison_window()


# Fonction pour ouvrir la fenêtre d'analyse de données

def open_data_analysis_window():
    data_analysis_window = tk.Toplevel(root)
    data_analysis_window.title("Analyse de données")

    # Titre de la première partie
    title1 = tk.Label(data_analysis_window, text="Analyse de corrélation entre Nutriscore, Ecoscore et Nova Group")
    title1.pack()

    # Charger l'image 1
    image1 = Image.open("Corr_nutri_eco_nova.png")#mettre les bon chemin
    image1 = ImageTk.PhotoImage(image1)
    label1 = tk.Label(data_analysis_window, image=image1)
    label1.image = image1  # Conserver une référence
    label1.pack()

    # Titre de la deuxième partie
    title2 = tk.Label(data_analysis_window, text="Analyse de corrélation entre Sucre et Gras")
    title2.pack()

    # Charger l'image 2
    image2 = Image.open("Corr_sucres_gras.png")#mettre le bon chemin
    image2 = ImageTk.PhotoImage(image2)
    label2 = tk.Label(data_analysis_window, image=image2)
    label2.image = image2  # Conserver une référence
    label2.pack()


# Fonction pour ouvrir la fenêtre de top 5
#open_top5_window()
    
# Création de la fenêtre principale
root = tk.Tk()
root.title("Menu Principal")
root.geometry("280x250")  # taille de la fenêtre

# Création du bouton pour ouvrir la fenêtre d'analyse de données
button_data_analysis = tk.Button(root, text="Analyse de données", command=open_data_analysis_window, font=("Helvetica", 14))
button_food_comparison = tk.Button(root, text="Comparaison nutritionnelle entre 2 produits alimentaires.", command=open_food_comparison_window, font=("Helvetica", 14))
button_top5 = tk.Button(root, text="Top 5 des produits les plus recommandés", command=open_top5_window, font=("Helvetica", 14))

# Lancements des instances
button_data_analysis.pack(pady=15)
button_food_comparison.pack(pady=15)
button_top5.pack(pady=15)

# Lancer la boucle
root.mainloop()