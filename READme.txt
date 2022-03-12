ce projet est réalisé par reda merbah

les Bibliothèques que j'ai utilisé utilisées :

-time
-sqlite3
-pygal
-datetype
-flask

a propos les fonctionalité :
	j'ai collecté les informations sur le système qui sont décrit dans l'énoncé : 
		-la Ram utilisé par chaque user
		-stockage
		-cpu

pour avoire tous ces information j'ai fait une boucle qui commence de 1 jusqu'a le nombre des utilisateurs ($usercount)

tous ces informations sont stocké dans une base de donneé (sqlite3 monitor.db)
pour la gestion d'historique j'archive tous les fichier creer.csv chaque 24h et je supprime les anciens

a propos de Fonctionnement :

pour fair collecter les information et les stocker dans la base de donnée et la de tester l'utilisateur si il a dépasser la ram et cpu ou pas 
il faut juste lancer le scriptBash.sh sur la crontab avec une durré de 5 min
crontab -e 
*/5 * * * * bash /home/reda/MiniProjet/scriptBash.sh 
et pour l'archivache

23 59 * * * bash /home/reda/MiniProjet/archive.sh

et pour la suppression des anciens fichier.csv

23 59 * * * bash /home/reda/MiniProjet/scriptTest.sh
pour la  détection de situation de crise j'ai fait un teste qui teste si l'utilisateur x a dépasser la ram ou cpu il envoie un mail accompagné d'un graphe 
pour le quel si utilisateur a dépasser la ram il envoie dans le mail juste que ce utilisateur a depasser la ram +le graphe sans envoyer le mail qui conserne cpu et vice versa
sinon si l'utilisateur a dépasser la ram et cpu il envoie tout les deux mail.

le module d'envoie de ce mail il envoie un texte de détéction accompagné d'un graphe 

pour la partie d'affichage j'ai creer 4 graphe (historique de 24h  12h  6h  1h)
je prend tous les informatons de chaque utilisateur et je les affiche sous forme d'un graphe en couleur et interactif

le fonctionement de la partie 4 j'ai afficher l'ensemble des derrnier informations collecter pour chaque utilisateur a chaque fois la cronetab exécute le scriptBash.sh
tous les information ce change on actualise la page 
dans cette interface j'ai afficher l'historique d'utilisation dans 6h pour chaque utilisateur sous forme d'un graphe interactif et d'un diagramme serculaire et aussi il y a un lien 
pour afficher les dérrnier mise a jour d'utilisation de chaque utilisateur   








