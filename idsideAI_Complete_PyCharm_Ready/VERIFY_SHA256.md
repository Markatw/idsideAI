# Master Green App 040925 — Integrity Verification Guide

This archive includes a file: `HASHES_SHA256.json`  
It contains the SHA-256 hash for every file in the release.

## How to verify

### Linux / macOS (Terminal)
```bash
shasum -a 256 <filename>
# or
openssl dgst -sha256 <filename>
```
Compare the output with the value in `HASHES_SHA256.json`.

### Windows (PowerShell)
```powershell
Get-FileHash <filename> -Algorithm SHA256
```
Compare the `Hash` value with the value in `HASHES_SHA256.json`.

### Example
Suppose `reports/S30_DeepApp_Imports_FINAL.csv` shows this in the manifest:
```json
"reports/S30_DeepApp_Imports_FINAL.csv": "abc123..."
```
Then run:
```bash
shasum -a 256 reports/S30_DeepApp_Imports_FINAL.csv
```
The output should match `abc123...` exactly.

## Purpose
This guarantees:
- Files are unchanged since packaging
- Tampering can be detected immediately
- Board / CI can prove provenance of the release

---
Release: **idsideAI_Master_Green_App_040925**
