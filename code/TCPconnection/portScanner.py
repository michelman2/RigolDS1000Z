import socket, threading


def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    # TCPsock.settimeout(20)
    try:
        TCPsock.connect((ip, port_number))
        output[port_number] = 'Listening'
    except:
        output[port_number] = ''
        TCPsock.close()
    
    TCPsock.close()




def scan_ports(host_ip, delay):

    threads = []        # To run TCP_connect concurrently
    output = {}         # For printing purposes

    thread_group_members = 500 
    thread_group_cnt = 20
    for thread_group_idx in range(thread_group_cnt): 
        
        # Spawning threads to scan ports
        for i in range(thread_group_members):
            port_num = thread_group_members * thread_group_idx + i
            # print(i)
            t = threading.Thread(target=TCP_connect, args=(host_ip, port_num , delay, output))
            threads.append(t)

        
        # Starting threads
        for i in range(thread_group_members): 
            port_num = thread_group_members * thread_group_idx + i       
            threads[port_num].start()

        # Locking the main thread until all threads complete
        for i in range(thread_group_members):
            port_num = thread_group_members * thread_group_idx + i
            threads[port_num].join()

    # Printing listening ports from small to large

    print(host_ip)
    for port_num in range(len(output)): 
        if output[port_num] == 'Listening':
            print(str(port_num) + ': ' + output[port_num])



def main():
    host_ip = "169.254.16.78"
    # host_ip = input("Enter host IP: ")
    # delay = int(input("How many seconds the socket is going to wait until timeout: "))   
    delay = 20
    scan_ports(host_ip, delay)

if __name__ == "__main__":
    main()