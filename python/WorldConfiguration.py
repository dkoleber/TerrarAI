import json
import os
import urllib.request
from abc import ABC, abstractmethod
from typing import List, Tuple
from shutil import copyfile

from SharedDataTypes import Serializable
from State import PlayerState, NpcState

HERE = os.path.dirname(os.path.abspath(__file__))

RESOURCES_PATH = '../res/'
WORLDS_DIR_NAME = 'worlds'
PLAYERS_DIR_NAME = 'players'
MODLOADER_WORLDS_DIR_NAME = 'Worlds'
MODLOADER_PLAYERS_DIR_NAME = 'Players'

def init_resource_dirs():
    dirs = [os.path.join(HERE, RESOURCES_PATH, x) for x in [WORLDS_DIR_NAME, PLAYERS_DIR_NAME]]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

init_resource_dirs()

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

def all_files_exist(files:List[str]) -> bool:
    for file in files:
        if not os.path.exists(file):
            return False
    return True

def remove_if_exists(file:str):
    if os.path.exists(file):
        os.remove(file)

class WorldConfigurer:
    def __init__(self, url='http://localhost:8001', resource_dir_abs_path=None):
        self.url = url
        self.resource_dir = resource_dir_abs_path
        if self.resource_dir is None:
            self.resource_dir = os.path.join(HERE, RESOURCES_PATH)
        self.modloader_resource_dir = os.path.join(HERE, '../../../')

        self.current_world_name = None
        self.current_player_name = None
        self.world_from_backup = False
        self.player_from_backup = False

    def enter_world(self, world_name, player_name) -> bool:
        if self.current_player_name is not None or self.current_world_name is not None:
            return False

        enter_success = False

        self.world_from_backup = False
        self.player_from_backup = False

        world_file_names = [world_name + y for y in ['.twld', '.twld.bak', '.wld', '.wld.bak']]
        player_file_names = [player_name + y for y in ['.plr', '.plr.bak', '.tplr', '.tplr.bak']]

        world_files = [os.path.join(self.resource_dir, WORLDS_DIR_NAME, x) for x in world_file_names]
        player_files = [os.path.join(self.resource_dir, PLAYERS_DIR_NAME, x) for x in player_file_names]

        if all_files_exist(world_files):
            for i in range(len(world_files)):
                dest_path = os.path.join(self.modloader_resource_dir, MODLOADER_WORLDS_DIR_NAME, world_file_names[i])
                remove_if_exists(dest_path)
                copyfile(world_files[i], dest_path)
            self.world_from_backup = True
        else:
            world_files_default = [os.path.join(self.modloader_resource_dir, MODLOADER_WORLDS_DIR_NAME, x) for x in world_file_names]
            if not all_files_exist(world_files_default):
                print(f'could not find \'{world_name}\' world files')
                return False

        if all_files_exist(player_files):
            for i in range(len(player_files)):
                dest_path = os.path.join(self.modloader_resource_dir, MODLOADER_PLAYERS_DIR_NAME, player_file_names[i])
                remove_if_exists(dest_path)
                copyfile(player_files[i], dest_path)
            self.player_from_backup = True
        else:
            player_files_default = [os.path.join(self.modloader_resource_dir, MODLOADER_PLAYERS_DIR_NAME, x) for x in player_file_names]
            if not all_files_exist(player_files_default):
                print(f'could not find \'{player_name}\' player files')
                return False

        self.current_world_name = world_name
        self.current_player_name = player_name

        url = f'{self.url}/EnterWorld?worldName={world_name}&playerName={player_name}'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    response_data = response.read().decode('utf-8')
                    enter_success = 'true' in response_data
                else:
                    print(f'failed call to enter world {world_name} as {player_name}')
        except Exception as e:
            print(f'failed to connect to {url}')
            print(e)

        if not enter_success:
            print(f'failed to enter world {world_name} as {player_name}')
            if self.world_from_backup:
                for file in world_file_names:
                    dest_path = os.path.join(self.modloader_resource_dir, MODLOADER_WORLDS_DIR_NAME, file)
                    remove_if_exists(dest_path)
            if self.player_from_backup:
                for file in player_file_names:
                    dest_path = os.path.join(self.modloader_resource_dir, MODLOADER_PLAYERS_DIR_NAME, file)
                    remove_if_exists(dest_path)
            self.current_player_name = None
            self.current_world_name = None
            self.world_from_backup = False
            self.player_from_backup = False
        else:
            print(f'entered world {world_name} as {player_name}')

        return enter_success

    def exit_world(self) -> bool:
        if self.current_player_name is None or self.current_world_name is None:
            return False

        exit_success = False

        url = f'{self.url}/ExitWorld'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    response_data = response.read().decode('utf-8')
                    exit_success = 'true' in response_data
                else:
                    print(f'failed call to exit world')
        except:
            print(f'failed to connect to {url}')

        if exit_success:
            print(f'exited world {self.current_world_name} as {self.current_player_name}')
            if self.world_from_backup:
                world_file_names = [self.current_world_name + y for y in ['.twld', '.twld.bak', '.wld', '.bak']]
                for file in world_file_names:
                    dest_path = os.path.join(self.modloader_resource_dir, 'Worlds', file)
                    remove_if_exists(dest_path)

            if self.player_from_backup:
                player_file_names = [self.current_player_name + y for y in ['.plr', '.plr.bak', '.tplr', '.tplr.bak']]
                for file in player_file_names:
                    dest_path = os.path.join(self.modloader_resource_dir, 'Players', file)
                    remove_if_exists(dest_path)

            self.current_world_name = None
            self.current_player_name = None
        else:
            print(f'failed to exit world {self.current_world_name} as {self.current_player_name}')

        return exit_success

    def configure_world(self, world_configuration:WorldConfiguration):
        url = f'{self.url}/ConfigureWorld'
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
        url = f'{self.url}/ConfigurePlayer'
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
        url = f'{self.url}/GetDummyConfiguration'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    print(f'config: {response.read()}')
                else:
                    print(f'failed to get configuration')
        except:
            print(f'failed to connect to {url}')