<h1 align="center">
  <br>
  🦅 KESTREL
  <br>
</h1>

<h4 align="center">Multi-layered Reconnaissance Tool</h4>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#structure">Structure</a> •
  <a href="#disclaimer">Disclaimer</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python3-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Linux-lightgrey?style=for-the-badge&logo=linux" alt="Platform">
  <img src="https://img.shields.io/badge/Focus-Reconnaissance-red?style=for-the-badge" alt="Focus">
</p>

---

<p align="center">
  <b>KESTREL</b> is an advanced, modular reconnaissance tool designed for red teamers and penetration testers. It automates the intelligence gathering process by orchestrating specific industry-standard tools into a unified, powerful pipeline.
</p>

## 🚀 Features

*   **🔍 Multi-Layered Scan:** Seamlessly combines Whois, Subdomain Enumeration, Web Service Discovery, Port Scanning, and Visual Reconnaissance.
*   **🧩 Modular Architecture:** Built with extensibility in mind. Easily add or modify modules (located in `Modules/`).
*   **⏯️ Runtime Control:** Full control over the execution flow. **Pause**, **Resume**, **Skip**, or **Quit** steps in real-time.
*   **📦 Automated Dependencies:** Smart detection system that checks for and installs missing external tools (Nmap, Amass, Subfinder, etc.).
*   **📊 Professional Reporting:** Generates beautiful, interactive HTML reports with detailed findings and visualizations.
*   **📂 Batch Processing:** Support for file inputs (`@targets.txt`) to process multiple domains in a single run.

## 🛠️ Integrated Tools

| Tool | Purpose |
| :--- | :--- |
| **Whois** | Domain registration intelligence & ownership details. |
| **Dig** | DNS Record enumeration (A, MX, NS, TXT, SOA). |
| **Subfinder** | Fast passive subdomain enumeration. |
| **Amass** | Deep, comprehensive subdomain mapping. |
| **HTTPX-Toolkit** | Active probing to identify live web servers. |
| **Nmap** | Advanced port scanning & service version detection. |
| **Eyewitness** | Visual reconnaissance (Automated Screenshots). |

## 📥 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/KESTREL.git

# Navigate to the directory
cd KESTREL

# Install Python dependencies
pip install -r requirements.txt
```

> **Note:** KESTREL will automatically attempt to install external tools (like Subfinder, Amass) if they are missing from your system path.

## ⚡ Usage

Simply run the main script to start the interactive wizard:

```bash
python3 kestrel.py
```

### 🎯 Scan Modes

| Mode | Description |
| :--- | :--- |
| **0. Run All** | 🚀 **Recommended.** Executes the full pipeline (Whois -> Subdomains -> Live Check -> Port Scan -> Screenshot). |
| **1. Whois** | Basic domain registration info. |
| **2. Dig** | DNS record analysis (A, MX, NS, TXT). |
| **3. Subfinder** | Passive subdomain gathering only. |
| **4. Amass** | Deep subdomain enumeration only. |
| **5. HTTPX-Toolkit** | Check for live web servers. |
| **6. Nmap** | Network mapping with various intensity levels. |
| **7. Screenshot** | Visual evidence capture. |

## 💡 Interactive Help Menu

<<<<<<< HEAD
KESTREL has a built-in help system (`000`) and a runtime controller (`00`) to manage your scans dynamically.

### 🎮 Runtime Control (New!)
While a scan is running, you can pause, resume, or skip modules without killing the entire process.
=======
- `whois` — domain WHOIS lookups.
- `amass` — subdomain enumeration via Amass.
- `subfinder` — subdomain finding.
- `nmap` — port/service scanning and OS detection.
- `httpx` — HTTP probing for responsive hosts.
- `screenshot` — webpage screenshotting.

Each module is designed for orchestration logic.
>>>>>>> 6f43303beea856ad680ff4d7a5b606bf3e9e1298

1.  **Trigger:** Type `00` and hit **ENTER** while a module is running.
2.  **Actions:**
    *   `p` → **Pause** the current module.
    *   `r` → **Resume** the paused module.
    *   `s` → **Skip** the current module (moves to the next one).
    *   `q` → **Quit** KESTREL entirely.

### ⌨️ Input Formats
KESTREL supports various target inputs:
*   **Domain:** `target.com`
*   **Subdomain:** `sub.target.com`
*   **IP Address:** `192.168.1.1`
*   **CIDR Range:** `192.168.1.0/24`
*   **File Input:** `@list.txt` (Reads targets line-by-line)

### 🧩 Module Selection
You can run a single module, a combination, or the full suite:
*   `0` : Run everything.
*   `1` : Run only Whois.
*   `1 2 5` : Run Whois, Dig, and HTTPX in order.
*   `000` : View the full **Help Menu** inside the tool.

## ⚠️ Disclaimer

This tool is created for **educational purposes** and **authorized security testing** only. The developers are not responsible for any misuse or damage caused by this tool. Always obtain proper authorization before scanning any network.

---
<p align="center">Made with ❤️ for Red Teams</p>
