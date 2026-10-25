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

```

**Examples:**

* Scan all ports (default): `port_scanner 192.168.1.1`
* Scan a specific port: `port_scanner scanme.nmap.org -p 80`
* Scan a range of ports: `port_scanner 10.0.0.5 -p 1-1000`
* Scan a list of ports: `port_scanner 127.0.0.1 -p 22,80,443`

## 🧪 Test Case Scenarios

### 1. The Local Loopback Test (Verifying the Environment)

Proves your system drivers are working correctly without hitting the internet.

* **Setup:** Open a separate terminal and run `python -m http.server 8000`.
* **Command:** `port_scanner 127.0.0.1 -p 8000`
* **Expected Result:** The scanner identifies port 8000 as **Open**.

### 2. The Targeted Web Scan (Verifying DNS & Routing)

Proves the tool can resolve hostnames and route packets.

* **Command:** `port_scanner scanme.nmap.org -p 22,80,443`
* **Expected Result:** Resolves the Nmap test server IP and accurately reports the status of the SSH and HTTP/HTTPS ports.

### 3. The Firewall Check (Verifying Filtered Status)

Demonstrates the tool's ability to catch silent packet drops.

* **Command:** `port_scanner 192.168.1.250 -p 80` *(Use an IP address on your local network that does NOT exist).*
* **Expected Result:** Packets will time out. The scanner reports the port as **Filtered**.

## 🛠️ Building from Source

```bash
pip install -r requirements.txt
python -m PyInstaller --onefile src/port_scanner.py

```
## ⚠️ Note on Latency
Because this scanner uses Scapy to batch and send all packets simultaneously for maximum speed, you may notice artificially high latency times for later ports in a large scan. This is caused by **OS Queuing Delay** (buffer bloat). Packets wait in the operating system's network buffer before hitting the wire, so the reported latency reflects the total time spent in the queue rather than the true network ping.
