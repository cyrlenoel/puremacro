## 2026-08-31 - Memory reallocation in numpy simulation loops
**Learning:** Calling `np.concatenate` to manage rolling history buffers in tight simulation loops (like for Generalized IRF trajectories across `H` steps and `M` parallel histories) is a significant bottleneck due to constant reallocation and copying of the whole buffer, even though the arrays are relatively small per iteration. Pre-allocating the full future length works but increases peak memory. Simply slicing and re-assigning inplace (`buf[:, :-1] = buf[:, 1:]` and `buf[:, -1] = y`) gives ~15% speedup vs `np.concatenate` without the overhead and memory jump of full pre-allocation.
**Action:** When shifting time buffers inplace in high-throughput hot loops with Numpy, use slicing and inplace assignment instead of `np.concatenate` to minimize reallocation.

## 2025-02-12 - Vectorize SQLite operations
**Learning:** For SQLite bulk inserts/updates in a high-iteration python loop with N+1 queries, we can pull data in batches (e.g., using `itertools.islice`) to perform `SELECT ... WHERE IN (...)` to check existence. Follow this by appending into distinct python lists, allowing us to perform batch execution via `cur.executemany(...)`.
**Action:** Replace `for` loop `execute` logic with batch query checking + `executemany` statements for large SQLite read/write scenarios.
