from Action import ActionSpace
from Agent import AgentFactory, Agent


class HardCodedAction:
    def __init__(self, key, amount, delay, x=None, y=None):
        self.key = key
        self.amount = amount
        self.delay = delay
        self.x = x
        self.y = y


class SequentialAgentFactory(AgentFactory):
    def get_agent(self, action_space_definition: ActionSpace):
        return SequentialAgent(action_space_definition)


class SequentialAgent(Agent):
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

    def apply_reward(self, reward):
        pass