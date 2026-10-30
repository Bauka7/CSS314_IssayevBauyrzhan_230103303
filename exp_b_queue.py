import time
from multiprocessing import Process, Queue


def queue_worker(out_queue, items_per_worker):
  for i in range(items_per_worker):
    out_queue.put(i % 7)


def run_queue_benchmark(p, total_items=200_000):
  q = Queue()
  items_per_worker = total_items // p
  workers = [
      Process(target=queue_worker, args=(q, items_per_worker))
      for _ in range(p)
  ]

  t0 = time.perf_counter()
  for w in workers:
    w.start()

  collected = 0
  while collected < total_items:
    _ = q.get()
    collected += 1

  for w in workers:
    w.join()
  return time.perf_counter() - t0


if __name__ == "__main__":
  TOTAL_ITEMS = 200_000
  cores = [1, 2, 4, 8]

  print(f"\n--- Experiment B: Queue Contention Analysis ({TOTAL_ITEMS} items) ---")
  runtimes = {}

  for p in cores:
    print(f"Выполнение для P={p} ядер...", end="", flush=True)
    t = run_queue_benchmark(p, total_items=TOTAL_ITEMS)
    runtimes[p] = t
    print(f" Готово ({t:.2f}s)")

  t1 = runtimes[1]
  print("\n--- Итоговые результаты Experiment B ---")
  for p in cores:
    tp = runtimes[p]
    sp = t1 / tp
    e = ((p * tp / t1) - 1.0) / (p - 1.0) if p > 1 else 0.0
    print(
        f"P={p:2d} | Time={tp:6.3f}s | Speedup={sp:5.2f}x | Karp-Flatt"
        f" e={e:6.3f}"
    )