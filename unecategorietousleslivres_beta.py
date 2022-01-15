
# ----------------------------------------------------
#    importation des packages necessaires au projet
# ----------------------------------------------------
import sys
import requests
from bs4 import BeautifulSoup
from math import *
from unecategorieunlivre_beta import extract_book

# Script unecategorietousleslivres avec la ligne de commande avec une url comme parametre
if len(sys.argv) > 1 and sys.argv[0] == 'unecategorietousleslivres_beta.py':
    url = sys.argv[1]
else: # Script unecategorietousleslivres lancé avec Pycharm
    if sys.argv[0][-33:] == 'unecategorietousleslivres_beta.py':
        # print('sys.argv[0][-33:] : ', sys.argv[0][-33:])
        url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'

def extract_all_books_one_cat(url: str) :
    # méthode .get()pour récupérer les données HTML dans la variable reponse
    reponse = requests.get(url)
    #print(reponse)

    page = reponse.content #text sous forme de texte
    # print(page)

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

    # nom_categorie est une sous-chaine de la chaine contenant l'url
    # en enlenvant les 52 premiers et les 11 derniers caractères
    nom_categorie = url[52:-11]
    print('Nom categorie :', nom_categorie)

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
            # print('url page suivante', urlpsuiv)

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

    # print("liste des liens des livres", lienslivres)
    print("taille liste de liens de livres : ", len(lienslivres))

    for url in range(len(lienslivres)):
        url_livre = lienslivres[url]
        # print('url_livre : ', url_livre)
        extract_book(url_livre)

if sys.argv[0][-33:] == 'unecategorietousleslivres_beta.py':
    extract_all_books_one_cat(url)