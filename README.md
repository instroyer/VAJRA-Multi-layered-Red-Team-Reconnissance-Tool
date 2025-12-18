# VAJRA

> VAJRA is a Multi-layered Red Team Reconnisance tool implemented in Python.

This repository contains an interactive tool that orchestrates several reconnaissance modules (amass, subfinder, nmap, whois, httpx, screenshot) and engine utilities to run scans and produce reports.

## Project structure

- `vajra.py` - entry point for the application (run this to start the interactive menu).
- `config.py` - global configuration and settings.
- `requirements.txt` - Python dependencies.
- `Engine/` - core runtime, utilities and reporting code (menu, runtime, report, file ops, logging, etc.).
- `Modules/` - individual scanning/recon modules (amass, subfinder, nmap, whois, httpx, screenshot, ...).
- `Results/` - output directory where scan results are stored.

## Requirements

- Python 3.8+ (recommended)
- Dependencies listed in `requirements.txt`.

## Installation

Create and activate a virtual environment, then install dependencies:

```powershell
gitclone https://github.com/instroyer/VAJRA.git
```

## Usage

Start the tool from the repository root:

```powershell
python3 vajra.py
```

The application provides an interactive menu (see `Engine/menu.py`) to run modules and collect results. Configuration is read from `config.py`.

## Modules

The `Modules/` folder contains integration wrappers for common recon tools and scanners. Example modules included:

- `whois` — domain WHOIS lookups.
- `amass` — subdomain enumeration via Amass.
- `subfinder` — subdomain finding.
- `nmap` — port/service scanning and OS detection.
- `httpx` — HTTP probing for responsive hosts.
- `screenshot` — webpage screenshotting.

Each module is designed for orchestration logic.

## Results & Reports

Scan outputs are written to the `Results/` directory. The engine includes reporting utilities in `Engine/report.py` and `Engine/finaljson.py` for generating structured outputs.

## Contributing

Contributions are welcome. Please fork the repository, create a branch for your feature or bugfix, and open a pull request.

Suggested small improvements:
- Add unit tests for core Engine functions.
- Add clearer CLI flags (non-interactive runs).

## License

This project is provided under the MIT License. (Add your LICENSE file as needed.)

## Notes

- This README is a lightweight overview. For module-specific usage, inspect the corresponding files in `Modules/` and the engine code in `Engine/`.
- If a module requires external binaries (e.g., `amass`, `nmap`), ensure they are installed and available on your PATH.
