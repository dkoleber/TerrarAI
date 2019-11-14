from enum import Enum
from queue import Queue
from typing import List
import threading
from abc import ABC, abstractmethod

import pyautogui as pg
import time
from IOAdapter import IOAdapter



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
        else:
            if not self.is_held:
                global_io_adapter.click()
            else:
                global_io_adapter.mouse_down()

    def end(self):
        if self.key == 'mouse_click' and self.is_held:
            global_io_adapter.mouse_up()

    def extend(self):
        if self.key == 'mouse_click' and not self.is_held:
            global_io_adapter.click()


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
        action_names = ['mouse_click']
        action_names.extend(self.adapter.get_available_keys())
        result = [
            ActionDefinition('mouse_x', ActionType.REAL),
            ActionDefinition('mouse_y', ActionType.REAL),
        ]
        result.extend([ActionDefinition(name, ActionType.PROBABILITY) for name in action_names])
        return ActionSpace(result)

    def io_actions_from_action_vector(self, action_vector: List[float]) -> IOActions:
        actions = [MouseAction(False, 'mouse_move', action_vector[0], action_vector[1])]
        for i in range(2,3):
            if action_vector[i] > .66:
                actions.append(MouseAction(True, self.space_definition.definition[i].name))
            elif action_vector[i] > .33:
                actions.append(MouseAction(False, self.space_definition.definition[i].name))
        for i in range(3, len(action_vector)):
            if action_vector[i] > .66:
                actions.append(KeyAction(True, self.space_definition.definition[i].name))
            elif action_vector[i] > .33:
                actions.append(KeyAction(False, self.space_definition.definition[i].name))

        return IOActions(actions)

class HardCodedAction:
    def __init__(self, key, amount, delay, x=None, y=None):
        self.key = key
        self.amount = amount
        self.delay = delay
        self.x = x
        self.y = y


class BaseAgent(ABC):
    def __init__(self, action_space: ActionSpace):
        self.action_space = action_space

    @abstractmethod
    def get_action(self, agent_input):
        pass

class SequentialAgent(BaseAgent):
    def __init__(self, action_space: ActionSpace):
        super().__init__(action_space)

        self.key_translator = {}
        for i in range(len(self.action_space.definition)):
            self.key_translator[self.action_space.definition[i].name] = i

        self.movement_sequence = [
            # HardCodedAction('1', .4, 3),
            # HardCodedAction('2', .4, 3),
            # HardCodedAction('a', .7, 3),
            # HardCodedAction('a', .7, 3),
            # HardCodedAction('a', .4, 3),
            # HardCodedAction('a', .0,  1),
            # HardCodedAction('d', .4, 3),
            # HardCodedAction('d', .0, 1),
            # HardCodedAction('space', .4,  1),
            HardCodedAction('a', .0,  1, 100, 100),
        ]


    def get_action(self, agent_input) -> List[float]:
        result = [0. for x in range(len(self.action_space.definition))]
        if len(self.movement_sequence) > 0:
            movement = self.movement_sequence[0]

            result[self.key_translator[movement.key]] = movement.amount
            if movement.x is not None and movement.y is not None:
                result[self.key_translator['mouse_x']] = movement.x
                result[self.key_translator['mouse_y']] = movement.y

            time.sleep(movement.delay)
            del self.movement_sequence[0]

        return result


def run():
    time.sleep(5)
    manager = ActionManager()
    action_space = manager.get_action_space_definition()
    agent = SequentialAgent(action_space)

    while(True):
        agent_input = global_io_adapter.get_screen()
        agent_output = agent.get_action(agent_input)
        manager.execute_actions(agent_output)




if __name__=='__main__':
    run()