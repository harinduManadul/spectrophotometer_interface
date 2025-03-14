import time
import serial.tools.list_ports

class SerialCtrl():
    def __init__(self): 
        self.com_ports_list = []
        self.sync_count = 20

    def getCOMList(self):
        ports = serial.tools.list_ports.comports()#, serial.tools.list_ports.
        self.com_ports_list = [com[0] for com in ports]
        self.com_ports_list.insert(0, "-")
    def serialOpen(self, ComGui):
        try:
            # Check if self.ser is already open; initialize if not
            if not hasattr(self, 'ser') or not self.ser.is_open:
                PORT = ComGui.clickedCom.get()
                BAUD = ComGui.clickdeBound.get()
                self.ser = serial.Serial()
                self.ser.baudrate = int(BAUD)  # Ensure BAUD is an integer
                self.ser.port = PORT
                self.ser.timeout = 0.1

            # Check if the port is open and set status
            if self.ser.is_open:
                self.ser.status = True
            else:
                # Attempt to open the port again
                PORT = ComGui.clickedCom.get()
                BAUD = ComGui.clickdeBound.get()
                self.ser = serial.Serial()
                self.ser.baudrate = int(BAUD)  # Ensure BAUD is an integer
                self.ser.port = PORT
                self.ser.timeout = 0.1
                self.ser.open()
                self.ser.status = True
        except:
            self.ser.status = False
    def serialClose(self, gui):
        try:
            self.ser.is_open
            self.ser.close()
            self.ser.status = False   
        except:
            self.ser.status = False  
      
    def serialSync(self, gui):
        self.threading = True
        count = 0
        while self.threading:
            try:
                self.ser.write(gui.data.sync.encode())
                gui.connection.sync_status["text"] = "Sync..."
                gui.connection.sync_status["fg"] = "orange"
                gui.data.rowMsg = self.ser.readline()
                #print(f"Row message: {gui.data.rowMsg}")
                gui.data.decodeMsg()
                
                if gui.data.sync_ok in gui.data.msg[0]:
                    if int(gui.data.msg[1]) > 0:
                        gui.connection.btn_start_stream['state'] = 'active'
                        gui.connection.btn_add_chart['state'] = 'active'
                        gui.connection.btn_kill_chart['state'] = 'active'
                        gui.connection.save_check['state'] = 'active'
                        gui.connection.sync_status['text'] = 'OK'
                        gui.connection.sync_status['fg'] = 'green'
                        gui.connection.ch_status['text'] = gui.data.msg[1]
                        gui.connection.ch_status['fg'] = 'green'
                        gui.data.syncChChannel = int(gui.data.msg[1])
                        
                        gui.data.genaratechannels()
                        gui.data.buildYData()
                        print(gui.data.channels, gui.data.yData)
                        
                        self.threading = False
                        break
                
                if self.threading == False:
                    break
            except Exception as e:
                print(e)
            count += 1
            if self.threading == False:
                    break
            
            if count > self.sync_count:
                count = 0
                gui.connection.sync_status["text"] = "Failed"
                gui.connection.sync_status["fg"] = "red"
                if self.threading == False:
                    break
                time.sleep(.5)
                
        
if __name__ == '__main__':
    SerialCtrl()
    