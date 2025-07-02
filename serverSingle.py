from socket import *
import sys  # Untuk keluar dari program

# Membuat socket server
serverSocket = socket(AF_INET, SOCK_STREAM)

# Menentukan port dan mengikat socket
serverPort = 2525
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("Server siap untuk menerima koneksi...")

while True:
    # Menerima koneksi dari client
    connectionSocket, addr = serverSocket.accept()

    try:
        # Menerima request HTTP dari client
        message = connectionSocket.recv(1024).decode()

        # Mendapatkan nama file dari request
        filename = message.split()[1]
        f = open(filename[1:], 'rb') 
        outputdata = f.read()
        f.close()

        # Mengirim header HTTP 200 OK
        header = "HTTP/1.1 200 OK\r\n\r\n"
        connectionSocket.send(header.encode())

        # Mengirim isi file ke client
        connectionSocket.send(outputdata)
        connectionSocket.send(b"\r\n")

    except IOError:
        # File tidak ditemukan, kirim pesan 404
        header = "HTTP/1.1 404 Not Found\r\n\r\n"
        body = "<html><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(header.encode())
        connectionSocket.send(body.encode())

    # Menutup koneksi
    connectionSocket.close()

serverSocket.close()
sys.exit()
