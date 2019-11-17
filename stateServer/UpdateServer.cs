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



        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool EnterWorld(string worldName, string playerName);

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        bool ExitWorld();

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void ConfigureWorld(string worldConfiguration); //includes npc locations

        [OperationContract]
        [WebInvoke(Method = "GET", RequestFormat = WebMessageFormat.Json, ResponseFormat = WebMessageFormat.Json)]
        void ConfigurePlayer(string playerConfiguration); //includes inventory, health, buffs, and location


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


        public UpdateService()
        {
            _playerStateSubscribed = false;
            _npcStateSubscriptions = new List<NpcSubscription>();
            _unanchoredWorldSliceSubscriptions = new List<WorldSliceSpecifier>();
            _anchoredWorldSliceSubscriptions = new List<WorldSliceSpecifier>();
            _worldInterface = new WorldInterface();
        }


        #region State

        public List<StateObject> GetState()
        {
            var result = new List<StateObject>();
            try
            {
                if (_worldInterface.IsWorldLoaded())
                {
                    if (_playerStateSubscribed) result.Add(_worldInterface.GetPlayerState());

                    foreach (NpcSubscription npc in _npcStateSubscriptions)
                    {
                        List<NpcState> npcState = _worldInterface.GetNpcState(npc.npcName, npc.nearestN);
                        if(npcState.Count > 0)
                        {
                            result = result.Union(npcState).ToList();
                        }
                    }
                    
                    foreach (WorldSliceSpecifier slice in _unanchoredWorldSliceSubscriptions)
                    {
                        result.Add(_worldInterface.GetUnanchoredWorldSlice(slice));
                    }
                    foreach (WorldSliceSpecifier slice in _anchoredWorldSliceSubscriptions)
                    {
                        result.Add(_worldInterface.GetAnchoredWorldSlice(slice));
                    }
                }
            }
            catch (Exception e)
            {
                result.Add(new ErrorState(e.Message + "|" + e.StackTrace + "|" + e.Source));
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

        public void ConfigureWorld(string worldConfiguration)
        {

        }

        public void ConfigurePlayer(string playerConfiguration)
        {

        }

        #endregion
    }

    public class UpdateServer
    {
        private WebServiceHost _host;

        public UpdateServer()
        {
            var instance = new UpdateService();
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

