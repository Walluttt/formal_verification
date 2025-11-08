from collections import deque
from typing import Set, Dict, List, Tuple, Callable
from TransitionSystem import State, TransitionSystem, SatisfactionFunction 
from properties import check_satisfaction 


def invariant_checker(ts: TransitionSystem, phi_func: SatisfactionFunction) -> Tuple[bool, List[State]]:
    """
    Implémentation de l'Algorithme 1 de Vérification d'invariant.
    Détermine si ST vérifie la proposition logique Phi.

    :param ts: Le Système de Transition ST.
    :param phi_func: La fonction de satisfaction pour l'invariant Phi.
    :return: Tuple (booléen, contre-exemple: List[State]).
             booléen est True si OUI, False si NON.
             La liste est vide si True, sinon elle contient la pile U comme contre-exemple.
    """
    # Ensemble d'états R <- vide (états accessibles/marqués) [cite: 25, 54]
    R: Set[State] = set()
    # Pile d'états U [cite: 26] (utilisé comme un chemin pour le contre-exemple)
    U: deque[State] = deque()
    # Booléen b VRAI (validité de l'invariant) [cite: 27]
    b: bool = True

    # Définition de la procédure auxiliaire visiter(état s) [cite: 37]
    def visiter(s: State):
        nonlocal b
        # push(s, U) [cite: 38]
        U.append(s)
        # R <- R union {s} (on marque s comme accessible) [cite: 39, 60]
        R.add(s)

        # Répéter (boucle principale du DFS) [cite: 40]
        while U and b: # Jusqu'à (U=epsilon) V non b [cite: 51]
            # s' <- top(U) [cite: 41, 61]
            s_prime = U[-1] # top de la pile
            
            # Post_st(s') [cite: 42]
            post_s_prime = ts.get_post(s_prime)
            
            # Successeurs non visités de s'
            new_successors = post_s_prime.difference(R)
            
            if not new_successors: # Si Post_st(s') C R alors (tous les successeurs sont dans R) [cite: 42]
                # pop(U) [cite: 43, 62]
                U.pop()
                
                # b <- b AND (s' |= Phi) (on vérifie la validité de Phi en s') [cite: 44, 62]
                if b and not check_satisfaction(s_prime, ts, phi_func):
                    b = False
                    
            else: # Sinon (il existe un successeur non visité) [cite: 45]
                # choisir s'' dans Post(s') \ R [cite: 46, 47]
                s_double_prime = next(iter(new_successors)) # choix arbitraire
                
                # push(s'', U) [cite: 48]
                U.append(s_double_prime)
                # R <- R union {s''} (s'' est un nouvel état accessible) [cite: 49, 63]
                R.add(s_double_prime)
        # Fin Procédure [cite: 52]

    # Début de l'Algorithme 1 - Boucle principale [cite: 28]
    # Tant que I \ R != vide AND b faire [cite: 28]
    initial_unvisited = ts.I.difference(R)
    while initial_unvisited and b:
        # choisir s dans I \ R (on choisit arbitrairement un état initial qui n'est pas dans R) [cite: 29, 55]
        s = next(iter(initial_unvisited))
        # visiter(s) (on appelle la procédure de balayage) [cite: 30, 56]
        visiter(s)
        # Mettre à jour l'ensemble des états initiaux non visités pour la condition de boucle
        initial_unvisited = ts.I.difference(R)
    # Fin Tant que [cite: 31]

    # Si b alors [cite: 32]
    if b:
        # renvoyer OUI (ST satisfait toujours Phi) [cite: 33, 57]
        return True, []
    # Sinon [cite: 34]
    else:
        # renvoyer (NON, U) (la pile U fournit un contre-exemple) [cite: 35, 58, 53]
        # U contient le chemin menant à l'état qui viole l'invariant (grâce au pop/check dans visiter)
        return False, list(U)