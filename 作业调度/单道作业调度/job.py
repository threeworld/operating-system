#coding=utf-8

import sys,random,time
from prettytable import PrettyTable

#作业控制块
class jcb:
    def __init__(self):
        self.status='Wait'                  #Run, Finish or wait
        self.name=GetName()                 #动态生成名字
        self.submitTime=random.randint(0,5) #提交作业的时间
        self.needTime=random.randint(5,6)   #所需运行的时间
        self.resource=random.randint(5,20)  #所需的资源
        self.isAlive=False                  #是否被激活进入handlerJcb处理队列中，激活后应该变身为Wait状态
        self.runtime=0                      #运行时间
        """"
        周转时间: 完成时间-提交作业的时间 
        平均周转时间= 周转时间/运行时间 
        """
        self.startTime=-1
        self.endTime=-1             
        self.cycling_time=-1        #周转时间
        self.w_cycling_time=-1.0    #带权周转时间

#FCFS队列
class FCFSQueue:
    
    def __init__(self):
        self.q=[]    
       
    def insert(self,e):
        """ 先来先服务算法，只要把新提交的作业放到等待队列的最后面 """
        self.q.append(e)

    def pop(self):
        return self.q.pop(0)

    def isEmpty(self):
        return len(self.q)==0

#SJF最短作业优先队列
class SJFQueue:
    
    def __init__(self):
        self.q=[]     

    def insert(self,e):
        """ 最短作业优先"""
        if len(self.q)==0:
            self.q.append(e)
        else:
            for i in range(len(self.q)):
                if e.needTime<self.q[i].needTime:
                    break
            self.q.insert(i,e)

    def pop(self):
        return self.q.pop(0)

    def isEmpty(self):
        return len(self.q)==0

#HRN 最高响应度优先
class HRNQueue:
    
    def __init__(self):
        self.q=[]      

    def insert(self,e):
        self.q.append(e)

    def dynamicSort(self):
        #响应比xyb
        #xyb=1.0+e.waittime/e.needTime
        #e.waittime=currentTime-e.submitTime
        global hj
        currentTime=hj.getCurrentTime()
        self.q.sort(key=lambda x: 1.0+(0.0+currentTime-x.submitTime)/x.needTime,reverse=False)
    
    def pop(self):
        self.dynamicSort()
        return self.q.pop()

    def isEmpty(self):
        return len(self.q)==0

