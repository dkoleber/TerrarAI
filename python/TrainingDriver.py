import time

from BridgeListener import Listener
from GameBridge import ActionManager, SequentialAgent
from GameBridge import global_io_adapter




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
