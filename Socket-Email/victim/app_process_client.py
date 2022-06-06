import  pickle, psutil, struct
import os
import subprocess

BUFSIZ = 1024 * 4

def send_data(client, data):
    size = struct.pack('!I', len(data))
    data = size + data
    client.sendall(data)
    return

def list_apps():
    ls1 = list()
    ls2 = list()
    ls3 = list()

    cmd = ['C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe', 
        'gps | where {$_.mainWindowTitle} | select Description, ID, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}']
    #proc = os.popen(cmd).read().split('\n')
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read().split(b'\n')
    tmp = list()
    for line in proc:
        if not line.isspace():
            tmp.append(line)
    print(len(tmp))
    tmp = tmp[3:]
    for line in tmp:
        try:
            arr = line.split(b" ")
            if len(arr) < 3:
                continue
            if arr[0] == b'' or arr[0] == b' ':
                continue

            name = arr[0]
            threads = arr[-1]
            ID = 0
            # interation
            cur = len(arr) - 2
            for i in range (cur, -1, -1):
                if len(arr[i]) != 0:
                    ID = arr[i]
                    cur = i
                    break
            for i in range (1, cur, 1):
                if len(arr[i]) != 0:
                    name += ' ' + arr[i]
            ls1.append(name)
            ls2.append(ID)
            ls3.append(threads)
        except:
            pass
    return ls1, ls2, ls3



def list_processes():
    ls1 = list()
    ls2 = list()
    ls3 = list()
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            name = proc.name()
            pid = proc.pid
            threads = proc.num_threads()
            ls1.append(str(name))
            ls2.append(str(pid))
            ls3.append(str(threads))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return ls1, ls2, ls3

def kill(pid):
    cmd = 'taskkill.exe /F /PID ' + str(pid)
    try:
        a = os.system(cmd)
        if a == 0:
            return 1
        else:
            return 0
    except:
        return 0
    
def start(name):
    os.system(name)
    return

def app_process(client):
    global msg
    msg = client.recv(BUFSIZ).decode("utf8")
    print("Messages:", msg)
    res = 0
    ls1 = list()
    ls2 = list()
    ls3 = list()
    action = int(msg)
    #0-kill
    if action == 0:
        pid = client.recv(BUFSIZ).decode("utf8")
        pid = int(pid)
        # print(pid)
        try:
            res = kill(pid)
            
        except:
            res = 0
        if res == 1:
            mesg = "Process " + str(pid) + " killed!"
        else:
            mesg = "Process " + str(pid) + " not found!"
        client.sendall(mesg.encode("utf8"))
    #1-xem
    elif action == 1:
        try:
            status = client.recv(BUFSIZ).decode("utf8")
            # print("Status:", status)
            # print(status)
            if "PROCESS" not in status:
                ls1, ls2, ls3 = list_apps()
            else:
                ls1, ls2, ls3 = list_processes()
            res = 1
        except:
            res = 0
    #2-xoa
    elif action == 2:
        res = 1
    #3 - start
    elif action == 3:
        pname = client.recv(BUFSIZ).decode("utf8")
        try:
            start(pname)
            res = 1
        except:
            res = 0
    if action != 1 and action != 3:
        client.sendall(bytes(str(res), "utf8"))
    if action == 1:
        ls1 = pickle.dumps(ls1)
        ls2 = pickle.dumps(ls2)
        ls3 = pickle.dumps(ls3)

        send_data(client, ls1)   
        send_data(client, ls2)
        send_data(client, ls3)
