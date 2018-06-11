#encoding:utf-8
import csv


# product_dict = {}
# data_set=[]
# d={}
# cvs_file = csv.reader(open('order_products__prior.csv','r'))
#     # print(cvs_file)
# cvs_file2 = csv.reader(open('products.csv','r'))
# # for x in cvs_file2:
# #     print(x)
# cvs_file3 = open('products_aisle.csv','w',newline='')

# writer = csv.writer(cvs_file3)

# for x in cvs_file2:
#     d[x[0]]=x[2]
# for abc in cvs_file:
#     if (abc[0]=='order_id'):
#         continue
#         # t=find(abc[1])        
#     if (abc[1] in d):
#         t=d.get(abc[1])

#     if (abc[0] in product_dict):
#         if (product_dict[abc[0]].count(t)==0):
#             product_dict[abc[0]].append(t)
#     else:
#         product_dict.setdefault(abc[0],[]).append(t)
# writer.writerow(['order_id','aisle_id'])
# for kiy in product_dict:
#     writer.writerow([kiy,';'.join(product_dict[kiy])])

# product_dict = {}
# data_set=[]
# cvs_file = csv.reader(open('order_products__prior.csv','r'))
# cvs_file3 = open('order_products.csv','w',newline='')
# writer = csv.writer(cvs_file3)
# # print(cvs_file)
# for abc in cvs_file:
#     if abc[0]=='order_id':
#         continue
#     if abc[0] in product_dict:
#         product_dict[abc[0]].append(abc[1])
#     else:
#         product_dict.setdefault(abc[0],[]).append(abc[1])

#         # if i>n:
#         #     break
# writer.writerow(['order_id','product_id'])
# for kiy in product_dict:
#     writer.writerow([kiy,product_dict[kiy]])

# product_dict = {}
# data_set=[]
# cvs_file = csv.reader(open('order_products__prior.csv','r'))
# cvs_file3 = open('order_products.csv','w',newline='')
# writer = csv.writer(cvs_file3)
# # print(cvs_file)
# for abc in cvs_file:
#     if abc[0]=='order_id':
#         continue
#     if abc[0] in product_dict:
#         product_dict[abc[0]].append(abc[1])
#     else:
#         product_dict.setdefault(abc[0],[]).append(abc[1])

#         # if i>n:
#         #     break
# writer.writerow(['order_id','product_id'])
# for kiy in product_dict:
#     writer.writerow([kiy,';'.join(product_dict[kiy])])

