# ----------------------------------------------------
#    importation des packages necessaires au projet
# ----------------------------------------------------
import csv
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import sys
from pprint import pprint

# Script unecategorieunlivre lancé avec la ligne de commande avec une url comme parametre
if len(sys.argv) > 1 and sys.argv[0] == 'unecategorieunlivre.py':
    urlbook = sys.argv[1]

else: # Script unecategorieunlivre lancé avec Pycharm
    # print('syargvsplit :', sys.argv[0].split("/")[-1])
    if sys.argv[0].split("/")[-1] == 'unecategorieunlivre.py':
        urlbook = 'https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html'

# ----------------------------------------------------
# fonction d'extraction d'informations pour un livre
# ----------------------------------------------------
def extract_book(urlbook: str):
    reponse = requests.get(urlbook)
    # print(reponse)

    page = reponse.content
    # print(page)

    # on parse le code html obtenu avec la package BeautifulSoup
    # A partir de l'objet soup, on obtient des éléments par leurs balises, ID ou classes.
    # on obtient l'objet soup de type liste contenant tous les elements

    soup = BeautifulSoup(page, "html.parser")
    # print(soup)

    # ---------------------------------------------------------
    #    EXTRACTION DES INFORMATIONS D'UN LIVRE D'UNE CATEGORIE
    # ----------------------------------------------------------

    # product_page_url
    # product_page_url = urlbook

    # affiche dans une liste tous les elements délimités par la balise <td>: voir le contenu de soup
    description = soup.findAll('td')
    # print(description)

    # universal_ product_code (upc)
    universal_product_code = description[0].text
    # print(universal_product_code)

    # title : titre du livre
    title = soup.select("div.product_main>h1")[0].text
    # print(title)

    # price_including_tax
    price_including_tax = description[2].text
    # print('price_including_tax:', price_including_tax)

    # price_excluding_tax
    price_excluding_tax = description[3].text
    # print('price_excluding_tax: ', price_excluding_tax)

    # number_available
    number_available = description[5].text
    # print('number_available : ', number_available)
    number_available = number_available.split("(")[1].split()[0]
    # print('number_available', number_available)

    # Recherche de toutes les balises 'p' pour extraire product_description
    # On garde le format text en remplaçant les ';' par ',' et les '\n' par '-' dans le cas où ce champs n'existe pas.
    # dans ce dernier cas, on laisse quand meme ce champs à '---' pourqu'il apparaisse dans le fichier csv

    product_description = soup.findAll("p")[3].text.replace(';', ',').replace('\n', '-')
    # print('product_description:', product_description)

    # category : nom de la catégorie au niveau du lien de navigation
    category = soup.select("ul.breadcrumb>li>a")[2].text
    # print('category :', category)

    # review_rating
    review_rating = soup.select("p.star-rating")[0].get("class")[1]
    # print('review_rating', review_rating)

    # conversion de star_rating écrit en lettres en chiffres, ex two = 2 etc
    listetoiles = ["One", "Two", "Three", "Four", "Five"]
    # print("len(listetoiles)", len(listetoiles))

    for i in range(len(listetoiles)):
        if listetoiles[i] == review_rating:
            # print("listetoiles[i]",listetoiles[i])
            review_rating = i + 1

    # print('review_rating converti', review_rating)
    # print('review rating: ', review_rating)

    # image_url : url de l'image du livre
    # on reconstitue l'url de l'image
    image_url = "http://books.toscrape.com" + soup.img['src'][5:]
    # print("image_url :", image_url)

    # dictionnaire contenant les infos demandées
    infos_livre = {"Code": universal_product_code, "Title": title, "url": urlbook, "price_including_tax":
                price_including_tax, "price_excluding_tax": price_excluding_tax, "number_available": number_available,
                "product_description": product_description, "category": category, "review_rating": review_rating,
                "image_url": image_url}

    # pprint(infos_livre)
    # print('Infos livre: ', infos_livre)

    # sauvegarde de l'image à partir du site
    # on recupere l'url de l'image
    urlimage = infos_livre["image_url"]
    # print("url de l'image: ", urlimage)

    # nom de l'image = nom du livre
    nom_livre = infos_livre["Title"]
    # print("nom du livre : ", nom_livre)

    # on enleve les caracteres speciaux des titres ? : ! pour generer un nom d'image correct
    new_string = ''.join(filter(str.isalnum, nom_livre))
    # print('titre du livre sans les carac speciaux: ', new_string)
    nom_livre = new_string

    # -----------------------------------------------------------------------
    # création de deux dossiers Dossier_image et Dossier_data
    # qui contiendront toutes les images et le fichier de données
    # -----------------------------------------------------------------------

    # ---------------
    # Dossier images
    # ---------------
    dossier_images = "Projet2_images"

    # si le dossier n'existe pas, on le crée
    if not os.path.exists(dossier_images):
        os.mkdir(dossier_images)

    if os.path.exists(dossier_images):
        path = os.path.abspath(dossier_images)
        os.chdir(path)
        titre_image = nom_livre + '_' + urlimage.split("/")[-1]
        # print("titre de l'image split:", titre_image)
        urllib.request.urlretrieve(urlimage, titre_image)
        # print("Nom de l image: ", titre_image)
        os.chdir('..')

    # ---------------
    # Dossier data :
    # ---------------
    dossier_data = "Projet2_data"
    if not os.path.exists(dossier_data):
        os.mkdir(dossier_data)

    if os.path.exists(dossier_data):
        path = os.path.abspath(dossier_data)
        os.chdir(path)
        nom_fichier = "Projet2_Data.csv"
        # nom_fichier = "Projet2_Data.uos"

        # On utilise l'encodage 16 bits pour éliminer les caractères spéciaux lors lors de l'ecriture dans csvfile
        label = ["Code", "Title", "url", "price_including_tax", "price_excluding_tax", "number_available",
                 "product_description", "category", "review_rating", "image_url"]

        with open(nom_fichier, 'a', newline='', encoding='UTF8') as file:
            writer = csv.DictWriter(file, fieldnames=label)

            if os.stat(nom_fichier).st_size == 0:
                # L'en-tête n'est écrit que si le fichier est vide
                writer.writeheader()
            # La méthode writerow() est utilisée pour écrire des lignes de données dans le fichier spécifié.
            writer.writerow(infos_livre)

            # for elem in infos_livre:
            #   writer.writerow(elem)

        os.chdir('..')

if sys.argv[0].split("/")[-1] == 'unecategorieunlivre.py':
   extract_book(urlbook)
