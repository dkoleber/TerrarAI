using Terraria.ModLoader;

namespace PythonBridge
{
	public class PythonBridge : Mod
	{
        private UpdateServer _server;
        public PythonBridge()
		{
            _server = new UpdateServer(() => { return "hello everyone"; });
            
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