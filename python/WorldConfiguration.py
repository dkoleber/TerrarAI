import json
import urllib.request
from abc import ABC, abstractmethod
from typing import List, Tuple

from SharedDataTypes import Serializable
from State import PlayerState, NpcState



class NpcConfiguration(Serializable):
    '''
    coordinates come in as [x, y] (as an array)
    coordinates go out as {"x": x, "y": y} (as a dict)

    '''
    def __init__(self, rep:dict):
        keys = rep.keys()
        self.npc_name = rep['npcName']
        self.spawn_rate = rep['spawnRate'] if 'spawnRate' in keys else -1
        self.initial_locations = rep['initialLocations'] if 'initialLocations' in keys else []
        self.remove_instances = rep['removeInitialInstances'] if 'removeInitialInstances' in keys else False
    def to_dict(self):
        result = {}
        result['initialLocations'] = []
        for coord in self.initial_locations:
            result['initialLocations'].append({'x': coord[0], 'y': coord[1]})
        result['npcName'] = self.npc_name
        result['removeExistingInstances'] = self.remove_instances
        result['spawnRate'] = self.spawn_rate
        return result
    def __str__(self):
        return f'<NpcConfig {self.npc_name} x{len(self.initial_locations)} @{self.spawn_rate} ({self.remove_instances})>'
    def __repr__(self):
        return str(self)

class WorldConfiguration(Serializable):
    def __init__(self, rep:dict):
        keys = rep.keys()
        self.npc_configurations = [NpcConfiguration(x) for x in rep['npcConfigurations']] if 'npcConfigurations' in keys else []
    def to_dict(self):
        return {'npcConfigurations':[x.to_dict() for x in self.npc_configurations]}
    def __str__(self):
        return f'<Wcfg {[str(x) for x in self.npc_configurations]}>'
    def __repr__(self):
        return str(self)

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
        url = f'http://localhost:8001/ConfigureWorld'
        try:
            request = urllib.request.Request(url, data=bytearray(json.dumps(world_configuration.to_dict()), encoding='utf-8'))
            request.add_header('Content-Type', 'application/json')
            request.method = 'POST'
            with urllib.request.urlopen(request) as response:
                if response.status == 200:
                    print(f'set world configuration: {response.read()}')
                else:
                    print(f'failed to set configuration')
        except Exception as e:
            print(f'failed to connect to {url}: {e}')

    def configure_player(self, player_configuration:PlayerState):
        url = f'http://localhost:8001/ConfigurePlayer'
        try:
            request = urllib.request.Request(url, data=bytearray(json.dumps(player_configuration.to_dict()), encoding='utf-8'))
            request.add_header('Content-Type', 'application/json')
            request.method = 'POST'
            with urllib.request.urlopen(request) as response:
                if response.status == 200:
                    print(f'set world configuration: {response.read()}')
                else:
                    print(f'failed to set configuration')
        except Exception as e:
            print(f'failed to connect to {url}: {e}')

    def get_dummy_configuration(self):
        url = f'http://localhost:8001/GetDummyConfiguration'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'config: {response.read()}')
                else:
                    print(f'failed to get configuration')
        except:
            print(f'failed to connect to {url}')