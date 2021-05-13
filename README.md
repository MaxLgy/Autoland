# Autoland
vidéo à récupérer pour voir les étapes d'avancement
https://drive.google.com/file/d/1b7YXzXZivvZNM_Xcs4f1uyjZCCxyZShl/view?usp=sharing

Mise en fonctionnement du drone et du  docking : 

Mise en place Navcam : 

![branchement_na](https://github.com/MaxLgy/Autoland/blob/main/images/branchement_Navcam.png)
Définissez l'adresse IP de l'ordinateur portable pour qu'elle soit compatible avec la configuration réseau du Nav Cam (par défaut 192.168.1.x avec x entre 150 et 250, le masque de sous-réseau étant 255.255.255.0). Ouvrez Google Chrome sur l'ordinateur portable et saisissez l'adresse IP du Nav Cam dans l'entrée URL (par défaut 192.168.1.85).

![page_démarrage](https://github.com/MaxLgy/Autoland/blob/main/images/page_demarrage.png)

Appuyez ensuite sur les touches ctrl + shift + R pour vider le cache du navigateur. Cliquez ensuite sur Marker Settings (bouton en haut à gauche).

![choix_marker](https://github.com/MaxLgy/Autoland/blob/main/images/choix_marker.png)

Sélectionnez ensuite la bonne famille de marqueurs et placez un marqueur dans le champ de vision de la caméra. Vous pouvez utiliser un des marqueur dans le dossier /image. Assurez-vous que le marqueur est plat, vous pouvez le coller sur une surface plane, et assurez-vous que rien ne masque les points. Une fois cela fait, vous devriez voir l'ID du marqueur détecté (sur l'image précédente, c'est l'ID 1), alors entrez cet ID tel qu'il est écrit (ne tapez pas 001 par exemple), et entrez la taille du carré noir du marqueur en millimètres. Cliquez ensuite sur Ajouter et revenez à l'écran principal, vous devriez voir une représentation du marqueur et les données affichées dans l'onglet en bas à droite. Sélectionner le mode Air au lieu du mode Eau.

Mise en place Drone : 

1. Allumer le drone en appuyant sur son bouton latéral (et unique bouton)
2. Se connecter sur le wifi généré par le drone (TelloXXXX) 
3. Lancer le code python : examples/Threads.py : c'est le fichier qui contient notre main (fonction d'entrée de notre code)
