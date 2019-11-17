import time

from Agent import SequentialAgent
from Action import ActionManager
from Action import global_io_adapter

class GameDriver:
    pass

def run():
    time.sleep(5)
    manager = ActionManager()
    action_space = manager.get_action_space_definition()
    agent = SequentialAgent(action_space)

    while (True):
        agent_input = global_io_adapter.get_screen()
        agent_output = agent.get_action(agent_input)
        manager.execute_actions(agent_output)


if __name__=='__main__':
    run()
