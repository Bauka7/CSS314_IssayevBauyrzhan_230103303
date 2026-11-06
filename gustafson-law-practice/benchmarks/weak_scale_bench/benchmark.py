"""Tasks 22-23: actual multiprocessing weak scaling, including process startup."""
import argparse
import csv
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import platform
import random
import statistics
import sys
import time


def integrate(k):
    # Midpoint quadrature: integral_0^1 4/(1+x*x) dx = pi.
    h = 1.0 / k
    total = 0.0
    for i in range(k):
        x = (i + .5) * h
        total += 4.0 / (1.0 + x*x)
    return total * h


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--k', type=int, default=500000)
    ap.add_argument('--runs', type=int, default=5)
    ap.add_argument('--counts', type=int, nargs='+')
    ap.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1]/'results.csv')
    args = ap.parse_args()
    maximum = os.cpu_count() or 1
    counts = sorted(set(args.counts or range(1, maximum + 1)))
    if args.k < 1 or args.runs < 2 or any(p < 1 or p > maximum for p in counts):
        ap.error('k >= 1, runs >= 2, counts within host hardware concurrency required')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    metadata = {'platform': platform.platform(), 'python': sys.version,
                'processor': platform.processor(), 'logical_processors': maximum,
                'k_per_process': args.k, 'runs': args.runs, 'counts': counts,
                'timer': 'perf_counter', 'start_method': 'spawn',
                'timing_scope': 'end-to-end including Pool spawn, IPC, reduction and shutdown',
                'serial_reference': 'same P independent quadratures, sequentially',
                'utc_started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    args.output.with_name('environment.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    ctx = mp.get_context('spawn')
    # Warm interpreter and arithmetic before measured trials.
    integrate(min(args.k, 10000))
    schedule = [(p, run) for p in counts for run in range(1, args.runs + 1)]
    random.Random(230103303).shuffle(schedule)
    with args.output.open('w', newline='') as f:
        fields = ['P', 'run', 'k', 'total_samples', 'serial_seconds', 'parallel_seconds',
                  'scaled_speedup', 'pi_estimate', 'absolute_error']
        writer = csv.DictWriter(f, fields); writer.writeheader()
        for p, run in schedule:
            def serial():
                start = time.perf_counter()
                values = [integrate(args.k) for _ in range(p)]
                return time.perf_counter()-start, statistics.fmean(values)
            def parallel():
                start = time.perf_counter()
                with ctx.Pool(p) as pool:
                    values = pool.map(integrate, [args.k]*p, chunksize=1)
                    estimate = statistics.fmean(values)
                return time.perf_counter()-start, estimate
            # Alternate reference order to reduce systematic order bias.
            if run % 2:
                ts, reference = serial(); tp, result = parallel()
            else:
                tp, result = parallel(); ts, reference = serial()
            if abs(result-reference) > 1e-12 or abs(result-math.pi) > max(1e-10, 1/args.k**2):
                raise RuntimeError('Quadrature validation failed')
            writer.writerow(dict(zip(fields, [p,run,args.k,p*args.k,ts,tp,ts/tp,result,abs(result-math.pi)])))
            f.flush()
            print(f'P={p:2d} run={run} serial={ts:.4f}s parallel={tp:.4f}s S={ts/tp:.3f}', flush=True)


if __name__ == '__main__':
    mp.freeze_support()
    main()
