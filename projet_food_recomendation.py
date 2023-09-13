#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install openfoodfacts


# In[3]:


###### codes tests : 7613036501354 (sel) et 20252281 (poivre)
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


# In[4]:


# Fonction pour obtenir les détails d'un aliment à partir de son code barre
def get_food_details(barcode):
        product = api.product.get(barcode)
        return product


# In[10]:


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
    #energy = float(product['product']['nutriments'].get('energy-kcal_100g', 0))
    #fat = float(product['product']['nutriments'].get('fat_100g', 0))
    #fiber = float(product['product']['nutriments'].get('fiber_100g', 0))
    
    recommendation = ""
    
    
    if user_goal == "Moins de sucres":
        if sugar1 < sugar2:
            recommendation = f"Choisissez le produit {product1['product']['product_name_fr']} qui contient {sugar2-sugar1}g moins de sucre que le produit {product2['product']['product_name_fr']}."
        elif sugar2 < sugar1:
            recommendation = f"Choisissez le produit {product2['product']['product_name_fr']} qui contient {sugar1-sugar2}g moins de sucre que le produit {product1['product']['product_name_fr']}."
        else:
            recommendation = "Les deux produits ont la même teneur en sucres."
    elif user_goal == "Plus de protéines":
        if protein1 > protein2:
            recommendation = f"Choisissez le produit {product1['product']['product_name_fr']} qui contient {protein1-protein2}g plus de protéines que le produit {product2['product']['product_name_fr']}."
        elif protein2 > protein1:
            recommendation = f"Choisissez le produit {product2['product']['product_name_fr']} qui contient {protein2-protein1}g plus de protéines que le produit {product1['product']['product_name_fr']}."
        else:
            recommendation = "Les deux produits ont la même teneur en protéines."

    result_label.config(text=recommendation)


# In[11]:


# Création fenêtre Tkinter
window = tk.Tk()
window.title("Comparaison d'aliments")


# In[12]:



# Création des étiquettes et des champs de texte
label1 = tk.Label(window, text="Code-barres du produit 1:")
label2 = tk.Label(window, text="Code-barres du produit 2:")
entry1 = tk.Entry(window)
entry2 = tk.Entry(window)
label1.pack()
entry1.pack()
label2.pack()
entry2.pack()


# In[13]:


# Options pour l'objectif de l'utilisateur
goal_var = tk.StringVar()
goal_var.set("Moins de sucres")  # on doit sélectionner une valeur par défaut
#réduire les calories/augmenter la teneur en fibres/réduire les Matières grasses
goal_label = tk.Label(window, text="Sélectionnez votre objectif:")
goal_menu = tk.OptionMenu(window, goal_var, "Moins de sucres", "Plus de protéines")
compare_button = tk.Button(window, text="Comparer", command=recommend_food)
result_label = tk.Label(window, text="")
goal_label.pack()
goal_menu.pack()
compare_button.pack()
result_label.pack()


# In[14]:



# Lancer la boucle
window.mainloop()


# In[15]:


product1=get_food_details(3229820019307)
print(product1['product'])


# In[ ]:


5449000214911 coca
5449000214799 coca zero

3229820019307 flocon 
3168930010265 cruesli

