from DFSM import DFSM

class NDFSMToDFSMConverter:
    def __init__(self, ndfsm):
        self.ndfsm = ndfsm
        self.state_name_map = {}
        self.state_counter = 0

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for (from_state, symbol), to_states in self.ndfsm.transitions.items():
                if from_state == state and symbol is None:
                    for t in to_states:
                        if t not in closure:
                            closure.add(t)
                            stack.append(t)
        return closure

    def move(self, states, symbol):
        result = set()
        for state in states:
            if (state, symbol) in self.ndfsm.transitions:
                result.update(self.ndfsm.transitions[(state, symbol)])
        return result

    def generate_state_name(self, state_set):
        frozen = frozenset(state_set)
        if frozen not in self.state_name_map:
            self.state_name_map[frozen] = f"D{self.state_counter}"
            self.state_counter += 1
        return self.state_name_map[frozen]


    def convert(self):
        from collections import deque

        start_closure = self.epsilon_closure({self.ndfsm.initial_state})
        queue = deque([start_closure])
        all_dfa_states = {frozenset(start_closure)}
        transitions = {}
        accepting_states = set()

        start_name = self.generate_state_name(start_closure)
        if self.ndfsm.accepting_states & start_closure:
            accepting_states.add(start_name)

        while queue:
            current = queue.popleft()
            current_name = self.generate_state_name(current)

            for symbol in self.ndfsm.alphabet:
                move_result = self.move(current, symbol)
                closure = self.epsilon_closure(move_result)
                if not closure:
                    continue
                closure_frozen = frozenset(closure)
                target_name = self.generate_state_name(closure)

                transitions[(current_name, symbol)] = {target_name}

                if closure_frozen not in all_dfa_states:
                    all_dfa_states.add(closure_frozen)
                    queue.append(closure)
                    if self.ndfsm.accepting_states & closure:
                        accepting_states.add(target_name)

        return DFSM(
            states=set(self.state_name_map.values()),
            alphabet=self.ndfsm.alphabet,
            transitions=transitions,
            initial_state=start_name,
            accepting_states=accepting_states
        )


