import math
import time
from multiprocessing import Pool


def heavy_math(n):
  return sum(math.sin(i) * math.cos(i) for i in range(1, n))


def experiment(workers, total_chunks=16, chunk_size=2_000_000):
  t0 = time.perf_counter()
  time.sleep(0.40)  # Намеренный последовательный затор (~12% serial fraction)
  with Pool(processes=workers) as pool:
    pool.map(heavy_math, [chunk_size] * total_chunks)
  return time.perf_counter() - t0


def karp_flatt(t1, tp, p):
  if p <= 1:
    return 0.0
  sp = t1 / tp
  return ((1.0 / sp) - (1.0 / p)) / (1.0 - (1.0 / p))


if __name__ == '__main__':
  print('Запуск Эксперимента A...')
  cores = [1, 2, 4]
  runtimes = {}

  for p in cores:
    print(f' -> Выполнение расчетов на P = {p} ядрах...')
    runtimes[p] = experiment(p)

  t1 = runtimes[1]

  print('\n' + '=' * 50)
  print(f"{'P':<5}{'Runtime (s)':<15}{'Speedup':<12}{'Karp-Flatt e(p)':<15}")
  print('-' * 50)
  for p in cores:
    tp = runtimes[p]
    sp = t1 / tp
    e = karp_flatt(t1, tp, p)
    print(f'{p:<5}{tp:<15.3f}{sp:<12.2f}{e:<15.3f}')