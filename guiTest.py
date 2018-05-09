# !/usr/bin/python
# -*- coding: UTF-8 -*-

import apriori4
import fpgrowthDiy
import loaddata
import threading
from tkinter import *
from tkinter import scrolledtext
import os
import hashlib
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as tkFiledialog      


class MY_GUI():

	def __init__(self,window):
		self.window=window 

	#设置窗口
	def set_init_window(self):
		self.window.title("第一个GUI界面")      #窗口名
		self.window.geometry('1080x680+10+10')                 #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
		self.window["bg"] = "pink"                            #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
		self.init_data_label = Label(self.window, text="待处理数据")
		self.init_data_label.grid(row=0, column=0)
		self.result_data_label = Label(self.window, text="输出结果")
		self.result_data_label.grid(row=0, column=12)
		self.clean_data_label = Label(self.window,text="清空",width=8)
		self.clean_data_label.grid(row=0,column=18)
		self.log_label = Label(self.window, text="日志")
		self.log_label.grid(row=12, column=0)
		#文本框
		self.init_data_Text = scrolledtext.ScrolledText(self.window, width=67, height=35)  #原始数据录入框
		self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
		self.result_data_Text = scrolledtext.ScrolledText(self.window, width=70, height=49)  #处理结果展示
		self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
		self.log_data_Text = scrolledtext.ScrolledText(self.window, width=66, height=9)  # 日志框
		self.log_data_Text.grid(row=13, column=0, columnspan=10)
		#按钮
		Button(self.window, text="加载数据集",command=self.click1,  bg="lightblue", width=10).grid(row=1,column=11)  # 调用内部方法  加()为直接调用
		# self.str_trans_to_md5_button.grid(row=1, column=11)
		Button(self.window, text="选择算法",command=lambda:self.click2(), bg="lightblue", width=10).grid(row=2,column=11)  # 调用内部方法  加()为直接调用
 		# # self.str_trans_to_md5_button.grid(row=2, column=11)
		Button(self.window,text="输入参数",command=lambda:self.click3(),bg="lightblue",width=10).grid(row=3,column=11)
		# self.str_trans_to_md5_button
		Button(self.window, text="运行",command=lambda:self.click4(), bg="lightblue", width=10).grid(row=4, column=11)  # 调用内部方法  加()为直接调用
		# self.str_trans_to_md5_button
		Button(self.window,text="生成规则",command=lambda:self.click5(),bg="lightblue",width=10).grid(row=5,column=11)

	def click1(self):
		fn = tkFiledialog.askopenfilename()    #选择文件夹
		# fnlist = os.walk( fn )                  #列出目录
		# print(fn)
		self.log_data_Text.insert(INSERT,'正在加载数据...\n')
		self.dataset = loaddata.load_data(fn)
		# print(self.dataset)
		for i in self.dataset:
			self.init_data_Text.insert(INSERT,i)
			self.init_data_Text.insert(INSERT,'\n')

		self.log_data_Text.insert(INSERT,'加载完毕！\n')

	def click2(self):
		self.top = Toplevel()
		self.top.title('选择算法')
		self.top.geometry('150x200')
		self.top['bg']='pink'
		self.top.v = StringVar()
		Radiobutton(self.top,text = 'Aprioi',bg="pink", variable = self.top.v,value = "Aprioi").grid(row=1,column=1,padx=30,pady=10)
		Radiobutton(self.top,text = 'FP-Growth',bg="pink", variable = self.top.v,value = "FP-Growth").grid(row=2,column=1,padx=30,pady=10)
		Button(self.top,text='确定',command=self.clk2_commit).grid(row=3,column=1,padx=30,pady=10)

	def clk2_commit(self):
		self.suanfa=self.top.v.get()
		print(self.suanfa)
		self.top.destroy()

	def click3(self):
		self.top = Toplevel()
		self.top.title('输入参数')
		self.top.geometry('300x200')
		self.top['bg']='pink'
		self.top.v1 = DoubleVar()
		self.top.v2 = DoubleVar()
		Label(self.top,text="最小支持度").grid(row=0,column=0)
		Entry(self.top,textvariable=self.top.v1 ,show=None).grid(row=0,column=1)
		Label(self.top,text="最小置信度").grid(row=1,column=0)
		Entry(self.top,textvariable=self.top.v2 ,show=None).grid(row=1,column=1)
		Button(self.top,text="确定",command=self.clk3_commit).grid(row=2,column=1)

	def clk3_commit(self):
		self.minsupport=self.top.v1.get()
		self.minconfig=self.top.v2.get()
		print(self.minsupport)
		print(self.minconfig)
		self.top.destroy()

	def aprithread(self):
		if (self.suanfa=='Aprioi'):
			if(self.minsupport!=0):
				self.L,self.support=apriori4.apriori(self.dataset,self.minsupport)
			else:
				self.L,self.support=apriori4.apriori(self.dataset)
		else:
			self.frozenDataSet = fpgrowthDiy.transfer2FrozenDataSet(self.dataset)
			self.fptree,self.headPointTable = fpgrowthDiy.createFPTree(self.frozenDataSet, self.minsupport)
			# fptree.disp()
			self.L = {}
			self.prefix = set([])
			fpgrowthDiy.mineFPTree(self.headPointTable, self.prefix, self.L, self.minsupport)
			# print(L)

	def click4(self):
		self.log_data_Text.insert(INSERT,'正在挖掘频繁项集...\n')
		t=threading.Thread(target=self.aprithread)
		t.start()
		t.join()
		self.result_data_Text.insert(INSERT,'频繁项集\n')	
		for i in self.L:
			print(i)
			self.result_data_Text.insert(INSERT,i)
			self.result_data_Text.insert(INSERT,'\n')
		self.log_data_Text.insert(INSERT,'频繁项集已生成！\n')

	
	def rulesthread(self):
		if (self.suanfa=='Aprioi'):
			if(self.minconfig!=0):
				self.rules=apriori4.generateRules(self.L,self.support,self.minconfig)
			else:
				self.rules=apriori4.generateRules(self.L,self.support)
		else:
			self.rules = []
			fpgrowthDiy.rulesGenerator(self.L, self.minconfig, self.rules)

	def click5(self):
		self.log_data_Text.insert(INSERT,'正在生成关联规则...\n')
		t=threading.Thread(target=self.rulesthread)
		t.start()
		t.join()
		self.result_data_Text.insert(INSERT,'关联规则\n')
		for i in self.rules:
			print(i)
			self.result_data_Text.insert(INSERT,i)
			self.result_data_Text.insert(INSERT,'\n')
		self.log_data_Text.insert(INSERT,'关联规则生成完毕...\n')


        # self.result_data_scrollbar_y = Scrollbar(self.window)                #创建纵向滚动条
        # self.result_data_scrollbar_y.config(command=self.result_data_Text.yview)       #将创建的滚动条通过command参数绑定到需要拖动的Text上
        # self.result_data_Text.config(yscrollcommand=self.result_data_scrollbar_y.set)　#Text反向绑定滚动条
        # self.result_data_scrollbar_y.grid(row=1, column=23, rowspan=15) 

    # def get_current_time(self):																#获取当前时间
    #     current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #     return current_time
    #日志动态打印
    # def write_log_to_Text(self,logmsg):
    #     global LOG_LINE_NUM
    #     current_time = self.get_current_time()
    #     logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
    #     if LOG_LINE_NUM <= 7:
    #         self.log_data_Text.insert(END, logmsg_in)
    #         LOG_LINE_NUM = LOG_LINE_NUM + 1
    #     else:
    #         self.log_data_Text.delete(1.0,2.0)
    #         self.log_data_Text.insert(END, logmsg_in) 
	# def click(event):
 #    	index = listbox.curselection()
 #    	path = listbox.get(index)
 #    	if not path:
 #    		return
 #    		window = Tk()
 #    		window.title('查看文件')
	#     text = Text(window, width = 100)  #多行文本框
	#     text.grid()
	#     fn_text = open(path).read()
	#     text.insert(END, fn_text)



def gui_start():
	init_window = Tk()              #实例化出一个父窗口
	ZMJ_PORTAL = MY_GUI(init_window)
	ZMJ_PORTAL.set_init_window()    # 设置根窗口默认属性
	init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()