using Terraria.ModLoader;

namespace PythonBridge
{
    using Terraria;
    public class PythonBridge : Mod
	{
        

        private UpdateServer _server;
        public PythonBridge()
		{
            _server = new UpdateServer(GetPlayerState, GetNpcState, GetUnanchoredWorldSlice, GetAnchoredWorldSlice);
            
        }

        public override void Load()
        {
            base.Load();
            _server.Run();
        }
        public override void Close()
        {
            base.Close();
            _server.Close();
        }

        private PlayerState GetPlayerState()
        {
            return new PlayerState(Main.player[Terraria.Main.myPlayer]);
        }
        private NpcState GetNpcState(string npcName)
        {
            return new NpcState(); // $"(npc state: {npcName})";
        }
        private WorldSlice GetUnanchoredWorldSlice(WorldSliceSpecifier slice)
        {
            return new WorldSlice(); // $"(unanchored world slice: {slice.x}+{slice.width},{slice.y}+{slice.height})";
        }
        private WorldSlice GetAnchoredWorldSlice(WorldSliceSpecifier slice)
        {
            return new WorldSlice(); // $"(anchored world slice: {slice.x}+{slice.width},{slice.y}+{slice.height})";
        }
    }
}