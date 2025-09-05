import threading, time

N = 50  # ajuste conforme sua maquina
def worker(i):
    time.sleep(10)  # simula trabalho/espera

threads = []
for i in range(N):
    t = threading.Thread(target=worker, args=(i,), name=f"thr-{i:02d}")
    t.start()
    threads.append(t)

# pausa curta para voce observar no Task Manager
time.sleep(2)

# lista as threads ativas do processo (so nomes, para registro)
print("Threads ativas (amostra):")
for t in threading.enumerate()[:10]:
    print("-", t.name)

input("Observe 'Threads' no Task Manager e pressione Enter para encerrar...")


