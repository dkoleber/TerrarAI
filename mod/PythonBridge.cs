using Terraria.ModLoader;

namespace PythonBridge
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using Terraria;
    using Terraria.ModLoader;
    public class PythonBridge : Mod
	{
        

        private UpdateServer _server;
        public PythonBridge()
		{
            _server = new UpdateServer();
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

        
    }
}