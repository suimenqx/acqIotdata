#! /usr/bin/env python3
import sys, time, socket
import threading, signal
import inspect
import ctypes

cycle_time=5


def _async_raise(tid, exctype):  
    """raises the exception, performs cleanup if needed"""  
    tid = ctypes.c_long(tid)  
    if not inspect.isclass(exctype):  
        exctype = type(exctype)  
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))  
    if res == 0:  
        raise ValueError("invalid thread id")  
    elif res != 1:  
        # """if it returns a number greater than one, you're in trouble,  
        # and you should call it again with exc=NULL to revert the effect"""  
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)  
        raise SystemError("PyThreadState_SetAsyncExc failed")  
  
def kill_thread(thread):  
    _async_raise(thread.ident, SystemExit)


def read_cpu_temp():
    file = open('/sys/class/thermal/thermal_zone0/temp')
    cpu_temp = float(file.read()) / 1000
    file.close()
    return cpu_temp

def tcp_upload():
    #global cycle_time
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.43.64',26711))
    print("Thread tcp_upload %s is runging..." % threading.current_thread().name)
    while True:
        if cycle_time != 88888 :
            cpu_temp=read_cpu_temp()
            print("cpu_temp:%s" % cpu_temp)
            cpu_temp="cpu_temp:{}".format(cpu_temp)
            s.send(cpu_temp.encode(encoding="utf-8"))
            time.sleep(cycle_time)
            print("current cycle_time %s" % cycle_time)
        else :
            # kill_thread(threading.current_thread())
            # pass
            time.sleep(1)
    s.close()

def receve_cmd():
    #global cycle_timea
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.43.64',26711))
    print("Thread receve_cmd  %s is runging..." % threading.current_thread().name)
    while True:
        global cycle_time
        recv_data = s.recv(1024).decode('utf-8')
        print(recv_data)
        if recv_data[0:12] == 'change rate ' and recv_data[12:].isdigit():  
            cycle_time = int(recv_data[12:])
            print("cycle_time is changed to be %s" % cycle_time)
            send_data="Successfully {} !!".format(recv_data)
            s.send(send_data.encode(encoding="utf-8"))
        elif recv_data == "stop":
            cycle_time = 88888
            print("cycle_time is changed to be %s" % cycle_time)
            send_data="Successfully {} !!".format(recv_data)
            s.send(send_data.encode(encoding="utf-8"))
        elif recv_data == "start":
            cycle_time = 5
            print("cycle_time is changed to be %s" % cycle_time)
            send_data="Successfully {} !!".format(recv_data)
            s.send(send_data.encode(encoding="utf-8"))
        else:
            s.send(b'please input true cmd !!')
 

if __name__ == '__main__':
    # cpu_temp=read_cpu_temp()
    # print("cpu_temp:%s"%cpu_temp)
    # cpu_temp="cpu_temp:{}".format(cpu_temp)
    print("Thread %s is runging..." % threading.current_thread().name)
    # s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s1.connect(('192.168.43.64',26711))
    # s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s2.connect(('192.168.43.64',26711))
    print("Start upload cpu_temp")
    upload_thread = threading.Thread(target = tcp_upload, name = 'tcp_upload')
    receve_thread = threading.Thread(target = receve_cmd, name = 'receve_cmd')
    receve_thread.start()
    upload_thread.start()
    receve_thread.join()
    upload_thread.join()
    print("thread % ended." % threading.current_thread().name)
