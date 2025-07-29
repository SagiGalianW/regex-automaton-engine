from NDFSM import NDFSM

class RegexToNDFSM:
    state_namer = 0

    def __init__(self, regex, operators):
        self.regex = regex
        self.operators = operators
        self.alphabet = set()
        for c in self.regex:
            if c not in operators and c != '(' and c != ')':
                self.alphabet.add(c)

    def generate_state_name(self):
        state = f'q{self.state_namer}'
        self.state_namer += 1
        return state
    
    # this function will return 2 sub regexes and operator like this regex left, regex right, operator
    def simplify_regex(self, regex):
        dept = 0
        for i in range(len(regex)):
            if regex[i] == '(':
                dept += 1
            elif regex[i] == ')':
                dept -= 1

            if regex[i] in self.operators and dept == 1:
                if regex[i] != "+" and regex[i] != "*":
                    return (
                        None if regex[2:i-1] == '' else regex[1:i],
                        None if regex[i+1:-1] == '' else regex[i+1:-1],
                        regex[i]
                    )
                else:
                    return (
                        None if regex[2:i-1] == '' else regex[2:i-1],
                        None,
                        regex[i]
                    )
                
            
        return None, None, None
    
    def is_atomic_regex(self, regex):
        for c in regex:
            if c in self.operators:
                return False
        return True

    def build_DFSM_helper(self):
        return self.build_DFSM(self.regex)
    
    def build_DFSM(self, regex):
        if self.is_atomic_regex(regex):
            initial = self.generate_state_name()
            accept = self.generate_state_name()
            return NDFSM({initial, accept}, self.alphabet, {(initial, regex[1:-1]):{accept}}, initial, {accept}) # the atomic regex will be with prantecies e.i => (a)
        
        left, right, operator = self.simplify_regex(regex)
        print(f'left = {left}       right = {right}        operator = {operator}        regex = {regex}')
        left_machine = self.build_DFSM(left) if left is not None else None
        right_machine = self.build_DFSM(right) if right is not None else None

        if operator == '|':
            ''' 
                --- Union ---
                In this case we create a new initial state and
                we will connect it with epsilon transitions to
                the initials states of left_machine & right_machine
            '''
            transitions = {
                **left_machine.transitions,
                **right_machine.transitions,
            }
            new_initial_state = self.generate_state_name()
            transitions[(new_initial_state, None)] = {left_machine.initial_state, right_machine.initial_state}
            return NDFSM(left_machine.states|right_machine.states|{new_initial_state}, 
                          self.alphabet, 
                          transitions, 
                          new_initial_state, 
                          right_machine.accepting_states|left_machine.accepting_states)
        
        if operator == '+':
            ''' 
                --- Kleen Star (plus addition) ---
                In this case we connect all of the accepting states
                of the left machine, to the initial state of the left machine.
            '''
            transitions = {
                **left_machine.transitions
            }
            for accepting_state in left_machine.accepting_states:
                transitions.setdefault((accepting_state, None), set()).add(left_machine.initial_state)


            return NDFSM(left_machine.states,
                         self.alphabet, 
                         transitions,
                         left_machine.initial_state,
                         left_machine.accepting_states)
        
        if operator == '*':
            ''' 
                --- Kleen Star ---
                In this case we connect all of the accepting states
                of the left machine, to the initial state of the left machine.
            '''
            transitions = {
                **left_machine.transitions
            }
            for accepting_state in left_machine.accepting_states:
                transitions.setdefault((accepting_state, None), set()).add(left_machine.initial_state)


            return NDFSM(left_machine.states,
                         self.alphabet, 
                         transitions,
                         left_machine.initial_state,
                         left_machine.accepting_states|{left_machine.initial_state})
        
        if operator == '$':
            ''' 
                --- Concatination ---
                In this case we connect all of the accepting states
                of the left machine, to the initial state of the right machine.
            '''
            transitions = {
                **left_machine.transitions,
                **right_machine.transitions,
            }
            for accepting_state in left_machine.accepting_states:
                transitions.setdefault((accepting_state, None), set()).add(right_machine.initial_state)
            
            return NDFSM(left_machine.states|right_machine.states,
                         self.alphabet, 
                         transitions,
                         left_machine.initial_state,
                         right_machine.accepting_states)