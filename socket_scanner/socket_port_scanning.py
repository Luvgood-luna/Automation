# Script to scan ports using sockets
from socket import *
import time

startTime = time.time()
if __name__ == '__main__':
    target = input("Enter the host for scanning")
    t_IP = gethostbyname(target)
    print("Starting scanning on host IP: ", t_IP)

    for i in range(50,500):
        s = socket(AF_INET, SOCK_STREAM)
        #print(i)
        conn = s.connect_ex((t_IP, i))
        if(conn == 0):
            print("Port %d: is open" % (i,))
        s.close()

print("Time taken to scan: ", time.time() - startTime)
