# Variant B: Scalability Diagnostics Results

| Configuration | $T_1$ (s) | $T_2$ (s) | $T_4$ (s) | $T_8$ (s) | $S_8$ | $e(2)$ | $e(8)$ | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A: Micro (k=1)** | 44.700 | 49.969 | 54.805 | 59.652 | 0.75x | 1.236 | 1.382 | Master dispatch serialization |
| **B: Queue Choke** | 10.156 | 55.603 | 86.578 | 92.357 | 0.11x | 9.950 | 10.250 | IPC lock contention explosion |
| **C: Buffered Batch** | 3.131 | 1.802 | 1.253 | 1.299 | 2.41x | 0.151 | 0.331 | Amortized synchronization |