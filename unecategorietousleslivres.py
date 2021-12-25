
# ----------------------------------------------------
#    importation des packages necessaires au projet
# ----------------------------------------------------
import csv
import requests
from bs4 import BeautifulSoup
from math import *
# on initialise url à l'adresse url de la page qu'on veut extraire: une categorie
#url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html' # Categorie Travel 1 page
#url = 'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html'# Categrie Mystery 2 pages
url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html' # 4 pages

# ..... A DEFINIR APRES fonction qui permet d'extraire toutes les données d'un livre
# def extract_book(url_book):

# méthode .get()pour récupérer les données HTML dans la variable reponse
reponse = requests.get(url)
#print(reponse)

page = reponse.content #text sous forme de texte
#print(page)

# on parse le code html obtenu avec la package BeautifulSoup
# A partir de l'objet soup, on obtient des éléments par leur balise, ID ou classe.
# on obtient une liste de tous les elements

soup = BeautifulSoup(page, "html.parser")
#print(soup)

# ----------------------------------------------------
#    RECHERCHE DES INFOS DEMANDEES
#    tous les livres d'une categorie
# ----------------------------------------------------

# 1)  recuperer le nombre de livres dans la categorie
# 2) definir une liste de tous les liens de livres de cette categorie
# 3) extraire toutes les infos de chaque livre

# 1)  recuperer le nombre de livres dans la categorie
nombrelivres = int(soup.select("strong")[1].text)
print("nombre total de livres", nombrelivres)

# 2) definir une liste de tous les liens des livres de cette categorie
baliseh3 = soup.findAll('h3')
#print(baliseh3)
print("nombre de livres dans la page", len(baliseh3))

nbpage = ceil(nombrelivres/20)
print("nombre de pages de la categorie:", nbpage)

# on definit une liste vide des liens de tous les livres de la categorie

lienslivres = []
for x in range(nbpage):
    #print('nbpages', nbpage)
    if x < 1:
        # on recupere les liens de la 1ere page
        for h3 in baliseh3:
            # on recherche la balise 'a' dans la liste baliseh3
            a = h3.find('a')
            # on recherche l'attribut href contenant le lien url
            lien = a['href']
            #print(lien[9:])

            # on rajoute ce lien generique au lien du livre auquel on a enlevé les 9 premiers caractères
            lienslivres.append('https://books.toscrape.com/catalogue/' + lien[9:])
            print('url 1ère page', url)
            print(lienslivres)

    else:
        # on recupere les liens des pages suivantes
        urlpsuiv = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-" + str(x+1) + ".html"
        print('url page suivante', urlpsuiv)

        reponsesuiv = requests.get(urlpsuiv)
        # print(reponse)
        pagesuiv = reponsesuiv.content  # text sous forme de texte
        soup = BeautifulSoup(pagesuiv, "html.parser")
        baliseh3suiv = soup.findAll('h3')
        # on recherche la balise 'a' dans l'objet soup baliseh3
        for h3suiv in baliseh3suiv:
            asuiv = h3suiv.find('a')
            print('h3 a page suivante', asuiv)

            # on recherche l'attribut href contenant le lien url
            liensuiv = asuiv['href']
            print('lien href page suivante', liensuiv)
            lienslivres.append('https://books.toscrape.com/catalogue/' + liensuiv[9:])
            print('url page suivante', urlpsuiv)

            print(lienslivres)


# sauvegarder les images
# sauvegarder
"""
# product_page_url
product_page_url = url
# affiche dans une liste tous les elements délimités par la balise <td>: voir le contenu de soup
description = soup.findAll('td')
#print(description)

# universal_ product_code (upc)
universal_product_code = description[0].text
print(universal_product_code)

# title : titre du livre
title = soup.select("div.product_main>h1")[0].text
print(title)

# price_including_tax
price_including_tax = description[2].text
print(price_including_tax)

# price_excluding_tax
price_excluding_tax = description[3].text
print(price_excluding_tax)

# number_available
number_available = description[5].text
test = number_available.split("(")[1].split()[0]
print(test)

# product_description
product_description = soup.findAll("p")[3].text
print(product_description)

# category : nom de la catégorie au niveau du lien de navigation
category = soup.select("ul.breadcrumb>li>a")[2].text
print(category)

# review_rating
# review_rating = soup.select("p.star-rating")[0].get("class")[-1]
review_rating = soup.select("p.star-rating")[0].get("class")[1]
# print(review_rating)

# conversion de star_rating écrit en lettres en chiffres, ex two = 2 etc
listetoiles = ["One", "Two", "Three", "For", "Five"]
# print("len(listetoiles)", len(listetoiles))

for i in range(len(listetoiles)):
    if listetoiles[i] == review_rating:
       # print("listetoiles[i]",listetoiles[i])
       review_rating = i+1

#print('review_rating converti', review_rating)
print(review_rating)

# image_url : url de l'image du livre
image_url = "http://books.toscrape.com" + soup.img['src'][5:]
print(image_url)


# création du fichier data.csv pour enregistrer toutes les données extraites d'un livre
listecolones = ["Code", "Title", "url", "price_including_tax", "price_excluding_tax", "number_available",
                "product_description", "category", "review_rating", "image_url"]


infos_livre = {"Code": universal_product_code, "Title": title, "url": url, "price_including_tax": price_including_tax,
               "price_excluding_tax": price_excluding_tax, "number_available": number_available,
               "product_description": product_description, "category": category, "review_rating": review_rating,
               "image_url": image_url}
print(infos_livre)

#return infos_livre

with open('unlivreunecat.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=listecolones)
    writer.writeheader()
    # La méthode writerow() est utilisée pour écrire des lignes de données dans le fichier spécifié.
    writer.writerow(infos_livre)
    
"""""
"""""  
field_names = ['No', 'Company', 'Car Model'] 
  
cars = [ 
{'No': 1, 'Company': 'Ferrari', 'Car Model': '488 GTB'}, 
{'No': 2, 'Company': 'Porsche', 'Car Model': '918 Spyder'}, 
{'No': 3, 'Company': 'Bugatti', 'Car Model': 'La Voiture Noire'}, 
{'No': 4, 'Company': 'Rolls Royce', 'Car Model': 'Phantom'}, 
{'No': 5, 'Company': 'BMW', 'Car Model': 'BMW X7'}, ] 
  
with open('Names.csv', 'w') as csvfile: 
    writer = csv.DictWriter(csvfile, fieldnames = field_names) 
    writer.writeheader() 
    writer.writerows(cars) 
    
---------
def save_book_to_csv(liste: list, name: str) -> None:
   
    print(name)
    fichier = name +".csv" 
    for livre in liste:  
        with open(fichier, 'a', newline='', encoding='UTF8') as file:
            writer = csv.DictWriter(file, fieldnames=list(livre.keys()))
            if os.stat(fichier).st_size == 0:
                        # The header is written only if the file is empty
                        writer.writeheader()
            writer.writerow(livre)
-----------------------


# création du fichier data.csv pour enregistrer toutes les données extraite d'un livre
	en_tete = ['titre', 'description']
	with open('data.csv', 'w') as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(en_tete)
		# zip permet d'itérer sur deux listes à la fois
		for titre, description in zip(titre_textes, description_textes):
			writer.writerow([titre, description])

"""

