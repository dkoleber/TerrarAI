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
    [KnownType(typeof(PlayerState))]
    [KnownType(typeof(WorldSlice))]
    public class StateObject
    {

    }


    [DataContract]
    public class BuffState
    {
  
    }
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
        public InventoryState(Item[] items, int selectedIndex)
        {
            this.items = new List<InventoryItem>();
            for(int i = 0; i < items.Length; i++)
            {
                Item item = items[i];
                if(item.stack != 0)
                {
                    this.items.Add(new InventoryItem(i, item, i == selectedIndex));
                }
            }
        }
    }

    [DataContract]
    public class PlayerState : StateObject
    {
        public PlayerState(Player player)
        {
            x = player.position.X;
            y = player.position.Y;
            inventoryState = new InventoryState(player.inventory, player.selectedItem);
        }
        [DataMember]
        public float x;
        [DataMember]
        public float y;
        [DataMember]
        public InventoryState inventoryState;
        [DataMember]
        public BuffState buffState;
    }

    [DataContract]
    public class NpcState : StateObject
    {

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
    public class WorldSlice: StateObject
    {   
        [DataMember]
        public WorldSliceSpecifier slice;
    }


    

}
