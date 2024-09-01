from enum import Enum
from mdp import State, MDP


def test_1():
    states = State({1, 2, 3}, {3})
    actions = {1}
    trans_fun = {(s, 1, s1): p
                 for s in states.active_states
                 for (s1, p) in [(s, 0.2), (s+1, 0.8)]
                 }
    costs = {1: lambda _: 1.0}
    markov = MDP(states, actions, trans_fun, costs)

    for s in states.active_states:
        for i in range(7):
            print(f"pi({s})_{i}={markov.optimal_policy(s, i)}\n")
            #print(f"V({s})_{i}={markov.value_iteration(s, i)}\n")

def test_2():
    class Actions(Enum):
        L, R, D, A = 0, 1, 2, 3
        def __repr__(self):
            return f"{self._name_}"

    states = State({0, 1, 2}, {2})

    actions = {Actions.R, Actions.D, Actions.L, Actions.A}

    trans_fun = {
        (0, Actions.R, 2): 1.0,
        (0, Actions.D, 1): 1.0,
        (0, Actions.L, 1): 0.25,
        (0, Actions.L, 2): 0.75,
        (1, Actions.A, 1): 0.2,
        (1, Actions.A, 2): 0.8,
    }

    markov = MDP(states, actions, trans_fun, dir_cost)

    s = 0
    for s in (0, 1):
        i = 5
        print(f"pi({s})_{i}={markov.optimal_policy(s, i)}\n")



def test_3(min_temp, max_temp, goal):
    class Actions(Enum):
        Off, On = 0, 1
        def __repr__(self):
            return f"{self._name_}"

    def conditional_probability(s, a):
        next_state = []
        prob_next_state = []
        match (s, a):
            case (t, Actions.Off):
                next_state = [s, s+0.5, s-0.5]
                if t == min_temp:
                    prob_next_state = [0.9, 0.1, 0]
                elif t == max_temp:
                    prob_next_state = [0.3, 0, 0.7]
                elif min_temp < t < max_temp:
                    prob_next_state = [0.2, 0.1, 0.7]
                else:
                    next_state = [0, 0, 0, 0]
            case (t, Actions.On):
                next_state = [s, s+0.5, s+1, s-0.5]
                if t == min_temp:
                    prob_next_state = [0.3, 0.5, 0.2, 0]
                elif t == max_temp-0.5:
                    prob_next_state = [0.2, 0.7, 0, 0.1]
                elif t == max_temp:
                    prob_next_state = [0.9, 0, 0, 0.1]
                elif min_temp < t < max_temp:
                    prob_next_state = [0.2, 0.5, 0.2, 0.1]
                else:
                    next_state = [0, 0, 0, 0]
        return zip(next_state, prob_next_state)

    states = State({i * 0.1 for i in range(min_temp*10,max_temp*10+5,5)}, {goal})

    actions = {Actions.On, Actions.Off}
        #s: [Actions.On, Actions.Off] if s not in states.goal else [] for s in states.domain
        #}

    trans_func = {
        (s0, a, s1):
        p if s1 in states.domain else 0.0
        for s0 in states.active_states
        for a in actions
        for (s1, p) in conditional_probability(s0, a)
    }

    cost = {Actions.On: 4,
            Actions.Off: 1}

    markov = MDP(states, actions, trans_func, cost)

    for s in range(min_temp*10,max_temp*10+5,5):
        a, c = markov.optimal_policy(s*0.1, 0.01)
        print(f"π({s*0.1})={(a, c)}\n")
    #markov.optimal_policy("I", i)

def test_4():
    states = State({"E", "I", "D"}, {"E"})
    actions = {"staff", "antivirus"}
    trans_func = {
        ("D", "antivirus", "D"): 0.5,
        ("D", "antivirus", "E"): 0.2,
        ("D", "antivirus", "I"): 0.3,
        ("I", "antivirus", "I"): 0.8,
        ("I", "antivirus", "E"): 0.2,
        ("D", "staff", "D"): 0.2,
        ("D", "staff", "I"): 0.7,
        ("D", "staff", "E"): 0.1,
        ("I", "staff", "I"): 0.3,
        ("I", "staff", "E"): 0.7
    }
    cost = {"staff": 25,
            "antivirus": 10}

    markov = MDP(states, actions, trans_func, cost)
    #markov.value_iteration("I",i)
    for s in states.domain:
        a = markov.optimal_policy(s, 0.01)
        print(f"π({s})={a}\n")
    #markov.optimal_policy("I", i)

test_3(16,25,22)
