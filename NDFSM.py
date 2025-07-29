

class NDFSM:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states

    def __str__(self):
        return (
            "--- Non deterministic finite state machine ---\n"
            f"States: {self.states}\n"
            f"Alphabet: {self.alphabet}\n"
            f"Transitions: {self.transitions}\n"
            f"Initial state: {self.initial_state}\n"
            f"Accepting states: {self.accepting_states}"
        )