# 🔥 AFW Firewall v2.3.0

**Advanced Firewall Management & Integrated WireGuard VPN for Linux Servers**

## Features

- Port Management — Open/close TCP/UDP ports, ranges, and IP-restricted rules
- Port Protection — Rate limiting for brute-force defense
- IP Management — Whitelist and blacklist IP addresses
- NAT & Port Forwarding — PREROUTING REDIRECT and POSTROUTING masquerade
- IGMP/Multicast — Multicast traffic control
- WireGuard VPN — Integrated road-warrior VPN with QR export & AES-GCM encrypted keys
- IPv6 Filtering — Auto-detects host IPv6 and filters it with ip6tables
- Factory Reset — Wipe rules, state, and WireGuard configuration (afw reset)
- Docker Protection — Rate-limit container ports & auto-reload on Docker events
- External Rules Preservation — Keep Docker/K8s/libvirt rules intact
- Kernel Hardening — sysctl security parameters
- Automatic Snapshots — State is backed up before each change, pruned to a retention limit

## Built-in Security

- WireGuard AES-GCM Key Encryption at rest (0600 root-only key file)
- IPv6 filtering with a full ip6tables ruleset (automatic on IPv6 hosts)
- SYN flood protection with rate limiting
- Ping of death protection (ICMP rate limiting)
- Port scan detection (RST packet analysis)
- IP spoofing defense (bogon/reserved-range blocking)
- Windows port blocking (135,137,138,139,445)
- SSH brute-force protection
- Input sanitization (no shell injection)

## Installation

**✨ Zero-Config Setup:** AFW automatically detects your network interface and SSH port during installation. Conflicting firewalls (UFW, firewalld) are disabled on fresh install only.

### Debian / Ubuntu (APT)

```bash

curl -fsSL https://irtec.github.io/afw-repo/pubkey.asc | sudo gpg --dearmor -o /usr/share/keyrings/afw.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/afw.gpg] https://irtec.github.io/afw-repo stable main" | sudo tee /etc/apt/sources.list.d/afw.list
sudo apt update && sudo apt install afw
```

### RHEL / Fedora / CentOS (YUM/DNF)

```bash

sudo curl -fsSL https://irtec.github.io/afw-repo/afw.repo -o /etc/yum.repos.d/afw.repo
sudo rpm --import https://irtec.github.io/afw-repo/pubkey.asc
sudo dnf install afw
```

### Ubuntu PPA

```bash

sudo add-apt-repository ppa:irya31/afw
sudo apt update && sudo apt install afw
```

*After installation, your firewall is automatically configured and active!*

## Quick Start

After installation, AFW is already configured and running! No manual setup needed.

## IPv6 Filtering

IPv6 is filtered by default whenever the host actually uses it, so it can never become a bypass around your IPv4 rules.

- **auto** (default) — filter IPv6 only if the host has a global IPv6 address
- **on** — always filter IPv6
- **off** — IPv4 only

```bash

sudo afw config                        # show current mode and the decision
sudo afw config set ipv6_mode auto     # auto | on | off
sudo afw reload                        # apply
```

### Interactive TUI

```bash
sudo afw
```

Launches the modern interactive TUI with master-detail layout, telemetry header, rules overview, and category panels.

### Manual Reconfiguration (Optional)

```bash

# Only needed on a fresh, unconfigured install — a configured
# install is preserved and  is a safe no-op.
sudo afw setup --interface eth0 --ssh-port 22
```

### CLI Examples

```bash

# Port management
sudo afw port tcp add 80
sudo afw port udp add 53
sudo afw port tcp range 3000 4000      # range
sudo afw port tcp add 8080 -s 10.0.0.5  # IP-restricted
sudo afw port tcp remove 80
sudo afw port list

# Port protection (rate limiting)
sudo afw protect add 22 --rate 10 --per 60
sudo afw protect remove 22

# WireGuard VPN Server
sudo afw wg install                      # Install wireguard-tools
sudo afw wg server up                    # Start WireGuard server
sudo afw wg peer add phone               # Add client device
sudo afw wg client export phone --qr     # Export config as QR code
sudo afw wg server show                  # Show status & peers
sudo afw wg server down                  # Stop server
sudo afw wg uninstall                    # Teardown server & remove tools

# IP management
sudo afw whitelist add 10.0.0.1
sudo afw blacklist add 1.2.3.4

# NAT / Masquerade & IGMP
sudo afw nat enable
sudo afw nat disable
sudo afw igmp enable 239.255.255.250 1900
sudo afw igmp disable

# Port forwarding
sudo afw forward add eth0 8080 80

# Firewall control
sudo afw enable
sudo afw disable
sudo afw reload
sudo afw status

# Settings (IPv6 filtering mode)
sudo afw config
sudo afw config set ipv6_mode auto

# Factory reset
sudo afw reset                           # Wipe all rules, state & WireGuard
```

## Systemd Service

```bash

sudo systemctl enable afw       # Auto-start on boot
sudo systemctl start afw        # Start firewall
sudo systemctl stop afw         # Stop firewall
sudo systemctl reload afw       # Reload rules
sudo systemctl status afw       # Check status
```

## Upgrade

```bash

# APT (Debian/Ubuntu)
sudo apt update && sudo apt upgrade -y

# DNF (RHEL/Fedora/CentOS)
sudo dnf upgrade -y
```

*Config and rules are preserved. Reload after upgrade: `sudo afw reload`*

## Resources

- [GPG Public Key](https://irtec.github.io/afw-repo/pubkey.asc)
- [Package Repository](https://irtec.github.io/afw-repo/)
- [Ubuntu PPA](https://launchpad.net/~irya31/+archive/ubuntu/afw)

## License

**GNU General Public License v3.0 or later** (GPL-3.0-or-later) — Copyright © 2024–2026 [IRTech](https://www.irya.dev).
