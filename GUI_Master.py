# Description: This file contains the GUI class for the master GUI

import threading
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RootGUI():
    def __init__ (self, serial, data):
        self.root = Tk()#root window
        self.root.title("Serial Commiunication")#title of the rooot window
        self.root.geometry("360x120")#size of the root window
        self.root.config(bg="white")#configuring the background color of the root window
        self.serial = serial
        self.data = data
        
        self.root.protocol("WH_DELETE_WINDOW", self.closeWindow)
        
    def closeWindow(self):
        print("closing window and exiting...")
        self.root.destroy
        self.serial.serialClose(self)
        self.serial.threading = False
        
class ComGui(): 
    def __init__(self, 
                 root, 
                 serial,
                 data):
        
        
        self.root = root#root object
        self.serial = serial#serial object
        self.data = data#data object
        
        
        self.frame = LabelFrame(root, text = "Com Manager", padx = 5, pady = 5, bg = "white")#create frame
        
        self.label_com = Label(self.frame, text = "Available Port(s)", width=15, bg = "white", anchor="w")#create widget
        self.label_bd = Label(self.frame, text = "Bound Rate: ", width=15, bg = "white", anchor="w")#create widget
        
        self.boundOptionMenu()#call bound option menu function
        self.comOptionMenu()#call com option menu function
        
        self.btn_refresh = Button(self.frame, text = "refresh", width =10, command = self.com_refresh)#create reefresh button
        self.btn_connect = Button(self.frame, text = "connect", width = 10, state = "disabled", command = self.serial_connect)#create connect button
        
        self.padx = 20#create padding x variable
        self.pady = 5#create padding y variable
        
        self.publish()#call publish function
    
    #publish the widgets
    def publish(self):
        self.frame.grid(row = 0, column = 0, rowspan = 3, columnspan = 3 , padx = 5, pady = 5)
        
        self.label_com.grid(row = 2, column = 1)
        self.drop_com.grid(row = 2, column = 2, padx = self.padx, pady = self.pady)
        self.label_bd.grid(row = 3, column = 1)
        self.drop_bound.grid(row = 3, column = 2)
        self.btn_refresh.grid(row = 2, column = 3)
        self.btn_connect.grid(row = 3, column = 3)
        
    #connections port option menu
    def comOptionMenu(self):
        self.serial.getCOMList()
        
        #coms = ["-", "COM3", "COM4", "COM5", "COM6"]
        coms = self.serial.com_ports_list
        
        self.clickedCom = StringVar()
        self.clickedCom.set(coms[0])
        self.drop_com = OptionMenu(self.frame, self.clickedCom, *coms, command = self.connect_ctrl)
        self.drop_com.config(width = 10)
    #bound rate option menu
    def boundOptionMenu(self):
        baudRate = ["-", "110", "300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200"]
        self.clickdeBound = StringVar()
        self.clickdeBound.set(baudRate[0])
        self.drop_bound = OptionMenu(self.frame, self.clickdeBound, *baudRate, command = self.connect_ctrl)
        self.drop_bound.config(width = 10)
    #connect control
    def connect_ctrl(self, other):
        #activate connect button
        if "-" in self.clickedCom.get() or "-" in self.clickdeBound.get():
            self.btn_connect.config(state = "disabled")
        else:
            #self.btn_connect.config(state = "normal")
            self.btn_connect["state"] = "normal"
    #refresh
    def com_refresh(self):
        self.drop_com.destroy()
        self.comOptionMenu()
        self.drop_com.grid(row = 2, column = 2, padx = self.padx, pady = self.pady)
        logic = []
        self.connect_ctrl(logic)
    #connect with serialmport
    def serial_connect(self):
        
        if self.btn_connect["text"] in "connect":
            #start the connection
            self.serial.serialOpen(self)
            if self.serial.ser.status:
                self.btn_connect.config(text = "disconnect")
                self.btn_refresh.config(state = "disabled")
                self.drop_com.config(state = "disabled")
                self.drop_bound.config(state = "disabled")
                
                self.connection = ConnectionGui(self.root, self.serial, self.data)
                self.serial.t1 = threading.Thread(target = self.serial.serialSync,
                                                  args = (self,),
                                                  daemon = True)
                self.serial.t1.start()
                
                InfoMesg = f"Successfully connected to {self.clickedCom.get()}"
                messagebox.showinfo("Info", InfoMesg)
                
            else:
                ErrorMwssage = f"Error connecting to {self.clickedCom.get()}"
                messagebox.showerror("Error", ErrorMwssage)
        else:
             #stop the connection
            self.serial.threading = False
            self.connection.connectionGuiClose()
            self.data.clearData()
            self.serial.serialClose(self)
            self.btn_connect.config(text = "connect")
            self.btn_refresh.config(state = "active")
            self.drop_com.config(state = "active")
            self.drop_bound.config(state = "active")
      
