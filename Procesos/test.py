from multiprocessing import Process
import random as rnd
import os

def child_task():
    print(f"Child process: PID={os.getpid()}, Parent={os.getppid()}")

if __name__ == "__main__":
    n = rnd.randint(0, 10)
    A = []
    for i in range(n): 
        p = Process(target=child_task)
        A.append(p)

    for i in range(len(A)):
        A[i].start()
        print(f"Parent process: PID={os.getpid()}, Child={p.pid}")
        A[i].join()
