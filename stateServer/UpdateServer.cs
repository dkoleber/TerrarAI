using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.ServiceModel.Web;
using System.Text;
using System.Threading.Tasks;

namespace PythonBridge
{





    [ServiceContract]
    public interface IUpdateService
    {
        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        List<StateObject> GetState();

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool SubscribeToPlayerState();

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool SubscribeToNpcState(string npcName);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool SubscribeToUnanchoredWorldSlice(int x, int y, int width, int height);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool SubscribeToPlayerAnchoredWorldSlice(int xOffset, int yOffset, int width, int height);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void UnsubscribeFromPlayerState();

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void UnsubscribeFromNpcState(string npcName);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void UnsubscribeFromUnanchoredWorldSlice(int x, int y, int width, int height);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void UnsubscribeFromAnchoredWorldSlice(int xOffset, int yOffset, int width, int height);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void UnsubscribeFromAll();




        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void LoadWorld(string worldName);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void ConfigureWorld(string worldConfiguration); //includes npc locations

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void ConfigurePlayer(string playerConfiguration); //includes inventory, health, buffs, and location

    }

    [ServiceBehavior(InstanceContextMode = InstanceContextMode.Single)]
    public class UpdateService : IUpdateService
    {
        private Func<PlayerState> _playerStateGetter;
        private Func<string, NpcState> _npcStateGetter;
        private Func<WorldSliceSpecifier, WorldSlice> _unanchoredWorldSliceGetter;
        private Func<WorldSliceSpecifier, WorldSlice> _anchoredWorldSliceGetter;

        private bool _playerStateSubscribed;
        private List<string> _npcStateSubscriptions;
        private List<WorldSliceSpecifier> _unanchoredWorldSliceSubscriptions;
        private List<WorldSliceSpecifier> _anchoredWorldSliceSubscriptions;



        public UpdateService(Func<PlayerState> playerStateGetter,
            Func<string, NpcState> npcStateGetter,
            Func<WorldSliceSpecifier, WorldSlice> unanchoredWorldSliceGetter,
            Func<WorldSliceSpecifier, WorldSlice> anchoredWorldSliceGetter)
        {
            _playerStateSubscribed = false;
            _npcStateSubscriptions = new List<string>();
            _unanchoredWorldSliceSubscriptions = new List<WorldSliceSpecifier>();
            _anchoredWorldSliceSubscriptions = new List<WorldSliceSpecifier>();


            _playerStateGetter = playerStateGetter;
            _npcStateGetter = npcStateGetter;
            _unanchoredWorldSliceGetter = unanchoredWorldSliceGetter;
            _anchoredWorldSliceGetter = anchoredWorldSliceGetter;
        }
        public List<StateObject> GetState()
        {
            var result = new List<StateObject>();
            if (_playerStateSubscribed) result.Add(_playerStateGetter());
            foreach (string npcKey in _npcStateSubscriptions)
            {
                result.Add(_npcStateGetter(npcKey));
            }
            foreach (WorldSliceSpecifier slice in _unanchoredWorldSliceSubscriptions)
            {
                result.Add(_unanchoredWorldSliceGetter(slice));
            }
            foreach (WorldSliceSpecifier slice in _anchoredWorldSliceSubscriptions)
            {
                result.Add(_anchoredWorldSliceGetter(slice));
            }
            return result;
        }

        public bool SubscribeToPlayerState()
        {
            if (_playerStateSubscribed) return false;
            _playerStateSubscribed = true;
            return true;
        }
        public bool SubscribeToNpcState(string npcName)
        {
            if (_npcStateSubscriptions.Exists(x => x == npcName))
            {
                return false;
            }
            _npcStateSubscriptions.Add(npcName);
            return true;
        }
        public bool SubscribeToUnanchoredWorldSlice(int x, int y, int width, int height)
        {
            WorldSliceSpecifier newSlice = new WorldSliceSpecifier(x, y, width, height);
            if (_unanchoredWorldSliceSubscriptions.Exists(z => z.Equals(newSlice)))
            {
                return false;
            }
            _unanchoredWorldSliceSubscriptions.Add(newSlice);
            return true;
        }

        public bool SubscribeToPlayerAnchoredWorldSlice(int xOffset, int yOffset, int width, int height)
        {
            WorldSliceSpecifier newSlice = new WorldSliceSpecifier(xOffset, yOffset, width, height);
            if (_anchoredWorldSliceSubscriptions.Exists(z => z.Equals(newSlice)))
            {
                return false;
            }
            _anchoredWorldSliceSubscriptions.Add(newSlice);
            return true;
        }
        public void UnsubscribeFromPlayerState()
        {
            _playerStateSubscribed = false;
        }
        public void UnsubscribeFromNpcState(string npcName)
        {
            _npcStateSubscriptions.RemoveAll(x => x == npcName);
        }
        public void UnsubscribeFromUnanchoredWorldSlice(int x, int y, int width, int height)
        {
            WorldSliceSpecifier newSlice = new WorldSliceSpecifier(x, y, width, height);
            _unanchoredWorldSliceSubscriptions.RemoveAll(z => z.Equals(newSlice));
        }

        public void UnsubscribeFromAnchoredWorldSlice(int xOffset, int yOffset, int width, int height)
        {

            WorldSliceSpecifier newSlice = new WorldSliceSpecifier(xOffset, yOffset, width, height);
            _anchoredWorldSliceSubscriptions.RemoveAll(z => z.Equals(newSlice));
        }

        public void UnsubscribeFromAll()
        {
            _playerStateSubscribed = false;
            _npcStateSubscriptions.Clear();
            _unanchoredWorldSliceSubscriptions.Clear();
            _anchoredWorldSliceSubscriptions.Clear();
        }

        public void LoadWorld(string worldName)
        {

        }

        public void ConfigureWorld(string worldConfiguration)
        {

        }

        public void ConfigurePlayer(string playerConfiguration)
        {

        }
    }

    public class UpdateServer
    {
        private WebServiceHost _host;

        public UpdateServer(Func<PlayerState> playerStateGetter,
            Func<string, NpcState> npcStateGetter,
            Func<WorldSliceSpecifier, WorldSlice> unanchoredWorldSliceGetter,
            Func<WorldSliceSpecifier, WorldSlice> anchoredWorldSliceGetter)
        {
            var instance = new UpdateService(playerStateGetter, npcStateGetter, unanchoredWorldSliceGetter, anchoredWorldSliceGetter);
            _host = new WebServiceHost(instance, new Uri("http://localhost:8001"));
            _host.AddServiceEndpoint(typeof(IUpdateService), new WebHttpBinding(), "");
        }
        public void Run()
        {
            _host.Open();
        }
        public void Close()
        {
            _host.Close();
        }


    }
}

