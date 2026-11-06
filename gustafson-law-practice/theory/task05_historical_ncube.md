# Task 05. Historical nCUBE reconstruction

Gustafson's 1988 report discusses a 1024-processor hypercube at Sandia. It lists scaled speedups of 1021 for beam stress analysis, 1020 for a surface-wave simulation and 1016 for fluid flow. The associated work by Gustafson, Montry and Benner concerned scientific applications on this machine. The report describes serial fractions in the approximate .4-.8% range; these rounded figures are not exact parameters for reproducing every reported speedup.

The experiment expanded scientific problems as processor resources grew. It therefore compared parallel runtime with the sequential cost of the expanded problem. Reading .004 as a fixed original one-core fraction gives a ceiling 250 and S_A(1024)=1/(.004+.996/1024)=201.10. Reading it as a parallel-machine fraction gives S_G=1024-.004*1023=1019.908, illustrating why near-linear scaled speedup was possible. This example is a model reconstruction, not a fresh measurement or an exact reconstruction of the three applications.

The result changes the workload assumption, not Amdahl's algebra. Larger problems can amortize bounded serial stages; fixed-size latency remains constrained.

Primary source: [Gustafson, Reevaluating Amdahl's Law, CACM 31(5), 1988, DOI 10.1145/42411.42415](https://citeseerx.ist.psu.edu/document?doi=2514eef3fd17294045718403263224fc9f35f75d&repid=rep1&type=pdf).
