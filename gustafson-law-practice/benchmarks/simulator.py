"""Task 21: deterministic strong/weak scaling simulator and CSV/plot export."""
import argparse
import csv
from pathlib import Path


def amdahl(p, alpha):
    return 1 / (alpha + (1 - alpha) / p)


def gustafson(p, alpha):
    return p - alpha * (p - 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-p', type=int, default=65536)
    parser.add_argument('--alphas', type=float, nargs='+', default=[.001, .04, .08, .20])
    parser.add_argument('--output', type=Path, default=Path(__file__).parent / 'simulator.csv')
    args = parser.parse_args()
    if not 1 <= args.max_p <= 65536 or any(not .001 <= a <= .20 for a in args.alphas):
        parser.error('Require 1 <= max-p <= 65536 and .001 <= alpha <= .20')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(['P', 'alpha', 'amdahl', 'gustafson', 'gustafson_efficiency'])
        for a in args.alphas:
            for p in range(1, args.max_p + 1):
                writer.writerow([p, a, amdahl(p, a), gustafson(p, a), gustafson(p, a)/p])
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
    ps = list(range(1, args.max_p + 1))
    for a in args.alphas:
        color = axes[0]._get_lines.get_next_color()
        for ax in axes:
            ax.plot(ps, [gustafson(p, a) for p in ps], color=color, label=f'Gustafson a={a:g}')
            ax.plot(ps, [amdahl(p, a) for p in ps], '--', color=color, label=f'Amdahl s={a:g}')
    axes[1].set_xscale('log'); axes[1].set_yscale('log')
    for ax in axes:
        ax.set(xlabel='Processors P', ylabel='Speedup (x)')
        ax.grid(alpha=.25); ax.legend(fontsize=7)
    fig.savefig(args.output.with_suffix('.png'), dpi=300)
    fig.savefig(args.output.with_suffix('.svg'))
    plt.close(fig)
    print(args.output)


if __name__ == '__main__':
    main()
