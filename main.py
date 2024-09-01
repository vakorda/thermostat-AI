from mdp import MDP, State
from typing import Dict, Set, Tuple, TypeVar
T = TypeVar("T")
A = TypeVar("A")

MIN_TEMP = -16
MAX_TEMP = 35
GOAL = 22


class Thermostat(MDP):
    def __init__(self, states: State[T], actions: Set[A],
                 transition_function: Dict[Tuple[T,A,T], float],
                 costs: Dict[A, float],
                 strict: bool=True,
                 precision: float=0.01) -> None:
        self.__strict = False
        super().__init__(states, actions, transition_function, costs, precision)
        self.__strict = strict

    @property
    def costs(self):
        return self.__costs

    @costs.setter
    def costs(self, dictionary):
        if self.__strict:
            raise AttributeError("The thermostat was initialized as strict. NO change of the costs can be effectuated")
        if type(dictionary) != dict:
            raise TypeError("The costs must be a dictionary with actions as keys")
        try:
            # Dummy list that just checks that the costs are associated with valid actions
            lst = [c for (a,c) in dictionary.items() if a in actions]
        except Exception:
            raise ValueError("Invalid dictionary")
        if len(lst) == 0:
            raise ValueError("Invalid keys")
        self.__costs = dictionary

if __name__ == '__main__':
    def next_state_and_probability(s, a):
        """
        Function that returns a list of possible next states and the probability of
        get there from a given state after executing certain action
        """
        next_state = []
        prob_next_state = []
        if a == "off":
            next_state = [s, s+0.5, s-0.5]
            if s == MIN_TEMP:
                prob_next_state = [0.9, 0.1, 0.0]
            elif s == MAX_TEMP:
                prob_next_state = [0.3, 0.0, 0.7]
            elif MIN_TEMP < s < MAX_TEMP:
                prob_next_state = [0.2, 0.1, 0.7]
            else:
                next_state= [0.0, 0.0, 0.0, 0.0]
        elif a == "on":
            next_state = [s, s+0.5, s+1, s-0.5]
            if s == MIN_TEMP:
                prob_next_state = [0.3, 0.5, 0.2, 0.0]
            elif s == MAX_TEMP-0.5:
                prob_next_state = [0.2, 0.7, 0.0, 0.1]
            elif s == MAX_TEMP:
                prob_next_state = [0.9, 0.0, 0.0, 0.1]
            elif MIN_TEMP < s < MAX_TEMP:
                prob_next_state = [0.2, 0.5, 0.2, 0.1]
            else:
                next_state = [0.0, 0.0, 0.0, 0.0]

        return zip(next_state, prob_next_state)

    states = State({t*0.1 for t in range(MIN_TEMP*10, MAX_TEMP*10+5, 5)}, {GOAL})
    actions = {"on", "off"}

    trans_func = {
        (s0, a, s1):
        p if s1 in states.domain else 0.0
        for s0 in states.active_states
        for a in actions
        for (s1, p) in next_state_and_probability(s0, a)
    }

    costs = {"on": 4, "off": 0.5}

    termostat_mdp = Thermostat(states, actions, trans_func, costs)
    for i in sorted(states.domain):
        print(termostat_mdp.optimal_policy(i))
