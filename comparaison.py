# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
from openfoodfacts import API, APIVersion, Country, Environment, Flavor
import cv2
from pyzbar.pyzbar import decode

def open_food_comparison_window():
    # Connexion à l'api
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
    
        return barcode_data_list  # Retourner la liste des codes-barres

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
        
     # dans le cas où on a des erreurs...

        if not barcode_image1 or not barcode_image2:
            recommendation = "Aucun code-barre valide n'a été trouvé dans les images fournies."
            result_label.config(text=recommendation)
            return


    def recommend_food():
        global barcode_image1, barcode_image2 
        barcode1 = entry1.get()
        barcode2 = entry2.get()
        user_goal = goal_var.get()

# vérification et stockage des codes barres
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
        
        # Récupération des valeurs demandées
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
        # Recommandations en fonction des différents scénarios
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

# Fonction pour choisir parmi les deux options de code barres ("_" important sinon erreur)
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
    label1 = tk.Label(window, text="Code-barres du produit 1 :")
    label2 = tk.Label(window, text="Code-barres du produit 2 :")
    entry1 = tk.Entry(window)
    entry2 = tk.Entry(window)
    label1.pack()
    entry1.pack()
    label2.pack()
    entry2.pack()

    # Création des étiquettes et des champs de texte pour l'envoi d'image
    label3 = tk.Label(window, text="Chemin de l'image du code-barres (produit 1) :")
    entry3 = tk.Entry(window)
    label4 = tk.Label(window, text="Chemin de l'image du code-barres (produit 2) :")
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

    input_method_label = tk.Label(window, text="Choisissez la méthode de saisie :")
    input_method_menu = tk.OptionMenu(window, input_method_var, "Code-barres manuel", "Envoyer une image", command=toggle_input_method)

    goal_label = tk.Label(window, text="Sélectionnez votre objectif :")
    goal_menu = tk.OptionMenu(window, goal_var, "Moins de sucres", "Plus de protéines", "Moins de calories", "Moins de gras", "Plus de fibres")
    compare_button = tk.Button(window, text="Comparer", command=recommend_food)
    result_label = tk.Label(window, text="")
    
    # Lancement des  instances
    input_method_label.pack()
    input_method_menu.pack()
    goal_label.pack()
    goal_menu.pack()
    compare_button.pack()
    result_label.pack()

    # Démarrer la fenêtre Tkinter
    window.mainloop()

