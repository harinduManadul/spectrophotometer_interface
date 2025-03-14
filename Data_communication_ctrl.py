class DataMaster():
    def __init__(self):
        self.sync = "#?#\n"
        self.sync_ok = "!"
        self.startStream = "#A#\n"
        self.stpoStream = "#S#\n"
        self.syncChChannel = 0
        
        self.msg = []
        self.channels = []
        
        self.xData = []
        self.yData = []
        
    def decodeMsg(self):
        temp = self.rowMsg.decode('utf8')
        if len(temp) > 0:
            if "#" in temp:
                self.msg = temp.split("#")
                #print(f"Before Removeing Index: {self.msg}")
                del self.msg[0]
                #print(f"After Removeing Index: {self.msg}")
               
    def genaratechannels(self):
        self.channels = [f"Ch{ch}" for ch in range(self.syncChChannel)]
        
    def buildYData(self):
        for _ in range(self.syncChChannel):
            self.yData.append([])
            
    def clearData(self):
        self.rowMsg = ""
        self.msg = []
        self.yData = []
        