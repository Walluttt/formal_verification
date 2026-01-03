— TransitionSystem.py : Définition de la classe d’un système de transition.

— verifier_invariant.py : Fichier contenant l’implémentation de l’algorithme de vérification de
l’invariant (Algorithme 1) et de la procédure de visite.

— properties.py : Définition des fonctions de satisfaction (s |= Φ) pour les différentes propriétés à
valider pour chaque exemple.

— invariant_phi_test.py : Fichier d’exemple contenant les systèmes de transition et l’exécution
de leur vérification associée.

Pour obtenir le résultat, on exécute simplement python ./invariant_phi_test.py.

Dans le fichier test se trouve la déclaration de 2 objets de type TransitionSystem :
1. Un représentant la concurrence entre 2 programmes contrôlée par un sémaphore, dont la propriété
de sûreté que nous souhaitons vérifier est l’Exclusion Mutuelle ¬(C1 ∧C2).

2. L’autre, un système de transition simple représentant un compteur entre 0 et 4, dont la propriété
à valider est ¬MAX (le compteur ne doit pas atteindre 4).