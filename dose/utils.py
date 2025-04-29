import re
import socket
import random
import urllib.parse

def validate_target(target, return_ip=False):
    # Handle URLs
    if target.startswith("http"):
        parsed = urllib.parse.urlparse(target)
        hostname = parsed.hostname
    else:
        hostname = target
    # Validate IP
    ip_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if re.match(ip_pattern, hostname):
        return hostname, hostname
    # Resolve domain to IP
    try:
        ip = socket.gethostbyname(hostname)
        return hostname, ip
    except socket.gaierror:
        return None, None

def get_random_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    return random.choice(agents)
