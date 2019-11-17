import http.client
import os
import sys
import urllib.request
import threading
import time
import json
from typing import List

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

from State import PlayerState, NpcState, WorldSlice, StateListener
from WorldConfiguration import WorldConfigurer

UPDATE_PERIOD = 1 #in seconds

if __name__=='__main__':
    try:
        listener = StateListener(UPDATE_PERIOD)
        world_configurer = WorldConfigurer()

        listener.unsubscribe_from_all()
        listener.subscribe_to_player_state()
        listener.subscribe_to_npc_state('Green Slime', 2)
        listener.subscribe_to_npc_state('Zombie', 2)
        listener.subscribe_to_unanchored_world_slice(-1, 0, 2, 2)
        listener.start()
        time.sleep(1)

        world_configurer.load_world('TESTWORLD1', 'TEST2')

        time.sleep(5)

        world_configurer.exit_world()

        world_configurer.load_world('TESTWORLD2', 'TEST1')
        time.sleep(5)
        world_configurer.exit_world()
        time.sleep(2)
        listener.stop()

    except:
        time.sleep(10)
