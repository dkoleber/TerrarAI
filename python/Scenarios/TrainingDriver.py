import time
from typing import List

from Agent import AgentFactory
from State import PlayerState
from Test.Sandbox import StateListener, WorldConfigurer
from Action import ActionManager
from Action import global_io_adapter
from Scenarios.Scenarios import ScenarioTrainingSpecification

TRAINING_ROUNDS = 1000



class TrainingDriver:
    def __init__(self, agent_factory:AgentFactory):
        self.manager = ActionManager()
        self.listener = StateListener()
        self.world_configurer = WorldConfigurer()

        self.agent_factory = agent_factory
        self.agent = self.agent_factory.get_agent(self.manager.get_action_space_definition())

    def train(self, scenarios:List[ScenarioTrainingSpecification]):
        for scenario in scenarios:
            self.world_configurer.enter_world(scenario.scenario.world_name, scenario.scenario.player_name)
            self.world_configurer.configure_world(scenario.scenario.world_configuration)
            while True:
                agent_input = self.manager.get_screen()
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

class TrainingDriver2:
    def __init__(self, agent_factory:AgentFactory):
        self.manager = ActionManager()
        self.listener = StateListener()
        self.world_configurer = WorldConfigurer()
        self.agent = agent_factory.get_agent(self.manager.get_action_space_definition())
        self.num_training_steps = 1000
        self.num_training_epochs = 1000
        self.target_world = 'Test_world_1'
        self.target_player = 'Test_player_1'

    def train_epoch(self):
        player_config_dict = {
            'life': 100,
            'maxLife':200
        }
        player_config_init = PlayerState(player_config_dict)

        for step in range(self.num_training_steps):
            self.world_configurer.enter_world(self.target_world, self.target_player)
            self.world_configurer.configure_player(player_config_init)

            game_state_init = self.listener.get_state()
            game_state = self.listener.get_state()
            while True: # Training loop
                agent_input = self.manager.get_screen()
                agent_output = self.agent.get_action(agent_input)
                self.manager.execute_actions(agent_output)
                game_state = self.listener.get_state()
                if (game_state.time_state.ticks - game_state_init.time_state.ticks) > 1000: # Training step termination condition
                    break
            self.world_configurer.exit_world()

            success = game_state.player_state.life > 100
            reward = 1 if success else -1
            self.agent.apply_reward(reward)

    def train(self):
        self.listener.unsubscribe_from_all()
        self.listener.subscribe_to_player_state()
        for epoch in range(self.num_training_epochs):
            self.train_epoch()




def run():
    time.sleep(5)
    # manager = ActionManager()
    # listener = Listener()
    # action_space = manager.get_action_space_definition()
    # agent = SequentialAgent(action_space)
    #
    # while (True):
    #     agent_input = global_io_adapter.get_screen()
    #     agent_output = agent.get_action(agent_input)
    #     manager.execute_actions(agent_output)
    #     game_state = listener.get_state()
    #     # reinforce agent with resulting game state


if __name__=='__main__':
    run()
