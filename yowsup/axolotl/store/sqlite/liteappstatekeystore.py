from axolotl.state.appstatestore import AppStateStore
import time
from ....layers.protocol_historysync.protocolentities.attributes import *

class LiteAppStateStore(AppStateStore):

    def __init__(self, dbConn):
        """
        :type dbConn: Connection
        """
        self.dbConn = dbConn
        
        dbConn.execute("CREATE TABLE IF NOT EXISTS app_state_keys(_id INTEGER PRIMARY KEY AUTOINCREMENT,key_id BLOB,key_data BLOB,fingerprint BLOB,timestamp INTEGER);")                

    def addAppStateKeys(self, keys):
        for key in keys:
            q = "INSERT INTO app_state_keys(key_id,key_data,timestamp) VALUES(?,?,?)"
            c = self.dbConn.cursor()       
            c.execute(q, (key.key_id.key_id ,key.key_data.key_data,int(time.time())))     
        
        self.dbConn.commit()

    def getOneAppStateKey(self):
        q = "SELECT key_id,key_data,timestamp FROM app_state_keys ORDER BY timestamp DESC"
        c = self.dbConn.cursor()
        c.execute(q)
        result = c.fetchone()          
        if result is not None:
            key = AppStateSyncKeyAttribute(
                key_id= AppStateSyncKeyIdAttribute(key_id=result[0]),
                key_data=AppStateSyncKeyDataAttribute(
                    key_data=result[1],
                    fingerprint=None,
                    timestamp=result[2]                
                )
            )            
            return key
        else:
            return None
        
    def getAppStateKey(self, key_id):

        q = "SELECT key_id FROM app_state_keys WHERE key_id = ?"
        c = self.dbConn.cursor()
        c.execute(q, (key_id, ))
      
        result = c.fetchone()     

        if result:                                      
            key = AppStateSyncKeyAttribute(
                key_id= AppStateSyncKeyIdAttribute(key_id=result[0]),
                key_data=AppStateSyncKeyDataAttribute(
                    key_data=result[1],
                    fingerprint=None,
                    timestamp=result[2]                
                )
            )            
            return key
        else:            
            return None
            
    def deleteAppStateKey(self,key_id):
        q = "DELETE  FROM app_state_keys where key_id=?"
        c = self.dbConn.cursor()       
        c.execute(q, (key_id,))             
        self.dbConn.commit()        






