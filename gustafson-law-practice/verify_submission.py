"""Verify real numerical artifacts; exits nonzero on inconsistency or missing outputs."""
import csv
import importlib.util
import json
import math
from pathlib import Path
import re
import statistics

ROOT = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    simulator = load('simulator', ROOT/'benchmarks/simulator.py')
    fitting = load('fitting', ROOT/'benchmarks/fit_gustafson.py')
    # Cross-check reference-frame equivalence and mathematical boundary cases.
    for p in [1, 2, 16, 128, 1024, 65536]:
        for alpha in [0, .001, .04, .08, .2, 1]:
            speed = simulator.gustafson(p, alpha)
            serial_fraction = alpha/speed
            assert math.isclose(simulator.amdahl(p, serial_fraction), speed)
            assert 1 <= speed <= p
    assert math.isclose(simulator.gustafson(8192, 692/8191), 7500)
    # Integer capacity checks avoid floating-point cube-root rounding ambiguity.
    for p, b, n in [(64,32*10**9,6349),(512,32*10**9,12699),
                    (64,32*2**30,6501),(512,32*2**30,13003)]:
        assert 8*n**3 <= p*b < 8*(n+1)**3
    # Known synthetic regression must recover its exact generating parameter.
    synthetic = [{'P': str(p), 'scaled_speedup': str(p-.04*(p-1)), 'parallel_seconds': '1'}
                 for p in [1,2,4,8,16] for _ in range(5)]
    _, reference_fit = fitting.fit(synthetic)
    assert math.isclose(reference_fit['alpha_unconstrained'], .04, abs_tol=1e-12)
    assert reference_fit['rmse'] < 1e-12
    with (ROOT/'benchmarks/results.csv').open(newline='') as f:
        rows = list(csv.DictReader(f))
    environment = json.loads((ROOT/'benchmarks/environment.json').read_text())
    counts = environment['counts']
    assert len(counts) >= 5 and counts == list(range(1, environment['logical_processors']+1))
    assert len(rows) == len(counts)*5
    for p in counts:
        group = [r for r in rows if int(r['P']) == p]
        assert sorted(int(r['run']) for r in group) == [1,2,3,4,5]
        for r in group:
            assert int(r['k']) == environment['k_per_process']
            assert int(r['total_samples']) == p*int(r['k'])
            ts, tp, speed = map(float, [r['serial_seconds'],r['parallel_seconds'],r['scaled_speedup']])
            assert ts > 0 and tp > 0 and math.isclose(speed, ts/tp)
            assert abs(float(r['pi_estimate'])-math.pi) < 1e-10
    summary, fit = fitting.fit(rows)
    saved = json.loads((ROOT/'benchmarks/fit.json').read_text())
    assert fit == saved
    with (ROOT/'benchmarks/summary.csv').open(newline='') as f:
        stored = list(csv.DictReader(f))
    for actual, expected in zip(stored, summary, strict=True):
        for key in expected:
            assert math.isclose(float(actual[key]), expected[key], abs_tol=1e-12)
    with (ROOT/'benchmarks/simulator.csv').open(newline='') as f:
        total = 0
        for r in csv.DictReader(f):
            p, alpha = int(r['P']), float(r['alpha'])
            assert 1 <= p <= 65536 and .001 <= alpha <= .2
            assert math.isclose(float(r['amdahl']), simulator.amdahl(p,alpha))
            assert math.isclose(float(r['gustafson']), simulator.gustafson(p,alpha))
            assert math.isclose(float(r['gustafson_efficiency']), simulator.gustafson(p,alpha)/p)
            total += 1
        assert total == 4*65536
    docs = list(ROOT.rglob('*.md'))
    tasks = {int(m.group(1)) for d in docs if (m := re.match(r'task(\d+)_', d.name))}
    assert set(range(1,21)) <= tasks and {23,24} <= tasks
    for path in docs:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if not target.startswith(('https:', 'http:', '#')):
                assert (path.parent/target.split('#')[0]).exists(), (path, target)
    for relative in ['plots/scaling_comparison.png','plots/scaling_comparison.svg',
                     'benchmarks/simulator.png','benchmarks/simulator.svg']:
        assert (ROOT/relative).stat().st_size > 1000
    print(f'PASS: {len(rows)} measured trials, {len(counts)} process counts, {total} simulator rows; formulas, regression, summaries and links verified.')


if __name__ == '__main__':
    main()
