#encoding:utf-8
# import csv

# cvs_file = csv.reader(open('order_products__prior.csv','r'))
#     # print(cvs_file)
# for abc in cvs_file:
# 	print(abc)


def loadDataSet():
    """
    加载数据
    返回：dataSet
    """
    dataSet = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],['l2'],['l1','l2','l3','l4','l5','l6','l7'],
        ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
        ['l1', 'l3'], ['l1', 'l2', 'l3','l4', 'l5'], ['l1', 'l2', 'l3','l4']]
    return dataSet


def transfer2FrozenDataSet(dataSet):
    """
    将初始数据装换为字典
    参数：dataSet
    返回：frozenDataSet
    """
    frozenDataSet = {}
    for elem in dataSet:
    	if(frozenset(elem) in frozenDataSet):
    		frozenDataSet[frozenset(elem)] +=1
    	else:
        	frozenDataSet[frozenset(elem)] = 1

    return frozenDataSet

print(transfer2FrozenDataSet(loadDataSet()))