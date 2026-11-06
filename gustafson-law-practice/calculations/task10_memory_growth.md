# Task 10. Memory ceiling of a cubic grid

The question does not specify bytes per cell, number of arrays, GB convention or reserved memory. Therefore N has no unique numeric value. Let b be the aggregate bytes per cell (all fields and buffers), B the usable bytes per node, and P the node count. Ignoring halos and decomposition constraints, b*N^3<=P*B, so N_max=floor((P*B/b)^(1/3)).

Explicit illustrative assumption: a single float64 field, b=8, decimal 32 GB=32*10^9 bytes/node, no reserves. The exact integer ceilings are:

| Nodes | Aggregate bytes | Maximum cells | N_max |
|---:|---:|---:|---:|
|64|2,048,000,000,000|256,000,000,000|6349|
|512|16,384,000,000,000|2,048,000,000,000|12699|

Using 32 GiB=32*2^30 instead gives N=6501 and 13003. These are aggregate capacity bounds; a partition must also fit each local subdomain. Halos, replicated metadata and temporary arrays reduce capacity. Two float64 grids mean b=16 and multiply the continuous dimension ceiling by 2^(-1/3).

With fixed b and B, increasing nodes eightfold doubles continuous N. For M(P)=cP, the per-node constraint is c<=B; c alone does not determine N until b is specified.
