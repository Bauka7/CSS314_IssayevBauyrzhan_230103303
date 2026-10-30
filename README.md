# CS482 Lab Practicum Summary

## Bottleneck Analysis Findings
1. **Memory Stride**: Clear latency jump observed moving from stride-1 to stride-8+, demonstrating cache-line (64-byte) eviction dynamics and DRAM bandwidth bottlenecks.
2. **False Sharing**: Unpadded shared array counters caused severe cache invalidation ping-ponging under multi-process execution (high Karp-Flatt metric `e(P)`), resolved completely by 64-byte padding and privatization.
3. **Scaling & Roofline**: Stencil execution exhibits low arithmetic intensity (~0.31 FLOP/byte), placing the execution firmly in the **Memory-Bandwidth Bound** regime on host architecture.