# Stand-up meeting du 27 juillet 2022.
Paul et Quentin.

## 1 Qu'ai je fais hier ?
* Paul: j'ai recherché dans la documentation comment rendre accessible jenkins sur son adresse, j'ai trouver comme solution d'utiliser une serveur ngnix comme proxy pass pour rediriger les requetes web vers le 127.0.0.1:8080 pour jenkins. J'ai recherché comment modifier le fichier default de ngnix en ligne de commande en utilisant une commande sed qui ajoute la redirection au bon endroit dans le fichier. J'ai trouver comment activier jenkins directement en ligne de commande sans passer par son interface web et installer les modules de jenkins directement en ligne de commande.
* Quentin: Correction d'un probleme de nom de domaine, je devais le changer car trop d'utilisation pour certbot, du coup j'ai script le changement dans les fichiers de config et le script pour la prise en charge de l'argument de la commande de mon script.


## 2 Que vais je faire aujourd'hui ?
* Paul: Consolider le script et le tester, vérifier les commande de configuration ngnix et jenkins. Ajouter les utilisateurs.
* Quentin: Consolider le script, régler mon probléme avec le tunnel qui ne fonctionne pas de temps en temps, préparé les livrables.

## 3 Quels problèmes je rencontre ?
* Paul: je me suis largement perdu dans les différentes docs avant de trouver la solution.
* Quentin: Fatigue.
