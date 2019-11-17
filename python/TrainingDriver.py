import time
from typing import List

from Agent import SequentialAgent, AgentFactory
from GameInterface import Listener, WorldConfigurer
from Action import ActionManager
from Action import global_io_adapter

TRAINING_ROUNDS = 1000

class Scenario:
    def __init__(self, rep):
        self.world_name = rep['world_name']
        self.player_name = rep['player_name']
        self.world_configuration = rep['world_configuration']
        self.success_state = rep['success_state']
        self.failure_state = rep['failure_state']

class ScenarioTrainingSpecification:
    def __init__(self, scenario: Scenario, rounds=TRAINING_ROUNDS, weight=1):
        self.scenario = scenario
        self.rounds = rounds
        self.weight = weight

class TrainingDriver:
    def __init__(self, agent_factory:AgentFactory):
        self.manager = ActionManager()
        self.listener = Listener()
        self.world_configurer = WorldConfigurer()

        self.agent_factory = agent_factory
        self.agent = self.agent_factory.get_agent(self.manager.get_action_space_definition())

    def train(self, scenarios:List[ScenarioTrainingSpecification]):
        shuffled_scenarios = scenarios #TODO
        for scenario in shuffled_scenarios:
            self.world_configurer.load_world(scenario.scenario.world_name, scenario.scenario.player_name)
            self.world_configurer.configure_world(scenario.scenario.world_configuration)
            while True:
                agent_input = global_io_adapter.get_screen()
                agent_output = self.agent.get_action(agent_input)
                self.manager.execute_actions(agent_output)
                game_state = self.listener.get_state()
                success_state = scenario.scenario.success_state.diff(game_state)
                failure_state = scenario.scenario.failure_state.diff(game_state)
                if failure_state > 0:
                    self.agent.apply_reward(-failure_state)
                    break
                elif success_state > 0:
                    self.agent.apply_reward(success_state)
                    break
            self.world_configurer.exit_world()





def run():
    time.sleep(5)
    manager = ActionManager()
    listener = Listener()
    action_space = manager.get_action_space_definition()
    agent = SequentialAgent(action_space)

    while (True):
        agent_input = global_io_adapter.get_screen()
        agent_output = agent.get_action(agent_input)
        manager.execute_actions(agent_output)
        game_state = listener.get_state()
        # reinforce agent with resulting game state


if __name__=='__main__':
    run()
