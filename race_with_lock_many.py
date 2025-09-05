import threading, time, random

lock = threading.Lock()
total = 0
N = 12000
T = 12

def inc():
    global total
    for _ in range(N):
        with lock:
            tmp = total
            time.sleep(random.uniform(0, 0.0005))
            total = tmp + 1

def dec():
    global total
    for _ in range(N):
        with lock:
            tmp = total
            time.sleep(random.uniform(0, 0.0005))
            total = tmp - 1

threads = []
for i in range(T):
    t = threading.Thread(target=inc if i % 2 == 0 else dec)
    t.start()
    threads.append(t)

for t in threads: t.join()
print("Valor final (com lock):", total)
