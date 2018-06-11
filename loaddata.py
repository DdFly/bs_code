
import csv

def load_data(path_str='order_products.csv'):

    data_set = []
    cvs_file = csv.reader(open(path_str,'r'))
    n=0
    for x in cvs_file:
        if (x[0]=='order_id'):
            continue
        data_set.append(x[1].split(";"))
        n+=1
        # if (n>30000):
        #     break

   

    # data_set = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],['l1','l2','l3','l4','l5','l6','l7'],
    #         ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
    #         ['l1', 'l3'], ['l1', 'l2', 'l3','l4', 'l5'], ['l1', 'l2', 'l3','l4']]
    # print(data_set)
    # for i in data_set:
    #     print (i)
    return data_set
# load_data()