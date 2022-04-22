# electors-recognizer-django

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
ensuite tapper la commande  npm run serve
et enfin ouvrez lz navigateur à l'adresse: http://localhost:8085/
