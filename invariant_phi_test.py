from typing import Set, Dict, List, Tuple

from TransitionSystem import TransitionSystem, State as GenericState, SatisfactionFunction
from verifier_invariant import invariant_checker
from properties import phi_mutex, phi_not_max


# ====================================================================
# EXEMPLE 1 : Système de Transition du Sémaphore Binaire (Exclusion Mutuelle)
# ====================================================================

# --- Composants du Modèle du Sémaphore Binaire  ---

# États: (loc1, loc2, sem)
State = Tuple[str, str, int] # Redéfinition nécessaire si elle n'est pas dans SystemTransition.py

S_SEM_SIMPLE: Set[State] = {
    ('N', 'N', 1), ('P', 'N', 1), ('N', 'P', 1),
    ('C', 'N', 0), ('N', 'C', 0),
    ('P', 'P', 1), # Les deux veulent entrer, sem libre
    ('P', 'N', 0), ('N', 'P', 0), # Un seul peut entrer, l'autre attend
    ('C', 'P', 0), ('P', 'C', 0), # Un est critique, l'autre attend
}

I_SEM_SIMPLE: Set[State] = {('N', 'N', 1)} # État initial
Prop_SEM: Set[str] = {"PC1", "PC2"}

# Fonction de labellisation L_SEM (aucune modification, car C reste l'état critique)
L_SEM_SIMPLE: Dict[State, Set[str]] = {
    s: ({"PC1"} if s[0] == 'C' else set()).union(
       {"PC2"} if s[1] == 'C' else set())
    for s in S_SEM_SIMPLE
}

# Relation de transition simplifiée (Post)
Post_SEM_SIMPLE: Dict[State, Set[State]] = {
    # 1. Tenter d'entrer (N -> P)
    ('N', 'N', 1): {('P', 'N', 1), ('N', 'P', 1)},
    
    # 2. wait() réussit (P -> C si Sem=1)
    ('P', 'N', 1): {('C', 'N', 0)},
    ('N', 'P', 1): {('N', 'C', 0)},
    
    # 3. wait() en concurrence (P, P, 1) -> un seul entre, l'autre passe à Sem=0 pour attendre
    ('P', 'P', 1): {('C', 'P', 0), ('P', 'C', 0)}, 
    
    # 4. Attendre (si Sem=0, P reste P)
    ('P', 'N', 0): {('P', 'N', 0)},
    ('N', 'P', 0): {('N', 'P', 0)},
    ('C', 'P', 0): {('C', 'P', 0)},
    ('P', 'C', 0): {('P', 'C', 0)},
    
    # 5. signal() (C -> N + Sem=1)
    ('C', 'N', 0): {('N', 'N', 1)},
    ('N', 'C', 0): {('N', 'N', 1)},

    # 6. signal() lorsqu'un autre attend (C -> P devient N -> P)
    ('C', 'P', 0): {('N', 'P', 1)}, # P1 sort, P2 passe à P + Sem=1
    ('P', 'C', 0): {('P', 'N', 1)}, # P2 sort, P1 passe à P + Sem=1
}

# --- Construction du Système de Transition ---
st_semaphore_simple = TransitionSystem(S_SEM_SIMPLE, I_SEM_SIMPLE, Post_SEM_SIMPLE, L_SEM_SIMPLE, Prop_SEM)

print("\n====================================================================")
print(f"EXEMPLE 1 : Système de Transition du Sémaphore (N, P, C)")

# Test 1 : Exclusion Mutuelle (Phi: non (PC1 AND PC2)) - DOIT RÉUSSIR
print("\n--- Test 1 : Vérification de l'Exclusion Mutuelle (doit être OUI) ---")
result_mutex_simple, counterexample_mutex_simple = invariant_checker(st_semaphore_simple, phi_mutex)

if result_mutex_simple:
    print("Résultat: OUI. L'invariant d'Exclusion Mutuelle est satisfait.")
else:
    print(f"Résultat: NON. L'invariant d'Exclusion Mutuelle est violé. Contre-exemple : {counterexample_mutex_simple}")

# ====================================================================
# EXEMPLE 2 : Système de Transition simple (Compteur) (consigne 5)
# ====================================================================

# Cet exemple utilise l'alias State = int défini dans SystemTransition.py
State = GenericState 

S_COUNT: Set[State] = {0, 1, 2, 3, 4}
I_COUNT: Set[State] = {0}
Prop_COUNT: Set[str] = {"HIGH", "MAX"}

# Labellisation : HIGH si > 2, MAX si = 4
L_COUNT: Dict[State, Set[str]] = {
    0: set(),
    1: set(),
    2: set(),
    3: {"HIGH"},
    4: {"HIGH", "MAX"},
}

# Relation de transition : compteur de 0 à 4, puis boucle sur 4
Post_COUNT: Dict[State, Set[State]] = {
    0: {1},
    1: {2},
    2: {3},
    3: {4},
    4: {4},
}

# --- Construction du Système de Transition ---
st_counter = TransitionSystem(S_COUNT, I_COUNT, Post_COUNT, L_COUNT, Prop_COUNT)

# --- Tests de l'Exemple 2 (Compteur) ---
print("\n====================================================================")
print(f"EXEMPLE 2 : Système de Transition Compteur (de 0 à 4)")

# Test 2 : Invariant not MAX (doit être NON, car l'état 4 est atteignable et satisfait MAX)
print("\n--- Test 2 : Vérification de l'invariant 'not MAX' (doit être NON) ---")
result_not_max, counterexample_not_max = invariant_checker(st_counter, phi_not_max)

if result_not_max:
    print("Résultat: OUI. (Le modèle est trop simple pour cela).")
else:

    print(f"Résultat: NON. L'invariant 'not MAX' est violé.")
    print(f"Contre-exemple (chemin vers l'état de violation): {counterexample_not_max}")
print("====================================================================")