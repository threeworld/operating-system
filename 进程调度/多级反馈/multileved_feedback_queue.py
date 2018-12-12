# -*- coding = utf-8 -*-

from prettytable import PrettyTable

class Process:
    '''
    结构体
    '''
    def __init__(self,name,arrive_time,serve_time):
        self.name=name #进程名
        self.arrive_time=arrive_time #到达时间
        self.serve_time=serve_time #需要服务的时间
        self.left_serve_time=serve_time #剩余需要服务的时间
        self.finish_time=0 #完成时间
        self.cycling_time=0 #周转时间
        self.w_cycling_time=0 #带权周转时间

class Queue:
    '''
    队列
    '''
    def __init__(self,level,process_list):
        self.level=level
        self.process_list=process_list
        self.q=0

    def size(self):
        return len(self.process_list)

    def get(self,index):
        return self.process_list[index]    

    def add(self,process):
        self.process_list.append(process)

    def delete(self,index):
        self.process_list.remove(self.process_list[index])

class RR:
    '''
    轮转法
    '''
    def __init__(self,process_list,q):
        self.process_list=process_list
        self.q=q
    def scheduling(self):
        #process_list.sort(key=lambda x:x.arrive_time)#按照.arrive_time进行排序
        len_queue=len(self.process_list) #进程队列的长度
        index=int(0)  #索引
        q=self.q      #时间片
        running_time=int(0)#已经运行了的时间

        #调度的循环
        while(True):
            #当前进程
            n=index%len_queue
            current_process=self.process_list[n]
            #判断当前进程是否已经被完成
            if current_process.left_serve_time>0: 
                #计算完成时间
                #还需要服务的时间大于等于时间片，则完成时间+时间片时间  此进程还没结束
                #还需要服务的时间小于时间片，则完成时间在原来基础上加上继续服务的时间
                rr_table = PrettyTable(['进程名','需要服务时间','已服务的时间','剩余需要服务时间'])
                if current_process.left_serve_time>=q:
                    running_time+=q
                    #print('正在运行: %s , 已运行时间: %d , 索引: %d'%(current_process.name,running_time,index))
                    current_process.left_serve_time-=q

                else :
                    #print('%s 还需要服务的时间小于当前时间片'%current_process.name)
                    running_time+=current_process.left_serve_time
                    current_process.left_serve_time=0
                for i in range(len_queue):
                    if n+i<len_queue:
                        rr_table.add_row([self.process_list[n+i].name,self.process_list[n+i].serve_time,self.process_list[n+i].serve_time-self.process_list[n+i].left_serve_time, self.process_list[n+i].left_serve_time])
                    else:
                        m=(n+i)%len_queue
                        rr_table.add_row([self.process_list[m].name,self.process_list[m].serve_time,self.process_list[m].serve_time-self.process_list[m].left_serve_time,self.process_list[m].left_serve_time])
                print(rr_table)

            #已完成
            if current_process.left_serve_time==0:
                #计算完成时间
                current_process.finish_time=running_time
                #计算周转时间
                current_process.cycling_time=current_process.finish_time-current_process.arrive_time
                #计算带权周转时间
                current_process.w_cycling_time=float(current_process.cycling_time)/current_process.serve_time
                #打印
                print('%s 进程已完成'%current_process.name)
                #print('进程名称：%s  ，完成时间： %d    ，周转时间：%d  ，带权周转时间： %.2f'%(current_process.name,current_process.finish_time,current_process.cycling_time,current_process.w_cycling_time))
                print('***********************************************************')
                #弹出
                self.process_list.remove(current_process)
                len_queue=len(self.process_list)
                #有进程完成任务后，index先回退，之后再加，以保持指向下一个需要调度的进程
                index-=1
            #index常规增加
            index+=1     

            #如果队列中没有进程则表示执行完毕
            if len(self.process_list)==0:
                print('全部进程都已完成')
                break

            #改变index，避免因为index大于len，导致取模时出错
            if index>=len(self.process_list):
                index=index%len_queue


