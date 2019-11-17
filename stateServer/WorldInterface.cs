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

        #region State

        public PlayerState GetPlayerState()
        {
            return new PlayerState(Main.player[Terraria.Main.myPlayer]);
        }

        public List<NpcState> GetNpcState(string npcName, int nearestN)
        {
            var states = new List<NpcState>();
            var closest = new List<float>();
            var matchingNpcs = Main.npc.ToList().Where(x => x.FullName.Contains(npcName) && x.life > 0).ToList();
            if (matchingNpcs.Count > nearestN)
            {
                foreach (NPC npc in matchingNpcs)
                {
                    states.Add(new NpcState(npc));
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
                            states.Insert(i, new NpcState(npc));
                            if (closest.Count > nearestN)
                            {
                                closest.RemoveAt(nearestN);
                                states.RemoveAt(nearestN);
                            }
                            break;
                        }
                    }
                    if (closest.Count < nearestN)
                    {
                        states.Add(new NpcState(npc));
                        closest.Add(distance);
                    }
                }
            }

            return states;
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

        #endregion


        #region World Configuration

        public bool EnterWorld(string worldName, string playerName)
        {
            //check if it's in the default folder
            //if not, move it there
            // and reload worlds

            WorldGen.clearWorld();
            Main.LoadWorlds();
            Main.LoadPlayers();
            WorldGen.EveryTileFrame();


            var worldFileData = Main.WorldList.Where(x => x.Name.Contains(worldName));
            var player = Main.PlayerList.Where(x => x.Player.name.Contains(playerName));
            if (worldFileData.Count() > 0 && player.Count() > 0)
            {
                Main.ActiveWorldFileData = worldFileData.First();
                player.First().SetAsActive();
                Main.ActivePlayerFileData.StartPlayTimer();
                Player.Hooks.EnterWorld(Main.myPlayer);
                Main.player[Main.myPlayer].Spawn();

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

        public bool ExitWorld()
        {
            WorldGen.SaveAndQuitCallBack(null);
            return true;
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
