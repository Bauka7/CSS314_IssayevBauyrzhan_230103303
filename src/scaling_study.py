import json
import time
import multiprocessing as mp
import numpy as np

def stencil_chunk(args):
    data, start_row, end_row = args
    res = np.copy(data[start_row:end_row, :])
    # 5-точечный 2D stencil update: 5 FLOPs на элемент
    res[1:-1, 1:-1] = 0.2 * (data[start_row+1:end_row+1, 1:-1] + 
                             data[start_row-1:end_row-1, 1:-1] + 
                             data[start_row:end_row, 2:] + 
                             data[start_row:end_row, :-2] + 
                             data[start_row:end_row, 1:-1])
    return res

def run_strong_scaling(N, max_cores):
    grid = np.ones((N, N), dtype=np.float64)
    runtimes = {}
    
    for P in range(1, max_cores + 1):
        print(f" -> Тестирование Strong Scaling на P = {P} ядрах...")
        chunk_size = N // P
        args = []
        for p in range(P):
            r_start = p * chunk_size
            r_end = (p + 1) * chunk_size if p != P - 1 else N
            args.append((grid, r_start, r_end))
        
        t0 = time.perf_counter()
        with mp.Pool(processes=P) as pool:
            _ = pool.map(stencil_chunk, args)
        runtimes[P] = time.perf_counter() - t0
        
    return runtimes

def main():
    print("Запуск Milestone 3: Scaling Models & Roofline Evaluation...")
    
    with open("results/salted_params.json") as f:
        params = json.load(f)
    N = params["N"]
    max_cores = mp.cpu_count()

    # 1. Strong Scaling Study
    t_strong = run_strong_scaling(N, max_cores)
    
    T1 = t_strong[1]
    with open("results/scaling_metrics.tsv", "w") as f:
        f.write("P\tT_strong\tSpeedup\tEfficiency\tAmdahl_s\n")
        for P in range(1, max_cores + 1):
            TP = t_strong[P]
            Sp = T1 / TP
            Ep = (Sp / P) * 100.0
            s = ((1.0 / Sp) - (1.0 / P)) / (1.0 - (1.0 / P)) if P > 1 else 0.0
            f.write(f"{P}\t{TP:.6f}\t{Sp:.4f}\t{Ep:.2f}%\t{s:.6f}\n")

    # 2. Arithmetic Intensity & Roofline Calculation
    # Stencil: 5 FLOPs на внутреннюю ячейку
    # Передача памяти: ~ 2 * 8 bytes (чтение + запись) = 16 bytes per element
    flops = 5 * (N - 2) * (N - 2)
    bytes_transferred = 16 * N * N
    arithmetic_intensity = flops / bytes_transferred

    roofline = {
        "N": N,
        "FLOPs": flops,
        "Bytes_Transferred": bytes_transferred,
        "Arithmetic_Intensity_FLOP_per_Byte": arithmetic_intensity,
        "Regime": "Memory-Bandwidth Bound" if arithmetic_intensity < 1.0 else "Compute Bound"
    }

    with open("results/roofline_summary.json", "w") as f:
        json.dump(roofline, f, indent=4)

    print("[УСПЕХ] Результаты M3 сохранены в results/scaling_metrics.tsv и results/roofline_summary.json")

if __name__ == "__main__":
    main()