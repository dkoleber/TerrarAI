import urllib.request
from typing import List

from State import PlayerState, NpcState


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