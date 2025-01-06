import socket,sys
import time, queue
import threading



usage ="python3 simple_scanner.py TARGET START_PORT END_PORT THREADS"

print("*" * 50)
print("Python Simple Port Scanner")
print("*" * 50)

target = sys.argv[1]
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])
thread_no = int(sys.argv[4])

result = "[+] Result:\nPORT\tSTATE\n"

try:
    target = socket.gethostbyname(target)
except:
    print("[-] Host resolution failed. ")
    exit()

print("[+] Scanning target: {}".format(target))

if not target or not str(start_port) or not end_port or not thread_no:
    print(usage)
    exit()

def scan_port(t_no):
    global result
    while not q.empty():
        port = q.get()
        print("Scanner for port {}...".format(port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            conn = s.connect_ex((target, port))
            if not conn:
                result += f"{port}\tOPEN\n"
            s.close()
        except:
            pass
        q.task_done()

q = queue.Queue()

start_time = time.time()

for i in range(thread_no):
    t = threading.Thread(target=scan_port,args=(i,))
    t.start()

for j in range(start_port, end_port + 1):
    q.put(j)

q.join()

end_time = time.time()
print(result)
print("Time taken: {}".format(end_time - start_time))