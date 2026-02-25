class StateMachine:
    transitions = {
        "TODO": ["IN_PROGRESS", "CANCELLED"],
        "IN_PROGRESS": ["DONE", "TODO", "CANCELLED"],
        "DONE": ["TODO"],
        "CANCELLED": [],
    }

    def __init__(self):
        pass

    def can_transition(self, from_state, to_state):
        final_states = self.transitions.get(from_state, [])
        return to_state in final_states


sm = StateMachine()

print(sm.can_transition("TODO", "DONE"))
print(sm.can_transition("TODO", "IN_PROGRESS"))
print(sm.can_transition("CANCELED", "IN_PROGRESS"))
