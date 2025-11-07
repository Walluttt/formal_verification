from typing import Set, Dict, List, Tuple, Callable
from SystemTransition import State, TransitionSystem, SatisfactionFunction 

def check_satisfaction(s: State, ts: TransitionSystem, phi_func: SatisfactionFunction) -> bool:
    """
    Vérifie si l'état s satisfait la proposition logique Phi.
    :param s: L'état à vérifier.
    :param ts: Le Système de Transition.
    :param phi_func: La fonction implémentant l'invariant Phi.
    :return: True si s |= Phi, False sinon.
    """
    return phi_func(s, ts)

def phi_mutex(s: State, ts: TransitionSystem) -> bool:
    """Vérifie si s |= not (PC1 AND PC2)."""
    labels = ts.L.get(s, set())
    return not ("PC1" in labels and "PC2" in labels)

def phi_pc1(s: State, ts: TransitionSystem) -> bool:
    """Vérifie si s |= PC1."""
    return "PC1" in ts.L.get(s, set())