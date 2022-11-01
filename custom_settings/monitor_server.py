
import subprocess
import socket
import locale
from socketserver import BaseRequestHandler, TCPServer

def process_detect(process_name):

    out_bytes = subprocess.check_output(['tasklist'])
    if process_name not in out_bytes.decode(locale.getdefaultlocale()[1]):
        #print("Process not exist")
        return 0
    else:
        #print("Find process")
        return 1

class DetectHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            try:
                monitor_process = self.request.recv(1024).decode('utf-8')
                if process_detect(monitor_process):
                    self.request.send(bytes('\x01',encoding='utf-8'))
                else:
                    print("Procsss %s has exit" % monitor_process)
                    self.request.send(bytes('\x00',encoding='utf-8'))
            except:
                print('Connection from %s disconnected'% repr(self.client_address))
                self.request.close()
                break

if __name__ == '__main__':
    serv = TCPServer(('', 20000), DetectHandler)
    serv.serve_forever()

    # process_detect("Server.exe")
