from collections import deque
from typing import Set, Dict, List, Tuple, Callable

# Définition de types pour la clarté
# Un état est simplement un hashable
State = int
# Un ensemble de propositions atomiques est un ensemble de chaînes de caractères
PropSet = Set[str]
# La fonction de labellisation L: S -> 2^Prop
LabelingFunction = Dict[State, PropSet]
# La relation de transition -> est représentée par un dictionnaire State -> Set[State]
TransitionRelation = Dict[State, Set[State]]

class TransitionSystem:
    """
    Représentation d'un Système de Transition ST = (S, Act, ->, I, Prop, L).
    """
    def __init__(self, states: Set[State], initial_states: Set[State],
                 transition_relation: TransitionRelation,
                 labeling_function: LabelingFunction,
                 atomic_propositions: Set[str]):
        """
        Initialise le Système de Transition.

        :param states: Ensemble des états S.
        :param initial_states: Ensemble des états initiaux I.
        :param transition_relation: Relation de transition -> (représentée par Post(s)).
        :param labeling_function: Fonction de labellisation L.
        :param atomic_propositions: Ensemble des propositions atomiques Prop.
        """
        self.S = states
        self.I = initial_states
        # Représentation de Post(s) pour la recherche: {s: {s1, s2, ...}}
        self.Post = transition_relation
        self.L = labeling_function
        self.Prop = atomic_propositions

    def get_post(self, s: State) -> Set[State]:
        """Retourne l'ensemble des successeurs Post(s)."""
        return self.Post.get(s, set())

    def __str__(self):
        return (f"TransitionSystem(S={len(self.S)} états, I={len(self.I)} initiaux, "
                f"Propositions={self.Prop})")

# Type pour la fonction de satisfaction: prend l'état et le ST, retourne True si s |= Phi
SatisfactionFunction = Callable[[State, TransitionSystem], bool]