class ConnectionGui():
    def __init__(self, 
                 root, 
                 serial, 
                 data):
        
        self.root = root
        self.serial = serial
        self.data = data
        
        self.frame = LabelFrame(root,
                                text = "Connection Manager",
                                padx = 5,
                                pady = 5,
                                bg = "white",
                                width = 60)
        
        self.sync_label = Label(self.frame,
                           text = 'Sync Status',
                           bg='white',
                           width = 15,
                           anchor='w')
        
        self.sync_status = Label(self.frame,
                           text = 'Sync......',
                           bg='white',
                           width = 5,
                           fg='orange')
        
        self.ch_label = Label(self.frame,
                              text="Active Channels",
                              bg="white",
                              width=15,
                              anchor='w')
        
        self.ch_status = Label(self.frame,
                               text="...",
                               bg="white",
                               width=5,
                               fg="orange")
        
        self.btn_start_stream = Button(self.frame,
                                       text="Start",
                                       width=5,
                                       state="disabled",
                                       command=self.start_stream)
        self.btn_stop_stream = Button(self.frame,
                                       text="Stop",
                                       width=5,
                                       state="disabled",
                                       command=self.stop_stream)
        
        self.btn_add_chart = Button(self.frame,
                                       text="+",
                                       width=5,
                                       state="disabled",
                                       bg='white',
                                       fg='#098577',
                                       command=self.new_chart)
        
        self.btn_kill_chart = Button(self.frame,
                                       text="-",
                                       width=5,
                                       state="disabled",
                                       bg='white',
                                        fg='#cc252c',
                                       command=self.kill_chart)
        
        self.save = False
        self.vaseVar = IntVar()
        self.save_check = Checkbutton(self.frame,
                                      text = 'Save data',
                                      variable=self.vaseVar,
                                      onvalue=1,
                                      offvalue=0,
                                      bg='white',
                                      state='disabled',
                                      command = self.save_data)
        
        self.separator = ttk.Separator(self.frame, orient='vertical')
        
        self.padx = 20
        self.pady = 15
        
        self.connectionGuiOpen()
        self.chartMaster = DisplayGUI(self.root, self.serial, self.data)
        
    def connectionGuiOpen(self):
        self.root.geometry("800x120")
        self.frame.grid(row = 0, 
                        column = 4, 
                        rowspan = 3, 
                        columnspan = 5, 
                        padx = 5, 
                        pady = 5)
        
        self.sync_label.grid(column=1, row=1)
        self.sync_status.grid(column=2, row=1)
        
        self.ch_label.grid(column=1, row=2)
        self.ch_status.grid(column=2, row=2, pady=self.pady)
        
        self.btn_start_stream.grid(column=3, row=1, padx=self.padx)
        self.btn_stop_stream.grid(column=3, row=2, padx=self.padx)
        
        self.btn_add_chart.grid(column=4, row=1, padx=self.padx)
        self.btn_kill_chart.grid(column=5, row=1, padx=self.padx)
        
        self.save_check.grid(column=4, row=2, columnspan=2)
        
        self.separator.place(relx=0.58, rely=0, relwidth=0.001, relheight=1)
    
    def connectionGuiClose(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.root.geometry("360x120")
        
    def start_stream(self):
        pass
    
    def stop_stream(self):
        pass
      
    def new_chart(self):
        self.chartMaster.addChannelMaster()

    def kill_chart(self):
       try:
           if len(self.chartMaster.frame) > 0:
                totalFrames = len(self.chartMaster.frame) - 1
                self.chartMaster.frame[totalFrames].destroy()
                self.chartMaster.frame.pop()
                self.chartMaster.figures.pop()
                self.chartMaster.controlFrames[totalFrames][0].destroy()
                self.chartMaster.controlFrames.pop()
                self.chartMaster.adjustRootFrame()
                
       except:
           pass    
    
    def save_data(self):
        pass

class DisplayGUI():
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data
        
        self.frame = []
        self.frameCollums = 0
        self.frameRows = 4
        self.totFrames = 0
        
        self.figures = []
        self.controlFrames = []
        
    def addChannelMaster(self):
        self.addMasterFrame()
        self.adjustRootFrame()
        self.addGraph()
        self.addButtonFrame()
        
    def addMasterFrame(self):
        self.frame.append(LabelFrame(self.root,
                                     text = f"Display Manager - {len(self.frame) + 1}",
                                     padx = 5,
                                     pady = 5,
                                     bg="white"))
        self.totFrames = len(self.frame) -1
        
        if self.totFrames % 2 == 0:
            self.frameCollums = 0
        else:
            self.frameCollums = 9
            
        self.frameRows = 4 + 4 * int(self.totFrames / 2) 
        self.frame[self.totFrames].grid(padx = 5,
                                        column = self.frameCollums,
                                        row = self.frameRows,
                                        columnspan = 9,
                                        sticky = NW)
    
    def adjustRootFrame(self):
        self.totFrames = len(self.frame) - 1
        
        if self.totFrames > 0:
            rootWidth = 800*2
        else:
            rootWidth = 800
        if self.totFrames + 1 == 0:
            rootHeight = 120
        else:
            rootHeight = 120 + 430 * (int(self.totFrames / 2) + 1)
        self.root.geometry(f"{rootWidth}x{rootHeight}")
        
    def addGraph(self):
        self.figures.append([])
        
        self.figures[self.totFrames].append(plt.figure(figsize=(7, 5), dpi=80))
        
        self.figures[self.totFrames].append(self.figures[self.totFrames][0].add_subplot(111))
        
        self.figures[self.totFrames].append(FigureCanvasTkAgg(self.figures[self.totFrames][0],
                                                            master=self.frame[self.totFrames]))

        self.figures[self.totFrames][2].get_tk_widget().grid(row=0, 
                                                             column=1, 
                                                             rowspan=17,
                                                             columnspan = 4, 
                                                             sticky=N)
                                                        
    def addButtonFrame(self):
        
        btnH = 2
        btnW = 4
        
        self.controlFrames.append([])
        self.controlFrames[self.totFrames].append(LabelFrame(self.frame[self.totFrames],
                                                             pady=5,
                                                             bg="white"))
        self.controlFrames[self.totFrames][0].grid(row = 0,
                                                   column = 0,
                                                   padx = 5,
                                                   pady=5,
                                                   sticky=N)
        
        self.controlFrames[self.totFrames].append(Button(self.controlFrames[self.totFrames][0],
                                                         text = "+",
                                                         bg = "white",
                                                         height=btnH,
                                                         width=btnW))
        
        self.controlFrames[self.totFrames][1].grid(row = 0,
                                                   column = 0,
                                                   padx = 5,
                                                   pady=5)
        
        self.controlFrames[self.totFrames].append(Button(self.controlFrames[self.totFrames][0],
                                                         text = "-",
                                                         bg = "white",
                                                         height=btnH,
                                                         width=btnW))
        
        self.controlFrames[self.totFrames][2].grid(row = 0,
                                                   column = 1,
                                                   padx = 5,
                                                   pady=5)
        
        

if __name__ == '__main__':
    RootGUI()
    ComGui() 
    ConnectionGui()
    DisplayGUI()