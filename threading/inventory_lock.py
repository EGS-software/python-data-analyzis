import threading, time, random

estoque = 120
lock = threading.Lock()
LOG = []

def vendedor(nome):
    global estoque
    time.sleep(random.uniform(0, 0.01))  # embaralha a ordem de chegada
    vendidos_local = 0
    while True:
        with lock:
            if estoque <= 0:
                LOG.append(f"{nome}: sem itens.")
                break
            estoque -= 1
            vendidos_local += 1
            rest = estoque
        # trabalho fora da secao critica
        time.sleep(random.uniform(0, 0.003))
        if vendidos_local % 10 == 0:
            LOG.append(f"{nome}: ja vendeu {vendidos_local} (restantes={rest})")

threads = [threading.Thread(target=vendedor, args=(f"V{i}",)) for i in range(6)]
for t in threads: t.start()
for t in threads: t.join()

vendidos = sum(1 for linha in LOG if "ja vendeu" in linha)  # apenas marca check, nao total
print(f"Restantes finais: {estoque}   (esperado: 0)")
print("Exemplos de log:")
for linha in LOG[:8]:
    print(linha)
