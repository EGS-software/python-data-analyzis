import threading, time, random

total = 0
N = 10000     # ops por thread
T = 12        # numero de threads (metade incrementa, metade decrementa)

def inc():
    global total
    for _ in range(N):
        tmp = total
        # pequenas esperas aleatorias aumentam interleaving
        time.sleep(random.uniform(0, 0.0005))
        total = tmp + 1

def dec():
    global total
    for _ in range(N):
        tmp = total
        time.sleep(random.uniform(0, 0.0005))
        total = tmp - 1

threads = []
for i in range(T):
    t = threading.Thread(target=inc if i % 2 == 0 else dec)
    t.start()
    threads.append(t)

for t in threads: t.join()
print("Valor final (sem lock):", total)
