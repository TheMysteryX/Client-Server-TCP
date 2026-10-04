##  Descriere

Acest proiect implementează un joc de **Piatră–Hârtie–Foarfecă** între un client și un server, utilizând protocolul **TCP** și modulul `socket` din Python.

Aplicația este alcătuită din două componente:

- **Serverul** – așteaptă conexiunea clientului, generează aleatoriu propria alegere și determină câștigătorul fiecărei runde.
- **Clientul** – se conectează la server, permite utilizatorului să introducă alegerile și afișează rezultatele.

Jocul este format din **3 runde**, iar la final este afișat câștigătorul pe baza scorului acumulat.

---

## Tehnologii utilizate

- **Python 3**
- **Socket Programming**
- **TCP/IP**
- Modulul standard `socket`
- Modulul standard `random`

Nu sunt necesare biblioteci externe.

---

## Structura proiectului

```text
.
├── client.py
├── server.py
└── README.md
```

### `server.py`

Fișierul `server.py` implementează partea de server a aplicației.

Serverul:

1. Creează un socket TCP.
2. Se leagă la adresa `127.0.0.1` și portul `8888`.
3. Așteaptă conectarea unui client.
4. Solicită clientului introducerea mesajului `START`.
5. Generează aleatoriu alegerea serverului.
6. Primește alegerea clientului.
7. Determină câștigătorul fiecărei runde.
8. Actualizează scorul.
9. După cele 3 runde, determină câștigătorul jocului.
10. Închide conexiunea.

Socket-ul serverului este configurat și pus în starea de așteptare prin:

```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 8888))
server_socket.listen(1)
```



### `client.py`

Fișierul `client.py` implementează partea de client.

Clientul:

1. Creează un socket TCP.
2. Se conectează la server.
3. Așteaptă instrucțiunea pentru începerea jocului.
4. Trimite `START`.
5. Introduce alegerea pentru fiecare rundă.
6. Primește alegerea serverului.
7. Primește rezultatul rundei.
8. La final primește rezultatul jocului.
9. Închide conexiunea.

Conectarea la server se realizează prin:

```python
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 8888))
```



---

## Regulile jocului

Jucătorul poate alege una dintre următoarele variante:

| Simbol | Alegere |
|---|---|
| `P` | Piatră |
| `H` | Hârtie |
| `F` | Foarfecă |

Regulile sunt:

```text
Piatra  > Foarfeca
Foarfeca > Hartia
Hartia  > Piatra
```

Dacă ambii jucători aleg aceeași variantă, runda se termină la egalitate.

---

## Desfășurarea jocului

### 1. Pornirea serverului

Mai întâi trebuie pornit serverul:

```bash
python server.py
```

Serverul va afișa:

```text
Serverul asteapta conexiunea...
```

Serverul așteaptă apoi conectarea clientului prin `accept()`.

---

### 2. Pornirea clientului

Într-un al doilea terminal se rulează:

```bash
python client.py
```

Clientul se conectează la:

```text
127.0.0.1:8888
```

Serverul trimite mesajul:

```text
Introduceti 'START' pentru a incepe jocul...
```

Acest mecanism este implementat în server prin recepționarea mesajului clientului și verificarea valorii `START`.

---

### 3. Pornirea jocului

Clientul trebuie să introducă:

```text
START
```

Dacă este introdus alt mesaj, serverul solicită din nou introducerea comenzii corecte.

După introducerea corectă, serverul transmite:

```text
Jocul incepe!
```

Clientul primește apoi confirmarea că serverul este pregătit.

---

## Desfășurarea unei runde

Jocul conține 3 runde.

La fiecare rundă, clientul trebuie să introducă:

```text
P
```

pentru Piatră,

```text
H
```

pentru Hârtie,

sau:

```text
F
```

pentru Foarfecă.

Clientul verifică dacă alegerea este una dintre cele trei variante acceptate înainte de a o trimite serverului.

Serverul primește alegerea clientului și generează propria alegere folosind modulul `random`:

```python
def getAlegereServer():
    return random.choice(['P', 'H', 'F'])
```



Alegerea serverului este apoi transmisă clientului:

```python
conn.send(alegere_server.encode())
```



---

## Determinarea câștigătorului

După ce serverul primește ambele alegeri, acestea sunt comparate.

Exemplu:

```text
Client: P
Server: F
```

Rezultatul este:

```text
Piatra bate foarfeca! Ai castigat aceasta runda!
```

Dacă serverul câștigă:

```text
Client: P
Server: H
```

rezultatul este:

```text
Hartia bate piatra! Server-ul a castigat aceasta runda!
```

În cazul în care alegerile sunt identice:

```text
Client: P
Server: P
```

rezultatul este:

```text
Este egalitate!
```

Serverul actualizează separat scorul clientului și scorul propriu pe parcursul celor trei runde.

---

## Stabilirea rezultatului final

