Target: `getsops/sops`, supplied snapshot `e39ca97b6209f9132ea40d22beb37d796060cb32`. Applied `skill/SKILL.md` alone, read-only, focusing on temporary-secret execution and nearby tests.

1. **G1 — Background execution removes its input before the child finishes**  
   **Behavior/failure handling · SUPPORTED · Medium**

   The CLI promises execution with decrypted contents in a temporary file (`cmd/sops/main.go:292–302`). `ExecWithFile` defers removal of the temporary directory (`cmd/sops/subcommand/exec/exec.go:71–75`), but background mode returns immediately after `cmd.Start()` (`119–120`). Cleanup therefore has no synchronization with the child opening the file or FIFO. A delayed reader can lose access to its input.

   **Counterevidence:** Foreground execution waits through `cmd.Run()` (`127`), and `--background` is explicitly deprecated, though still accepted and passed through (`cmd/sops/main.go:364–374`). The inspected functional tests exercise foreground execution only (`functional-tests/src/lib.rs:1565–1652`).

   **PROPOSED — NOT RUN:** Exercise background execution with a child that waits before opening `{}`, testing both FIFO and regular-file modes. Successful complete reads after the parent exits would weaken this concern.

2. **G2 — Plaintext delivery errors do not prevent command execution**  
   **Failure handling · SUPPORTED · Medium**

   Regular-file execution discards both `Write` and `Close` errors, then launches the child (`cmd/sops/subcommand/exec/exec.go:99–116`). FIFO delivery similarly discards those errors (`cmd/sops/subcommand/exec/exec_unix.go:23–32`). Consequently, a failed or partial plaintext write has no explicit propagation path; downstream automation could consume incomplete configuration while SOPS reports only the child’s outcome.

   **Counterevidence:** File creation and FIFO opening errors are handled. Foreground mode propagates child failure, and the inspected functional test checks exact FIFO output under normal conditions (`functional-tests/src/lib.rs:1587–1608`). Neither protection establishes behavior under write failure. No runtime failure was reproduced.

   **PROPOSED — NOT RUN:** Inject a regular-file write failure and verify that execution returns a delivery error without launching the child. Separately check FIFO write-error propagation.

Inspection used **12 inspection calls**, including three rejected argument attempts; successful operations were bounded reads, searches, and listing. Inspected the skill, execution implementations/tests, CLI wiring, selected configuration and publication code, and selected functional tests. No delegation, edits, network access, or credential inspection occurred. **Project code, tests, and builds executed: NONE.**

Limits: supplied tracked UTF-8 text only; binary assets and Git metadata unavailable. Snapshot identity was user-supplied, and uncommitted state was not independently established. Cryptographic correctness, key-provider behavior, and the broader test suite were not assessed. **Two supported findings; runtime consequences remain unverified.**