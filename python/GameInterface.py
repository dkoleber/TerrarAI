import http.client
import urllib.request
import threading
import time
import json
from typing import List

from DataTypes import PlayerState, NpcState, WorldSlice

UPDATE_PERIOD = 1 #in seconds

class Listener(threading.Thread):

    def __init__(self, min_update_period=UPDATE_PERIOD,):
        super().__init__()

        self.minimum_update_period = min_update_period

        self.is_running = True
    def run(self):
        while(self.is_running):
            start_time = time.time()
            state = self.get_state()
            if len(state) > 0:
                print(str(state))

            end_time = time.time()
            elapsed = end_time - start_time
            duration = max(self.minimum_update_period - elapsed, 0)
            time.sleep(duration)

    def get_state(self):
        states = []
        url = f'http://localhost:8001/GetState'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    data = response.read()
                    try:
                        state_objects = json.loads(data.decode('utf8'))
                        for state in state_objects:
                            if 'PlayerState' in state['__type']:
                               states.append(PlayerState(state))
                            elif 'NpcState' in state['__type']:
                                states.append(NpcState(state))
                            elif 'WorldSlice' in state['__type']:
                                states.append(WorldSlice(state))
                            # else:
                            #     print(f'unknown state: {state}')
                    except Exception as e:
                        print(f'exception: {e}')
        except Exception as ex:
            print(ex)
        return states

    def stop(self):
        self.is_running = False

    def subscribe_to_player_state(self):
        url = f'http://localhost:8001/SubscribeToPlayerState'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'subscribed to player state: ' + str(response.read()))
                else:
                    print(f'failed to subscribe to player state')
        except:
                    print(f'failed to connect to {url}')

    def unsubscribe_from_player_state(self):
        url = f'http://localhost:8001/UnsubscribeFromPlayerState'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'unsubscribed from player state')
                else:
                    print(f'failed to unsubscribe from player state')
        except:
            print(f'failed to connect to {url}')

    def subscribe_to_npc_state(self, npc_name, nearest_n):
        replaced = npc_name.replace(' ', '+')
        url = f'http://localhost:8001/SubscribeToNpcState?npcName={replaced}&nearestN={nearest_n}'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'subscribed to npc \'{npc_name}\' state: ' + str(response.read()))
                else:
                    print(f'failed to subscribe to npc \'{npc_name}\' state')
        except:
            print(f'failed to connect to {url}')

    def unsubscribe_from_npc_state(self, npc_name):
        replaced = npc_name.replace(' ', '+')
        url = f'http://localhost:8001/UnsubscribeFromNpcState?npcName={replaced}'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'unsubscribed from npc \'{npc_name}\' state')
                else:
                    print(f'failed to unsubscribe from npc \'{npc_name}\' state')
        except:
            print(f'failed to connect to {url}')

    def subscribe_to_unanchored_world_slice(self, x, y, width, height):
        url = f'http://localhost:8001/SubscribeToUnanchoredWorldSlice?x={x}&y={y}&width={width}&height={height}'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'subscribed to slice ({x}+{width}, {y}+{height}) state: ' + str(response.read()))
                else:
                    print(f'failed to subscribe to slice ({x}+{width}, {y}+{height}) state')
        except:
            print(f'failed to connect to {url}')
    def unsubscribe_from_unanchored_world_slice(self, x, y, width, height):
        url = f'http://localhost:8001/UnsubscribeFromUnanchoredWorldSlice?x={x}&y={y}&width={width}&height={height}'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'unsubscribed from slice ({x}+{width}, {y}+{height}) state')
                else:
                    print(f'failed to unsubscribe from slice ({x}+{width}, {y}+{height}) state')
        except:
            print(f'failed to connect to {url}')

    def subscribe_to_anchored_world_slice(self, x_offset, y_offset, width, height):
        url = f'http://localhost:8001/SubscribeToAnchoredWorldSlice?xOffset={x_offset}&yOffset={y_offset}&width={width}&height={height}'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'subscribed to slice ({x_offset}+{width}, {y_offset}+{height}) state: ' + str(response.read()))
                else:
                    print(f'failed to subscribe to slice ({x_offset}+{width}, {y_offset}+{height}) state')
        except:
            print(f'failed to connect to {url}')
    def unsubscribe_from_anchored_world_slice(self, x_offset, y_offset, width, height):
        url = f'http://localhost:8001/UnsubscribeFromUnanchoredWorldSlice?xOffset={x_offset}&yOffset={y_offset}&width={width}&height={height}'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'unsubscribed from slice ({x_offset}+{width}, {y_offset}+{height}) state')
                else:
                    print(f'failed to unsubscribe from slice ({x_offset}+{width}, {y_offset}+{height}) state')
        except:
            print(f'failed to connect to {url}')

    def unsubscribe_from_all(self):
        url = f'http://localhost:8001/UnsubscribeFromAll'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'unsubscribed from all')
                else:
                    print(f'failed to unsubscribe from all')
        except:
            print(f'failed to connect to {url}')


class SpawnConfiguration:
    def __init__(self, npc_name:str, spawn_rate, initial_number):
        self.npc_name = npc_name
        self.spawn_rate = spawn_rate
        self.initial_number = initial_number

class WorldConfiguration:
    def __init__(self, player_configuration:PlayerState, npc_configurations:List[NpcState], spawn_configurations:List[SpawnConfiguration]):
        self.player_configuration = player_configuration #PlayerState
        self.npc_configurations = npc_configurations #List[NpcState]
        self.spawn_configurations = spawn_configurations #List[SpawnConfiguration]

class WorldConfigurer:
    def load_world(self, world_name, player_name):
        url = f'http://localhost:8001/EnterWorld?worldName={world_name}&playerName={player_name}'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'entered world {world_name} as {player_name}: {response.read()}')
                else:
                    print(f'failed to enter world {world_name} as {player_name}')
        except Exception as e:
            print(f'failed to connect to {url}')
            print(e)

    def exit_world(self):
        url = f'http://localhost:8001/ExitWorld'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'exited world: {response.read()}')
                else:
                    print(f'failed to exit world')
        except:
            print(f'failed to connect to {url}')

    def configure_world(self, world_configuration:WorldConfiguration):
        pass #TODO

if __name__=='__main__':
    try:
        listener = Listener(UPDATE_PERIOD)
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

    except:
        time.sleep(10)
