# #!/usr/bin/env python3
from typing import Callable, Dict, List, Union, Set, Tuple, TypeVar, Generic

T = TypeVar("T")
A = TypeVar("A")

class State(Generic[T]):
    def __init__(self, domain: Set[T], goal: Set[T]):
        self.domain = domain
        self.goal = goal

    @property
    def active_states(self) -> Set[T]:
        return self.domain - self.goal

    @property
    def goal(self):
        return self.__goal

    @goal.setter
    def goal(self, value):
        outsiders = value - self.domain
        if outsiders != set():
            raise ValueError(f"ALL goal states must be inside the domain, the following are not: {outsiders}")
        self.__goal = value

class MDP(Generic[T, A]):
    def __init__(self, states: State[T], actions: Set[A],
                 transition_function: Dict[Tuple[T,A,T], float],
                 costs: Dict[A, float],
                 precision: float=0.01) -> None:
        self.states = states
        self.actions = actions
        self.transition_function = transition_function
        self.costs = costs
        self.precision = precision
        self.__previous_values = {s: [0] for s in self.states.domain}

        next_state = {(s,a):[] for s in states.active_states for a in actions}
        possible_actions = {s: [] for s in states.domain}
        for ((s0, a, s1), p) in self.transition_function.items():
            if s0 not in states.goal:
                possible_actions[s0].append(a)
            if p > 0 and s1 in self.states.domain:
                next_state[(s0,a)].append(s1)
        self.__next_state = next_state
        self.__possible_actions = possible_actions



    def __value_iteration(self, s: T, i: int) -> float:
        if i == 0:
            return 0

        if len(self.__previous_values[s]) > i:
            return self.__previous_values[s][i]

        if s in self.states.goal:
            min_val = 0
        else:
            lst = []
            for a in self.__possible_actions[s]:
                total = self.costs[a]
                for s1 in self.__next_state[(s,a)]:
                    tr = self.transition_function[(s, a, s1)]
                    while True:
                        try:
                            vi = self.__previous_values[s1][i-1]
                            break
                        except IndexError:
                            self.__value_iteration(s1, i-1)

                    total += tr * vi
                lst.append(total)
            min_val = min(lst)
        self.__previous_values[s].append(min_val)
        return min_val

    def optimal_policy(self, state: T) -> Tuple[Union[A, None], float]:
        if self.precision <= 0:
            raise ValueError

        if state in self.states.goal:
            return (None, 0.0)

        i, finished = 0, False
        while not finished:
            i += 1
            for s in self.states.domain:
                self.__value_iteration(s, i)
            finished = (self.__previous_values[state][i] - self.__previous_values[state][i-1]) < self.precision


        minim = [(a, self.costs[a] + sum([self.transition_function[(state, a, s1)] * self.__value_iteration(s1, i)
                                                        for s1 in self.__next_state[(state, a)]]))
                               for a in self.__possible_actions[state]]
        (action, value) = min(minim,
                              key=lambda x: x[1])
        return (action, value)

    @property
    def costs(self):
        return self.__costs

    @costs.setter
    def costs(self, dictionary):
        if type(dictionary) != dict:
            raise TypeError("The costs must be a dictionary with actions as keys")
        try:
            lst = [c for (a,c) in dictionary.items() if a in actions]
        except Exception:
            raise ValueError("Invalid dictionary")

        if len(lst) == 0:
            raise ValueError("Invalid keys")
        self.__costs = dictionary

    @property
    def states(self):
        return self.__states

    @states.setter
    def states(self, states):
        if type(states) != State:
            raise TypeError("The states must be inside the State class")
        self.__states = states

    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, actions):
        if type(actions) != set:
            raise TypeError("The actions must be a set")
        self.__actions = actions

    @property
    def transition_function(self):
        return self.__transition_function

    @transition_function.setter
    def transition_function(self, dictionary):
        self.__transition_function = dictionary

    @property
    def precision(self):
        return self.__precision

    @precision.setter
    def precision(self, value):
        self.__precision = value
