# Local build artifacts

This small publisher stores one immutable byte artifact per generation. A
single build process owns the directory; readers and publishers do not run
concurrently. It is used for generated configuration bundles that another
process consumes after the builder exits.

`ArtifactStore(root)` opens the directory and recovers leftovers from an
interrupted run. `publish(bytes)` creates a generation and returns its integer
ID. `read()` returns the current artifact, or `None` before the first commit.
`generations()` lists complete on-disk generations for diagnostics, including
ones that have not been published.

Publication commits only when the staged `CURRENT.next` pointer replaces
`CURRENT`. That replacement is atomic on the supported local filesystem. An
exception or interruption before replacement must never make that generation
visible through `read()`, including after reopening the store. A complete
generation and its matching checksum alone do not mean it was committed.
Reopening must preserve the last committed value, or the initial empty state.

The process may leave staging files behind after a failed publication.
Recovery removes pointer staging files. Generations are kept for diagnosis;
garbage collection, concurrent access, power-loss durability, and externally
corrupted directories are outside this utility's contract. Only this utility
writes the directory, and artifact bytes are opaque.

Run the public checks with `python -m unittest discover -v`.
