#main execution file

from GUI_Master import ComGui, RootGUI
from Serial_communication_ctrl import SerialCtrl
from Data_communication_ctrl import DataMaster


serial = SerialCtrl()
myData = DataMaster()
RootMaster = RootGUI(serial, myData)
ComMaster = ComGui(RootMaster.root, serial, myData)
RootMaster.root.mainloop()