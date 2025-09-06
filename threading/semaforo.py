import threading
import time

# Definindo um semáforo com 2 permissões (duas threads podem acessar o recurso simultaneamente)
semaforo = threading.Semaphore(2)

def acessar_recurso(thread_id):
    print(f'Thread {thread_id} esperando para acessar o recurso...')
    
    # Adquirir o semáforo (entrar na seção crítica)
    with semaforo:
        print(f'Thread {thread_id} acessou o recurso!')
        time.sleep(2)  # Simula o uso do recurso por 2 segundos
        print(f'Thread {thread_id} liberou o recurso.')

# Criar e iniciar múltiplas threads
threads = []
for i in range(5):  # Criando 5 threads
    t = threading.Thread(target=acessar_recurso, args=(i,))
    threads.append(t)
    t.start()

# Aguarda que todas as threads terminem a execução
for t in threads:
    t.join()

print('Todas as threads terminaram.')

