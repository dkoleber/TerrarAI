import json
import math
import os
import sys
import threading
import time
import urllib.request

import numpy as np
from abc import ABC, abstractmethod

from SharedDataTypes import Serializable

def remove_duplicates(s):
    res = ''
    for i in range(len(s)):
        if i == 0 or s[i-1] != s[i]:
            res += s[i]
    return res

def remove_vowels(s):
    res = s.replace('a','')
    res = res.replace('e','')
    res = res.replace('i','')
    res = res.replace('o','')
    res = res.replace('u','')
    res = res.replace(' ','')
    return res

def shorten_string(s):
    return remove_duplicates(remove_vowels(s))

class BuffState:
    def __init__(self, rep):
        pass
    def __str__(self):
        return '[]'
    def __repr__(self):
        return self.__str__()

class InventoryItem(Serializable):
    def __init__(self, rep):
        self.name = rep['name']
        self.quantity = rep['quantity']
        self.slot_number = rep['slotNumber']
        self.selected = rep['selected']
    def __str__(self):
        result = shorten_string((str(self.name))) + ' x' + str(self.quantity) + ' (' + str(self.slot_number)
        if self.selected:
            result += '-' + str(self.selected)
        result += ')'
        return result
    def __repr__(self):
        return self.__str__()
    def to_dict(self):
        result = {}
        result['name'] = self.name
        result['quantity'] = self.quantity
        result['slotNumber'] = self.slot_number
        result['selected'] = self.selected
        return result

class InventoryState(Serializable):
    def __init__(self, rep, item_type=InventoryItem):
        self.items = []
        for item in rep['items']:
            self.items.append(item_type(item))
    def __str__(self):
        result = '['
        for item in self.items:
            result += '<' + str(item) + '>, '
        result += ']'
        return result
    def __repr__(self):
        return self.__str__()
    def to_dict(self):
        return {'items':[item.to_dict() for item in self.items]}

class PlayerState(Serializable):
    def __init__(self, rep:dict, inventory_type=InventoryState):
        keys = rep.keys()
        self.buff_state = BuffState(rep['buffState']) if 'buffState' in keys else None
        self.x = rep['x'] if 'x' in keys else -1
        self.y = rep['y'] if 'y' in keys else -1
        self.life = rep['life'] if 'life' in keys else -1
        self.max_life = rep['maxLife'] if 'maxLife' in keys else -1
        self.mana = rep['mana'] if 'mana' in keys else -1
        self.max_mana = rep['maxMana'] if 'maxMana' in keys else -1
        self.inventory_state = inventory_type(rep['inventoryState']) if 'inventoryState' in keys else None
    def __str__(self):
        return  '<PlayerState (' + str(self.x) + ', ' + str(self.y) \
                + ') H=(' + str(self.life) + '/' + str(self.max_life) \
                + ') M=(' + str(self.mana) + '/' + str(self.max_mana) \
                + ')>'
                # + ') Inventory=' + str(self.inventory_state) + ' Buffs=' + str(self.buff_state)
    def __repr__(self):
        return self.__str__()
    def to_dict(self):
        result = {}
        result['buffState'] = None
        result['inventoryState'] = self.inventory_state.to_dict() if self.inventory_state is not None else None
        result['life'] = self.life
        result['maxLife'] = self.max_life
        result['mana'] = self.mana
        result['maxMana'] = self.max_mana
        result['x'] = self.x
        result['y'] = self.y
        return result

class NpcState:
    def __init__(self, rep):
        self.name = rep['name']
        self.x = rep['x']
        self.y = rep['y']
        self.life = rep['life']
        self.max_life = rep['maxLife']
    def __str__(self):
        return  f'<NpcState \'{self.name}\' ({self.x}, {self.y}) H=({self.life}/{self.max_life})>'
    def __repr__(self):
        return self.__str__()

class WorldSlice:
    def __init__(self, rep):
        self.x = rep['slice']['x']
        self.y = rep['slice']['y']
        self.width = rep['slice']['width']
        self.height = rep['slice']['height']
        self.grid = np.array(rep['data'])

    def __str__(self):
        result = f'<WorldSlice ({self.x}+{self.width}, {self.y}+{self.height})'
        # result += f' [{self.grid.flatten()}]'
        result += '>'
        return result
    def __repr__(self):
        return self.__str__()

class Timestate:
    def __init__(self, rep):
        self.ticks = rep['worldTicks']

class GameState:
    def __init__(self):
        self.player_state = None
        self.time_state = None
        self.npc_states = []
        self.slices = []

class StateListener(threading.Thread):

    def __init__(self, min_update_period=1):
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

    def get_state(self) -> GameState:
        game_state = GameState()
        url = f'http://localhost:8001/GetState'
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    data = response.read()
                    try:
                        state_objects = json.loads(data.decode('utf8'))
                        for state in state_objects:
                            if 'PlayerState' in state['__type']:
                                game_state.player_state = PlayerState(state)
                            elif 'NpcState' in state['__type']:
                                game_state.npc_states.append(NpcState(state))
                            elif 'WorldSlice' in state['__type']:
                                game_state.slices.append(WorldSlice(state))
                            # else:
                            #     print(f'unknown state: {state}')
                    except Exception as e:
                        print(f'exception: {e}')
        except Exception as ex:
            print(ex)
        return game_state

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

