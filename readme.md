
Pour lancer les scripts de ce projet, vous avez besoin de créer un environnement virtuel.
ETAPES: 
Création du répertoire projet2 : mkdir projet2
On se met au niveau du répertoire projet2 : cd projet2
On crée un environnement virtuel pour ce projet : 
On tape la commande : python -m venv env
On vérifie que le répertoire env est bien crée : 
On tape la commande dir 
On obtient  ==> env

On procède à l'activation de l'environnement virtuel env par la commande :
On tape la commande : env\Scripts\activate
On obtient  ==> (env) C:\...\projet2

Pour installer les packages spécifiques à ce projet, taper la commande suivante : 
pip install -r requirements.txt

EXECUTION DES SCRIPTS
Remarque : 
les 3 Scripts peuvent être lancés soit par la ligne de commande soit directement dans l'éditeur Pycharm.

1er script : unecategorieunlivre.py 
Lancer la commande : 
python unecategorieunlivre.py https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html

Le paramètre passé au Script est le lien du livre «It's Only the Himalayas » de la catégorie « Travel »
--> Vous pouvez choisir n'importe quel lien url d'un livre de n'importe quelle catégorie.
Résultat :
Un répertoire «Projet2_data » est créé contenant un fichier «Projet2_data.csv» avec les informations du livre.
Un répertoire «Projet2_images » est créé contenant l’image du livre.
 
2ème script : unecategorietousleslivres.py
Lancer la commande : 
python unecategorietousleslivres.py https://books.toscrape.com/catalogue/category/books/travel_2/index.html

Le paramètre passé au Script est le lien url de la catégorie "travel"
Résultat :
Un répertoire «Projet2_data » est créé contenant un fichier «Projet2_data.csv» avec les informations de tous les livres de la catégorie.
Un répertoire «Projet2_images » est créé contenant les images de tous les livres de la catégorie.
--> Vous pouvez choisir n'importe quel lien url d'une autre catégorie du site.


3ème script : toutescategoriestouslivres.py
Lancer la commande : 
python toutescategriestouslivres.py https://books.toscrape.com/index.html

Le paramètre passé est le lien url du site books.toscrape.com

Il extrait toutes les informations de tous les livres de toutes les catégories. 

Résultat :
Un répertoire «Projet2_data » est créé contenant un fichier «Projet2_data.csv» avec les informations de tous les livres de toutes les catégories.
Un répertoire «Projet2_images » est créé contenant les images de tous les livres de toutes les catégories.

Lien Github pour les Scripts, le fichier readme.md et le fichier requirements.txt
https://github.com/kachili/ocr_projet2
