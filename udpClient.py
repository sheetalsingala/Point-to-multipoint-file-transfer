import socket
import time
import sys
import threading
import select


flag = '0101010101010101'   # Data packet indication
sequenceNumber = 0          # Sequence number of data packet
udpIP = "127.0.0.1"
udpPort = [5005,5006]
timeout = 6
unsentList = []
threads = []
def to_bits(n):
    return bin(n)[2:]

def from_bits(n):
    return int(n, 2)

def checkSum(data):
    B = ''.join(format(ord(x), '016b') for x in data)
    sumBin = to_bits(0)
    res = to_bits(0)
    for i in range (0,len(B), 16):    
        Y = B[i:i+16]
        sumBin =  bin(int(Y,2)+int(sumBin,2))
        res = sumBin[2:]  # removing 'b'
    result = pad_bits(res,16)
    if len(result) > 16 :  #overflow condition  -- wrapraround
        result = bin(int(result[1:],2)+int(result[0],2))   
    comp = bin(~(int(result,2)) & 0xFFFF )     # Compliment
    checksum = comp[2:]   # removing 'b'
    return(checksum)

def headerEncapsulation(data):
    dataNew = pad_bits(flag,16) + pad_bits(to_bits(sequenceNumber),32) + pad_bits(check,16) + data
    return(dataNew)


def pad_bits(b, length):
    return b.rjust(length,'0')
    
def client_thread(IP,portNumber,seqNum):
    clientSock.sendto(str.encode(dataNew), (IP, portNumber))
    ready = select.select([clientSock], [], [], timeout)
    if ready[0]:
            data, addr = clientSock.recvfrom(buf)
            # print(data)  #Check if ACK is off right
    else:
            flag = 1
            # unsentList = [IP,portNumber,seqNum]
            # rdt_send(IP,portNumber,seqNum)
            


buf = 5
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


print ("Sending %s ..." )
f = open('bonus1.py', "r")
data = f.read(buf)
check = checkSum(data)
dataNew = headerEncapsulation(data)
# rdt_send()


while(data):
    for i in range(len(udpPort)):
        new_Thread = threading.Thread(target=client_thread, args=(udpIP, udpPort[i], sequenceNumber))
        new_Thread.start()
        threads.append(new_Thread)
    for thread in threads:   #Wait for thread to complete
        thread.join()
    sequenceNumber = sequenceNumber + 1
    data = f.read(buf)
    check = checkSum(data)
    dataNew = headerEncapsulation(data)




clientSock.close()
f.close()








