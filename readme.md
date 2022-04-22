# electors-recognizer-django

Notre machine prendra une image faciale en entrée de chaque électeur à l’aide d’un système de reconnaissance faciale basé sur un CNN profond avec alignement des visages Dlib, la vérifie avec un ensemble d’images faciales des électeurs enregistrés dans la base de données qui ont été prise lors de la phase pré-électorale, le résultat étant positif suppose qu’il peut voter pour un candidat. Après le vote, le système confirme le vote par ré-capture de l’image faciale du votant et il lui délivre un court message texte, ce qui garantit qu’il ne vote qu’une seul fois.

Notre projet est divisé en deux projets:
-electors-recognizer-django
-electors-recognizer-vuejs

pour exécuter ces projets vous devez installer un SGBD en particulier posgresql (pgadmin4). ENsuite chaque projet possède son readme et son fichier requirement qui vous donnera plus d'informations sur les dépendances et la manière d'exécuter.

installer l'environnement :
-Python 3.8.5
-postgreSQL11
-git
-installer npm
-Dans chaque projet, ouvrez le terminal, créer un environnement virtuel avec la commande python -m venv c:\path\to\myenv 
	activer cette environnement (par exemple venv\Scripts\activate) et installer les packages: pip install to-requirements.txt





les étapes de démarage:
-premièrement Ouvrez le terminal, Démarrer ensuite l'exécutable dans le projet elector-recognizer-django(lisez le fichier readme):
---activer cette environnement (par la commande venv\Scripts\activate) si elle ne l'ai pas encore
--- et enfin coler cette commande "python manage.py runserver"
- deuxièmement demarrer ensuite pgadmin4
-troisièmement demarrer enfin l'exécutable dans le projet elector-recognizer-vuejs: 
ouvrez un autre terminal: accéder au dossier du projet elector-recognizer-vuejs par la commande cd /chemin_du dossier
ensuite taper les commandes successives  pour la prmière utilisation : npm run serve ; npm run build ; npm run lint; mais pour la seconde utilisation tapez uniquement la commande npm run serve
et enfin ouvrez lz navigateur à l'adresse: http://localhost:8085/