class MulitlevedFeedbackQueue():
    '''
    多级反馈
    '''
    def __init__(self,queue_list,q_first):
        self.queue_list=queue_list
        self.q_first=q_first
    def scheduling(self):
        q_list=self.queue_list  #当前队列集合
        q_first=self.q_first                #第一个队列的时间片

        for i in range(len(q_list)):
            #确定每个队列的时间片
            if i==0:
                q_list[i].q=q_first
            else :
                q_list[i].q=q_list[i-1].q*2

            #从第一个队列开始执行时间片
            #先判断是否是最后一个队列，最后一个队列直接执行RR调度算法
            #不是最后一个队列的话，就执行当前队列时间片后判断是否有必要加入到下一个队列的末尾
            if i==len(q_list)-1 :               
                #print(q_list[i].process_list[])
                #最后一个队列重新设置到达时间
                #for t in range(len(q_list[i].process_list)):
                   # q_list[i].process_list[t].arrive_time=t
                if len(q_list[i].process_list)!=0:
                    print('***********对最后一个队列执行RR调度算法,时间片为%d**********'%(q_list[i].q))
                    rrr_table = PrettyTable(['进程名','需要服务时间','已服务的时间','剩余需要服务时间'])
                    for j in range(len(q_list[i].process_list)):
                        rrr_table.add_row([q_list[i].process_list[j].name,q_list[i].process_list[j].serve_time,q_list[i].process_list[j].serve_time-q_list[i].process_list[j].left_serve_time,q_list[i].process_list[j].left_serve_time])
                    print(rrr_table)
                    print('***********************************************************')
                    rr_last_queue=RR(q_list[i].process_list,q_list[i].q)
                    rr_last_queue.scheduling()
                else:
                    print('全部进程已完成')
            else:
                currentQueue=q_list[i]

                index=int(0)
                while(True):
                    print('第  %d  队列，时间片为: %d'%(i+1,q_list[i].q))
                    muti_table = PrettyTable(['进程名','需要服务时间','已服务的时间','剩余需要服务时间'])
                    if currentQueue.get(index).left_serve_time>q_list[i].q:
                        currentQueue.get(index).left_serve_time-=q_list[i].q
                        #将当前进程扔到下一个队列的尾部
                        q_list[i+1].add(currentQueue.get(index))
                        for j in range(index,len(q_list[i].process_list)):
                            muti_table.add_row([currentQueue.process_list[j].name,currentQueue.process_list[j].serve_time,currentQueue.process_list[j].serve_time-currentQueue.process_list[j].left_serve_time,currentQueue.process_list[j].left_serve_time])
                        print(muti_table)                      
                        print('%s 进程没有执行完毕,需要添加至下一队列末尾'%(currentQueue.get(index).name))
                        print('----------------------------------------------------------')
                        index+=1  
                    else:
                        currentQueue.get(index).left_serve_time=0
                        for j in range(index,len(q_list[i].process_list)):
                            muti_table.add_row([currentQueue.process_list[j].name,currentQueue.process_list[j].serve_time,currentQueue.process_list[j].serve_time-currentQueue.process_list[j].left_serve_time,currentQueue.process_list[j].left_serve_time])
                        print(muti_table)
                        print('%s 完成并弹出'%(currentQueue.get(index).name))
                        print('----------------------------------------------------------')
                        currentQueue.get(index).left_serve_time=0
                        currentQueue.delete(index)

                    if index==currentQueue.size():
                        break

if __name__=='__main__':
    '''产生进程'''
    process_list=[]
    processA=Process('A',0,4)
    processB=Process('B',1,3)
    processC=Process('C',2,4)
    processD=Process('D',3,2)
    processE=Process('E',4,4)

    process_list0,process_list1,process_list2=[],[],[]
    process_list0.append(processA),process_list0.append(processB)
    process_list0.append(processC),process_list0.append(processD)
    process_list0.append(processE)

    #队列
    queue_list=[]
    queue0=Queue(0,process_list0)
    queue1=Queue(1,process_list1)
    queue2=Queue(2,process_list2)
    queue_list.append(queue0),queue_list.append(queue1),queue_list.append(queue2)
    print('初始状态其他队列为空第一队列内的进程如下:')
    init_table = PrettyTable(['进程名','需要服务时间','已服务的时间','剩余需要服务时间'])
    for i in range(len(process_list0)):
       init_table.add_row([process_list0[i].name,process_list0[i].serve_time,process_list0[i].serve_time-process_list0[i].left_serve_time,process_list0[i].left_serve_time])
    print(init_table)
    print('***********************************************************')
    #使用多级反馈队列调度算法,第一队列时间片为1
    mfq=MulitlevedFeedbackQueue(queue_list,1)
    mfq.scheduling()