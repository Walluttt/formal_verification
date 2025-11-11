from typing import Set, Dict, List, Tuple

from TransitionSystem import TransitionSystem, State as GenericState, SatisfactionFunction
from verifier_invariant import invariant_checker
from properties import phi_mutex, phi_not_max


# ====================================================================
# EXEMPLE 1 : Système de Transition du Sémaphore Binaire (Exclusion Mutuelle)
# ====================================================================

# --- Composants du Modèle du Sémaphore Binaire  ---

# États: (loc1, loc2, sem)
State = Tuple[str, str, int]

# --- 1. Ensemble des États (S) ---
S_SEM_SIMPLE: Set[State] = {
    # -------------- sem = 1 --------------
    ('N1', 'N2', 1),
    ('P1', 'N2', 1),
    ('N1', 'P2', 1),
    ('P1', 'P2', 1),
    # -------------- sem = 0 --------------
    ('C1', 'N2', 0),
    ('N1', 'C2', 0),
    ('C1', 'P2', 0),
    ('P1', 'C2', 0),
    #Etats non accessibles depuis l'état initial
    ('C1', 'C2', 0),
    ('C1', 'C2', 1),
    ('P1', 'C2', 1),
    ('C1', 'P2', 1),

}
# --- 2. Ensemble des États Initiaux (I) ---
I_SEM_SIMPLE: Set[State] = {('N1', 'N2', 1)}

# --- 3. Propositions Atomiques (Prop) ---
# PC1 reste vrai si P1 est en C, PC2 si P2 est en C.
Prop_SEM: Set[str] = {"C1", "C2"}

# --- 4. Fonction de Labellisation (L) ---
L_SEM_SIMPLE = {}
for s in S_SEM_SIMPLE:
    props = set()
    if s[0] == 'C1':
        props.add("C1")
    if s[1] == 'C2':
        props.add("C2")
    L_SEM_SIMPLE[s] = props

# --- 5. Relation de Transition (Post) ---
Post_SEM_SIMPLE: Dict[State, Set[State]] = {
    # Transition des états accessibles par l'état initial ('N1', 'N2', 1)
    # =========================================================
    # sem = 1  (personne n’est en C)
    # =========================================================
    ('N1', 'N2', 1): {('N1', 'N2', 1), ('P1', 'N2', 1), ('N1', 'P2', 1)},
    ('P1', 'N2', 1): {('P1', 'N2', 1), ('C1', 'N2', 0)},
    ('N1', 'P2', 1): {('N1', 'P2', 1), ('N1', 'C2', 0)},
    ('P1', 'P2', 1): {('P1', 'P2', 1), ('C1', 'P2', 0), ('P1', 'C2', 0)},

    # =========================================================
    # sem = 0  (exactement un processus en C)
    # =========================================================
    # --- côté 1 en C ------------------------------------------------
    ('C1', 'N2', 0): {('C1', 'N2', 0), ('N1', 'N2', 1),          # signal / rien
                      ('C1', 'P2', 0)},                           # P2 veut entrer
    ('C1', 'P2', 0): {('C1', 'P2', 0), ('N1', 'P2', 1)},         # signal / rester bloqué

    # --- côté 2 en C ------------------------------------------------
    ('N1', 'C2', 0): {('N1', 'C2', 0), ('N1', 'N2', 1),          # signal / rien
                      ('P1', 'C2', 0)},                           # P1 veut entrer
    ('P1', 'C2', 0): {('P1', 'C2', 0), ('P1', 'N2', 1)},         # signal / rester bloqué
    # Transition des états non accessibles par l'état initial
    ('C1', 'C2', 0): {('C1', 'C2', 0)},                           # bloqué
    ('C1', 'C2', 1): {('C1', 'C2', 1)},                           # bloqué
    ('P1', 'C2', 1): {('P1', 'C2', 1), ('C1', 'C2', 0)},         # P1 entre en C
    ('C1', 'P2', 1): {('C1', 'P2', 1), ('C1', 'C2', 0)},         # P2 entre en C
}

st_semaphore_simple = TransitionSystem(S_SEM_SIMPLE, I_SEM_SIMPLE, Post_SEM_SIMPLE, L_SEM_SIMPLE, Prop_SEM)

print("\n====================================================================")
print(f"EXEMPLE 1 : Système de Transition du Sémaphore (N, P, C)")

# Test 1 : Exclusion Mutuelle (Phi: non (C1 AND C2)) - DOIT RÉUSSIR
print("\n--- Test : Vérification de l'Exclusion Mutuelle (doit être OUI) ---")
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
print("\n--- Test : Vérification de l'invariant 'not MAX' (doit être NON) ---")
result_not_max, counterexample_not_max = invariant_checker(st_counter, phi_not_max)

if result_not_max:
    print("Résultat: OUI. (Le modèle est trop simple pour cela).")
else:

    print(f"Résultat: NON. L'invariant 'not MAX' est violé.")
    print(f"Contre-exemple (chemin vers l'état de violation): {counterexample_not_max}")
print("====================================================================")