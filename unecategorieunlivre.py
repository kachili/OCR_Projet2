
# ----------------------------------------------------
#    importation des packages necessaires au projet
# ----------------------------------------------------
import csv
import requests
from bs4 import BeautifulSoup

# on initialise url à l'adresse url de la page qu'on veut extraire
url = 'https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html'

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
# print(soup)

# ----------------------------------------------------
#    RECHERCHE DES INFOS DEMANDEES
# ----------------------------------------------------

"""
product_page_url
universal_ product_code (upc)
title
price_including_tax
price_excluding_tax
number_available
product_description
category
review_rating
image_url
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

"""        
------------------------------
import csv 
  
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
"""