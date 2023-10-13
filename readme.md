# electors-recognizer-django

Our machine takes an input facial image of each voter using a deep CNN-based facial recognition system with Dlib face alignment, checks it against a set of facial images of voters registered in the database that were taken during the pre-election phase, the result being positive implies that he can vote for a candidate. After the vote has been cast, the system confirms the vote by re-capturing the voter's facial image and delivering a short text message, ensuring that the voter only votes once.

Our project is divided into two parts:
-electors-recognizer-django
-electors-recognizer-vuejs

to run these projects, you need to install a specific DBMS, posgresql (pgadmin4). Then each project has its own readme and requirement file, which will give you more information on dependencies and how to run it.

install the :
-Python 3.8.5
-postgreSQL11
-git
-install npm
-In each project, open the terminal and create a virtual environment with the command python -m venv c:\path\to\myenv 
	activate this environment (for example venv\Scripts\activate) and install packages: pip install to-requirements.txt





start-up steps:
-first open the terminal, then start the executable in the elector-recognizer-django project (read the readme file):
---activate this environment (with the command venv\Scripts\activate) if it hasn't already
--- and then paste this command "python manage.py runserver"
- secondly, start pgadmin4
-thirdly, start the executable in the elector-recognizer-vuejs project: 
open another terminal: access the elector-recognizer-vuejs project folder with the command cd /path_offolder
then type the following commands for the first use: npm run serve; npm run build; npm run lint; but for the second use type only the command npm run serve
and finally open the browser at: http://localhost:8085/
