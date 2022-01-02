# ----------------------------------------------------
#    importation des packages necessaires au projet
# ----------------------------------------------------
import csv
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import shutil

# on initialise url à l'adresse url de la page qu'on veut extraire

# cas où larubrqiue Description n'existe pas dans la page web (categorie :Default / livre : the-bridge-to-consciousness)# urlbook = 'https://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge-between-science-and-our-old-and-new-beliefs_840/index.html'
# urlbook = 'https://books.toscrape.com/catalogue/a-murder-in-time_877/index.html'
# urlbook = 'https://books.toscrape.com/catalogue/logan-kade-fallen-crest-high-55_384/index.html'
# urlbook = 'https://books.toscrape.com/catalogue/robin-war_730/index.html' # pb avec encodage ANSI



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

    # ----------------------------------------------------
    #    RECHERCHE DES INFOS DEMANDEES
    # ----------------------------------------------------

    # product_page_url
    product_page_url = urlbook

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
    number_available = number_available.split("(")[1].split()[0]
    # print('number_available', number_available)

    # ------------------------------------------------------------------------------
    # ammelioration de product_description
    product_description = soup.findAll("p")[3].text  # original
    # print('product_description:', product_description)

    product_description = product_description.replace(';', ',')
    # print('product_description:', product_description)

    # string.replace(oldStr, newStr, count) -on remplace les \n par 'X' dans le cas où la rubrique
    # product_description n'existe pas.
    new_product_description = product_description.replace('\n', '==')
    product_description = new_product_description
    # print('new_product_description:', product_description)
    # ------------------------------------------------------------------------------

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
    # image_livre = soup.ima['src']
    # image_livre = soup.findAll("img.src")
    # print("image_livre", image_livre)

    image_url = "http://books.toscrape.com" + soup.img['src'][5:]
    # print("image_url :", image_url)
    # init de info_livress
    infos_livre = {}

    # création du fichier data.csv pour enregistrer toutes les données extraites d'un livre

    infos_livre = {"Code": universal_product_code, "Title": title, "url": urlbook, "price_including_tax":
                price_including_tax, "price_excluding_tax": price_excluding_tax, "number_available": number_available,
                "product_description": product_description, "category": category, "review_rating": review_rating,
                "image_url": image_url}

    # print(infos_livre)

    # appel de la fonction
    # listecolones = extract_book(urlbook)
    print("Dictionnaire:", infos_livre)

    # sauvegarde de l'image à partir du site
    # on recupere le nom de l'image (qui prend le nom du livre)
    # on recupre le nom de la categorie pour créer un dossier qui contiendra les images

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

    titre_image = nom_livre + '_' + urlimage.split("/")[-1]
    # print("titre de l'image split:", titre_image)

    fichier_image_recupere = urllib.request.urlretrieve(urlimage, titre_image)
    # print("print IMAGE: ", IMAGE)

    # création d'un dossier qui aura le nom de la categorie
    nom_dossier = infos_livre["category"] + "_images"

    # si le dossier n'existe pa, on le crée
    if not os.path.exists(nom_dossier):
        os.mkdir(nom_dossier)

    if os.path.exists(nom_dossier):
        path = os.path.abspath(nom_dossier)
        filedest = os.path.join(path, titre_image)
        # Déplacer un fichier du répertoire rep1 vers rep2
        shutil.move(titre_image, filedest)

    nom_fichier = category + ".csv"
    # print('nom_fichier ecriture: ', nom_fichier)

    # with open(nom_fichier, 'a', newline='', encoding='UTF8') as csvfile:
    # with open(nom_fichier, 'a', newline='', encoding='ANSI') as csvfile:
    # with open(nom_fichier, 'a', newline='', encoding='UTF-16LE') as csvfile:
    with open(nom_fichier, 'a', newline='', encoding='UTF-16') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=infos_livre)

        if os.stat(nom_fichier).st_size == 0:
            # The header is written only if the file is empty
            writer.writeheader()
        # La méthode writerow() est utilisée pour écrire des lignes de données dans le fichier spécifié.
        writer.writerow(infos_livre)
# extract_book(urlbook)
