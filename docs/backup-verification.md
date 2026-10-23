# Standalone backup verification — 9 October 2026

All checks ran on the Mac without connecting to, deploying to or launching
anything on the Amiga. Existing physical evidence is preserved separately.

- `make test` with the pinned cross-toolchain and the active local Podman
  connection: rebuilt ZZFceux and ZZFceuxBench successfully.
- Both rebuilt Amiga executables are **byte-for-byte identical** to their saved
  hardware-tested originals, including ZZFceux MD5
  `ce77a7b5fd6a453d50a9a697b86d3ae9`.
- Original generated mapper-0 ROM: 120 frames with and without scripted input,
  native versus ASan/selected UBSan adapter output identical.
- Four ELF rejection tests, 200,000 triple-slot handoffs, 12,816 presentation
  mapping cases, 16,384 allocation alignments, and actual audio-worker checks
  (1,200 ordered blocks plus failure, cancel and cleanup paths) passed.
- Unicorn 2.1.4 Cortex-A9 instruction model: six generated-ROM frames matched
  native output; aligned accesses, all four display formats, both-end challenges,
  guard/padding bytes, cancellation and mapping revocation passed. Six frames
  do not exercise the script's later Start-button window. This is not a new
  physical cache/MMU test.
- `make mesen` rebuilt the current audio-Process candidate and passed its built-in
  native frame/controller/cancel/rejected-mapper checks. That executable is also
  byte-for-byte identical to its original workspace artifact. This does not
  reproduce the older installed baseline or make the candidate the default.
- Selected source/evidence files were audited for excluded ROM/image/archive
  types, NES binary or long hex payloads, private keys and common credential
  patterns. No findings. Generated files remain ignored.

[Build/test logs](backup-checks/), [binary comparisons](backup-checks/binary-comparison.json)
and [source provenance](backup-origin.json) preserve the details. Historical
absolute paths in these logs are evidence, not required build configuration.
The original build manifests precede final documentation/user-acceptance edits;
current standalone manifests and the repository snapshot record those later files.

The backup includes current sources and selected earlier evidence, not the
original repository's entire Git history or the Amiga's disk contents. ROMs,
firmware, commercial software, secrets and toolchain installations are excluded.
