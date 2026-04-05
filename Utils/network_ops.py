import scapy.all as scapy
import sys
import time
from utils.logger import logger

def toggle_ip_forwarding(enable=True):
    try:
        with open('/proc/sys/net/ipv4/ip_forward', 'w') as f:
            if enable:
                f.write('1')
                logger.info("IP Forwarding diaktifkan otomatis.")
            else:
                f.write('0')
                logger.info("IP Forwarding dinonaktifkan.")
    except PermissionError:
        logger.error("Akses ditolak! Jalankan script ini sebagai root (sudo).")
        sys.exit(1)

def get_mac(ip, retries=3):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    for attempt in range(retries):
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        if answered_list:
            return answered_list[0][1].hwsrc
        time.sleep(1)
    return None