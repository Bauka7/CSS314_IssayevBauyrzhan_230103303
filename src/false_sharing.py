import multiprocessing as mp
import ctypes
import time
import numpy as np

ITERATIONS = 5_000_000

def worker_unpadded(arr, worker_id, iterations):
    for _ in range(iterations):
        arr[worker_id] += 1

def worker_padded(arr, worker_id, iterations):
    idx = worker_id * 8
    for _ in range(iterations):
        arr[idx] += 1

def worker_privatized(arr, worker_id, iterations):
    local_count = 0
    for _ in range(iterations):
        local_count += 1
    arr[worker_id] = local_count

def run_experiment(worker_fn, P, array_size):
    arr = mp.Array(ctypes.c_int64, array_size)
    processes = []
    t0 = time.perf_counter()
    for p in range(P):
        proc = mp.Process(target=worker_fn, args=(arr, p, ITERATIONS))
        processes.append(proc)
        proc.start()
    for proc in processes:
        proc.join()
    t1 = time.perf_counter()
    return t1 - t0

def karp_flatt(T1, TP, P):
    if P <= 1:
        return 0.0
    Sp = T1 / TP
    return ((1.0 / Sp) - (1.0 / P)) / (1.0 - (1.0 / P))

if __name__ == "__main__":
    print("Запуск бенчмарка False Sharing (выполнение занимает ~30-60 секунд)...")
    
    cpu_cnt = mp.cpu_count()
    procs = [p for p in [1, 2, 4, 8] if p <= cpu_cnt]
    if 1 not in procs:
        procs.insert(0, 1)

    t_unpadded = {}
    t_padded = {}
    t_privatized = {}

    for p in procs:
        print(f" -> Выполнение для P = {p} процессов...")
        t_unpadded[p] = run_experiment(worker_unpadded, p, 8)
        t_padded[p] = run_experiment(worker_padded, p, 64)
        t_privatized[p] = run_experiment(worker_privatized, p, 8)

    with open("results/false_sharing_karp_flatt.tsv", "w") as f:
        f.write("P\tT_unpadded\tT_padded\tT_privatized\te_unpadded\te_padded\n")
        for p in procs:
            e_unp = karp_flatt(t_unpadded[1], t_unpadded[p], p)
            e_pad = karp_flatt(t_padded[1], t_padded[p], p)
            f.write(f"{p}\t{t_unpadded[p]:.6f}\t{t_padded[p]:.6f}\t{t_privatized[p]:.6f}\t{e_unp:.6f}\t{e_pad:.6f}\n")

    print("[УСПЕХ] Результаты сохранены в results/false_sharing_karp_flatt.tsv")