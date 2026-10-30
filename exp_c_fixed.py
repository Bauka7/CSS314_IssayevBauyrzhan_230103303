import time
from multiprocessing import Pool

def private_worker(iterations):
    local_sum = 0
    for _ in range(iterations):
        local_sum += 1
    return local_sum

def run_privatized(p, total_increments=20_000_000):
    increments_per_worker = total_increments // p
    tasks = [increments_per_worker] * p
    t0 = time.perf_counter()
    with Pool(processes=p) as pool:
        results = pool.map(private_worker, tasks)
    total = sum(results)
    t1 = time.perf_counter()
    assert total == total_increments
    return t1 - t0

def karp_flatt(t1, tp, p):
    if p <= 1:
        return 0.0
    sp = t1 / tp
    return ((1.0 / sp) - (1.0 / p)) / (1.0 - (1.0 / p))

if __name__ == "__main__":
    print("Запуск Эксперимента C (Privatization Fix)...")
    cores = [1, 2, 4]
    runtimes = {}
    for p in cores:
        print(f" -> Выполнение расчетов для P = {p}...")
        runtimes[p] = run_privatized(p)

    t1 = runtimes[1]
    print("\n" + "="*50)
    print(f"{'P':<5}{'Runtime (s)':<15}{'Speedup':<12}{'Karp-Flatt e(p)':<15}")
    print("-" * 50)
    for p in cores:
        tp = runtimes[p]
        sp = t1 / tp
        e = karp_flatt(t1, tp, p)
        print(f"{p:<5}{tp:<15.3f}{sp:<12.2f}{e:<15.3f}")