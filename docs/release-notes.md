# ZZNES 0.8.10 Beta

Application/launcher version: **0.8.10-dev**. AmiPkg version: **0.8.10-dev**.

## Changes

- iNES trainer loading on the eight supported mappers, preserving existing save compatibility.
- Matching rebuilt launcher and player versions, with isolated build records.
- AmiPkg includes the current README, credits and licence documents.

Trainer execution and state replay cover eight mapper fixtures. This does not add mapper IDs or guarantee every modified ROM works. Battery cartridges, NES 2.0 and UNIF remain unsupported.

## Installation

Extract the LHA and open Install. Choose a writable destination. Close the emulator
before updating; existing settings, ROMs and saves are preserved. MUI and AHI
requirements are checked. Clock controls require the optional clock service;
normal emulation does not. No firmware or clock change happens automatically.

## Validation

[Build identities, model tests and physical checks](validation/release-0.8.10/README.md).
Listening acceptance is separate from automated delivery and clean-exit checks.
