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
# MITM-Tactical-Suite
