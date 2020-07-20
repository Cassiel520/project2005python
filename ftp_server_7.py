from threading import  Thread
from socket import *
import os
from  time  import sleep
HOST="0.0.0.0"
POST=12345
ADDR=(HOST,POST)
FTP = "/home/tarena/ftp/"
class MyThread(Thread):
    def __init__(self,connfd):
        super().__init__()
        self.connfd=connfd
    def do_select(self,list01):
        if list01:
            self.connfd.send(b'ok')
            sleep(0.1)
            str_files = '\n'.join(list01)
            self.connfd.send(str_files.encode())
        else:
            self.connfd.send(b"fail")
            return
    def do_upload(self,list01,tmp):
        if tmp[1:] not in list01:
            self.connfd.send(b'ok')
            f1 = open(FTP + tmp[1:], 'wb')    #tmp是字符串，tmp[-1]是最后一个字符
            while True:
                data = self.connfd.recv(1024)
                if data == b'##':
                    break
                f1.write(data)
                f1.flush()
            f1.close()
        else:
            self.connfd.send(b'fail')
    def do_download(self,list01,tmp):
        if tmp[1:] in list01:
            self.connfd.send(b'ok')
            sleep(0.1)
            f = open(FTP + "/" + tmp[1:], 'rb')
            while True:
                data = f.read(128)
                if not data:
                    sleep(0.1)
                    f.close()
                    self.connfd.send(b'##')
                    break
                self.connfd.send(data)
        else:
            self.connfd.send(b'fail')
        self.connfd.close()
    def run(self):
        list01 = os.listdir(FTP)
        while True:
            data=self.connfd.recv(1024)
            tmp = data.decode()
            if not data or tmp[0]=='e':
#客户端退出的时候，tcp服务端会收到空，尽管不会再发消息给客户端而发生pipebroken error
# 如果不处理，再取索引会报错
                self.connfd.close()
                break
            elif tmp[0]=='s':
                self.do_select(list01)
            elif tmp[0]=='u':
                self.do_upload(list01,tmp)
            elif tmp[0] == 'd':
                self.do_upload(list01,tmp)

def main():
    sock=socket()
    sock.bind(ADDR)
    sock.listen(5)
    while True:
        try:
           connfd,addr=sock.accept()
        except KeyboardInterrupt:
            sock.close()
            return
        t=MyThread(connfd)
        t.setDaemon(True)  #主线程的退出，子线程也退出
        t.start()
if __name__ == '__main__':
    main()