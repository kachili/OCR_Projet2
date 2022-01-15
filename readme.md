
Pour lancer les scripts de ce projet, vous avez besoin de créer un environnement virtuel.
ETAPES: 
Création du répertoire projet2 : mkdir projet2
On se met au niveau du répertoire projet2 : cd projet2
On crée un environnement virtuel pour ce projet : 
On tape la commande : python -m venv venv
On vérifie que le répertoire env est bien crée : 
On tape la commande dir 
On obtient  ==> venv

On procède à l'activation de l'environnement virtuel env par la commande :
On tape la commande : venv\Scripts\activate
On obtient  ==> (env) C:\...\projet2

EXECUTION DES SCRIPTS
Remarque : 
les 3 Scripts peuvent étres lancés soit par la ligne de commande soit directement dans l'éditeur Pycharm.

1er script : unecategorieunlivre.py 
Lancer la commande : 
python unecategorieunlivre.py https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html

Le parametre passé au Script est le lien du livre «It's Only the Himalayas » de la catégorie « Travel »
--> Vous pouvez choisir n'importe quelle lien url d'un livre de n'importe quelle categorie.
Résultat :
Un fichier «Travel.csv » est créé avec les informations du livre.
Un répertoire «Travel_images » est créé avec l’image du livre.
 
2ème script : unecategorietousleslivres.py
Lancer la commande : 
python unecategorietousleslivres.py https://books.toscrape.com/catalogue/category/books/travel_2/index.html

Le parametre passé au Script est le lien url de la catégorie "travel"
Résultat :
Un fichier «Travel.csv » est créé avec les informations de tous les livres de cette catégorie.
Un répertoire «Travel_images » est créé avec l’ensemble des images des livres de la catégorie.
--> Vous pouvez choisir n'importe quelle lien url d'une autre catégorie du site.
 
3ème script : toutescategoriestouslivres.py
Lancer la commande : 
python toutescategriestouslivres.py https://books.toscrape.com/index.html

Le parametre passé est le lien url du site books.toscrape.com

Il extrait toutes les informations de tous les livres de toutes les catégories. 

Résultat :
Un fichier «nomdelacategorie.csv » est créé avec les informations de tous les livres pour chaque categorie.
Un répertoire «nomdelacategorie _images » est créé avec l’ensemble des images des livres pour chaque categorie.
