"""Tasks 23-24: constrained and unconstrained OLS plus measured error bars."""
import csv
import json
from pathlib import Path
import argparse
import statistics
import math


def fit(rows):
    grouped = {}
    for r in rows:
        grouped.setdefault(int(r['P']), []).append(r)
    summary = []
    for p, group in sorted(grouped.items()):
        speeds = [float(r['scaled_speedup']) for r in group]
        times = [float(r['parallel_seconds']) for r in group]
        sd = statistics.stdev(speeds)
        summary.append({'P': p, 'n': len(group), 'mean_seconds': statistics.mean(times),
                        'sd_seconds': statistics.stdev(times), 'mean_speedup': statistics.mean(speeds),
                        'sd_speedup': sd, 'se_speedup': sd/math.sqrt(len(group))})
    denominator = sum((r['P']-1)**2 for r in summary)
    if denominator == 0:
        raise ValueError('At least one count greater than 1 required')
    # S = P - alpha(P-1), fixed intercept at (P=1,S=1).
    alpha_raw = sum((r['P']-1)*(r['P']-r['mean_speedup']) for r in summary)/denominator
    alpha = min(1., max(0., alpha_raw))
    residuals = [r['mean_speedup']-(r['P']-alpha*(r['P']-1)) for r in summary]
    mean = statistics.mean(r['mean_speedup'] for r in summary)
    sse = sum(x*x for x in residuals)
    sst = sum((r['mean_speedup']-mean)**2 for r in summary)
    return summary, {'alpha_unconstrained': alpha_raw, 'alpha_observed_bounded': alpha,
                     'constraint': '0 <= alpha <= 1', 'fit': 'unweighted OLS of configuration means; fixed intercept',
                     'rmse': math.sqrt(sse/len(summary)), 'r_squared': 1-sse/sst if sst else None,
                     'residuals': residuals,
                     'interpretation': 'effective penalty, not direct measurement of serial code; startup and contention included'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', type=Path, default=Path(__file__).parent/'results.csv')
    args = ap.parse_args()
    with args.input.open(newline='') as f:
        summary, result = fit(list(csv.DictReader(f)))
    root = args.input.resolve().parents[1]
    with (args.input.parent/'summary.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, list(summary[0])); w.writeheader(); w.writerows(summary)
    (args.input.parent/'fit.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    ps = [r['P'] for r in summary]; alpha = result['alpha_observed_bounded']
    fig, ax = plt.subplots(figsize=(8, 5), constrained_layout=True)
    ax.plot(ps, ps, ':', color='black', label='Ideal linear')
    ax.plot(ps, [p-alpha*(p-1) for p in ps], label=f'Gustafson OLS, alpha={alpha:.4f}')
    ax.plot(ps, [1/(alpha+(1-alpha)/p) for p in ps], '--', label='Amdahl (same numeric fraction)')
    ax.errorbar(ps, [r['mean_speedup'] for r in summary], yerr=[r['se_speedup'] for r in summary],
                fmt='o', capsize=4, label='Measured mean +/- 1 SE (5 runs)')
    ax.set(xlabel='Worker processes P', ylabel='Scaled speedup: Tserial(W(P)) / Tparallel(W(P))',
           title='Weak scaling: midpoint integration, end-to-end process execution')
    ax.grid(alpha=.25); ax.legend(fontsize=8)
    dest = root/'plots'; dest.mkdir(exist_ok=True)
    fig.savefig(dest/'scaling_comparison.png', dpi=300)
    fig.savefig(dest/'scaling_comparison.svg')
    plt.close(fig)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