#处理作业函数
class handleJob:
    def __init__(self, kind):
        #选择的调度算法
        sche_method = kind + 'Queue'
        self.submitQueue=produceJobQueue()      #随机生成作业
        self.WaitQueue=eval(sche_method)()      #等待运行的作业
        self.runJcb=None                        #正在运行的作业
        self.doneJcb=[]                         #运行结束的作业
        self.currentTime=0                      #当前的时间
        self.solution=sche_method               #FCFS 

    #获取当前运行的时间
    def getCurrentTime(self):
        return self.currentTime
    
    #检测当前生成的作业
    def checkToSubmit(self):
        while True:
            if len(self.submitQueue)==0:  #如果队列为空
                break
            t=self.submitQueue[0]
            if t.submitTime==self.currentTime:
                self.submitQueue.pop(0)
                t.isAlive=True
                t.status='Wait'
                self.WaitQueue.insert(t)
                print('have submit job %s to cpu'%t.name)
            else:
                break

    #检查CPU当前情况
    def checkManageCPU(self):
        ##首先检查是否需要进行调度新的作业进来（是否可以运行新的作业，也就是cpu不存在作业或者作业刚好做完）
        if self.runJcb == None or self.runJcb.runtime == self.runJcb.needTime:
            #此时需要调度作业
            #先将作业调度出队列
            if self.runJcb!=None:
                t=self.runJcb
                t.status='Finish'
                t.endTime=self.currentTime
                t.cycling_time=t.endTime-t.submitTime
                t.w_cycling_time=1.0*t.cycling_time/t.needTime
                self.doneJcb.append(t)
                self.runJcb=None
                print('job %s finished and leave the cpu'%t.name)
            #如果有作业可以调度
            if not self.WaitQueue.isEmpty():
                t=self.WaitQueue.pop()
                t.status='Run'
                t.startTime=self.currentTime
                self.runJcb=t
                print("job %s starts to run"%t.name)
            else:
            #如果不存在作业
                print(u'no jobs to dive in the cpu')

    def runs(self):
        t=self.runJcb
        if t!=None:
            t.runtime+=1
            print('job %s have run %ds ,it needs %d seconds to complete'%(t.name,t.runtime,t.needTime))
        else:
            print('no job runs in the cpu')
        self.currentTime+=1
        time.sleep(1)


    def goOneSecond(self):
        print(u'第%d秒:'%self.currentTime)
        self.checkToSubmit()
        self.checkManageCPU()       
        self.runs()

    def isNeedRun(self):
        return not(len(self.submitQueue)==0 and self.WaitQueue.isEmpty() and self.runJcb==None)

    def displayEnding(self):
        jobtable = PrettyTable(['作业名称','到达时间','服务时间','开始执行时间','完成时间','周转时间','带权周转时间'])
        sumcycling_time=0
        sumw_cycling_time=0.0
        for i in range(len(self.doneJcb)):
            t=self.doneJcb[i]
            sumcycling_time += t.cycling_time
            sumw_cycling_time += t.w_cycling_time
            jobtable.add_row([t.name,t.submitTime,t.needTime,t.startTime,t.endTime,t.cycling_time,round(t.w_cycling_time,2)])
        average_table = PrettyTable(['平均周转时间','平均带权周转时间'])
        average_sumcycling_time = round(sumcycling_time*1.0/len(self.doneJcb),2)
        average_sumw_cycling_time = round(sumw_cycling_time*1.0/len(self.doneJcb),2)
        average_table.add_row([average_sumcycling_time,average_sumw_cycling_time])
        print(jobtable)
        print(average_table)

    def start(self):
        """ #因为不考虑作进程调度，又因为是单核cpu，所以作业调入cpu等到执行完才可以退出， 从而挑选下一个进程。代入Cpu执行 """
        print('采取的调度方式: '+self.solution)
        while self.isNeedRun():
            print('------------------------------------------------')
            self.goOneSecond()
        else:
            print('------------------------------------------------')
            print('All Jobs Done')
            print('------------------------------------------------')
        self.displayEnding()            

    """ 
    应该分两部分处理 未提交的jcb队列控制 和提交后的jcb队列控制（也就是handlerJcb）
    未提交队列应该有提交算法：也就是按时把作业提交给handlerJcb。其实它的作业就是激
    活一个作业，所以这部分可以写在handlerJcb里面 提交队列由handler控制有三种算法 
    """

def init():
    global nameI,jcbQueue
    nameI='a'

def GetName():
    global nameI
    t=nameI
    nameI=chr(ord(nameI)+1)
    return t

def produceJobQueue():
    num=input('How many job do you want?(suggested 3~5)\n>')
    num=int(num,10)
    print('\t\tproduce %d jobs'%num)
    jobqueue=[]
    #同时按照提交时间排序
    for i in range(num):
        t=jcb()
        j=0
        if len(jobqueue)!=0:
            for j in range(len(jobqueue)):
                if t.submitTime<jobqueue[j].submitTime:
                    jobqueue.insert(j,t)
                    break
            else:
                jobqueue.append(t)
        else:
            jobqueue.append(t)
        print('job '+t.name+':','submitTime=%d'%t.submitTime,'needTime=%d'%t.needTime,'resource=%d'%t.resource)
    while True:
        c=input('ok?(y/n/c)(input c for look all the jobQueue)')
        if c=='n':sys.exit()
        elif c=='c':
            print('------------------------------------------------')
            for i in range(len(jobqueue)):
                t=jobqueue[i]
                print('job '+t.name+':','submitTime=%d'%t.submitTime,'needTime=%d'%t.needTime,'resource=%d'%t.resource)
            print('------------------------------------------------')
        elif c=='y':
            return jobqueue

if __name__=="__main__":
    global hj
    print('1.FCFS')
    print('2.SJF')
    print('3.HRN')
    c=input('>')
    choose={
    '1':'FCFS',
    '2':'SJF',
    '3':'HRN'
    }
    if c not in choose.keys():
        print('exit')
        sys.exit()
    init()
    hj=handleJob(choose[c])
    hj.start()