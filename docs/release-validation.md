# ZZNES 0.7.4 Beta packaging validation

The release retains the physically tested **0.7.4-dev** executables byte-for-byte.
Packaging does not change emulation code or establish a new performance result.
Expected executable hashes and build selection: [release-build.json](release-build.json).

| Asset | Bytes | SHA256 |
| --- | ---: | --- |
| `ZZNES-0.7.4-dev-beta.zip` | 508,640 | `dbf9d4467ae1f9063ae455dd1e158172608d1c552549febafd98d92560954994` |
| `ZZNES-0.7.4-dev-beta-amipkg.lha` | 1,365,575 | `cbe8b0e727d83cfee7f2270d73c6b4d9bea473f8c5c8741d01d6262eb28ccff1` |
| `ZZNES-release.json` | 981 | `897ae30f37d166fbd79d97eee217da21fef159bfc5aa51695f4567a711b860f7` |

## Checks performed

- Cross-compiled the new installer helper and patched amipkg client for 68020.
- Ran the patched amipkg portable-core test suite successfully.
- Extracted both LHA layers with 7-Zip; every payload file matched the manual ZIP.
- Verified every inner SHA256 and each executable against its physical-test record.
- Verified the signed catalogue with the Python signer and the same C verifier used by the Amiga helper.
- Confirmed changed catalogues and empty keys fail authentication.
- Checked catalogue readability, prerequisite-before-copy order, destination assigns, scanline post-install action and Workbench icon types.
- Checked all files for excluded ROM/save/config/signing-key payloads.
- Passed current source/artifact verification and packaging/documentation whitespace checks.
- Preserved imported upstream/core bytes and unified-patch context, including inherited whitespace.

The original upstream C verification fixture expects its official catalogue and
was skipped when that catalogue was absent; the new installer test explicitly
checks our actual catalogue using the C verifier, so that path was not left untested.

These are release and host checks. The new complete offline wrapper has **not**
been installed on the physical Amiga in this packaging session. Earlier isolated
amipkg/scanline installations passed; current game execution evidence is in
`amiga/records/2026-10-19/cartridge/`.
The installer dependency checks are compiled for AmigaOS; host validation does not
prove that a different machine has those dependencies or compatible firmware.

Re-run: `python3 scripts/test_installer.py .context/release` (requires 7zz and a host C compiler).
