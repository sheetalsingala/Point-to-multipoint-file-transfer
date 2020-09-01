import socket
import select

udpIP = "127.0.0.1"
udpPort = 5006
timeout = 10   #Check for timeout!


serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((udpIP, udpPort))


def from_bits(n):
    return int(n, 2)

def extraction(data):
    return (data[64:])

f = open('receivedBonus1.py', 'wb')
while True:
  
        ready = select.select([serverSock], [], [], timeout)
        if ready[0]:
            data, addr = serverSock.recvfrom(1024)
        
            data1 = extraction(data)
            print(data1)
            f.write(data1)
            serverSock.sendto(str.encode("ACK"), (udpIP, addr[1]))
        else:
            print ("%s Finish!" )
            f.close()
            break

