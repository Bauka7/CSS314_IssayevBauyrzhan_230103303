import time
from multiprocessing import Pool


def collatz_steps(n):
  steps = 0
  while n > 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    steps += 1
  return steps


def run_granularity(workers, total_items=200_000, chunk_size=1):
  numbers = range(1, total_items + 1)
  t0 = time.perf_counter()
  with Pool(processes=workers) as pool:
    # chunksize=1 отправляет каждую задачу отдельным пакетом
    results = pool.map(collatz_steps, numbers, chunksize=chunk_size)
  return time.perf_counter() - t0, sum(results)


if __name__ == "__main__":
  # 200_000 задач достаточно для демонстрации проблемы на Windows
  TOTAL_ITEMS = 200_000
  cores = [1, 2, 4, 8]

  print(f"--- Experiment A: Granularity Benchmark ({TOTAL_ITEMS} items) ---")
  runtimes = {}

  # Выводим статус по мере выполнения каждого ядра
  for p in cores:
    print(f"Выполняется расчет для P={p} ядер...", end="", flush=True)
    t, _ = run_granularity(p, total_items=TOTAL_ITEMS, chunk_size=1)
    runtimes[p] = t
    print(f" Готово ({t:.2f}s)")

  t1 = runtimes[1]
  print("\n--- Итоговые результаты Experiment A ---")
  for p in cores:
    tp = runtimes[p]
    sp = t1 / tp
    e = ((p * tp / t1) - 1.0) / (p - 1.0) if p > 1 else 0.0
    print(
        f"P={p:2d} | Time={tp:6.3f}s | Speedup={sp:5.2f}x | Karp-Flatt"
        f" e={e:6.3f}"
    )