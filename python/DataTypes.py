import math

import numpy as np
from abc import ABC, abstractmethod

'''
A NOTE ON MASKING

Say we have two arrays representing quantities; the first is the actual and the second is the target.

    actual = [0, 5, 2, 1]
    target = [0, 3, 0, 2]

When the actual is masked by the target, then we get

    masked = [0, 0, 0, 1]

This represents the amount that the target requires to be fulfilled but is unfulfilled.
Algorithmically, this is equal to 

    [max(0, target[x]-actual[x]) for x in range(len(target))]

For non-array types that need to be masked, this is better represented as

    for every attribute in data type:
        mask.attribute = actual.attribute.fulfills(target.attribute) ? 0 : target.attribute - actual.attribute
'''




def euclidian_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)^2 + (y1-y2)^2)

def apply_operator_as_character(value_1, value_2, operator_character):
    if operator_character == '>':
        return value_1 > value_2
    elif operator_character == '>=':
        return value_1 >= value_2
    elif operator_character == '<':
        return value_1 < value_2
    elif operator_character == '<=':
        return value_1 <= value_2
    elif operator_character == '==':
        return value_1 == value_2
    elif operator_character == '!=':
        return value_1 != value_2
    return False

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

class InventoryItem:
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

class InventoryState:
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

class PlayerState:
    def __init__(self, rep, inventory_type=InventoryState):
        self.buff_state = BuffState(rep['buffState'])
        self.x = rep['x']
        self.y = rep['y']
        self.life = rep['life']
        self.max_life = rep['maxLife']
        self.mana = rep['mana']
        self.max_mana = rep['maxMana']
        self.inventory_state = inventory_type(rep['inventoryState'])
    def __str__(self):
        return  '<PlayerState (' + str(self.x) + ', ' + str(self.y) \
                + ') H=(' + str(self.life) + '/' + str(self.max_life) \
                + ') M=(' + str(self.mana) + '/' + str(self.max_mana) \
                + ')>'
                # + ') Inventory=' + str(self.inventory_state) + ' Buffs=' + str(self.buff_state)
    def __repr__(self):
        return self.__str__()

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

class WorldState:
    pass

class StateTarget(ABC):
    @abstractmethod
    def diff(self, actual_state) -> int:
        pass

class InventoryItemTarget(InventoryItem, StateTarget):
    def __init__(self, rep):
        super().__init__(rep)
        # self.function = rep['function']

    def diff(self, actual_state: InventoryItem):
        return self.quantity - actual_state.quantity
    # def get_reward(self, actual_state: InventoryItem):
    #     if apply_operator_as_character(actual_state.quantity, self.quantity, self.function):
    #         return

class InventoryStateTarget(InventoryState, StateTarget):
    def __init__(self, rep):
        super().__init__(rep, item_type=InventoryItemTarget)

    def diff(self, actual_state: InventoryState):
        sum_negative = 0
        sum_positive = 0
        for item in self.items:
            found = False
            for other_item in actual_state.items:
                if item.name == other_item.name:
                    reward = item.diff(other_item)
                    if reward > 0:
                        sum_negative += reward
                    else:
                        sum_positive -= reward
                    found = True
            if not found:
                sum_negative += item.quantity
        if sum_negative == 0:
            return sum_positive
        else:
            return sum_negative

class PlayerStateTarget(PlayerState, StateTarget):
    def __init__(self, rep):
        super().__init__(rep, inventory_type=InventoryStateTarget)
    def diff(self, actual_state: PlayerState):
        rewards = []
        rewards.append((self.x, self.y, actual_state.x, actual_state.y))
        rewards.append(self.life - actual_state.life)
        rewards.append(self.mana - actual_state.mana)
        rewards.append(self.inventory_state.diff(actual_state))
        rewards.append(0)#buff diff

        sum_positive = 0
        sum_negative = 0

        for reward in rewards:
            if reward > 0:
                sum_positive += reward
            else:
                sum_negative -= reward

        if sum_negative > 0:
            return -sum_negative
        else:
            return sum_positive

class NpcStateTarget(NpcState, StateTarget):
    def diff(self, actual_state: NpcState):
        rewards = []
        rewards.append(euclidian_distance(self.x, self.y, actual_state.x, actual_state.y))
        rewards.append(self.life - actual_state.life)

        sum_positive = 0
        sum_negative = 0

        for reward in rewards:
            if reward > 0:
                sum_positive += reward
            else:
                sum_negative -= reward

        if sum_negative > 0:
            return -sum_negative
        else:
            return sum_positive

class WorldSliceTarget(WorldSlice, StateTarget):
    def diff(self, actual_state:WorldSlice):
        incorrect = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.grid[i][j] != -2 and self.grid[i][j] != actual_state.grid[i][j]: #-2 indicates wildcard
                    incorrect += 1
        if incorrect > 0:
            return -incorrect
        else:
            return 1

class WorldStateTarget(WorldState, StateTarget):
    pass