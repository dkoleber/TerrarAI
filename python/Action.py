from enum import Enum
from typing import List
from abc import ABC, abstractmethod

from Backend.IOAdapter import IOAdapter


global_io_adapter = IOAdapter()


class IOAction(ABC):
    def __init__(self, is_held):
        self.is_held = is_held

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def extend(self):
        pass


class KeyAction(IOAction):
    def __init__(self, is_held, key):
        super().__init__(is_held)
        self.key = key

    def __eq__(self, other):
        if isinstance(other, KeyAction):
            return self.key == other.key and self.is_held == other.is_held
        else:
            return super().__eq__(other)

    def start(self):
        print('staring key ' + self.key)
        if not self.is_held:
            global_io_adapter.key(self.key)
        else:
            global_io_adapter.key_down(self.key)

    def end(self):
        print('ending key ' + self.key)
        if self.is_held:
            global_io_adapter.key_up(self.key)

    def extend(self):
        print('extending key ' + self.key)
        if not self.is_held:
            global_io_adapter.key(self.key)


class MouseAction(IOAction):
    def __init__(self, is_held, key, x=None, y=None ):
        super().__init__(is_held)
        self.key = key
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, MouseAction):
            return self.key == other.key and self.x == other.x and self.y == other.y and self.is_held == other.is_held
        else:
            return super().__eq__(other)

    def start(self):
        if self.key == 'mouse_move' and self.x is not None and self.y is not None:
            global_io_adapter.mouse_move_relative(self.x, self.y)
        elif self.key == 'mouse_left':
            if not self.is_held:
                global_io_adapter.left_click()
            else:
                global_io_adapter.left_mouse_down()
        elif self.key == 'mouse_right':
            if not self.is_held:
                global_io_adapter.right_click()
            else:
                global_io_adapter.right_mouse_down()

    def end(self):
        if self.key == 'mouse_left' and self.is_held:
            global_io_adapter.left_mouse_up()
        elif self.key == 'mouse_right' and self.is_held:
            global_io_adapter.left_mouse_up()

    def extend(self):
        if self.key == 'mouse_left' and not self.is_held:
            global_io_adapter.left_click()
        elif self.key == 'mouse_right' and not self.is_held:
            global_io_adapter.right_click()


class IOActions:
    def __init__(self, actions:List[IOAction]):
        self.actions = actions

    def start(self):
        for action in self.actions:
            action.start()

    def end(self):
        for action in self.actions:
            action.end()

    def extend(self):
        for action in self.actions:
            action.extend()

    def __eq__(self, other):
        if isinstance(other, IOActions):
            if len(other.actions) != len(self.actions):
                return False
            for i in range(len(self.actions)):
                if other.actions[i] != self.actions[i]:
                    return False
            return True
        else:
            return super().__eq__(other)


class ActionType(Enum):
    REAL = 0
    '''
    [0, .33) = action not taken
    [.33, .66) = action taken
    [.66, 1] = action held 
    '''
    PROBABILITY = 0


class ActionDefinition:
    def __init__(self, name, action_type):
        self.name = name
        self.action_type = action_type


class ActionSpace:
    def __init__(self, definition: List[ActionDefinition]):
        self.definition = definition

    def verify_action_vector(self, vector:List[float]):
        if len(vector) != len(self.definition):
            return False
        return True


class ActionManager:
    def __init__(self):
        self.adapter = global_io_adapter
        # self.queue = Queue()
        self.space_definition = self.get_action_space_definition()
        self.previous_actions = None

    def execute_actions(self, action_vector:List[float]):
        if self.space_definition.verify_action_vector(action_vector):
            new_actions = self.io_actions_from_action_vector(action_vector)
            if new_actions is not None:
                if self.previous_actions == new_actions:
                    self.previous_actions.extend()
                else:
                    if self.previous_actions is not None:
                        self.previous_actions.end()
                    new_actions.start()
                    self.previous_actions = new_actions

    def get_action_space_definition(self) -> ActionSpace:
        action_names = ['mouse_left', 'mouse_right']
        action_names.extend(self.adapter.get_available_keys())
        result = [
            ActionDefinition('mouse_x', ActionType.REAL),
            ActionDefinition('mouse_y', ActionType.REAL),
        ]
        result.extend([ActionDefinition(name, ActionType.PROBABILITY) for name in action_names])
        return ActionSpace(result)

    def io_actions_from_action_vector(self, action_vector: List[float]) -> IOActions:
        actions = [MouseAction(False, 'mouse_move', action_vector[0], action_vector[1])]
        for i in range(2,4):
            if action_vector[i] > .66:
                actions.append(MouseAction(True, self.space_definition.definition[i].name))
            elif action_vector[i] > .33:
                actions.append(MouseAction(False, self.space_definition.definition[i].name))
        for i in range(4, len(action_vector)):
            if action_vector[i] > .66:
                actions.append(KeyAction(True, self.space_definition.definition[i].name))
            elif action_vector[i] > .33:
                actions.append(KeyAction(False, self.space_definition.definition[i].name))

        return IOActions(actions)

    def get_screen(self):
        return global_io_adapter.get_screen()


