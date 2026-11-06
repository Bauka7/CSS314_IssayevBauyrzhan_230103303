# Task 13. Two failures of constant-time weak scaling

## Direct all-pairs N-body with fixed particles per worker

Assign k particles per processor, N=kP. Exact direct interactions require Theta(N^2) operations per iteration, so balanced compute time is Theta(N^2/P)=Theta(k^2 P). Even with zero network cost it grows linearly. Replicating all particle positions also grows per-worker storage and communication. To hold compute time fixed one needs N proportional to sqrt(P), which no longer keeps particles per worker fixed. Increasing raw input size linearly is not equivalent to increasing computational work linearly.

## Distributed BFS on a hub-dominated power-law graph

Scale vertices and edges per processor approximately constantly. Each BFS level still requires frontier exchange, visited-state coordination and a global termination decision. A hub owned by one rank can send a growing fraction of frontier messages; locks or atomics on its destination state serialize updates. Partitioning only by vertex count does not balance edges. The maximum rank time determines level time, not the average, and barriers multiply the penalty by the number of levels. Even a balanced reduction has a latency term proportional to log P. Thus constant local average work does not bound wall time. A 2D partition, edge balancing and aggregation may help but do not prove Gustafson compliance for arbitrary graph families.
