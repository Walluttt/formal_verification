from typing import Set, Dict, List, Tuple, Callable
from TransitionSystem import State, TransitionSystem, SatisfactionFunction 

def check_satisfaction(s: State, ts: TransitionSystem, phi_func: SatisfactionFunction) -> bool:
    """
    Vérifie si l'état s satisfait la proposition logique Phi.
    :param s: L'état à vérifier.
    :param ts: Le Système de Transition.
    :param phi_func: La fonction implémentant l'invariant Phi.
    :return: True si s |= Phi, False sinon.
    """
    return phi_func(s, ts)

# Invariant à vérifier : Phi_mutex: Exclusion Mutuelle (i.e., not (PC1 AND PC2))
def phi_mutex(s: State, ts: TransitionSystem) -> bool:
    """Vérifie si s |= not (C1 AND C2)."""
    
    # 1. Récupérer les labels de l'état s.
    labels = ts.L.get(s, set())
    
    # 2. Vérifier si l'état s satisfait l'expression de violation (PC1 AND PC2).
    violation_occurs = ("C1" in labels) and ("C2" in labels)
    
    # 3. La propriété d'invariant est l'inverse de la violation.
    return not violation_occurs

# Invariant à vérifier : Phi_count: L'état n'est jamais MAX (i.e., not MAX)
def phi_not_max(s: State, ts: TransitionSystem) -> bool:
    """Vérifie si s |= not MAX."""
    return "MAX" not in ts.L.get(s, set())