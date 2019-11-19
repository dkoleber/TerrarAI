using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;

namespace PythonBridge
{
    using Terraria;


    [DataContract]
    public class BuffState
    {}
    [DataContract]
    public class InventoryItem
    {
        public InventoryItem(int slot, Item item, bool selected)
        {
            slotNumber = slot;
            name = item.Name;
            quantity = item.stack;
            this.selected = selected;
        }
        public InventoryItem(string name, int slot, int quantity, bool selected)
        {
            this.name = name;
            this.quantity = quantity;
            this.slotNumber = slot;
            this.selected = selected;
        }
        [DataMember]
        public string name;
        [DataMember]
        public int slotNumber;
        [DataMember]
        public int quantity;
        [DataMember]
        public bool selected;
    }

    [DataContract]
    public class InventoryState
    {
        [DataMember]
        public List<InventoryItem> items;
        public InventoryState(Item[] items, int selectedIndex) : this()
        {
            for(int i = 0; i < items.Length; i++)
            {
                Item item = items[i];
                if(item.stack != 0)
                {
                    this.items.Add(new InventoryItem(i, item, i == selectedIndex));
                }
            }
        }
        public InventoryState()
        {
            this.items = new List<InventoryItem>();
        }
    }

    [DataContract]
    public class PlayerState
    {
        public PlayerState(Player player)
        {
            x = player.position.X;
            y = player.position.Y;
            inventoryState = new InventoryState(player.inventory, player.selectedItem);
            life = player.statLife;
            maxLife = player.statLifeMax;
            mana = player.statMana;
            maxMana = player.statManaMax;
        }
        public PlayerState(int x, int y, int life, int maxLife, int mana, int maxMana, InventoryState invState)
        {
            this.x = x;
            this.y = y;
            this.life = life;
            this.maxLife = maxLife;
            this.mana = mana;
            this.maxMana = maxMana;
            this.inventoryState = invState;
        }
        public PlayerState() : this(-1, -1, -1, -1, -1, -1, null) { }
        [DataMember]
        public float x;
        [DataMember]
        public float y;
        [DataMember]
        public int life;
        [DataMember]
        public int maxLife;
        [DataMember]
        public int mana;
        [DataMember]
        public int maxMana;

        [DataMember]
        public InventoryState inventoryState;
        [DataMember]
        public BuffState buffState;
    }

    [DataContract]
    public class NpcState
    {
        
        [DataMember]
        public float x;
        [DataMember]
        public float y;
        [DataMember]
        public int life;
        [DataMember]
        public int maxLife;

        public NpcState(NPC npc)
        {
            life = npc.life;
            maxLife = npc.lifeMax;
            x = npc.position.X;
            y = npc.position.Y;
        }
        public NpcState()
        {
            life = 0;
            maxLife = 0;
            x = 0;
            y = 0;
        }
    }

    [DataContract]
    public class NpcTypeState
    {
        [DataMember]
        public string npcName;
        [DataMember]
        public List<NpcState> npcStates;
        public NpcTypeState(string npcName) : this()
        {
            this.npcName = npcName;
        }
        public NpcTypeState()
        {
            this.npcStates = new List<NpcState>();
        }
    }

    [DataContract]
    public class WorldSliceSpecifier
    {
        public WorldSliceSpecifier(int x, int y, int width, int height)
        {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
        }
        [DataMember]
        public int x;
        [DataMember]
        public int y;
        [DataMember]
        public int width;
        [DataMember]
        public int height;
        public bool Equals(WorldSliceSpecifier other)
        {
            return this.x == other.x
                && this.y == other.y
                && this.width == other.width
                && this.height == other.height;
        }
    }

    [DataContract]
    public class WorldSlice
    {
        [DataMember]
        public WorldSliceSpecifier slice;
        [DataMember]
        public int[][] data;
        public WorldSlice(Tile[,] tiles, int x, int y, int width, int height) : this(tiles, new WorldSliceSpecifier(x, y, width, height)) { }

        public WorldSlice(Tile[,] tiles, WorldSliceSpecifier specifier)
        {
            this.slice = specifier;
            this.data = new int[specifier.width][];
            for (int i = 0; i < specifier.width; i++)
            {
                this.data[i] = new int[specifier.height];
                for (int j = 0; j < specifier.height; j++)
                {
                    var refTile = tiles[specifier.x + i, specifier.y + j];
                    this.data[i][j] = refTile.active() ? refTile.type : -1;
                }
            }
        }
        public WorldSlice(WorldSliceSpecifier specifier)
        {
            this.slice = specifier;
            this.data = new int[0][];
        }
    }

    [DataContract]
    public class TimeState
    {
        [DataMember]
        public uint worldTicks;

        public TimeState(uint ticks)
        {
            worldTicks = ticks;
        }
    }

    [DataContract]
    public class GameState
    {
        [DataMember]
        public TimeState timeState;
        [DataMember]
        public PlayerState playerState;
        [DataMember]
        public List<NpcTypeState> npcStates;
        [DataMember]
        public List<WorldSlice> unanchoredWorldSlices;
        [DataMember]
        public List<WorldSlice> anchoredWorldSlices;
        [DataMember]
        public string errorMessage;
        public GameState()
        {
            this.npcStates = new List<NpcTypeState>();
            this.unanchoredWorldSlices = new List<WorldSlice>();
            this.anchoredWorldSlices = new List<WorldSlice>();
        }
    }

}
