import itertools
import copy
import time
import random
import math
import config as thread_running
import threading
import pulp
from concurrent.futures import ThreadPoolExecutor

def greedy_cover(n,k,j,s):

    def Gen(x,y):
        if y > len(x):
            print("K is larger than N")
            return
        if y == len(x):
            return x
        Group = [each for each in itertools.combinations(x,y)]
        return list(Group)


    NK_Group = Gen(range(n),k)
    NK_Length = len(NK_Group)
    # print(NK_Length)
    NK_Group_num = list()
    Group_map = list()
    Mainlist = list()
    NK_Tag = list()
    NJ_Mark = set()
    Final_Ans = list()
    Final_Ans_example = list()

    for i in range(n):
        Mainlist.append(i)

    def transform(x):
        ans = 0
        for i in range(len(x)):
            ans = ans + int(2**(x[i]))
        return int(ans)

    def find_map(x):
        ans = list()
        if s == 1:
            print("s couldn't be 1")
            return
        Group = Gen(x,s)

        for each in Group:
            if j == s:
                ans.append(transform(each))
                continue
            
            cop = copy.deepcopy(Mainlist)
            set1 = set(each)
            set2 = set(cop)
            cop = tuple(set1.symmetric_difference(set2))
            Rest = Gen(cop, j-s)
            if (len(Rest) == 1):
                ans2 = tuple(list(each) + Rest)
                ans.append(transform(ans2))
            else:
                for each2 in Rest:
                    ans2 = each + each2
                    ans.append(transform(ans2))
        ans = set(ans)
        return ans
            

    for i in range (NK_Length):
        NK_Group_num.append(transform(NK_Group[i]))

    for i in range (NK_Length):
        if(not thread_running.get()):
            return 0,0,[]
        ThisMap = find_map(NK_Group[i])
        Group_map.append(ThisMap)
        NJ_Mark = NJ_Mark.union(ThisMap)


    for i in range (NK_Length):
        NK_Tag.append(False)


    NJ_Length = len(NJ_Mark)
    if(n>=12):
        type = True
    else:
        type = False

    testMap = Group_map

    while len(NJ_Mark)>0:
            if(not thread_running.get()):
                return 0,0,[]
            Max_Group_no = -1
            Max_Group_sum = 0
            for i in range (NK_Length):
                if(not thread_running.get()):
                    return False
                if(NK_Tag[i] == True):
                    continue
                if len(Group_map[i]) > Max_Group_sum:
                    Max_Group_no = i
                    Max_Group_sum = len(Group_map[i])
            if(Max_Group_no == -1):
                print("Error")
                break
            
            NK_Tag[Max_Group_no] = True
            for i in range (NK_Length):
                if(not thread_running.get()):
                    return 0,0,[]
                if(NK_Tag[i] == True):
                    continue
                Group_map[i] = Group_map[i].difference(Group_map[Max_Group_no])
            
            NJ_Mark = NJ_Mark.difference(Group_map[Max_Group_no])
            Final_Ans.append(Max_Group_no)
    result = [[i for i in group] for group in NK_Group]  # 将元组转换为列表
    final_result = [result[i] for i in Final_Ans]
    
    return final_result