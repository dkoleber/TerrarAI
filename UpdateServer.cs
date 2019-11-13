using System;
using System.Collections.Generic;
using System.Linq;
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
        string Echo();
    }

    [ServiceBehavior(InstanceContextMode = InstanceContextMode.Single)]
    public class UpdateService : IUpdateService
    {
        private Func<string> _stateGetter;
        public UpdateService(Func<string> stateGetter)
        {
            _stateGetter = stateGetter;
        }
        public string Echo()
        {
            return _stateGetter();
        }
    }
    
    public class UpdateServer
    {
        private WebServiceHost _host;

        public UpdateServer(Func<string> stateGetter)
        {
            var instance = new UpdateService(stateGetter);
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
