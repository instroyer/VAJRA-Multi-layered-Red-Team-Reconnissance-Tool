<div align="center">

<img src="Resources/logo.png" alt="KESTREL Logo" width="150"/>

# KESTREL
### Multi-layered Reconnaissance Tool

*Advanced, modular, CLI-based reconnaissance framework for red teams.*

[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg?style=flat-square)](#)
[![Platform](https://img.shields.io/badge/Platform-Linux-orange.svg?style=flat-square)](#)
[![Interface](https://img.shields.io/badge/Interface-CLI-success.svg?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg?style=flat-square)](#)

Built by **Yash Javiya**
</div>

---

<div align="center">

<a href="#overview">Overview</a> &nbsp;•&nbsp;
<a href="#core-features">Features</a> &nbsp;•&nbsp;
<a href="#integrated-arsenal">Integrated Arsenal</a> &nbsp;•&nbsp;
<a href="#installation--setup">Installation</a> &nbsp;•&nbsp;
<a href="#usage-guide">Usage</a>
<br>
<a href="#runtime-control">Runtime Control</a> &nbsp;•&nbsp;
<a href="#report-output">Reports</a> &nbsp;•&nbsp;
<a href="#support-the-project">Support</a> &nbsp;•&nbsp;
<a href="#warning--disclaimer">Disclaimer</a>

</div>

## 📋 Overview

**KESTREL** is an advanced, modular reconnaissance automation engine designed for red teamers and penetration testers. Unlike simple wrapper scripts, KESTREL orchestrates a multi-stage intelligence gathering pipeline—from passive OSINT to active scanning—within a single, interactive CLI environment.

It eliminates the need for manual tool chaining by handling dependencies, directory structures, and report generation automatically, allowing you to focus on analyzing the results rather than running commands.

---

## ⚡ Core Features

### 🛠️ Automation & Architecture
*   **Multi-Layered Pipeline**: Seamlessly chains Whois → Subdomains → Live Host Probing → Port Scanning → Screenshots.
*   **Modular Design**: A plugin-based architecture (located in `Modules/`) allowing for easy extensibility.
*   **Smart Dependencies**: Auto-detects and installs missing external binaries (Nmap, Amass, Subfinder) on first run.
*   **Batch Processing**: Supports `@targets.txt` input to process hundreds of domains sequentially.

### 🎮 Execution Control
*   **Interactive Menu**: A robust CLI menu system for selecting specific modules or running full automation.
*   **Runtime Interception**: Unique feature allowing users to **Skip (`s`)** or **Quit (`q`)** specific modules manually **while they are running**, without killing the entire session.

### 📊 Intelligence Reporting
*   **Professional HTML Reports**: Generates interactive, dashboard-style HTML reports containing all findings.
*   **Visual Evidence**: Embeds automated screenshots of live web services directly into the report.

---

## 🛠️ Integrated Arsenal

KESTREL unifies the following industry-standard tools into its workflow:



### 🤖 Automation (Run All)
| Tool | Purpose |
|------|---------|
| **Kestrel Engine** | Custom Python core for multi-threaded module orchestration. |
| **Runtime Control** | Real-time process management (Skip/Quit) without session kill. |

### 📡 Info Gathering
| Tool | Purpose |
|------|---------|
| **Whois** | Domain registration intelligence & ownership details. |
| **Dig** | DNS Record enumeration (A, MX, NS, TXT, SOA). |

### 🌐 Subdomain Enumeration
| Tool | Purpose |
|------|---------|
| **Subfinder** | Fast passive subdomain enumeration using online sources. |
| **Amass** | Deep, comprehensive subdomain mapping and OSINT. |

### 🟢 Live Subdomains
| Tool | Purpose |
|------|---------|
| **HTTPX-Toolkit** | Active probing to identify live web servers and status codes. |

### 🔍 Port Scanning
| Tool | Purpose |
|------|---------|
| **Nmap** | Advanced port scanning & service version detection. |

### 📸 Web Screenshots
| Tool | Purpose |
|------|---------|
| **Eyewitness** | Automated visual reconnaissance of web applications. |



---

## ⚙️ Installation & Setup

### 1. Prerequisites
*   **OS**: Linux (Kali, Debian, Ubuntu recommended)
*   **Python**: Version 3.8+

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/instroyer/KESTREL.git

# Navigate to directory
cd KESTREL

# Install dependencies
pip install -r requirements.txt
```

> **Note**: KESTREL will automatically attempt to install external tools (like Subfinder, Amass) if they are missing from your system path during the first run.

---

## 📖 Usage Guide

Simply run the main script to start the interactive wizard:

```bash
python3 kestrel.py
```

### 🎯 Scan Modes (Menu)

| Option | Mode | Description |
|:------:|------|-------------|
| **0** | **Run All** | 🚀 **Recommended.** Executes the full pipeline (Whois → Visual). |
| **1** | **Whois** | Basic domain registration info. |
| **2** | **Dig** | DNS record analysis (A, MX, NS, TXT). |
| **3** | **Subfinder** | Passive subdomain gathering only. |
| **4** | **Amass** | Deep subdomain enumeration only. |
| **5** | **HTTPX** | Check for live web servers. |
| **6** | **Nmap** | Network mapping with various intensity levels. |
| **7** | **Visual** | Eyewitness Screenshot capture. |

### 🧩 Advanced Selection
You can run combinations of modules by entering numbers separated by spaces:
*   `1 2 5` : Runs Whois, Dig, and HTTPX sequentially.
*   `3 5` : Runs Subfinder and then probes for live hosts.

---

## 🎮 Runtime Control

KESTREL features a unique runtime controller that lets you manage scans dynamically.

**Trigger**: Type `00` and hit `ENTER` **while a module is running**.

| Command | Action |
|:-------:|--------|
| `s` | **Skip**: Aborts the current module (e.g., stops a long Amass scan) and moves instantly to the next step. |
| `q` | **Quit**: Safely terminates the entire KESTREL session. |

---

## 📂 Report Output

All results are organized automatically by target:

```text
Results/
└── example.com/
    ├── reports/           # Final HTML Reports
    ├── scans/             # Raw tool logs (nmap.xml, amass.txt)
    └── screenshots/       # Eyewitness captures
```

---

## ❤️ Support the Project

If you find KESTREL useful for your red team operations, please consider supporting:

- ⭐ **Star** the repository on GitHub.
- ☕ **Tip the Developer**: [Buy me a Coffee on Ko-fi](https://ko-fi.com/yashjaviya)!

---

## ⚠️ Warning & Disclaimer

**KESTREL is a powerful reconnaissance tool designed for authorized security testing ONLY.**

By downloading and using this software, you agree that:
- ✅ You will use it only on systems you own or have explicit written permission to test.
- ❌ The developers assume **NO LIABILITY** for misuse or damage caused by this software.
- ❌ Unauthorized access to computer systems is illegal.

---

<div align="center">

**Built for Red Teams, by Yash Javiya**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/yash--javiya/)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support-FF5E5B.svg?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/yashjaviya)

</div>
