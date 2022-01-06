
# ----------------------------------------------------
#    importation des packages necessaires au projet
# ----------------------------------------------------
import requests
from bs4 import BeautifulSoup
from unecategorietousleslivres import extract_all_books_one_cat

# on initialise url à l'adresse du site :
url = 'https://books.toscrape.com/index.html'

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

# ------------------------------------------------------------------------------
#    RECHERCHE DE TOUTES LES INFOS DE TOUS LES LIVRES DANS TOUTES LES CATEGORIES
# ------------------------------------------------------------------------------
# 1) recuperer le Lien de chaque catégorie
# 2) stocker tous ces liens dans une liste
# 3) appeler le programme unecategorietousleslivres.py et extraire le contenu du site entier

# 1) recuperer le Lien de chaque catégorie
# on enleve les 2 premiers elements de la liste
lien_categorie = soup.select("li>a")[2:]
# print("lien_categorie : ", lien_categorie)

# 2) stocker tous ces liens des categories dans une liste
links = []
for link in lien_categorie:
    links.append(link.get('href'))
   # print('links :',  links)

links = links[:-1]
# print('len (links_total)', len(links))
# print('links_total :',  links)

# reconstitution de l'url complete de chaque categorie
for k in range(len(links)):
        links[k] = 'https://books.toscrape.com/' + links[k]
        # print(links[k])
print('Liste de liens des categories:', links)


# 3) appeler le programme unecategorietousleslivres.py et extraire le contenu du site entier
urlcat = links[0]
for urlcat in range(len(links)):
    urlcat = links[urlcat]
    print('url_cat : ', urlcat)
    extract_all_books_one_cat(urlcat)