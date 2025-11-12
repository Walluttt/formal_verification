from collections import deque
from typing import Set, List, Tuple
from TransitionSystem import State, TransitionSystem, SatisfactionFunction
from properties import check_satisfaction

def invariant_checker(ts: TransitionSystem, phi_func: SatisfactionFunction) -> Tuple[bool, List[State]]:
    R: Set[State] = set()
    U: deque[State] = deque()
    b = True  # invariant global

    def visiter(s: State) -> None:
        nonlocal b
        U.append(s)
        R.add(s)
        while U and b:
            s_prime = U[-1]
            post = ts.get_post(s_prime) - R
            if not post:
                s = U.pop()
                b = b and check_satisfaction(s_prime, ts, phi_func)
            else:
                s_double_prime = post.pop()
                U.append(s_double_prime)
                R.add(s_double_prime)
        if(not b):
            print("l'état de violation est: ", s)
    for s0 in ts.I - R:
        visiter(s0)
        if not b:
            return False, list(U)

    return True, []