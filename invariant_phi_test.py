from typing import Set, Dict, List, Tuple

from SystemTransition import TransitionSystem, State as GenericState, SatisfactionFunction
from verifier_invariant import invariant_checker
from properties import phi_mutex, phi_pc1
# ====================================================================
# EXEMPLE 1 : Système de Transition du Sémaphore Binaire (Exclusion Mutuelle)
# ====================================================================

# Redéfinition du type d'État pour cet exemple spécifique (consigne 5)
# État: (loc1: N/T/C/E, loc2: N/T/C/E, sem: 0/1)
State = Tuple[str, str, int]

# --- Composants du Modèle du Sémaphore Binaire (Simplifié) ---

S_SEM: Set[State] = {
    ('N', 'N', 1), ('T', 'N', 1), ('N', 'T', 1),
    ('C', 'N', 0), ('N', 'C', 0),
    ('T', 'T', 1),
    ('C', 'T', 0), ('T', 'C', 0),
    ('E', 'N', 0), ('N', 'E', 0),
    ('E', 'E', 1),
}

I_SEM: Set[State] = {('N', 'N', 1)} # État initial
Prop_SEM: Set[str] = {"PC1", "PC2"}

# Fonction de labellisation L_SEM (associée à l'état s = (loc1, loc2, sem))
L_SEM: Dict[State, Set[str]] = {
    s: ({"PC1"} if s[0] == 'C' else set()).union(
       {"PC2"} if s[1] == 'C' else set())
    for s in S_SEM
}

# Relation de transition simplifiée (Post)
Post_SEM: Dict[State, Set[State]] = {
    ('N', 'N', 1): {('T', 'N', 1), ('N', 'T', 1)},
    ('T', 'N', 1): {('C', 'N', 0)},
    ('N', 'T', 1): {('N', 'C', 0)},
    ('T', 'T', 1): {('C', 'T', 0), ('T', 'C', 0)}, # P1 ou P2 passe
    ('C', 'N', 0): {('E', 'N', 0)},
    ('N', 'C', 0): {('N', 'E', 0)},
    ('E', 'N', 0): {('N', 'N', 1)},
    ('N', 'E', 0): {('N', 'N', 1)},
    ('C', 'T', 0): {('C', 'T', 0), ('E', 'T', 0)}, # P1 sort ou P2 attend
    ('T', 'C', 0): {('T', 'C', 0), ('T', 'E', 0)}, # P2 sort ou P1 attend
}

# --- Construction du Système de Transition ---
st_semaphore = TransitionSystem(S_SEM, I_SEM, Post_SEM, L_SEM, Prop_SEM)


# --- Tests de l'Exemple 1 (Sémaphore) ---
print("====================================================================")
print(f"EXEMPLE 1 : Système de Transition du Sémaphore Binaire")

# Test 1.1 : Exclusion Mutuelle (Phi: non (PC1 AND PC2)) - DOIT RÉUSSIR
print("\n--- Test 1.1 : Vérification de l'Exclusion Mutuelle (doit être OUI) ---")
result_mutex, counterexample_mutex = invariant_checker(st_semaphore, phi_mutex)

if result_mutex:
    print("✅ Résultat: OUI. L'invariant d'Exclusion Mutuelle est satisfait.")
else:
    print(f"❌ Résultat: NON. L'invariant d'Exclusion Mutuelle est violé. Contre-exemple : {counterexample_mutex}")

# Test 1.2 : Invariant Faux (Phi: PC1) - DOIT ÉCHOUER (NON)
print("\n--- Test 1.2 : Vérification d'un invariant faux (Phi: PC1) (doit être NON) ---")
result_pc1, counterexample_pc1 = invariant_checker(st_semaphore, phi_pc1)

if result_pc1:
    print("✅ Résultat: OUI. (Peut arriver si le modèle est mal défini).")
else:
    print(f"❌ Résultat: NON. L'invariant PC1 est violé. Contre-exemple : {counterexample_pc1}")


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

# Invariant à vérifier : Phi_count: L'état n'est jamais MAX (i.e., not MAX)
def phi_not_max(s: State, ts: TransitionSystem) -> bool:
    """Vérifie si s |= not MAX."""
    return "MAX" not in ts.L.get(s, set())

# --- Construction du Système de Transition ---
st_counter = TransitionSystem(S_COUNT, I_COUNT, Post_COUNT, L_COUNT, Prop_COUNT)

# --- Tests de l'Exemple 2 (Compteur) ---
print("\n====================================================================")
print(f"EXEMPLE 2 : Système de Transition Compteur (de 0 à 4)")

# Test 2.1 : Invariant not MAX (doit être NON, car l'état 4 est atteignable et satisfait MAX)
print("\n--- Test 2.1 : Vérification de l'invariant 'not MAX' (doit être NON) ---")
result_not_max, counterexample_not_max = invariant_checker(st_counter, phi_not_max)

if result_not_max:
    print("✅ Résultat: OUI. (Le modèle est trop simple pour cela).")
else:
    # Le chemin de violation doit être [0, 1, 2, 3, 4]
    print(f"❌ Résultat: NON. L'invariant 'not MAX' est violé.")
    print(f"Contre-exemple (chemin vers l'état de violation): {counterexample_not_max}")
print("====================================================================")