from ....structs import ProtocolTreeNode
from ....layers.protocol_iq.protocolentities import IqProtocolEntity
import time
import json
from ....common import YowConstants

class StatusGetIqProtocolEntity(IqProtocolEntity):

    def __init__(self,_id = None, jids=["639622769809@s.whatsapp.net"]):
        super(StatusGetIqProtocolEntity, self).__init__(_type ="get", xmlns="w:mex", _id = _id,to = YowConstants.WHATSAPP_SERVER)
        self.jids = jids


    def __str__(self):
        out  = super(StatusGetIqProtocolEntity, self).__str__()
        out += "jid: %s\n" % self.jids
        return out

    def toProtocolTreeNode(self):

        user_id = self.jids[0].split("@")[0]        
        query=  {
            "variables":{
                "user_id":user_id,
                "include_username":True
            }            
        }
        queryNode = ProtocolTreeNode("query", {"query_id":"6556393721124826"},None, json.dumps(query).encode())

        node = super(StatusGetIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(queryNode)        
        return node


