*Read this in other languages: [Français](README.fr.md)*

# Custom TCP SYN Port Scanner 🔍

A lightweight, high-speed TCP SYN (Stealth) port scanner built with Python and Scapy. 

Unlike standard full-connect scanners, this tool crafts raw IP and TCP packets to initiate a half-open connection (SYN scan). This allows it to quickly identify Open, Closed, and Filtered (firewalled) ports without completing the three-way handshake. It generates automated, timestamped text reports for every scan in the current working directory.

## 🚀 Features
*   **Stealth Scanning:** Uses raw SYN packets to avoid full TCP connections.
*   **Smart Categorization:** Differentiates between closed ports (RST) and firewalled/filtered ports (ICMP drops/timeouts).
*   **Dynamic Reporting:** Automatically saves results with timestamped filenames (e.g., `scan_127.0.0.1_all_20261025_214356.txt`).
*   **Standalone Binaries:** Pre-compiled for Windows (`.exe`) and Debian/Ubuntu Linux (no Python installation required).

## ⚙️ Prerequisites & Setup

Because this tool injects raw packets directly onto the network card, it requires low-level OS permissions.

### 🪟 Windows Users
1. Download `port_scanner.exe` from the Releases page.
2. **Install Npcap:** You must install [Npcap](https://npcap.com/). During installation, **you must check the box for "Support loopback traffic"**, otherwise the scanner will fail on local tests.
3. **Run as Administrator:** Open your Command Prompt or PowerShell as an Administrator to execute the scanner.

### 🐧 Linux (Debian/Ubuntu) Users
1. Download the `port_scanner` binary from the Releases page.
2. Grant execution permissions: `chmod +x port_scanner`
3. **Run as Root:** You must use `sudo` to run the tool so the Linux kernel allows raw socket access.

## 💻 Usage

**Syntax:**
```bash
port_scanner <target_ip_or_hostname> [-p <ports>]