După terminarea celor 3 runde, scorurile sunt comparate.

Dacă:

```text
scor_client > scor_server
```

clientul câștigă jocul.

Dacă:

```text
scor_client < scor_server
```

serverul câștigă.

În caz contrar, jocul se termină la egalitate.

Această logică este implementată la finalul serverului.

Clientul primește rezultatul final și îl afișează.

---

## Comunicarea Client–Server

Aplicația utilizează modelul:

```text
             TCP
┌───────────────┐
│    CLIENT     │
│               │
│  Introducere  │
│   P / H / F   │
└───────┬───────┘
        │
        │ TCP
        │ 127.0.0.1:8888
        ▼
┌───────────────┐
│    SERVER     │
│               │
│ random P/H/F  │
│               │
│ Compară alegeri│
│ Calculează scor│
└───────┬───────┘
        │
        │ Rezultat
        ▼
┌───────────────┐
│    CLIENT     │
│               │
│ Afișează      │
│ rezultatul    │
└───────────────┘
```

Serverul utilizează:

```text
127.0.0.1:8888
```

unde `127.0.0.1` reprezintă calculatorul local, iar `8888` este portul utilizat pentru comunicație.

---

## Instalare și rulare

### Cerințe

Este necesar:

- Python 3 instalat;
- două terminale;
- fișierele `server.py` și `client.py`.

Nu este necesară instalarea unor pachete suplimentare.

### Pasul 1 – clonarea repository-ului

```bash
git clone https://github.com/TheMysteryX/Client-Server-TCP/
cd Client-Server-TCP
```

### Pasul 2 – pornirea serverului

În primul terminal:

```bash
python server.py
```

### Pasul 3 – pornirea clientului

Într-un al doilea terminal:

```bash
python client.py
```

### Pasul 4 – începerea jocului

Introdu:

```text
START
```

Apoi, pentru fiecare dintre cele 3 runde, introdu:

```text
P
```

```text
H
```

sau:

```text
F
```

---

## 💻 Exemplu de execuție

### Terminalul serverului

```text
Serverul asteapta conexiunea...
Conexiunea stabilita cu ('127.0.0.1', 54321)
```

### Terminalul clientului

```text
Introduceti 'START' pentru a incepe jocul...
Scrieti mesajul pentru server: START
Jocul incepe!

Server-ul este pregatit!

Introduceti alegerea dumneavoastra (P pentru piatra, H pentru hartie, F pentru foarfeca): P
Server-ul a ales: F
Piatra bate foarfeca! Ai castigat aceasta runda!

Introduceti alegerea dumneavoastra (P pentru piatra, H pentru hartie, F pentru foarfeca): H
Server-ul a ales: H
Este egalitate!

Introduceti alegerea dumneavoastra (P pentru piatra, H pentru hartie, F pentru foarfeca): F
Server-ul a ales: P
Piatra bate foarfeca! Server-ul a castigat aceasta runda!

Ai castigat din 1 incercari!
```

---

##  Validarea datelor

Aplicația verifică datele introduse de utilizator.

Pentru comanda de pornire, serverul acceptă doar:

```text
START
```

Comanda este verificată fără a ține cont de diferențele dintre litere mari și mici prin utilizarea:

```python
mesaj_client.strip().upper()
```

Pentru alegerile din timpul jocului sunt acceptate doar:

```text
P
H
F
```

Dacă utilizatorul introduce o altă valoare, serverul solicită o nouă alegere.

---

##  Funcțiile principale

### `getAlegereServer()`

Generează aleatoriu alegerea serverului:

```python
def getAlegereServer():
    return random.choice(['P', 'H', 'F'])
```



### `getAlegereClient()`

Primește alegerea clientului și verifică dacă aceasta este validă:

```python
def getAlegereClient():
    alegere = conn.recv(1024).decode()

    while alegere not in ['P', 'H', 'F']:
        conn.send(
            "Nu exista o astfel de varianta. Verificati si introduceti din nou."
            .encode()
        )
        alegere = conn.recv(1024).decode()

    return alegere
```



---

##  Protocolul de comunicare

Schimbul principal de mesaje dintre cele două componente este:

```text
CLIENT                         SERVER
  │                              │
  │─────── conectare ───────────>│
  │                              │
  │<────── solicitare START ─────│
  │                              │
  │────────── START ────────────>│
  │                              │
  │<────── Jocul incepe ─────────│
  │                              │
  │<──── Server pregatit ────────│
  │                              │
  │──────── P/H/F ──────────────>│
  │                              │
  │<──────── P/H/F ──────────────│
  │                              │
  │<────── rezultat rundă ───────│
  │                              │
  │          ...                 │
  │                              │
  │<────── rezultat final ───────│
  │                              │
  │──────── închidere ──────────>│
```

Comunicarea se realizează prin `send()` și `recv()`, iar mesajele sunt convertite între string și bytes folosind `encode()` și `decode()`.

---
