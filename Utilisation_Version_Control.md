Utilisation du version Control
Le contrôle de version est un système qui permet de suivre et de gérer les changements apportés à un fichier ou à un projet entier. Il permet de garder une trace de toutes les modifications sous forme de « commits », chaque commit étant accompagné d'un message décrivant la modification. Cela permet de savoir précisément ce qui a été modifié, quand, et par qui.
Dans le cadre d'un projet impliquant plusieurs développeurs, un système de contrôle de version est essentiel pour que chacun puisse apporter des modifications sans risquer de perdre des changements ou créer des conflits. Chaque développeur travaille sur sa propre copie du projet, puis les modifications peuvent être fusionnées dans le projet principal, tout en conservant la traçabilité des modifications, ce qui est utile en cas de problème.
En cas de difficulté, il est possible d'accéder à l'historique des versions pour récupérer une version antérieure ou la comparer avec la version actuelle afin de trouver l'erreur et analyser l'évolution du projet.
En résumé
Le contrôle de version est un système permettant de faire évoluer un projet principal (« master ») tout en effectuant des modifications sur des branches séparées. Chaque version peut ensuite être vérifiée avant d'être fusionnée avec le projet principal.
 
Création d’un contrôle de version dans un projet python, C++, C#...
•	Instalation de Git
  o	Instaler Git depuis le site git-scm.com
•	Initialiser un dépôt dans le dossier cible
  o	Terminal windows 
      •	cd C:\Chemin\Vers\Le\Dossier\cible
      •	git init
  o	Git bash
      •	cd /c/Chemin/Vers/Le/Dossier/cible
      •	git init
•	Choisir les fichier a suivre
    	Pour ajouter tout les fichier présent dans le dossier dans le version control
      •	git add .
    	Pour ajouter un fichier spécifique du dossier
      •	git add Nom_Du_Fichier.py
•	Faire un premier commit
    	Enregistrer l’état initial de votre projet
      •	git commit -m "Initial commit"
•	ajouter un dépot distant comme GitHub (facultatif)
  o	sur GitHub
      •	créer un nouveau dépôt / reposistory sans fichier README
      •	copier l’URL du dépôt
  o	Dans l’invite de commande / terminal
    	Ajouter l’URL du dépôt distant
      •	git remote add origin https://github.com/username/nom_du_depot.git
      •	pousser votre projet vers le dépôt distant
      •	Git push -u origin master
•	Faire réguliarement des commit
•	Si besoin pousser les modif vers le dépôt distant

 
Autres fonctionalités individuelles
•	Connection au dossier l’ouverture de l’indice de commande ou du git bash
  o	Terminal windows 
      •	cd C:\Chemin\Vers\Le\Dossier\cible
  o	Git bash
      •	cd /c/Chemin/Vers/Le/Dossier/cible
•	Travail avec dépôt distant
    	Nouveau commit/sauvegarde
      •	git add . ou git add Nom_Du_Fichier
      •	git commit -m "Description des changements"
    	pousser les sauvegardes vers le dépôt distant
      •	git push origin Nom_De_La_Branche
    	Mettre a jour votre dépôt local depuis le dépôt distant
      •	git pull ou git pull Nom_De_La_Branche
•	Travail avec des branches séparées
    	Créer une nouvelle branche 
      •	git checkout -b Nom_De_La_Branche
    	pousser une autre branche
      •	git push origin Nom_De_La_Branche
    	fusioner la branche avec le main
      •	git checkout main
      •	git merge Nom_De_La_Branche
      •	git push
•	Vérifications
    	voir l’historique de modifications
      •	git log
    	vérifier l’état du dépôt 
      •	git status
