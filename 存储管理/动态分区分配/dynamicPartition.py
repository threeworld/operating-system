# -*- codin=utf-8 -*-

import copy,sys
import random
import uuid
from prettytable import PrettyTable

class node(object):
    def __init__(self, start, end, length, state=1, uid=''):
        self.start = start
        self.end = end
        self.length = length
        self.state = state  ##state为1：内存未分配
        self.taskId = uid ##ID为0是未分配，其余为任务编号

#初始化分区
def init(start, end, length):
    table = node(start, end, length)
    b = []
    b.append(table)
    return b

#显示状态函数
def showList(ptlist):
    print("分区表状态如下")
    show_table = PrettyTable(['分区号','分区大小','分区始址','分区状态','任务ID'])
    for i in range(0, len(ptlist)):
        p = ptlist[i]
        show_table.add_row([i+1, p.length,p.start, p.state,p.taskId])
    print(show_table)

#冒泡排序
def bubble_sort(ptlist):
    count = len(ptlist)
    for i in range(0, count):
        for j in range(i + 1, count):
            if ptlist[i].length < ptlist[j].length:
                ptlist[i], ptlist[j] = ptlist[j], ptlist[i]
    return ptlist

# 首次适应算法
def FirstFit(taskID, Tasklength, ptlist):
    size = 5
    for i in range(0, len(ptlist)):
        p = ptlist[i]
        #寻找合适的分区块
        if p.state == 1 and p.length > Tasklength :#and p.length-Tasklength <= size:
            node2 = node(p.start + Tasklength, p.end, p.length - Tasklength, 1)
            a = node(p.start, p.start + Tasklength - 1, Tasklength, state=0, uid=taskID)
            del ptlist[i]
            ptlist.insert(i, node2)
            ptlist.insert(i, a)
            showList(ptlist)
            return
        #如果分区块大小刚好合适
        if p.state == 1 and p.length == Tasklength:
            p.state = 0
            showList(ptlist)
            return
    print("内存空间不足")


#回收内存
def FreeSubArea(taskID, ptlist):
    x = 0
    for i in range(0, len(ptlist)):
        p = ptlist[i]
        if p.taskId == taskID:
            p.state = 1
            p.taskId = ''
            x = i
            break

    # 向前合并空闲块
    if x - 1 >= 0:
        if ptlist[x - 1].state == 1:
            a = node(ptlist[x - 1].start, ptlist[x].end, ptlist[x - 1].length + ptlist[x].length, 1)
            del ptlist[x - 1]
            del ptlist[x - 1]
            ptlist.insert(x - 1, a)
            x = x - 1
    # 向后合并空闲块
    if x + 1 < len(ptlist):
        if ptlist[x + 1].state == 1:
            a = node(ptlist[x].start, ptlist[x + 1].end, ptlist[x].length + ptlist[x + 1].length, 1)
            del ptlist[x]
            del ptlist[x]
            ptlist.insert(x, a)
    showList(ptlist)

##最佳适应算法
def BestFit(taskID, Tasklength, ptlist):
    plist = copy.copy(ptlist)
    sort_plist = bubble_sort(plist)
    best_location = -1
    best_location_equal = -1
    for i in range(0, len(sort_plist)):
        p = sort_plist[i]
        if p.state == 1 and p.length > Tasklength:
            best_location = p.start
        elif p.state == 1 and p.length == Tasklength:
            best_location_equal = p.start
    if best_location == -1 and best_location_equal == -1:
        print("内存空间不足")
        return
    for i in range(0, len(ptlist)):
        p = ptlist[i]
        if p.start == best_location:
            node2 = node(p.start + Tasklength, p.end, p.length - Tasklength, 1)
            a = node(p.start, p.start + Tasklength - 1, Tasklength, state=0, uid=taskID)
            del ptlist[i]
            ptlist.insert(i, node2)
            ptlist.insert(i, a)
            showList(ptlist)
            return
        elif p.start == best_location_equal:
            p.state = 0
            showList(ptlist)
            return

def randomProducejob(num, ptlist, method):
    sche_method = method + 'Fit'
    for i in range(1, num+1):
        job_size = random.randint(50,150)
        taskid = str(uuid.uuid4())[-3:]
        print('####################################################')
        print('分配作业: 作业ID: %s \t作业大小: %s'%( taskid,job_size))
        eval(sche_method)(taskid, job_size , ptlist)
        
if __name__ == '__main__':
    print("1.使用首次适应算法")
    print('2.使用最佳适应算法')
    print('3.查看当前分区情况')
    print('4.回收指定的作业')
    print('0.退出程序')
    choose={
    '1':'First',
    '2':'Best',
    '3':'showList',
    '4':'FreeSubArea',
    '0':'exit'
    }
    b = init(0, 599, 600)
    while True:
        x = input('>')
        if x not in choose.keys():
            print('exit')
            sys.exit()
        method = choose[x]
        x = int(x)
        if x == 1:
            print('请输入要分配的作业数: (建议3~5)')
            job_num = input('>')
            randomProducejob(int(job_num), b, method)
        elif x == 2:
            print('请输入要分配的作业数: (建议3~5)')
            job_num = input('>')
            randomProducejob(int(job_num), b, method)
        elif x == 3:
            showList(b)
        elif x == 4:
            print('请输入要回收的作业id: ')
            job_id = input('>')
            eval(method)(job_id,b)
        else:
            print('exit.')
            sys.exit()
           