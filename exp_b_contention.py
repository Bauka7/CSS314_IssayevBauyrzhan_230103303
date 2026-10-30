import time
from multiprocessing import Process, Value, Lock

def contended_worker(shared_counter, lock, iterations):
    for _ in range(iterations):
        with lock:  # Борьба за мьютекс и сброс кэш-линий
            shared_counter.value += 1

def run_contended(p, total_increments=2_000_000):
    increments_per_worker = total_increments // p
    counter = Value('i', 0)
    lock = Lock()
    procs = [
        Process(target=contended_worker, args=(counter, lock, increments_per_worker))
        for _ in range(p)
    ]
    t0 = time.perf_counter()
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()
    t1 = time.perf_counter()
    assert counter.value == total_increments
    return t1 - t0

def karp_flatt(t1, tp, p):
    if p <= 1:
        return 0.0
    sp = t1 / tp
    return ((1.0 / sp) - (1.0 / p)) / (1.0 - (1.0 / p))

if __name__ == "__main__":
    print("Запуск Эксперимента B (Lock Contention)...")
    cores = [1, 2, 4]
    runtimes = {}
    for p in cores:
        print(f" -> Выполнение расчетов для P = {p} (занимает 10-30 сек)...")
        runtimes[p] = run_contended(p)

    t1 = runtimes[1]
    print("\n" + "="*50)
    print(f"{'P':<5}{'Runtime (s)':<15}{'Speedup':<12}{'Karp-Flatt e(p)':<15}")
    print("-" * 50)
    for p in cores:
        tp = runtimes[p]
        sp = t1 / tp
        e = karp_flatt(t1, tp, p)
        print(f"{p:<5}{tp:<15.3f}{sp:<12.2f}{e:<15.3f}")