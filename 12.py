#coding=utf-8
import numpy as np
import pandas as pd
import itertools
import time


#获取一个k4的weight值
def get_weight(l,right,left):  #l表示一个k4的四个顶点，right表示已经染right色的边集合，left表示已经染left色的边集合
    a=b=0  #a,b分别表示染色的条数
    for i in list(itertools.combinations(sorted(l),2)):
        if i in right:
            a+=1
        elif i in left:
            b+=1
        else:
            pass
    if a>0 and b>0:      #如果两种颜色都染，则返回weight=0
        return 0
    elif a>0:           #只染right色
        return pow(0.5,6-a)
    elif b>0:           #只染left色
        return pow(0.5,6-b)
    else:               #未染色
        return pow(0.5,5)


#如果下一条边e染成right色，则涉及e的k4的weight的和值
def get_weight_right(e,all_k4):
    tem_edge_right=edge_right.copy()
    tem_edge_right.append(e)
    tem_edge_left=edge_left.copy()
    # index = [i - 1 for i in e]
    # new_x = np.delete(x, index)
    # tem_k=list(itertools.combinations(new_x,2))
    # all_k4 = [i + e for i in tem_k]
    w=0
    for i in all_k4:
        w += get_weight(i,tem_edge_right,tem_edge_left)
    return w

#如果下一条边e染成left色，则涉及e的k4的weight的和值
def get_weight_left(e,all_k4):
    tem_edge_right=edge_right.copy()
    tem_edge_left=edge_left.copy()
    tem_edge_left.append(e)
    # index = [i - 1 for i in e]
    # new_x = np.delete(x, index)
    # tem_k=list(itertools.combinations(new_x,2))
    # all_k4 = [i + e for i in tem_k]
    w=0
    for i in all_k4:
        w += get_weight(i,tem_edge_right,tem_edge_left)
    return w


#下一条边e未染色前，涉及e的k4的weight的和值
def get_weight_none(all_k4):
    tem_edge_right=edge_right.copy()
    tem_edge_left=edge_left.copy()
    # index = [i - 1 for i in e]
    # new_x = np.delete(x, index)
    # tem_k=list(itertools.combinations(new_x,2))
    # all_k4 = [i + e for i in tem_k]
    w=0
    for i in all_k4:
        w += get_weight(i,tem_edge_right,tem_edge_left)
    return w

#获取同色的k4数量
def k4_number(final_edge_right,final_edge_left):  #final_edge_right表示最终染为right色的边集合，#final_edge_left表示最终染为left色的边集合
    number=0
    for l in K4:
        a=list(itertools.combinations(l, 2))  #a表示一个k4的六条边集合
        if set(a) <= set(final_edge_left) or \
                set(a) <= set(final_edge_right):    #判断边是都为right色还是left色
            number+=1
        else:
            pass
    return(number)



start=time.time()

n=100
x=np.arange(1,n+1,dtype=np.int64)     #x为1~100个点
K4=list(itertools.combinations(x,4))      #K4表示所有k4集合
edge=list(itertools.combinations(x,2))      #edge表示所有边集合
print(len(edge))
edge_right=[]
edge_left=[]
init_weight=len(K4)*pow(0.5,5)      #初始weight和
all_W=init_weight

for j,e in enumerate(edge):
    index = [i - 1 for i in e]          #选取与e相关的k4集合
    new_x = np.delete(x, index)
    tem_k = list(itertools.combinations(new_x, 2))
    all_k4 = [i + e for i in tem_k]    #all_k4为包含边e的所有k4集合
    weight=get_weight_none(all_k4)
    weight_r=get_weight_right(e,all_k4)

    if weight>=weight_r:            #weight=(weight_r+weight_l)/2
        all_W=all_W-weight+weight_r
        edge_right.append(e)
    else:
        weight_l=get_weight_left(e,all_k4)
        all_W=all_W-weight+weight_l
        edge_left.append(e)
    if j%100==0:
        print('The code run{}次'.format(j/100))

print(all_W)
print()
print(len(edge_left))
print(len(edge_right))

end=time.time()
print('The code run{:f}s'.format(end-start))

number=k4_number(edge_right,edge_left)
print(number)
print('The code run{:f}s'.format(time.time()-end))