# -*- coding:utf-8 -*-

"""Banker algorithm """

__author__ = 'twoday'

from copy import copy
from prettytable import PrettyTable

class BankerAlgorithm():
    """
    bankerAlgorithm class
    """
    def __init__(self, m=3, n=5):
        self.m = m              #number of resources
        self.n = n              #number of processes
        self.available = []     #number of resources available
        self.max = {}           #maximum need matrix
        self.allocation = {}    #allocation matrix 
        self.need = {}          #need matrix
        self.request ={}        #request matrix

        
        #init max
        for i in range(self.n):
            self.max['P{}'.format(i)] = []
        #init allocation
        for i in range(self.n):
            self.allocation['P{}'.format(i)] = []
        #init need
        for i in range(self.n):
            self.need['P{}'.format(i)] = []
        #init request
        for i in range(self.n):
            self.request['P{}'.format(i)] = []
    
    def get_resource_status(self):
        """show resource information"""
        status_table = PrettyTable(['Process ID', 'Max:A B C', 'Alloaction:A B C', 'Need:A B C'])
        for i in range(self.n):
            status_table.add_row(['P{}'.format(i), self.max['P{}'.format(i)], self.allocation['P{}'.format(i)], self.need['P{}'.format(i)]])
        print(status_table)

    def get_safe_sequence_info(self):
        """show safe sequence info"""
        sequence_info_table = PrettyTable(['Process ID', 'work:A B C', 'need:A B C', 'Allocation:A B C', 'work+Allocation:A B C', 'Finish'])
        for i in range(self.n):
            index = self.safe_sequence[i]
            sequence_info_table.add_row(['P{}'.format(index), self._work[i],self.need['P{}'.format(index)],
                                        self.allocation['P{}'.format(index)], self.work_add_allocation[i], 'true'
                                        ])
        print(sequence_info_table)

    def get_avaiable(self):
        self.available = []
        print('[*] init the number of avaiable source')
        for i in range(self.m):
            tmp = input('{} >'.format(chr(65+i)))
            self.available.append(int(tmp))
        
    def get_max(self):
        print('[*] Initial process maximum demand resources')
        for i in range(self.n):
            print('----P{}----'.format(i))
            for j in range(self.m):
                tmp = input('P{}[{}] >'.format(i,chr(65+j)))
                self.max['P{}'.format(i)].append(int(tmp))
    
    def get_allocation(self):
        print('[*] Initial process already have resources')
        for i in range(self.n):
            print('----P{}----'.format(i))
            for j in range(self.m):
                tmp = input('P{}[{}] >'.format(i,chr(65+j)))
                self.allocation['P{}'.format(i)].append(int(tmp))

    def get_need(self):
        for i in range(self.n):
            for j in range(self.m):
                tmp = self.max['P{}'.format(i)][j] - self.allocation['P{}'.format(i)][j]
                if tmp < 0:
                    print('[-] P{}Need Matrix{} Error".format(i, j)')
                self.need['P{}'.format(i)].append(int(tmp))
    
    def command_init(self):
        """Command line input"""
        self.get_avaiable()
        self.get_max()
        self.get_allocation()
        self.get_need()
        self.get_resource_status()
    
    def send_request(self, px, req_vector):
        """request resource

        Args:
            px (str): process of requesting resources
            req_vector (list): source list
        """
        self.check_input_valid(px, req_vector)      #todo
        self.request[px] = req_vector

        for i in range(self.m):
            if self.request[px][i] > self.need[px][i]:
                print('[-] {0} the number of {1} requested has exceeded \
                       the maximum value it needs'.format(px, chr(65+i)))
                return
            if self.request[px][i] > self.available[i]:
                print('[-] Not enough resources, need to wait')
                return

        tmp_available = self.available[:]
        tmp_allocation = self.allocation.copy()
        tmp_need = self.need.copy()

        for i in range(self.m):
            tmp_available[i] = tmp_available[i] - self.request[px][i]
            tmp_allocation[px][i] = tmp_allocation[px][i] + self.request[px][i]
            tmp_need[px][i] = tmp_need[px][i] - self.request[px][i]
        
        if self.check_safe(tmp_available, tmp_allocation, tmp_need) == True:
            print('[+] Check safe, Format changed, The following is the security sequence information.')
            self.allocation = tmp_allocation.copy()
            self.available = tmp_available[:]
            self.need = tmp_need.copy()
            print('[+] Current avaliable: {}'.format(str(self.available)))
            self.get_safe_sequence_info()
        else:
            print("[-] Not safe, Format not changed")


    def check_safe(self, tmp_available, tmp_allocation, tmp_need):
        """Check if it is safe at this moment
        
        Args:
            tmp_available (list): 
            tmp_allocation (dict): 
            tmp_need (dict): 
        """
        finish = [False] * self.n 
        work = tmp_available[:]
        self._work = []                  #Record change in work
        self._work.append(str(work))
        self.safe_sequence = []
        self.work_add_allocation = []     #Record change in work+allocation

        while True:
            process = -1 
            
            #find a process like this finish = false, need < work.
            for i in range(self.n):
                if finish[i] == True:
                    continue
                if finish[i] == False: 
                    for j in range(self.m):
                        #compare need[i,j] <work[j].i-process number, j-resource number.
                        if self.need['P{}'.format(i)][j] > work[j]:
                            process = -1
                            break
                        process = i     #record current index
                    if process != -1:
                        self.safe_sequence.append(i)
                        break
                else:
                    process = -1
            if process != -1:
                for j in range(self.m):
                    work[j] += tmp_allocation['P{}'.format(process)][j]
                    finish[process] = True
                self._work.append(str(work))
                self.work_add_allocation.append(str(work))
                #print('[*] Finding P{} is safe'.format(process))
            else:
                if finish != [True] * self.n:
                    return False
                else:
                    return True
                


    def example_init(self):
        """initialize example in the program"""
        self.available = [3, 3, 2]
        self.max = {
            "P0": [7, 5, 3],
            "P1": [3, 2, 2],
            "P2": [9, 0, 2],
            "P3": [2, 2, 2],
            "P4": [4, 3, 3]
        }
        self.allocation = {
            "P0": [0, 1, 0],
            "P1": [2, 0, 0],
            "P2": [3, 0, 2],
            "P3": [2, 1, 1],
            "P4": [0, 0, 2]
        }
        self.get_need()
        self.get_resource_status()
        print('[+] Current avaliable: {}'.format(str(self.available)))
        if self.check_safe(self.available, self.allocation, self.need) == True:
            print('[+] Current status is safe')
            self.get_safe_sequence_info()
        else:
            print('[-] Current status is not safe')

        #P1 send request resource [1, 0, 2]
        print('[+] P1 send request [1, 0, 2]')
        p1_req_vector = [1, 0, 2]
        self.send_request('P1', p1_req_vector)

        #P0 send request resource [0, 2, 0]
        print('[+] P0 send request [0, 2, 0]')
        p0_req_vector = [0, 2, 0]
        self.send_request('P0', p0_req_vector)

        #P4 send request resource [3, 3, 0]
        print('[+] P4 send request [3, 3, 0]')
        p4_req_vector = [3, 3, 0]
        self.send_request('P4', p4_req_vector)

    def check_input_valid(self, px, req_vector):
        """check input """
        pass
        
        
if __name__ == '__main__':
    banker = BankerAlgorithm()
    banker.example_init()
    #banker.command_init()