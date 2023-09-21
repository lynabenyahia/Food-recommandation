# -*- coding: utf-8 -*-



###### codes tests : 7613036501354 (arome maggi) et 20252281 (poivre)
import tkinter as tk
from tkinter import messagebox
from openfoodfacts import API, APIVersion, Country, Environment, Flavor
import cv2
from pyzbar.pyzbar import decode

def code_barre(image_path):
    image = cv2.imread(image_path)

    decoded_barcodes = decode(image)

    for barcode in decoded_barcodes:
        barcode_data = barcode.data.decode('utf-8')  # Convertir les données en chaîne de caractères

        print(f"Code-barres: {barcode_data}")

code_barre("/Users/HaksNSH/Documents/GitHub/Food-recommandation/image code barre/coca.jpeg")
code_barre("/Users/HaksNSH/Documents/GitHub/Food-recommandation/image code barre/pepsi.jpeg")
