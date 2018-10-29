# -*- coding = utf-8 -*-


#队列类
class Queue:
    
    def __init__(self, level, process_queue):
        self.level = level                  #优先级
        self.process_queue = process_queue    #进程队列
        self.q = 0                          #时间片

    def size(self):
        return len(self.process_queue)

    def empty(self):
        return self.size() == 0

    def add(self, process):
        self.process_queue.append(process)

    def get(self, index):
        return self.process_queue[index]
    
    def remove(self, index):
        self.process_queue.remove(self.process_queue[index])

#进程类
class Process:
     
     def __init__(self, name, arrive_time, serve_time):
         self.name = name                   #进程名
         self.arrive_time = arrive_time     #进程到达时间
         self.serve_time = serve_time       #进程服务时间
         self.left_serve_time=serve_time    #剩余需要服务的时间
         self.finish_time = 0               #进程完成时间
         self.turnaround_time = 0           #周转时间
         self.w_turnaround_time = 0         #带权周转时间


class RR:
    """
    轮转调度算法
    """
    #初始化进程队列和时间片
    def __init__(self, process_queue, q):
        self.process_queue = process_queue
        self.q = q
    
    #轮转算法
    def scheduling(self):
        #按进程到达的时间排序
        self.process_queue.sort(key=lambda x: x.arrive_time)
        len_queue = self.process_queue.size()
        index = 0
        running_time = 0

        while True:
            #选取当前服务进程
            current_process = self.process_queue[index % len_queue]
            #判断是否完成当前进程
            if current_process.left_serve_time > 0:
                #判断剩余服务时间和时间片的关系
                if current_process.left_serve_time > self.q:
                    current_process.left_serve_time -= self.q
                    running_time += self.q
                #时间片大于剩余服务时间
                else:
                    running_time += current_process.left_serve_time
                    current_process.left_serve_time = 0

            #进程完成的操作
            if  current_process.left_serve_time == 0 :
                current_process.finish_time = running_time
                current_process.turnaround_time = current_process.finish_time - current_process.arrive_time
                current_process.w_turnaround_time = current_process.turnaround_time / current_process.serve_time
                self.process_queue.remove(index)
                len_queue = self.process_queue.size()
                index -= 1

            index += 1
            len_queue = self.process_queue.size()
            
            if len_queue == 0:
                break

            if index > len_queue:
                index = index % len_queue