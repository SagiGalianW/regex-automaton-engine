from NDFSM import NDFSM

class DFSM(NDFSM):
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        super().__init__(states, alphabet, transitions, initial_state, accepting_states)
        self.deterministic = True  # example flag

    def __str__(self):
        return (
            "--- Deterministic finite state machine ---\n"
            f"States: {self.states}\n"
            f"Alphabet: {self.alphabet}\n"
            f"Transitions: {self.transitions}\n"
            f"Initial state: {self.initial_state}\n"
            f"Accepting states: {self.accepting_states}"
        )
    
    def minimize(self):
        from collections import defaultdict

        # Step 1: Initialize partitions
        non_accepting = self.states - self.accepting_states
        partitions = [self.accepting_states, non_accepting]
        worklist = [self.accepting_states.copy(), non_accepting.copy()]

        def get_partition(state):
            for i, part in enumerate(partitions):
                if state in part:
                    return i
            return -1

        while worklist:
            current = worklist.pop()
            for symbol in self.alphabet:
                affected = set()
                for (src, sym), dst in self.transitions.items():
                    if sym == symbol and next(iter(dst)) in current:
                        affected.add(src)

                new_partitions = []
                for part in partitions:
                    intersect = part & affected
                    difference = part - affected
                    if intersect and difference:
                        new_partitions.append(intersect)
                        new_partitions.append(difference)

                        if part in worklist:
                            worklist.remove(part)
                            worklist.append(intersect)
                            worklist.append(difference)
                        else:
                            if len(intersect) <= len(difference):
                                worklist.append(intersect)
                            else:
                                worklist.append(difference)
                    else:
                        new_partitions.append(part)
                partitions = new_partitions

        # Step 2: Reconstruct minimized DFA (in-place)
        state_map = {}
        for i, part in enumerate(partitions):
            name = f'M{i}'
            for state in part:
                state_map[state] = name

        new_states = set(state_map.values())
        new_transitions = {}
        for (src, sym), dst in self.transitions.items():
            new_src = state_map[src]
            new_dst = state_map[next(iter(dst))]
            new_transitions[(new_src, sym)] = {new_dst}

        new_initial = state_map[self.initial_state]
        new_accepting = {state_map[s] for s in self.accepting_states}

        # --- Update this object (in-place) ---
        self.states = new_states
        self.transitions = new_transitions
        self.initial_state = new_initial
        self.accepting_states = new_accepting

    def run(self, input_string):
        current_state = self.initial_state

        for symbol in input_string:
            key = (current_state, symbol)
            if key not in self.transitions:
                return False  # No valid transition
            # Since DFSM has single target per transition (in a set)
            current_state = next(iter(self.transitions[key]))

        return current_state in self.accepting_states
