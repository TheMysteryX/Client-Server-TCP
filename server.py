import socket
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 8888))  
server_socket.listen(1)

print("Serverul asteapta conexiunea...")
conn, addr = server_socket.accept()
print(f"Conexiunea stabilita cu {addr}")

conn.send("Introduceti 'START' pentru a incepe jocul... ".encode())

while True:
    mesaj_client = conn.recv(1024).decode() # primeste mesajul introdus de utilizator de la client
    if mesaj_client.strip().upper() == "START":
        conn.send("Jocul incepe!\n".encode())
        break
    else:
        conn.send("Mesaj incorect. Introduceti 'START' pentru a incepe: ".encode())

def getAlegereServer():
    return random.choice(['P', 'H', 'F'])

def getAlegereClient():
    alegere = conn.recv(1024).decode()  #primeste input-ul de la client
    while alegere not in ['P', 'H', 'F']:
        conn.send("Nu exista o astfel de varianta. Verificati si introduceti din nou.".encode())
        alegere = conn.recv(1024).decode()
    return alegere

conn.send("Server-ul este pregatit!".encode())

scor_client = 0
scor_server = 0

#inceperea jocului
for i in range(3):  #un joc este reprezentat de 3 runde
    alegere_client = getAlegereClient() #asteapta alegerea clientului
    alegere_server = getAlegereServer() #generare alegere server
    conn.send(alegere_server.encode()) #trimite alegerea serverului clientului

    #evaluarea castigatorului unei runde
    if alegere_client == alegere_server:
        conn.send("Este egalitate!".encode())
    elif alegere_client == "P" and alegere_server == "F":
        scor_client += 1
        conn.send("Piatra bate foarfeca! Ai castigat aceasta runda!".encode())
    elif alegere_client == "P" and alegere_server == "H":
        scor_server += 1
        conn.send("Hartia bate piatra! Server-ul a castigat aceasta runda!".encode())
    elif alegere_client == "H" and alegere_server == "P":
        scor_client += 1
        conn.send("Hartia bate piatra! Ai castigat aceasta runda!".encode())
    elif alegere_client == "H" and alegere_server == "F":
        scor_server += 1
        conn.send("Foarfeca bate hartia! Server-ul a castigat aceasta runda!".encode())
    elif alegere_client == "F" and alegere_server == "P":
        scor_server += 1
        conn.send("Piatra bate foarfeca! Server-ul a castigat aceasta runda!".encode())
    elif alegere_client == "F" and alegere_server == "H":
        scor_client += 1
        conn.send("Foarfeca bate hartia! Ai castigat aceasta runda!".encode())

#evaluarea castigatorului jocului
if scor_client > scor_server:
    conn.send(f"Ai castigat din {scor_client} incercari!".encode())
elif scor_client < scor_server:
    conn.send("Serverul a castigat!".encode())
else:
    conn.send("Scorul se afla la egalitate!".encode())

conn.close()
