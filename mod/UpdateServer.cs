using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
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
        string GetPort();       

        #region State

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        GameState GetState();

        #region Subscriptions

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool SubscribeToPlayerState();

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool SubscribeToNpcState(string npcName, int nearestN);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool SubscribeToUnanchoredWorldSlice(int x, int y, int width, int height);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool SubscribeToAnchoredWorldSlice(int xOffset, int yOffset, int width, int height);

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

        #endregion

        #endregion

        #region Configuration

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool EnterWorld(string worldName, string playerName);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool ExitWorld();

        [OperationContract]
        [WebInvoke(Method = "POST", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        string ConfigureWorld(WorldConfiguration worldConfiguration);

        [OperationContract]
        [WebInvoke(Method = "POST", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        string ConfigurePlayer(PlayerState playerConfiguration);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        WorldConfiguration GetDummyConfiguration();

        #endregion
    }

    public class NpcSubscription
    {
        public string npcName;
        public int nearestN;
        public NpcSubscription(string npcName, int nearestN)
        {
            this.npcName = npcName;
            this.nearestN = nearestN;
        }
    }

    [ServiceBehavior(InstanceContextMode = InstanceContextMode.Single)]
    public class UpdateService : IUpdateService
    {

        private bool _playerStateSubscribed;
        private List<NpcSubscription> _npcStateSubscriptions;
        private List<WorldSliceSpecifier> _unanchoredWorldSliceSubscriptions;
        private List<WorldSliceSpecifier> _anchoredWorldSliceSubscriptions;
        private WorldInterface _worldInterface;
        private string _port;


        public UpdateService(string port)
        {
            _port = port;
            _playerStateSubscribed = false;
            _npcStateSubscriptions = new List<NpcSubscription>();
            _unanchoredWorldSliceSubscriptions = new List<WorldSliceSpecifier>();
            _anchoredWorldSliceSubscriptions = new List<WorldSliceSpecifier>();
            _worldInterface = new WorldInterface();
            _worldInterface.SetWindowTitle($"TerrarAI: {_port}");
        }

        public string GetPort()
        {
            return _port;
        }

        #region State

        public GameState GetState()
        {
            var result = new GameState();
            try
            {
                if (_worldInterface.IsWorldLoaded())
                {
                    result.timeState = _worldInterface.GetTimeState();

                    if (_playerStateSubscribed) result.playerState  = _worldInterface.GetPlayerState();

                    foreach (NpcSubscription npc in _npcStateSubscriptions)
                    {
                        result.npcStates.Add(_worldInterface.GetNpcState(npc.npcName, npc.nearestN));
                    }
                    
                    foreach (WorldSliceSpecifier slice in _unanchoredWorldSliceSubscriptions)
                    {
                        result.unanchoredWorldSlices.Add(_worldInterface.GetUnanchoredWorldSlice(slice));
                    }
                    foreach (WorldSliceSpecifier slice in _anchoredWorldSliceSubscriptions)
                    {
                        result.anchoredWorldSlices.Add(_worldInterface.GetAnchoredWorldSlice(slice));
                    }
                }
            }
            catch (Exception e)
            {
                result.errorMessage =  e.Message + "|" + e.StackTrace + "|" + e.Source;
            }

            return result;
        }

        #region State Subscriptions

        public bool SubscribeToPlayerState()
        {
            if (_playerStateSubscribed) return false;
            _playerStateSubscribed = true;
            return true;
        }
        public bool SubscribeToNpcState(string npcName, int nearestN)
        {
            var matchingNames = _npcStateSubscriptions.Where(x => x.npcName == npcName).ToList();
            if (matchingNames.Count > 0)
            {
                if(matchingNames[0].nearestN == nearestN)
                {
                    return false;
                }
                else
                {
                    matchingNames[0].nearestN = nearestN;
                    return true;
                }
                
            }
            _npcStateSubscriptions.Add(new NpcSubscription(npcName, nearestN));
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
        public bool SubscribeToAnchoredWorldSlice(int xOffset, int yOffset, int width, int height)
        {
            WorldSliceSpecifier newSlice = new WorldSliceSpecifier(xOffset, yOffset, width, height);
            if (_anchoredWorldSliceSubscriptions.Exists(z => z.Equals(newSlice)))
            {
                return false;
            }
            _anchoredWorldSliceSubscriptions.Add(newSlice);
            return true;
        }

        #endregion

        #region State Unsubscriptions

        public void UnsubscribeFromPlayerState()
        {
            _playerStateSubscribed = false;
        }
        public void UnsubscribeFromNpcState(string npcName)
        {
            _npcStateSubscriptions.RemoveAll(x => x.npcName == npcName);
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

        #endregion

        #endregion

        #region Loading

        public bool EnterWorld(string worldName, string playerName)
        {
            return _worldInterface.EnterWorld(worldName, playerName);
        }

        public bool ExitWorld()
        {
            return _worldInterface.ExitWorld();
        }

        #endregion

        #region Configuration

        public string ConfigureWorld(WorldConfiguration worldConfiguration)
        {
            return _worldInterface.ConfigureWorld(worldConfiguration);
        }

        public string ConfigurePlayer(PlayerState playerConfiguration)
        {
            return _worldInterface.ConfigurePlayer(playerConfiguration);
        }

        public WorldConfiguration GetDummyConfiguration()
        {
            return _worldInterface.GetDummyWorldConfiguration();
        }

        #endregion
    }

    public class UpdateServer
    {
        private static int _basePort = 8001;
        private WebServiceHost _host;

        public UpdateServer()
        {
            var chosenPort = this.GetNextPort();
            var instance = new UpdateService(chosenPort);
            _host = new WebServiceHost(instance, new Uri("http://localhost:" + chosenPort));
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

        private string GetNextPort()
        {
            var client = new HttpClient();
            var baseAddress = "http://localhost:";
            var baseEndpont = "/GetPort";
            var currentPort = _basePort;
            var foundUnusedAddress = false;
            do
            {
                try
                {
                    var otherPortTask = client.GetStringAsync(baseAddress + currentPort + baseEndpont);
                    otherPortTask.Wait();
                    if (otherPortTask.IsFaulted)
                    {
                        foundUnusedAddress = true;
                    }
                    else
                    {
                        currentPort++;
                    }
                }
                catch
                {
                    foundUnusedAddress = true;
                }
            } while (!foundUnusedAddress);

            return currentPort + "";
        }


    }
}

