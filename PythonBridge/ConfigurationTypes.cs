using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;

namespace PythonBridge
{
    [DataContract]
    public class Coordinate
    {
        [DataMember]
        public float x;
        [DataMember]
        public float y;
        public Coordinate(float x, float y)
        {
            this.x = x;
            this.y = y;
        }
    }


    [DataContract]
    public class NpcConfiguration
    {
        [DataMember]
        public string npcName;
        [DataMember]
        public bool removeExistingInstances;
        [DataMember]
        public List<Coordinate> initialLocations;
        [DataMember]
        public int spawnRate;

        public NpcConfiguration()
        {
            this.initialLocations = new List<Coordinate>();
        }

    }


    public class DayTimeConfiguration { } //TODO

    public class EventConfiguration { } //TODO

    [DataContract]
    public class WorldConfiguration
    {
        [DataMember]
        public List<NpcConfiguration> npcConfigurations;
        public WorldConfiguration()
        {
            this.npcConfigurations = new List<NpcConfiguration>();
        }
    }



}
