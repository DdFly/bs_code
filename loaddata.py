


def load_data(path_str='order_products__prior.csv'):
    import csv
    n=100000
    i=1
    product_dict = {}
    data_set=[]
    cvs_file = csv.reader(open(path_str,'r'))
    # print(cvs_file)
    for abc in cvs_file:
        if abc[0]=='order_id':
            continue
        if abc[0] in product_dict:
            product_dict[abc[0]].append(abc[1])
        else:
            product_dict.setdefault(abc[0],[]).append(abc[1])
        i+=1
        # if i>n:
        #     break
    for l in product_dict:
        data_set.append(product_dict[l])
    # print(data_set)
    # data_set = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],['l1','l2','l3','l4','l5','l6','l7'],
    #         ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
    #         ['l1', 'l3'], ['l1', 'l2', 'l3','l4', 'l5'], ['l1', 'l2', 'l3','l4']]
    return data_set