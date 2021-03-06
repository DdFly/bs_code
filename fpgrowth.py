#coding=utf-8  

import loaddata
# import fpgrouth


def transfer2FrozenDataSet(dataSet):
    """
    将初始数据装换为字典
    参数：dataSet
    返回：frozenDataSet
    """
    frozenDataSet = {}
    global n
    n=0
    for elem in dataSet:
        if(frozenset(elem) in frozenDataSet):
            frozenDataSet[frozenset(elem)] +=1
        else:
            frozenDataSet[frozenset(elem)] = 1
        n+=1
    return frozenDataSet


class TreeNode:
    """
    节点类型：
    nodeName:节点名称
    count:节点计数
    nodeParent:父节点指针
    increaseC:修改节点计数
    """
    def __init__(self, nodeName, count, nodeParent):
        self.nodeName = nodeName
        self.count = count
        self.nodeParent = nodeParent
        self.nextSimilarItem = None
        self.children = {}

    def increaseC(self, count):
        self.count += count

def createFPTree(frozenDataSet, minSupport=0.01):
    
    """
    构建FP-Tree
    参数：  frozenDataSet：初始数据字典
            minSupprot：最小支持多
    返回：  fpTree：FP树
            headPointTable：项头表
    """
    #第一次扫描数据，创建项头表，统计各个数据的支持度
    headPointTable = {}
    for items in frozenDataSet:
        for item in items:
            headPointTable[item] = headPointTable.get(item, 0) + frozenDataSet[items]

    # 删除不满足最小支持度的节点
    headPointTable = {k:v for k,v in headPointTable.items() if v/n >= minSupport}
    frequentItems = set(headPointTable.keys())
    if len(frequentItems) == 0: return None, None
    # 遍历项头表，保存节点计数，增加指向第一个元素项的指针
    for k in headPointTable:
        headPointTable[k] = [headPointTable[k], None]
    # 初始化根节点
    fptree = TreeNode("null", 1, None)
    
    # 第二次扫描数据，
    for items,count in frozenDataSet.items():
        frequentItemsInRecord = {}
        for item in items:
            if item in frequentItems:
                #筛选出频繁项集
                frequentItemsInRecord[item] = headPointTable[item][0]
        if len(frequentItemsInRecord) > 0:
            #对频繁项集进行排序
            orderedFrequentItems = [v[0] for v in sorted(frequentItemsInRecord.items(), key=lambda v:v[1], reverse = True)]
            #向树中添加该条数据
            updateFPTree(fptree, orderedFrequentItems, headPointTable, count)

    return fptree, headPointTable

def updateFPTree(fptree, orderedFrequentItems, headPointTable, count):
    
    if orderedFrequentItems[0] in fptree.children:
        #树中存在该节点，则增高该节点的计数
        fptree.children[orderedFrequentItems[0]].increaseC(count)
    else:
        #创建一个新节点，将该节点插入树中
        fptree.children[orderedFrequentItems[0]] = TreeNode(orderedFrequentItems[0], count, fptree)

        #更新项头表
        if headPointTable[orderedFrequentItems[0]][1] == None:
            headPointTable[orderedFrequentItems[0]][1] = fptree.children[orderedFrequentItems[0]]
        else:
            updateHeadPointTable(headPointTable[orderedFrequentItems[0]][1], fptree.children[orderedFrequentItems[0]])
    
    if(len(orderedFrequentItems) > 1):
        updateFPTree(fptree.children[orderedFrequentItems[0]], orderedFrequentItems[1::], headPointTable, count)

def updateHeadPointTable(headPointBeginNode, targetNode):
    #更新频繁项集
    while(headPointBeginNode.nextSimilarItem != None):
        headPointBeginNode = headPointBeginNode.nextSimilarItem
    headPointBeginNode.nextSimilarItem = targetNode
#递归查找频繁项集
def mineFPTree(headPointTable, prefix, frequentPatterns, minSupport=0.01):
    #将项头表中的元素按支持度升序排序
    headPointItems = [v[0] for v in sorted(headPointTable.items(), key = lambda v:v[1][0])]
    if(len(headPointItems) == 0): return
    #从fp树的底层向根基地点逐层查找
    for headPointItem in headPointItems:
        newPrefix = prefix.copy()
        newPrefix.add(headPointItem)
        support = headPointTable[headPointItem][0]
        frequentPatterns[frozenset(newPrefix)] = support
        #创建条件模式基
        prefixPath = getPrefixPath(headPointTable, headPointItem)
        #递归
        if(prefixPath != {}):
            conditionalFPtree, conditionalHeadPointTable = createFPTree(prefixPath, minSupport)
            if conditionalHeadPointTable != None:
                mineFPTree(conditionalHeadPointTable, newPrefix, frequentPatterns, minSupport)

def getPrefixPath(headPointTable, headPointItem):
    """
    寻找该节点的条件模式基
    参数：  headPointTable:项头表
            headPointItem:项头表里的元素，寻找该元素的条件模式基
    返回：FP树中所有headPointItem节点的条件模式基
    """
    prefixPath = {}
    beginNode = headPointTable[headPointItem][1]
    prefixs = ascendTree(beginNode)
    if((prefixs != [])):
        prefixPath[frozenset(prefixs)] = beginNode.count

    while(beginNode.nextSimilarItem != None):
        beginNode = beginNode.nextSimilarItem
        prefixs = ascendTree(beginNode)
        if (prefixs != []):
            prefixPath[frozenset(prefixs)] = beginNode.count
    return prefixPath


def ascendTree(treeNode):
    """
    由当前节点向根节点回溯
    参数：treeNode:当前节点
    返回：prefixs：条件模式基
    """
    prefixs = []
    while((treeNode.nodeParent != None) and (treeNode.nodeParent.nodeName != 'null')):
        treeNode = treeNode.nodeParent
        prefixs.append(treeNode.nodeName)
    return prefixs

def rulesGenerator(frequentPatterns, rules, minConf=0.1):
    """
    计算关联规则
    参数：frequentpatterns:频繁项集
            rules：已生成的规则
            minConf:最小支持度
    """
    for frequentset in frequentPatterns:
        if(len(frequentset) > 1):
            getRules(frequentset,frequentset, rules, frequentPatterns, minConf)

def removeStr(set, str):

    tempSet = []
    for elem in set:
        if(elem != str):
            tempSet.append(elem)
    tempFrozenSet = frozenset(tempSet)
    return tempFrozenSet


def getRules(frequentset,currentset, rules, frequentPatterns, minConf=0.1):
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

