#!/usr/bin/env python
#------------------------------------------------------------------
from logging import exception
from scapy.all import *
import socket
import time

import pdb
import sys

# 三种情况均会通知主Fuzzing线程
# 1.远端monitor server无法连接
# 2.与远端monitor 通讯异常
# 3.远端monitor报告监控进程退出
# 只有第三种情况导致的Crash记录是真正的Crash
def check_process_alive(client_s, monitor_process):
    #print("Monitor check alive")
    try:
        
        client_s.send(bytes(monitor_process,encoding='utf-8'))
        res = client_s.recv(1024)
        #pdb.set_trace()
        if res == b'\x00':
            return 0;
        elif res == b'\x01':
            return 1
    except Exception as e:
        
        print("@@@"*10)
        print(repr(e))
        print("Remote monitor seems not works!")
        print("@@@"*10)
        print("Should stop fuzzing?")
        return -1

class Monitor(object):
    # This function will run asynchronously in a different thread to monitor the host
    def monitorTarget(self, targetIP, targetPort, signalMain):
        # Can do something like:
        # while True:
        #   read file, etc
        #   if errorConditionHasOccurred:
        #       signalMain()
        #
        # Calling signalMain() at any time will indicate to Mutiny
        # that the target has crashed and a crash should be logged
        try:
            client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_s.connect(("172.16.16.10",20000)) # 远程监控Server地址，按需修改
        except Exception as e:
            print("[!]\nRemote monitor can not connected! Stop Fuzzing\n@@@")
            signalMain()
            exit()            
        while True:
            check_alive = check_process_alive(client_s, "Server.exe")
            # 注意，这里的sleep时间选择要根据Fuzzing每一个Run的间隔确定，过大会导致
						# 触发中断的时机不对。
            time.sleep(0.2)
            if check_alive == 1:
                continue
            elif check_alive == 0:
                print("Carsh occured")
                signalMain()
                exit()
            elif check_alive == -1:
                
                signalMain()
                exit()
            
        pass
#check_process_alive()
