# 🔥 AFW Firewall - Package Repository

Advanced Firewall Management & Integrated WireGuard VPN for Linux Servers

## About AFW Firewall

AFW (Advanced Firewall) is a powerful firewall management tool designed for Linux servers. It provides both CLI and a modern interactive TUI (Terminal User Interface) for easy firewall configuration and management.

### Key Features

- **Port Management** — Open/close TCP/UDP ports and port ranges
- **Port Protection** — Rate limiting for brute-force defense
- **IP Management** — Whitelist and blacklist IP addresses
- **NAT & Port Forwarding** — PREROUTING REDIRECT and POSTROUTING masquerade
- **IGMP/Multicast** — Multicast traffic control
- **WireGuard VPN** — Integrated road-warrior VPN server with QR export & AES-GCM encrypted keys
- **Factory Reset** — Wipe rules, state, and WireGuard server (`afw reset`)
- **Docker Protection** — Rate-limit container ports & auto-reload on Docker daemon events
- **External Rules Preservation** — Intelligently preserve Docker, K8s, and libvirt rules
- **Kernel Hardening** — sysctl security parameters
- **Backup/Restore** — State snapshots for easy recovery

### Built-in Security

- WireGuard AES-GCM Key Encryption at rest (`0600` root-only key file)
- SYN flood protection with rate limiting
- Ping of death protection (ICMP rate limiting)
- Port scan detection (RST packet analysis)
- IP spoofing defense (bogon/RFC1918 blocking)
- Windows port blocking (135,137,138,139,445)
- SSH brute-force protection
- Input sanitization (no shell injection)

## Installation

> **✨ Zero-Config Setup:** AFW automatically detects your network interface and SSH port during installation. Conflicting firewalls (UFW, firewalld) are disabled on fresh install only.

### Debian / Ubuntu (APT)

```bash
curl -fsSL https://irtec.github.io/afw-repo/pubkey.asc | sudo gpg --dearmor -o /usr/share/keyrings/afw.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/afw.gpg] https://irtec.github.io/afw-repo stable main" | sudo tee /etc/apt/sources.list.d/afw.list
sudo apt update && sudo apt install afw
```

Or one-liner:
```bash
curl -fsSL https://irtec.github.io/afw-repo/setup-apt.sh | sudo bash
```

### RHEL / Fedora / CentOS (YUM/DNF)

```bash
sudo curl -fsSL https://irtec.github.io/afw-repo/afw.repo -o /etc/yum.repos.d/afw.repo
sudo rpm --import https://irtec.github.io/afw-repo/pubkey.asc
sudo dnf install afw
```

Or one-liner:
```bash
curl -fsSL https://irtec.github.io/afw-repo/setup-yum.sh | sudo bash
```

### Ubuntu PPA

```bash
sudo add-apt-repository ppa:irya31/afw
sudo apt update && sudo apt install afw
```

## Usage

> **Note:** After installation, AFW is already configured and running! No manual setup needed.

### Interactive TUI

```bash
sudo afw
```

Launches the modern interactive TUI with master-detail layout, telemetry header, rules overview, and category panels.

### CLI Commands

```bash
# Manual Reconfiguration (Optional) - if you need to change interface/SSH port
sudo afw setup --interface eth0 --ssh-port 22

# Port management
sudo afw port add tcp 80
sudo afw port add udp 53
sudo afw port add tcp 3000-4000         # range
sudo afw port add tcp 8080 -s 10.0.0.5  # IP-restricted
sudo afw port remove tcp 80
sudo afw port list

# Port protection (rate limiting)
sudo afw protect add 22 --rate 10 --per 60
sudo afw protect remove 22

# WireGuard VPN Server (Road-Warrior)
sudo afw wg install                      # Install wireguard-tools
sudo afw wg server up                    # Start WireGuard server
sudo afw wg peer add phone               # Add client device
sudo afw wg client export phone --qr     # Export config as QR code
sudo afw wg server show                  # Show status & peers
sudo afw wg server down                  # Stop server
sudo afw wg uninstall                    # Teardown server & remove tools

# IP management
sudo afw whitelist add 10.0.0.1
sudo afw whitelist remove 10.0.0.1
sudo afw blacklist add 1.2.3.4
sudo afw blacklist remove 1.2.3.4

# NAT / Masquerade & IGMP
sudo afw nat enable
sudo afw nat disable
sudo afw igmp enable 239.255.255.250 1900
sudo afw igmp disable

# Port forwarding
sudo afw forward add eth0 8080 80
sudo afw forward remove eth0 8080 80

# Firewall control
sudo afw enable
sudo afw disable
sudo afw reload
sudo afw status

# Systemd service management
sudo systemctl enable afw       # Auto-start on boot
sudo systemctl start afw        # Start firewall
sudo systemctl stop afw         # Stop firewall
sudo systemctl reload afw       # Reload rules
sudo systemctl status afw       # Check status

# Backup & Factory Reset
sudo afw backup create
sudo afw backup list
sudo afw backup restore /etc/afw/snapshots/state-20240101-120000.json
sudo afw reset                           # Wipe all rules, state & WireGuard

# Info
sudo afw rules show             # Detailed rules view
sudo afw version
```

## Upgrade

Upgrading AFW is seamless - your configuration and rules are preserved:

```bash
# Debian / Ubuntu
sudo apt update && sudo apt upgrade -y

# RHEL / Fedora / CentOS
sudo dnf upgrade -y
```

After upgrade, reload to apply new features:
```bash
sudo afw reload
```

## Resources

- [Package Repository](https://irtec.github.io/afw-repo/)
- [GPG Public Key](https://irtec.github.io/afw-repo/pubkey.asc)
- [Ubuntu PPA](https://launchpad.net/~irya31/+archive/ubuntu/afw)

## License

GPL © [irya](https://www.irya.dev)
