
# ----------------------------------------------------
#    importation des packages necessaires au projet
# ----------------------------------------------------
import csv
import requests
from bs4 import BeautifulSoup
from math import *
from unecategorieunlivre_beta import extract_book
import pprint

# on initialise url à l'adresse url de la page qu'on veut extraire: une categorie
url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

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

# 1) recuperer le nombre de livres dans la categorie
# 2) definir une liste de tous les liens de livres de cette categorie
# 3) extraire toutes les infos de chaque livre

# 1)  recuperer le nombre de livres dans la categorie
nombrelivres = int(soup.select("strong")[1].text)
print("nombre total de livres", nombrelivres)

# 2) definir une liste de tous les liens des livres de cette categorie
baliseh3 = soup.findAll('h3')
# print("balise h3 : ", baliseh3)
# print("nombre de livres dans la page", len(baliseh3))

nbpage = ceil(nombrelivres/20)
print("nombre de pages de la categorie:", nbpage)


# category : on recupere le nom de la catégorie au niveau du lien de navigation pour les pages suplementaires
links = []
for link in soup.find_all('a'):
    links.append(link.get('href'))
    #print('linsks :',  links)

#print('len links :', len(links))
# print('links :', links)

# on enleve les 3 premiers elements
# print('links[3:]', links[3:])

liens_categories = links[3:]
# on laisse uniquement les 51 premiers elements de la liste
liens_categories = liens_categories[:51]
# print('liens_categories :', liens_categories)


# on recupere le nom de la categorie dans l'url reçue
nom_categorie = url[52:]
# print('nom_categorie -52:', nom_categorie)

# on supprime les derniers caracteres
nom_categorie = nom_categorie[:-11]
print('nom_categorie -4:', nom_categorie)

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
            # print('lien [9]', lien[9:])

            # on rajoute ce lien generique au lien du livre auquel on a enlevé les 9 premiers caractères
            lienslivres.append('https://books.toscrape.com/catalogue/' + lien[9:])
            # print('url 1ère page', url)
            # print(lienslivres)

    else:
        # on recupere les liens des pages suivantes
        urlpsuiv = "https://books.toscrape.com/catalogue/category/books/" + nom_categorie + "/" + "page-" + str(x+1) + ".html"
        print('url page suivante', urlpsuiv)

        reponsesuiv = requests.get(urlpsuiv)
        # print(reponse)
        pagesuiv = reponsesuiv.content  # text sous forme de texte
        soup = BeautifulSoup(pagesuiv, "html.parser")
        baliseh3suiv = soup.findAll('h3')
        # on recherche la balise 'a' dans l'objet soup baliseh3
        for h3suiv in baliseh3suiv:
            asuiv = h3suiv.find('a')
            #print('h3 a page suivante', asuiv)

            # on recherche l'attribut href contenant le lien url
            liensuiv = asuiv['href']
            #print('lien href page suivante', liensuiv)
            lienslivres.append('https://books.toscrape.com/catalogue/' + liensuiv[9:])
            #print('url page suivante', urlpsuiv)

print("liste des liens des livres", lienslivres)
print("len(lienslivres)", len(lienslivres))

url = lienslivres[0]
for url in range(len(lienslivres)):
    url_livre = lienslivres[url]
    print('url_livre : ', url_livre)
    extract_book(url_livre)
