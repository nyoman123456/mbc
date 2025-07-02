from socket import *
import sys
import threading  

# Fungsi untuk menangani request klien
def handle_client(connectionSocket):
    try:
        # Menerima permintaan dari klien
        message = connectionSocket.recv(1024).decode()

        # Mengambil nama file dari request
        filename = message.split()[1]
        f = open(filename[1:], 'rb')  
        outputdata = f.read()
        f.close()

        # Kirim header HTTP 200 OK
        header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(header.encode())

        # Kirim isi file ke klien
        connectionSocket.send(outputdata)
        connectionSocket.send(b"\r\n")

    except IOError:
        # Kirim response 404 jika file tidak ditemukan
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head><title>404</title></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

    # Tutup koneksi setelah selesai
    connectionSocket.close()

# Konfigurasi socket server utama
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 2525
serverSocket.bind(('', serverPort))
serverSocket.listen(5)  # Maksimum 5 koneksi antrean

print("Multithreaded server siap menerima koneksi...")

# Loop utama menerima koneksi dan buat thread baru
while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Koneksi diterima dari {addr}")

    # Buat dan mulai thread untuk menangani request klien
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
    client_thread.start()

serverSocket.close()
sys.exit()
