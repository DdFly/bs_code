

class treeNode:
	# 树中节点定义
	"""
		self.name:节点名称
		self.count:
		self.nodeLink:链接相似的元素项
		self.parent:指向父节点
		self.children:指向子节点

	"""
	def __init__(self, nameValue, numOccur, parentNode):
		self.name = nameValue
		self.count = numOccur
		self.nodeLink = None 		#链接相似的元素项
		self.parent = parentNode	#指向父节点
		self.children = {}			#空字典，存放子节点
 	
	def inc(self, numOccur):
		self.count += numOccur
 	# 以文本形式打印树
	# def disp(self, ind=1):
	# 	print(' ' * ind, self.name, ' ', self.count)
	# 	for child in list(self.children.values()):
	# 		child.disp(ind + 1)

def createTree(dataSet, minSup=1):
	''' 创建FP树 '''
	# 第一次遍历数据集，创建项头表
	headerTable = {}
	for trans in dataSet:
		for item in trans:
			headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
	# 移除不满足最小支持度的元素项
	for k in list(headerTable.keys()) :
		if headerTable[k] < minSup:
			del(headerTable[k])
	# 空元素集，返回空
	freqItemSet = set(headerTable.keys())
	if len(freqItemSet) == 0:
		return None, None
	# 增加一个数据项，用于存放指向相似元素项指针
	for k in headerTable:
		headerTable[k] = [headerTable[k], None]
	# print ('headerTable: ',headerTable)
	retTree = treeNode('Null Set', 1, None) # 根节点
	# 第二次遍历数据集，创建FP树
	for tranSet, count in list(dataSet.items()):
		localD = {} # 对一个项集tranSet，记录其中每个元素项的全局频率，用于排序
		for item in tranSet:
			if item in freqItemSet:
				localD[item] = headerTable[item][0] # 注意这个[0]，因为之前加过一个数据项
		if len(localD) > 0:
			orderedItems = [v[0] for v in sorted(list(localD.items()), key=lambda p: p[1], reverse=True)] # 排序
			updateTree(orderedItems, retTree, headerTable, count) # 更新FP树
	return retTree, headerTable

def loadSimpDat():
	simpDat = [['r', 'z', 'h', 'j', 'p'],
			   ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
			   ['z'],
			   ['r', 'x', 'n', 'o', 's'],
			   ['y', 'r', 'x', 'z', 'q', 't', 'p'],
			   ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
	return simpDat

def updateTree(items, inTree, headerTable, count):
	if items[0] in inTree.children:
		# 有该元素项时计数值+1
		inTree.children[items[0]].inc(count)
	else:
		# 没有这个元素项时创建一个新节点
		inTree.children[items[0]] = treeNode(items[0], count, inTree)
		# 更新头指针表或前一个相似元素项节点的指针指向新节点
		if headerTable[items[0]][1] == None:
			headerTable[items[0]][1] = inTree.children[items[0]]
		else:
			updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
 
	if len(items) > 1:
		# 对剩下的元素项迭代调用updateTree函数
		updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):
	while (nodeToTest.nodeLink != None):
		nodeToTest = nodeToTest.nodeLink
	nodeToTest.nodeLink = targetNode

""" 将初始数据由列表转换为字典 """
def createInitSet(dataSet):
	retDict = {}
	for trans in dataSet:
		retDict[frozenset(trans)] = 1
	return retDict

"""寻找条件模式基"""
def findPrefixPath(basePat, treeNode):
	''' 创建前缀路径 '''
	condPats = {}
	while treeNode != None:
		prefixPath = []
		ascendTree(treeNode, prefixPath)
		if len(prefixPath) > 1:
			condPats[frozenset(prefixPath[1:])] = treeNode.count
		treeNode = treeNode.nodeLink
	return condPats
"""向上回溯，直到根节点"""
def ascendTree(leafNode, prefixPath):
	if leafNode.parent != None:
		prefixPath.append(leafNode.name)
		ascendTree(leafNode.parent, prefixPath)

""" 查找频繁项集 """
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
	bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: str(p[1]))]
	for basePat in bigL:
		newFreqSet = preFix.copy()
		newFreqSet.add(basePat)
		freqItemList.append(newFreqSet)
		condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
		myCondTree, myHead = createTree(condPattBases, minSup)
 
		if myHead != None:
			# 用于测试
			# print('conditional tree for:', newFreqSet)
			# myCondTree.disp()
			mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def fpGrowth(dataSet, minSup=3):
	initSet = createInitSet(dataSet)
	# print(initSet)
	myFPtree, myHeaderTab = createTree(initSet, minSup)
	# print(myFPtree)
	freqItems = []
	mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
	return freqItems


def removeStr(set, str):
    tempSet = []
    for elem in set:
        if(elem != str):
            tempSet.append(elem)
    tempFrozenSet = frozenset(tempSet)
    return tempFrozenSet

def rulesGenerator(frequentPatterns, minConf, rules):
    for frequentset in frequentPatterns:
        if(len(frequentset) > 1):
            getRules(frequentset,frequentset, rules, frequentPatterns, minConf)
 
def getRules(frequentset,currentset, rules, frequentPatterns, minConf):
    for frequentElem in currentset:
        subSet = removeStr(currentset, frequentElem)
        confidence = frequentPatterns[frequentset] / frequentPatterns[subSet]
        if (confidence >= minConf):
            flag = False
            for rule in rules:
                if(rule[0] == subSet and rule[1] == frequentset - subSet):
                    flag = True
            if(flag == False):
                rules.append((subSet, frequentset - subSet, confidence))
 
            if(len(subSet) >= 2):
                getRules(frequentset, subSet, rules, frequentPatterns, minConf)



# rootNode = treeNode('pyramid', 9, None)
# rootNode.children['eye'] = treeNode('eye', 13, None)
# rootNode.children['phoenix'] = treeNode('phoenix', 3, None)
# rootNode.disp()

""" 加载数据 """
dataSet = loadSimpDat()
# # freqItems = fpGrowth(dataSet)
""" 列表转为字典 """
initSet = createInitSet(dataSet)

myFPtree, myHeaderTab = createTree(initSet, 3)
# # myFPtree.disp()
freqItems = []
mineTree(myFPtree, myHeaderTab, 3, set([]), freqItems)
print(freqItems)
rules = []
rulesGenerator(freqItems,0.7,rules)
print(rules)
# if __name__=="__main__":
	
	# print(dataSet)
	
	# print(freqItems)