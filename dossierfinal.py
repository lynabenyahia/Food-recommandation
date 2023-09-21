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
import cv2
from PIL import Image, ImageTk
import requests
from concurrent.futures import ThreadPoolExecutor



    
# Fonction pour ouvrir la fenêtre de comparaison d'aliments
def open_food_comparison_window():
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

    # Fonction pour numériser un code-barres à partir d'une image
    def code_barre(image_path):
        image = cv2.imread(image_path)
        decoded_barcodes = decode(image)
        
        barcode_data_list = []  # Liste pour stocker les codes-barres
    
        for barcode in decoded_barcodes:
            barcode_data = barcode.data.decode('utf-8')  # Convertir les données en chaîne de caractères
            barcode_data_list.append(barcode_data)  # Ajouter le code-barre à la liste
    
        return barcode_data_list  # Retourner la liste de codes-barres

    barcode_image1 = ""
    barcode_image2 = ""
    # Fonction pour charger l'image du code-barres
    def load_barcode_image():
        global barcode_image1, barcode_image2 
        image_path1 = entry3.get()
        image_path2 = entry4.get()
    

        if not image_path1 or not image_path2:
            recommendation = "Veuillez spécifier les chemins des images du code-barres pour les deux produits."
            result_label.config(text=recommendation)
            return

        barcode_image1 = code_barre(image_path1)
        barcode_image2 = code_barre(image_path2)

        if not barcode_image1 or not barcode_image2:
            recommendation = "Aucun code-barre valide n'a été trouvé dans les images fournies."
            result_label.config(text=recommendation)
            return


        print("Code-barre image 1:", barcode_image1)
        print("Code-barre image 2:", barcode_image2)




    def recommend_food():
        global barcode_image1, barcode_image2 
        barcode1 = entry1.get()
        barcode2 = entry2.get()
        user_goal = goal_var.get()

        if barcode1 and barcode2 :
            product1 = get_food_details(barcode1) 
            product2 = get_food_details(barcode2) 
        elif barcode_image1 and barcode_image2 :
                product1 = get_food_details(barcode_image1[0])
                product2 = get_food_details(barcode_image2[0])
        else:
            recommendation = "Aucun code-barre valide n'a été fourni."
            result_label.config(text=recommendation)
            return
        if product1 and product2:

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

    def toggle_input_method(_):
        if input_method_var.get() == "Code-barres manuel":
            entry1.config(state=tk.NORMAL)
            entry2.config(state=tk.NORMAL)
            entry3.config(state=tk.DISABLED)
            entry4.config(state=tk.DISABLED)
            load_image_button.config(state=tk.DISABLED)
        elif input_method_var.get() == "Envoyer une image":
            entry1.config(state=tk.DISABLED)
            entry2.config(state=tk.DISABLED)
            entry3.config(state=tk.NORMAL)
            entry4.config(state=tk.NORMAL)
            load_image_button.config(state=tk.NORMAL)


    window = tk.Tk()
    window.title("Comparaison d'aliments")

    # Création des étiquettes et des champs de texte pour le code-barres manuel
    label1 = tk.Label(window, text="Code-barres du produit 1:")
    label2 = tk.Label(window, text="Code-barres du produit 2:")
    entry1 = tk.Entry(window)
    entry2 = tk.Entry(window)
    label1.pack()
    entry1.pack()
    label2.pack()
    entry2.pack()

    # Création des étiquettes et des champs de texte pour l'envoi d'image
    label3 = tk.Label(window, text="Chemin de l'image du code-barres (produit 1):")
    entry3 = tk.Entry(window)
    label4 = tk.Label(window, text="Chemin de l'image du code-barres (produit 2):")
    entry4 = tk.Entry(window)
    label3.pack()
    entry3.pack()
    label4.pack()
    entry4.pack()

    # Bouton pour charger l'image du code-barres
    load_image_button = tk.Button(window, text="Charger Image", command=load_barcode_image)
    load_image_button.pack()

    # Options pour l'objectif de l'utilisateur
    goal_var = tk.StringVar()
    goal_var.set("Moins de sucres")  # on doit sélectionner une valeur par défaut

    # Sélecteur pour choisir la méthode de saisie
    input_method_var = tk.StringVar()
    input_method_var.set("Code-barres manuel")

    input_method_label = tk.Label(window, text="Choisissez la méthode de saisie:")
    input_method_menu = tk.OptionMenu(window, input_method_var, "Code-barres manuel", "Envoyer une image", command=toggle_input_method)

    goal_label = tk.Label(window, text="Sélectionnez votre objectif:")
    goal_menu = tk.OptionMenu(window, goal_var, "Moins de sucres", "Plus de protéines", "Moins de calories", "Moins de gras", "Plus de fibres")
    compare_button = tk.Button(window, text="Comparer", command=recommend_food)
    result_label = tk.Label(window, text="")
    
    input_method_label.pack()
    input_method_menu.pack()
    goal_label.pack()
    goal_menu.pack()
    compare_button.pack()
    result_label.pack()

    # Démarrer la fenêtre Tkinter
    window.mainloop()


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

# Fonction pour ouvrir la fenêtre de top 5
def open_top5_window():
    # URL de l'API Open Food Facts pour la France
    API_URL = "https://world.openfoodfacts.org/cgi/search.pl"

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

    def recup_produit(cat):
        params = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": cat,
            "countries": "France",
            "json": "1",
            "page_size": 20,  # Vous pouvez augmenter ou diminuer selon vos besoins
        }

        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            data = response.json().get("products", [])
            return data
        return []

    def top_food():
        user_category = category_var.get()
        user_goal = goal_var.get()

        products_list = []

        # Utiliser ThreadPoolExecutor pour paralléliser les requêtes API
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

                # Vérifiez si le produit est unique, appartient à la catégorie 
                if produit_est_unique(product, products_list) and product['Catégorie'] :
                    products_list.append(product)

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
        
        if nutrient_column:
            df[nutrient_column] = pd.to_numeric(df[nutrient_column], errors='coerce')

            df = df.dropna(subset=[nutrient_column])  
            
            
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

            top_5_products = sorted_df.head(5)
            advice = f"Voici les cinq meilleurs produits qui correspondent à votre objectif :"
            for i, products in enumerate(top_5_products.iterrows(), start=1):
                advice += f"\n{i}. {products[1]['Produit']} - {products[1]['Marque']} - {products[1][nutrient_column]}g"

            result_label.config(text=advice)
        else:
            result_label.config(text="Objectif invalide")

    window = tk.Tk()
    window.title("Recommandation d'aliments")

    category_var = tk.StringVar()
    category_var.set("Produits laitiers, Desserts, Fromages")  
    category_label = tk.Label(window, text="Sélectionnez la catégorie d'aliments que vous recherchez :")
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
    
    
# Création de la fenêtre principale
root = tk.Tk()
root.title("Menu Principal")
root.geometry("280x250")  # Vous pouvez ajuster la taille selon vos préférences

# Création du bouton pour ouvrir la fenêtre d'analyse de données
button_data_analysis = tk.Button(root, text="Analyse de données", command=open_data_analysis_window, font=("Helvetica", 14))
button_food_comparison = tk.Button(root, text="Comparaison d'aliments", command=open_food_comparison_window, font=("Helvetica", 14))
button_top5 = tk.Button(root, text="Top 5 d'aliments", command=open_top5_window, font=("Helvetica", 14))

# Utilisez pack ou grid pour organiser les boutons
button_data_analysis.pack(pady=15)
button_food_comparison.pack(pady=15)
button_top5.pack(pady=15)

# Lancer la boucle
root.mainloop()