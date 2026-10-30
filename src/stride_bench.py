import time
import numpy as np

def run_stride_bench():
    elements = 16_777_216
    data = np.ones(elements, dtype=np.float64)
    strides = [1, 2, 4, 8, 16, 32, 64, 128]
    
    with open("results/stride_results.tsv", "w") as f:
        f.write("stride\tlatency_per_element_ns\n")
        for s in strides:
            for _ in range(5):
                _ = np.sum(data[::s])
            
            times = []
            for _ in range(5):
                t0 = time.perf_counter_ns()
                sub_arr = data[::s]
                total = np.sum(sub_arr)
                t1 = time.perf_counter_ns()
                times.append(t1 - t0)
            
            median_ns = float(np.median(times))
            elements_touched = len(data[::s])
            latency_per_elem = median_ns / elements_touched
            f.write(f"{s}\t{latency_per_elem:.4f}\n")

if __name__ == "__main__":
    run_stride_bench()