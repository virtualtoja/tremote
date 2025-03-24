import socket

class Server:
    port: int
    ip_str: str

w_servers = []
w_clients = []

while True:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", #ENTER YOUR MAIN SERVER PORT HERE!))
    server.listen(5)

    print("[+] Waiting for connections...");
    conn, addr = server.accept()

    conf = conn.recv(16)
    print(f"\n[+] New {conf[:6].decode('ascii')} connected. ({addr[0]})")

    if str(conf[:6]).startswith("b'server'"):
        ls = Server()
        ls.ip_str = addr[0]
        ls.port = int.from_bytes(conf[6:10], 'little')
    
        w_servers.append(ls)
        print(f"[+] Server {addr[0]}:{ls.port} added to waiting list.\n")
    elif str(conf[:6]).startswith("b'client'"):
        lc = addr[0]
        if len(w_servers) == 0:
            print(f"[-] No servers connected. Closing connection.\n")
            conn.send(bytes(10))
            conn.close()
        else:
            serv = w_servers[len(w_servers)-1]

            data = socket.inet_aton(serv.ip_str)[::-1] + int.to_bytes(serv.port, 2, 'little') + int.to_bytes(0xFFFF, 2, 'little');
            conn.send(data)
            conn.close()

            w_servers.remove(serv)
            print(f"[+] Client {lc} redirected to server {serv.ip_str}:{serv.port}.\n")

