import time
from abc import ABC, abstractmethod
from typing import List

from Action import ActionSpace


class Agent(ABC):
    def __init__(self, action_space: ActionSpace):
        self.action_space = action_space

    @abstractmethod
    def get_action(self, agent_input):
        pass
    @abstractmethod
    def apply_reward(self, reward):
        pass


class AgentFactory(ABC):
    @abstractmethod
    def get_agent(self, action_space_definition: ActionSpace):
        pass