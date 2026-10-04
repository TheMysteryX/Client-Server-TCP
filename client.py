import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client_socket.connect(("127.0.0.1", 8888))  

raspuns = client_socket.recv(1024).decode()  # primeste solicitarea pentru START
print(raspuns)

while True:
    mesaj = input("Scrieti mesajul pentru server: ")  # citeste mesajul de la utilizator pana cand se introduce 'START'
    client_socket.send(mesaj.encode()) 
    raspuns = client_socket.recv(1024).decode()  #confirmarea server-ului daca incepe jocul sau s-a introdus gresit 'START"
    print(raspuns)
    if mesaj.strip().upper() == "START":
        break

raspuns2 = client_socket.recv(1024).decode()  #confirmare server pregatit
print(raspuns2)

for i in range(3):  #3 runde de joc
    while True:  
        alegere = input("Introduceti alegerea dumneavoastra (P pentru piatra, H pentru hartie, F pentru foarfeca): ")
        if alegere in ['P', 'H', 'F']:
            client_socket.send(alegere.encode())  #alegerea clientului trimisa catre server
            break
        else:
            print("Nu exista o astfel de varianta. Verificati si introduceti din nou.")

    alegere_server = client_socket.recv(1024).decode()  #alegerea server-ului primita de catre client
    print(f"Server-ul a ales: {alegere_server}")

    rez_runda = client_socket.recv(1024).decode()  #confirmarea castigatorului unei runde
    print(rez_runda)

rez_final = client_socket.recv(1024).decode()  #confirmarea castigatorului jocului
print(rez_final)

client_socket.close()
