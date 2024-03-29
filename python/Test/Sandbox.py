import http.client
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
import urllib.request
import threading
import time
import json
from typing import List

from Action import ActionManager



from State import PlayerState, NpcState, WorldSlice, StateListener
from WorldConfiguration import WorldConfigurer, WorldConfiguration

UPDATE_PERIOD = 1 #in seconds

def test_world_loading():
    listener = StateListener(UPDATE_PERIOD)
    world_configurer = WorldConfigurer()

    listener.unsubscribe_from_all()
    listener.subscribe_to_player_state()
    listener.subscribe_to_npc_state('Green Slime', 2)
    listener.subscribe_to_npc_state('Zombie', 2)
    listener.subscribe_to_unanchored_world_slice(-1, 0, 2, 2)

    time.sleep(1)

    if world_configurer.enter_world('TESTWORLD1', 'TEST2'):
        for i in range(5):
            print(listener.get_state())
            time.sleep(1)

        if world_configurer.exit_world():
            if world_configurer.enter_world('TESTWORLD2', 'TEST1'):
                for i in range(5):
                    print(listener.get_state())
                    time.sleep(1)
                world_configurer.exit_world()

def get_test_world_configuration():
    config_dict = {
        'npcConfigurations':[
            {'npcName':'Green Slime', 'removeExistingInstances':False, 'spawnRate':40}
        ]
    }

    config = WorldConfiguration(config_dict)
    return config

def get_test_player_configuration():
    config_dict = {
        'life': 50,
        'maxLife':200
    }
    config = PlayerState(config_dict)
    return config


def test_world_configuration():
    world_config = get_test_world_configuration()
    player_config = get_test_player_configuration()


    world_configurer = WorldConfigurer()
    world_configurer.enter_world('TESTWORLD1', 'TEST2')
    # world_configurer.get_dummy_configuration()
    world_configurer.configure_world(world_config)

    world_configurer.configure_player(player_config)

    time.sleep(5)
    world_configurer.exit_world()


def test_screenshot():
    manager = ActionManager()
    print(manager.get_screen().shape)

if __name__=='__main__':
    # test_world_configuration()
    # test_world_loading()
    test_screenshot()
