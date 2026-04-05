# ☠️ MITM Tactical Suite (ARP & DNS Spoofing)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)

**MITM Tactical Suite** is an advanced, modular toolkit designed for executing Man-in-the-Middle (MITM) simulations. It combines Layer 2 routing manipulation (ARP Cache Poisoning) with Layer 7 payload interception (DNS Hijacking).

This suite is explicitly built to help cybersecurity professionals, penetration testers, and network administrators evaluate local network resilience against credential harvesting and redirection attacks.

> **⚠️ Disclaimer:** This toolset was created for **Educational Purposes and Proof of Concept (PoC) only**. Do not execute these scripts on any network where you do not have explicit, written permission. The author is not responsible for any misuse, damage, or legal consequences caused by this program.

## 🌟 Features

- **Modular Architecture:** Run ARP poisoning and DNS spoofing independently or simultaneously.
- **Automated OS Configuration:** Automatically enables/disables Linux kernel IP forwarding during ARP execution.
- **Dynamic CLI Interface:** Built with `argparse` for seamless, hacker-friendly command-line execution.
- **Layer 7 DNS Hijacking:** Intercepts UDP/53 queries and injects rogue A-records to redirect targets.
- **Safe Auto-Restoration:** Safely restores the victim's ARP table upon exiting (CTRL+C) to prevent network Denial of Service (DoS).

## 🗂️ Modules Overview

1. `arppoison.py` : Acts as the malicious router. Intercepts traffic between the victim and the gateway.
2. `dns_spoofer.py`: Acts as the malicious resolver. Listens for specific domain requests and replies with a controlled Rogue IP (e.g., a phishing server).

## ⚙️ Prerequisites

This tool requires **Linux** (Kali Linux recommended) for low-level packet manipulation and **Python 3**.

1. Clone this repository:
   ```bash
   git clone [https://github.com/](https://github.com/)[USERNAME_GITHUB_ANDA]/MITM-Tactical-Suite.git
   cd MITM-Tactical-Suite
   ```
2. Install required dependencies:
pip install -r requirements.txt

🚀 Usage: Kill Chain Simulation
To execute a full MITM redirection attack, you need to run both modules in tandem. Open two separate terminal windows.

Make sure you have root privileges (sudo), as Scapy requires low-level network socket access.

Step 1: Establish the MITM Position (Terminal 1)
First, place your machine between the victim and the gateway using the ARP module.

chmod +x arppoison.py
sudo ./arppoison.py -t <VICTIM_IP> -g <GATEWAY_IP>

Step 2: Execute DNS Hijacking (Terminal 2)
While the ARP script is running, execute the DNS spoofer to redirect a specific domain to your rogue server (e.g., an Apache server hosting a fake login page).

chmod +x dns_spoofer.py
sudo ./dns_spoofer.py -d <TARGET_DOMAIN> -r <ROGUE_IP>

Example: sudo ./dns_spoofer.py -d facebook.com -r 192.168.1.50

(When the victim attempts to browse facebook.com, they will be transparently redirected to 192.168.1.50)

🛡️ Mitigation
To protect networks from this suite, administrators should implement:

Dynamic ARP Inspection (DAI) and DHCP Snooping on enterprise switches.

DNSSEC (Domain Name System Security Extensions) to validate DNS responses cryptographically.

Static ARP entries for critical infrastructure components.

Developed by Haykal Azriel Priatama as part of Telkom University.
# MITM-Tactical-Suite
