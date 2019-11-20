using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Terraria;
using Terraria.ModLoader;

namespace PythonBridge
{
    public class WorldInterface
    {
        public void SetWindowTitle(string title)
        {
            ReLogic.OS.Platform.Current.SetWindowUnicodeTitle(Main.instance.Window, title);
        }



        #region State

        public PlayerState GetPlayerState()
        {
            return new PlayerState(Main.player[Terraria.Main.myPlayer]);
        }

        public NpcTypeState GetNpcState(string npcName, int nearestN)
        {
            var state = new NpcTypeState(npcName);
            var closest = new List<float>();
            var matchingNpcs = Main.npc.ToList().Where(x => x.FullName.Contains(npcName) && x.life > 0).ToList();
            if (matchingNpcs.Count > nearestN)
            {
                foreach (NPC npc in matchingNpcs)
                {
                    state.npcStates.Add(new NpcState(npc));
                }
            }
            else
            {
                foreach (NPC npc in matchingNpcs)
                {
                    var distance = DistanceFromPlayer(npc);
                    for (int i = 0; i < closest.Count; i++)
                    {
                        if (distance < closest[i])
                        {
                            closest.Insert(i, distance);
                            state.npcStates.Insert(i, new NpcState(npc));
                            if (closest.Count > nearestN)
                            {
                                closest.RemoveAt(nearestN);
                                state.npcStates.RemoveAt(nearestN);
                            }
                            break;
                        }
                    }
                    if (closest.Count < nearestN)
                    {
                        state.npcStates.Add(new NpcState(npc));
                        closest.Add(distance);
                    }
                }
            }

            return state;
        }

        public bool IsWorldLoaded()
        {
            return WorldGen.loadSuccess && !Main.gameMenu;
        }
        public WorldSlice GetUnanchoredWorldSlice(WorldSliceSpecifier slice)
        {
            //var playerPos = Main.player[Main.myPlayer].Center.ToTileCoordinates();
            var playerPos = Main.LocalPlayer.Center.ToTileCoordinates();
            var offset = new WorldSliceSpecifier(slice.x + playerPos.X, slice.y + playerPos.Y, slice.width, slice.height);
            return new WorldSlice(Main.tile, offset);
        }

        public WorldSlice GetAnchoredWorldSlice(WorldSliceSpecifier slice)
        {
            return new WorldSlice(Main.tile, slice);
        }

        public TimeState GetTimeState()
        {
            return new TimeState(Main.GameUpdateCount);
        }

        #endregion

        #region World Configuration

        public bool EnterWorld(string worldName, string playerName)
        {
            try
            {
                WorldGen.clearWorld();
                Main.LoadPlayers();
                Main.LoadWorlds();


                var worldFileData = Main.WorldList.Where(x => x.Name.Contains(worldName));
                var player = Main.PlayerList.Where(x => x.Player.name.Contains(playerName));
                if (worldFileData.Count() > 0 && player.Count() > 0)
                {
                    
                    player.First().SetAsActive();
                    
                    Main.ActiveWorldFileData = worldFileData.First();
                    WorldGen.EveryTileFrame();

                    //Player p = Main.player[Main.myPlayer];
                    //preValue = "" + Main.myPlayer;
                    //try
                    //{
                    //    p.Spawn();
                    //}
                    //catch
                    //{
                    //    return "oh no";
                    //}
                    
                    //Main.ActivePlayerFileData.StartPlayTimer();
                    //Player.Hooks.EnterWorld(Main.myPlayer);

                    //WorldGen.playWorld();
                    WorldGen.playWorldCallBack(null);
                    //Main.gameMenu = false;
                    //Main.menuMode = 10;

                    return true;
                }
                else
                {
                    return false;
                }
            }
            catch
            {
                return false;
            }
        }

        public bool ExitWorld()
        {

            WorldGen.SaveAndQuitCallBack(null);
            return true;
        }

        public WorldConfiguration GetDummyWorldConfiguration()
        {
            var npc = new NpcConfiguration();
            npc.npcName = "Green Slime";
            npc.removeExistingInstances = true;
            npc.spawnRate = 30;
            var coord = new Coordinate(50, 20);
            npc.initialLocations.Add(coord);
            var result = new WorldConfiguration();
            result.npcConfigurations.Add(npc);

            return result;
        }
        public PlayerState GetDummyPlayerConfiguration()
        {
            var invItem = new InventoryItem("test_item", 1, 10, false);
            var inv = new InventoryState();
            inv.items.Add(invItem);
            var player = new PlayerState();
            player.inventoryState = inv;
            return player;
        }

        public string ConfigureWorld(WorldConfiguration worldConfiguration)
        {
            if(worldConfiguration.npcConfigurations != null)
            {
                foreach(NpcConfiguration npcConfig in worldConfiguration.npcConfigurations)
                {
                    var npcs = Main.npc.Where(x => x.FullName.Contains(npcConfig.npcName));
                    if(npcs.Count() > 0)
                    {
                        var npc = npcs.First();
                        
                    }
                }
            }

            return "success";
        }
        public string ConfigurePlayer(PlayerState playerConfiguration)
        {
            var player = Main.player[Main.myPlayer];
            if (playerConfiguration.life != -1) player.statLife = playerConfiguration.life;
            if (playerConfiguration.maxLife != -1) player.statLifeMax = playerConfiguration.maxLife;
            if (playerConfiguration.mana != -1) player.statMana = playerConfiguration.mana;
            if (playerConfiguration.maxMana != -1) player.statManaMax = playerConfiguration.maxMana;

            return "success";
        }



        private void InitWorld()
        {
            int maxSpawns = 0;
            int spawnRate = 0;
            NPCLoader.EditSpawnRate(Main.player[Main.myPlayer], ref spawnRate, ref maxSpawns);
        }

        #endregion

        #region Helpers

        private float DistanceFromPlayer(NPC npc)
        {
            var playerPos = Main.player[Main.myPlayer].position;
            var npcPos = npc.position;
            return (float)Math.Sqrt(((playerPos.X - npcPos.X) * (playerPos.X - npcPos.X)) + ((playerPos.Y - npcPos.Y) * (playerPos.Y - npcPos.Y)));
        }

        #endregion

    }
}
