# Task 17. 3D stencil surface/volume

For a fixed number of time steps, global work is Theta(N^3). Weak scaling sets N=N0*P^(1/3). The exterior global surface/volume ratio is 6N^2/N^3=6/N, so it decreases as P^(-1/3). However, the physical exterior is not the sum of interprocessor exchange surfaces.

With a balanced 3D decomposition, each rank owns side length n=N/P^(1/3)=N0. Its compute work is Theta(n^3) and exchanges up to six faces of Theta(n^2) cells. Per-rank communication/compute ratio is Theta(1/n)=Theta(1/N0), constant in weak scaling. Aggregate internal exchange is Theta(P*n^2)=Theta(N^2*P^(1/3)); dividing by global work gives Theta(P^(1/3)/N), again constant.

In strong scaling N stays fixed and local n shrinks, so the ratio worsens as P^(1/3)/N. A slab decomposition under volume weak scaling can also worsen: slab thickness N/P decreases, face size N^2 grows, and face/volume per rank is P/N=Theta(P^(2/3)). Process topology matters.

Thus the global exterior ratio improves, ideal local 3D exchange ratio remains constant, and unfavorable partitions or growing network contention can degrade actual performance. A global timestep reduction contributes log P latency even with constant local faces. The proof concerns each iteration; refining resolution at fixed physical duration may require more timesteps because of stability constraints.
