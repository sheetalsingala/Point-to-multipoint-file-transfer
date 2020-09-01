import socket
import select
import sys
import random

udpIP = "127.0.0.1"
udpPort = 5005
timeout = 3   #Check for timeout!

def checkSum(arg):
    B = ''.join(format(ord(x), '016b') for x in arg)
    print('B',len(B))
    sumBin = createBits(0)
    res = createBits(0)
    for i in range (0,len(B), 16):    
        Y = B[i:i+16]
        sumBin =  bin(int(Y,2)+int(sumBin,2))
        res = sumBin[2:]  # removing 'b'
    result = bitsPadder(res,16)
    print('result',result)
    if len(result) > 16 :  #overflow condition  -- wrapraround
        result = bin(int(result[1:],2)+int(result[0],2))
    comp = bin(~(int(result,2)) & 0xFFFF )     # Compliment
    checksum = comp[2:]
    print('checksum',checksum)  
    return result 

# def extractClientPkt(arg1):
#     previous_val = arg1[:16]
#     i=16
#     while(i < len(arg1)-2):
#         current_val = arg1[i:i+16]
#         current_sum = add_bits(previous_val, current_val)
#         previous_val = current_sum
#         i+=16
#     return previous_val

# def createPKT():
    
def createACK(arg1, port):
    ACKmsg = '1010101010101010'+'0000000000000000'+arg1
    print('ACK',ACKmsg)
    sendACK(ACKmsg, port)

def sendACK(arg1, port):
    serverSock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # serverSock1.bind((udpIP, udpPort))
    serverSock1.sendto(str.encode(arg1), (udpIP, port))
    # serverSock1.close()

# def SocketFunc():
def createBits(n):
    return bin(n)[2:]

def createInt(n):
    print("n:",n)
    return int(n, 2)

def bitsPadder(b, length=16):
    return "0"*(length-len(b)) + b

def checksumtest(arg3, arg4):
    sum = add_bits(arg3,arg4)
    # print(sum)
    if(sum == '1111111111111111'):
        return 1

def add_bits(num3, num4):
    result = createBits(createInt(num3) + createInt(num4))
    if len(result) <= 16: # no carry
        return bitsPadder(result)
    return bitsPadder(createBits(createInt(result[1:]) + 1))
    

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((udpIP, udpPort))

f = open('receivedBonus.py', 'wb')
sequence_local = 0
while True:
   
    ready = select.select([serverSock], [], [], timeout)
    if ready[0]:
        data, addr = serverSock.recvfrom(1024)
        udpP = addr[1]
        rnumber = random.random()
        print('r', rnumber)
        print('sen seq', sequence_local)
        c = float(sys.argv[1])
        print('c', c)
        if((rnumber)<=c):
            sat = createBits(sequence_local)
            print('sat',sat)
            createACK(str(sequence_local), udpP)
            continue
        data1 = data[64:]
        print('data1',data1)
        # validCheck = checkSum(data)
        rawpkt=data.decode('utf-8')
        # rawpkt = rawdata[2:]
        print('data',data)
        flag_data = (rawpkt[:16])
        flag_data_int = int(flag_data,2)
        seq_data = (rawpkt[16:48])
        seq_data_int = int(seq_data, 2)
        print('recv seq_data_int',seq_data_int)
        checksum_data = (rawpkt[48:64])
        pktdata = rawpkt[64:]
        validCheck = checkSum(pktdata)
        print(len(pktdata)-2)
        flag = checksumtest(validCheck, checksum_data)
        print(flag)
        if(flag == 1):
            f.write(data1)
            sequence_local=+1
            createACK(seq_data, udpP)
    else:
        print ("%s Finish!" )
        f.close()
        break