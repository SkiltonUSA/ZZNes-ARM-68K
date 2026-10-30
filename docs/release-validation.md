# ZZNES 0.8.7 Beta validation

Matching 0.8.7-dev launcher/player binaries from the installed and tested Native
columns build. [Executable hashes](release-build.json).

| Asset | Bytes | SHA256 |
| --- | ---: | --- |
| `ZZNES-0.8.7-dev-beta-amipkg.lha` | 1392021 | `08ec5281282bf3b670501b208e944f9b5907e90630297b325dc0e827b9f4c872` |
| `ZZNES-0.8.7-dev-beta.zip` | 521740 | `3c2af263bec8640c5b66795a323ca9d3a1cbee8db689cb3d34d1a289a0d98a61` |
| `ZZNES-release.json` | 981 | `8b09120060d05d3233c09e4e8a5a9a60bb13f6dc53be6084352cdb4d9280ca58` |

## Checks and limits

Native sanitizer, relocated ARM pixel/reference, legacy settings and compact
MUI tests pass. Super Mario World hardware checks cover fullscreen and 3×
windows: four exact pixel readbacks in each 180-frame verification run, followed
by 600-frame normal runs with complete PCM delivery and zero starvation
transitions. Clean register/cache/MMU restoration and owned-memory release pass.
Verification stalls audio; it is not a performance measurement. The exact
reported scrolling symptom still needs visual confirmation.

[Native-column evidence](native-columns.md) records the runs and limits.
[Previous audio release validation](output-quality-release-validation.md)
remains historical evidence for the unchanged audio code, not a rerun on 0.8.7.

The refreshed ZIP and offline amipkg installer pass payload byte-equivalence,
executable and member hashes, Ed25519 signature verification, corrupt-catalogue
rejection, dependency-first recipe checks, icons and private-data exclusions.
The packaging framework is unchanged. The 0.8.7 binaries were installed and
checked on hardware; this new installer archive was validated locally, not
rerun on the Amiga. Existing user preferences are preserved; select
Display → Scaling → Native columns and save settings to use the new mode.
