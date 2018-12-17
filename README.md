# Le fantome de l'opera
Projet d'IA - Epitech tech 5 - Introduction a l'intelligence artificielle

## Contributeur:
Pierre-Marie Danieau (pierre-marie.danieau@epitech.eu)
Simon Bertho (simon.bertho@epitech.eu)
Maxence Plou (maxence.plou@epitech.eu)
Paul-Emmanuel Berte (paul-emmanuel.berte@epitech.eu)

## Architecture
Notre IA est ploymorphe (elle peut autant jouer le fantome que l'inspecteur).
Base sur un joueur id elle genere un arbre avec une heurisitique en fonction de ce joueur id. La generation de l'arbre se fait en fonction des personnages, puis des salles disponible pour le personnages et enfin l'activation (ou non) du pouvoir du personnage.

L'heuristique est calculee en fonction du nombre de personne en groupe ou seul et en fonction de leur etat (suspect ou non-suspect).
Le scope de point varie entre 0 et 8. Pour le fantome le score le plus bas est le meilleur et vice versa pour l'inspecteur.

### L'arbre
Notre arbre (tree.py) s'articule autour de noeux (node.py) qui represente un seul mouvement. Cet arbre dispose d'une reference sur sa racine a tout moment pour revenir au debut.

- La generation : La generation n'est pas optimise par manque de temps. Cependant un trie des noeux sur l'heuristique est fait pour gagner du temps sur la selection des noeux. La generation est procedurale et genere toutes les actions possibles sur une profondeur d'un enfant.

### Les noeux
Les noeux disposent d'une liste d'enfants, d'une heuristique ainsi que la couleur du personnage joue.

### Les personnages
Les personnages (character.py) sont stockes dans une classe disposant d'un enum (Color), d'une position (0 - 9) et un status (suspect ou non-suspect).

## Le parser d'info
Le parser d'info (info_parser.py) est un element cle pour la conprehension de l'etat du jeu ainsi que les etapes suivantes. Bien que peu pousse sur les differents type de question, il permet la creation et la generation de l'arbre. Il permet aussi de mettre a jour l'arbre.

# Piste d'ameliorations et optimisations
Afin de pouvoir generer des reponses plus rapide et plus intelligente, une grande amelioration sur la classe Node est a faire. La creation est la mise a jour des etats du monde (lumiere, etat des personnages et cadena) devrait etre moins longue (soit en integrant un info_parser dans le node et un Thread avec un Thread manager).
La generation devrait se focaliser sur les enfants ayant une heuristique importante pour le joueur cible. Enfin une fois toutes les ameliorations faites, une profondeur de generation d'au moins 3 enfants supplementaires devrait permettre un temps de calcule plus important mais un scope decisionnel aussi plus important.