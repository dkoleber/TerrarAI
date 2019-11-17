import numpy as np

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
    def __init__(self, rep):
        self.items = []
        for item in rep['items']:
            self.items.append(InventoryItem(item))
    def __str__(self):
        result = '['
        for item in self.items:
            result += '<' + str(item) + '>, '
        result += ']'
        return result
    def __repr__(self):
        return self.__str__()

class PlayerState:
    def __init__(self, rep):
        self.buff_state = BuffState(rep['buffState'])
        self.x = rep['x']
        self.y = rep['y']
        self.life = rep['life']
        self.max_life = rep['maxLife']
        self.mana = rep['mana']
        self.max_mana = rep['maxMana']
        self.inventory_state = InventoryState(rep['inventoryState'])
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