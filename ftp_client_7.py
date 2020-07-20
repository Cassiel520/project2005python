'''
agjkznjikaj
'''
from socket import *
from time import sleep
import sys
class Handle:
    def __init__(self,sock):
        self.sock=sock
    def select(self):
        self.sock.send('s'.encode())
        data=self.sock.recv(1024)
        if data.decode()=='ok':
           data=self.sock.recv(1024*1024)
           print(data.decode())
        else:
            print("文件夹为空")
    def upload(self,file_name):
        f=open(file_name,'rb')
        #上传file_name可能是绝对路径
        file_name=file_name.split("/")[-1]
        msg='u'+file_name
        self.sock.send(msg.encode())
        item=self.sock.recv(1024)
        if item.decode()=='ok':
            #发送文件
            while True:
                data=f.read(1024)
                if not data:
                    sleep(0.3)
                    self.sock.send(b'##')
                    break
                self.sock.send(data)
            print("上传成功")
            f.close()
        else:
            print("文件名已存在")
    def download(self,file_name):
        msg="d"+file_name
        self.sock.send(msg.encode())
        f=open(file_name,"wb")
        data=self.sock.recv(1024)
        if data.decode()=='ok':
            while True:
                data=self.sock.recv(128)
                if data.decode()=="##":
#文件已经下载，但依然没有打印下载成功，循环没有结束，主要检查此处的判断两边是否相等(字节？＝字符)
                    print("下载成功")
                    break
                f.write(data)
            f.close()
            return
        else:
            print("文件不存在")

def main():
    sock = socket()
    sock.connect(("127.0.0.1", 12345))
    handle=Handle(sock)
    while True:
        print('''
            s.查看select
            d:下载download
            u:上传upload
            e:退出
            ''')
        choice = input("请选择(s｜d|u|e):")
        if choice=='s':
            handle.select()
        elif choice=='d':
            file_name=input("请输入下载的文件名：")
            handle.download(file_name)
        elif choice=='u':
            try:
                file_name = input("请输入上传的文件名：")
                handle.upload(file_name)
            except FileNotFoundError:
                print("文件不存在")
        elif choice=='e':
            sock.send(b'e')
            sys.exit("退出")
        else:
            print("输入有误，请在s|u|d|e中选择")
if __name__ == '__main__':
    main()


