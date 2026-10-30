import json
import time
import numpy as np

def run_kernels():
    with open("results/salted_params.json") as f:
        params = json.load(f)
    
    N = params["N"] // 2
    np.random.seed(params["seed"])
    A = np.random.rand(N, N).astype(np.float64)
    B = np.random.rand(N, N).astype(np.float64)

    # Naive i-j-k
    times_ijk = []
    for _ in range(3):
        C_ijk = np.zeros((N, N), dtype=np.float64)
        t0 = time.perf_counter()
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    C_ijk[i, j] += A[i, k] * B[k, j]
        times_ijk.append(time.perf_counter() - t0)
    
    # Interchanged i-k-j
    times_ikj = []
    for _ in range(3):
        C_ikj = np.zeros((N, N), dtype=np.float64)
        t0 = time.perf_counter()
        for i in range(N):
            for k in range(N):
                r = A[i, k]
                for j in range(N):
                    C_ikj[i, j] += r * B[k, j]
        times_ikj.append(time.perf_counter() - t0)

    t_naive = float(np.median(times_ijk))
    t_interchanged = float(np.median(times_ikj))
    speedup = t_naive / t_interchanged

    res = {
        "N_subblock": N,
        "time_naive_sec": t_naive,
        "time_interchanged_sec": t_interchanged,
        "speedup": speedup
    }
    
    with open("results/loop_interchange.json", "w") as f:
        json.dump(res, f, indent=4)

    np.save("results/C_interchanged.npy", C_ikj)

if __name__ == "__main__":
    run_kernels()