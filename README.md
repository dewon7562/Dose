by @dewon7562
---

### Setup and Running Instructions

1. **Prepare Kali Linux VM**:
   - Ensure Kali Linux 2023.x or later is updated: `sudo apt update && sudo apt upgrade`.
   - Install Python 3: `sudo apt install python3 python3-pip`.
   - Install `libpcap-dev` for `scapy`: `sudo apt install libpcap-dev`.

2. **Clone and Set Up**:
   ```bash
   git clone https://github.com/dewon7562/Dose/ 
   cd dose
   pip3 install -r requirements.txt
   python3 setup.py install
