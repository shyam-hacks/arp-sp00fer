# ARP Spoofer

A Python script for educational purposes that performs an ARP spoofing (ARP poisoning) attack on a local network.

It sends forged ARP replies to redirect traffic between a target device and the gateway through your machine, enabling a Man-in-the-Middle (MITM) position.

---

## Features

- Resolves MAC addresses of target and gateway
- Enables IP forwarding to maintain network connectivity
- Sends spoofed ARP packets continuously
- Restores ARP tables on exit (Ctrl+C)
- Lightweight and uses Scapy

---

## Usage

```bash
sudo python3 arpspoof.py <target_ip> <gateway_ip>
