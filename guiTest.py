# !/usr/bin/python
# -*- coding: UTF-8 -*-

import apriori
import fpgrowth
import loaddata
import threading
import Rules
import time
from tkinter import *
from tkinter import scrolledtext
import os
import hashlib
from tkinter import messagebox as tkMessageBox
from tkinter import filedialog as tkFiledialog      


class MY_GUI():

	def __init__(self,window):
		self.window=window
		self.minsupport=0
		self.minconfig=0 
		self.suanfa='FP-Growth'

	
	#设置窗口
	def set_init_window(self):
		self.window.title("第一个GUI界面")      #窗口名
		self.window.geometry('1080x680+10+10')                 #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
		self.window["bg"] = "pink"                            #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
		self.init_data_label = Label(self.window, text="待处理数据")
		self.init_data_label.grid(row=0, column=0)
		self.result_data_label = Label(self.window, text="输出结果")
		self.result_data_label.grid(row=0, column=12)
		self.log_label = Label(self.window, text="日志")
		self.log_label.grid(row=12, column=0)
		self.init_data_Text = scrolledtext.ScrolledText(self.window, width=67, height=35,wrap=WORD)  #原始数据录入框
		self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
		self.result_data_Text = scrolledtext.ScrolledText(self.window, width=70, height=49,wrap=WORD)  #处理结果展示
		self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
		self.log_data_Text = scrolledtext.ScrolledText(self.window, width=66, height=9,wrap=WORD)  # 日志框
		self.log_data_Text.grid(row=13, column=0, columnspan=10)
		#按钮

		Button(self.window,text="清空",command=self.clear_result ,width=8).grid(row=0,column=18)
		Button(self.window,text="清空",command=self.clear_data,width=8).grid(row=0,column=5)

		Button(self.window, text="加载数据集",command=self.click1,  bg="lightblue", width=10).grid(row=1,column=11)  # 调用内部方法  加()为直接调用
		# self.str_trans_to_md5_button.grid(row=1, column=11)
		Button(self.window, text="选择算法",command=lambda:self.click2(), bg="lightblue", width=10).grid(row=2,column=11)  # 调用内部方法  加()为直接调用
 		# # self.str_trans_to_md5_button.grid(row=2, column=11)
		Button(self.window,text="输入参数",command=lambda:self.click3(),bg="lightblue",width=10).grid(row=3,column=11)
		# self.str_trans_to_md5_button
		Button(self.window, text="运行",command=lambda:self.click4(), bg="lightblue", width=10).grid(row=4, column=11)  # 调用内部方法  加()为直接调用
		# self.str_trans_to_md5_button
		Button(self.window,text="生成规则",command=lambda:self.click5(),bg="lightblue",width=10).grid(row=5,column=11)

	def clear_result(self):
		self.result_data_Text.delete(0.0,END)

	def clear_data(self):
		self.init_data_Text.delete(0.0,END)

	def loaddata_thread(self,fn):
		start = time.time()
		self.dataset = loaddata.load_data(fn)
		for i in self.dataset:
			self.init_data_Text.insert(INSERT,str(i))
			self.init_data_Text.insert(INSERT,'\n')
		end = time.time()
		self.log_data_Text.insert(INSERT,'加载完毕！共'+str(len(self.dataset))+'项	耗时：'+str(round(end-start,2))+'s\n')
	def click1(self):
		fn = tkFiledialog.askopenfilename()    #选择文件夹
		if (fn!=''):
			self.log_data_Text.insert(INSERT,'正在加载数据...\n')
			t=threading.Thread(target=self.loaddata_thread,args=(fn,))
			t.setDaemon(True)
			t.start()
		
		

		
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
		self.result_data_Text.insert(INSERT,'频繁项集:\n')
		start = time.time()	
		n=0
		if (self.suanfa=='Aprioi'):
			if(self.minsupport!=0):
				self.L,self.support=apriori.apriori(self.dataset,self.minsupport)
			else:
				self.L,self.support=apriori.apriori(self.dataset)
			for x in self.L:
				for i in x:
					self.result_data_Text.insert(INSERT,i)
					self.result_data_Text.insert(INSERT,'\n')
					n+=1

		else:
			self.frozenDataSet = fpgrowth.transfer2FrozenDataSet(self.dataset)
			self.L = {}
			self.prefix = set([])
			if(self.minconfig!=0):
				self.fptree,self.headPointTable = fpgrowth.createFPTree(self.frozenDataSet, self.minsupport)				
				fpgrowth.mineFPTree(self.headPointTable, self.prefix, self.L, self.minsupport)
			else:
				self.fptree,self.headPointTable = fpgrowth.createFPTree(self.frozenDataSet)
				fpgrowth.mineFPTree(self.headPointTable, self.prefix,self.L)
			for i in self.L:
				# print(i)
				self.result_data_Text.insert(INSERT,i)
				self.result_data_Text.insert(INSERT,'\n')
				n+=1
		self.result_data_Text.insert(INSERT,str(n)+'\n')	
		end = time.time()
		self.log_data_Text.insert(INSERT,'频繁项集已生成！	共'+str(n)+'项	耗时：'+str(round(end-start,2))+'s\n')

	def click4(self):
		self.log_data_Text.insert(INSERT,self.suanfa+'：正在挖掘频繁项集...\n')
		t=threading.Thread(target=self.aprithread)
		t.setDaemon(True)
		t.start()


	
	def rulesthread(self):
		start = time.time()
		if (self.suanfa=='Aprioi'):
			if(self.minconfig!=0):
				self.rules=apriori.generateRules(self.L,self.support,self.minconfig)
			else:
				self.rules=apriori.generateRules(self.L,self.support)
		else:
			self.rules = []
			if (self.minconfig!=0):
				Rules.rulesGenerator(self.L, self.rules, self.minconfig)
			else:
				Rules.rulesGenerator(self.L, self.rules)
		# self.rules = []
		# if (self.minconfig!=0):
		# 	Rules.rulesGenerator(self.L, self.rules, self.minconfig)
		# else:
		# 	Rules.rulesGenerator(self.L, self.rules)
		self.result_data_Text.insert(INSERT,'关联规则\n')
		for i in self.rules:
			self.result_data_Text.insert(INSERT,list(i))
			self.result_data_Text.insert(INSERT,'\n')
		end = time.time()
		self.result_data_Text.insert(INSERT,str(len(self.rules))+'\n')
		self.log_data_Text.insert(INSERT,'关联规则生成完毕! 共'+str(len(self.rules))+'项	耗时：'+str(round(end-start,2))+'s\n')


	def click5(self):
		self.log_data_Text.insert(INSERT,'正在生成关联规则...\n')
		t=threading.Thread(target=self.rulesthread)
		t.setDaemon(True)
		t.start()
