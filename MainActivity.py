# -*- coding: UTF-8 -*-
import guiTest
from tkinter import *

if __name__ == '__main__':
	init_window = Tk() 
	ZMJ_PORTAL = guiTest.MY_GUI(init_window)
	ZMJ_PORTAL.set_init_window()
	init_window.mainloop()