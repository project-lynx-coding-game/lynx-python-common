from typing import Union
from enum import Enum
from typing import Callable
from abc import ABC, abstractmethod


class Transition:
    def __init__(self, from_state: Union[str, Enum], to_state: Union[str, Enum], condition_func: Callable[[], bool]):
        self.from_state = from_state
        self.to_state = to_state
        self.condition_func = condition_func


class StateMachine(ABC):
    """
    Simple state machine.
    It checks transitions, and moves one state at a time (if possible) during tick() method.
    States can be virtually anything, but best kept as either strings or enums.
    """

    def __init__(self):
        self._state = None
        self._previous_state = None
        self._states = {}
        self._transitions = {}

    @abstractmethod
    def _state_logic(self):
        pass

    def _get_transition(self):
        for transition in self._transitions[self._state]:
            if transition.condition_func():
                return transition.to_state
        return None

    @abstractmethod
    def _enter_state(self, new_state: Union[str, Enum], old_state: Union[str, Enum]):
        pass

    @abstractmethod
    def _exit_state(self, old_state: Union[str, Enum], new_state: Union[str, Enum]):
        pass

    def set_state(self, new_state: Union[str, Enum]):
        self._previous_state = self._state
        self._state = new_state
        if self._previous_state:
            self._exit_state(self._previous_state, new_state)
        if new_state:
            self._enter_state(new_state, self._previous_state)

    def add_state(self, state: Union[str, Enum]):
        self._states[state] = state
        self._transitions[state] = []
        return self

    def add_transition(self, from_state: Union[str, Enum], to_state: Union[str, Enum], condition_func: Callable[[], bool]):
        self._transitions[from_state].append(Transition(from_state, to_state, condition_func))
        return self

    def tick(self):
        if self._state:
            self._state_logic()
            transition = self._get_transition()
            if transition:
                self.set_state(transition)
