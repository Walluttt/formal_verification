from collections import deque
from typing import Set, Dict, List, Tuple, Callable
from TransitionSystem import State, TransitionSystem, SatisfactionFunction 
from properties import check_satisfaction 


def invariant_checker(ts: TransitionSystem, phi_func: SatisfactionFunction) -> Tuple[bool, List[State]]:
    R: Set[State] = set()
    U: deque[State] = deque()
    violating: State | None = None

    for s0 in ts.I - R:
        U.append(s0)
        R.add(s0)

        while U and violating is None:
            current = U[-1]
            news = ts.get_post(current) - R

            if not news:                       # tous les successeurs vus
                U.pop()
                if not check_satisfaction(current, ts, phi_func):
                    violating = current
            else:                              # explorer un nouvel état
                nxt = news.pop()
                U.append(nxt)
                R.add(nxt)

        if violating is not None:
            return False, list(U) + [violating]

    return True, []