import socket
import sys

def main():
    if len(sys.argv) != 4:
        print("Cara pakai: python client.py HOST PORT filename")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    request = f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = s.recv(4096).decode()

    print("Response dari server:\n")
    print(response)

if __name__ == "__main__":
    main()
