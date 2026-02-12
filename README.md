# 🔥 AFW Firewall - Package Repository

Advanced Firewall Management for Linux Servers

## About AFW Firewall

AFW (Advanced Firewall) is a powerful firewall management tool designed for Linux servers. It provides both CLI and TUI (Terminal User Interface) for easy firewall configuration and management.

### Key Features

- **Port Management** — Open/close TCP/UDP ports and port ranges
- **Port Protection** — Rate limiting for brute-force defense
- **IP Management** — Whitelist and blacklist IP addresses
- **NAT & Port Forwarding** — PREROUTING REDIRECT and POSTROUTING masquerade
- **IGMP/Multicast** — Multicast traffic control
- **Kernel Hardening** — sysctl security parameters
- **Backup/Restore** — State snapshots for easy recovery

### Built-in Security

- SYN flood protection with rate limiting
- Ping of death protection (ICMP rate limiting)
- Port scan detection (RST packet analysis)
- IP spoofing defense (bogon/RFC1918 blocking)
- Windows port blocking (135,137,138,139,445)
- SSH brute-force protection
- Input sanitization (no shell injection)

## Installation

> **⚠️ Important:** AFW will automatically detect and disable conflicting firewall services (UFW, firewalld, iptables service) during **fresh installation** to prevent conflicts and crashes.

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

## Usage

### Interactive TUI

```bash
sudo afw
```

Launches the interactive menu with 12 options — navigate with arrow keys:

1. **Open TCP Port** — Allow incoming TCP connections
2. **Open UDP Port** — Allow incoming UDP traffic
3. **Close Port** — Remove port rule
4. **List Ports** — Show all open ports
5. **Whitelist IP** — Allow all traffic from IP
6. **Blacklist IP** — Block all traffic from IP
7. **Port Forward** — PREROUTING redirect
8. **Enable NAT** — POSTROUTING masquerade
9. **Port Protection** — Rate limiting (brute-force defense)
10. **Enable Firewall** — Activate all rules
11. **Disable Firewall** — Flush all rules
12. **Exit** — Quit TUI

### CLI Commands

```bash
# Setup (first time) - auto-detect interface and SSH port
sudo afw setup

# Or specify manually
sudo afw setup --interface eth0 --ssh-port 22

# Port management
sudo afw port add tcp 80
sudo afw port add udp 53
sudo afw port add tcp 3000-4000      # range
sudo afw port add tcp 8080 -s 10.0.0.5  # IP-restricted
sudo afw port remove tcp 80
sudo afw port list

# Port protection (rate limiting)
sudo afw protect add 22 --rate 10 --per 60
sudo afw protect remove 22

# IP management
sudo afw whitelist add 10.0.0.1
sudo afw whitelist remove 10.0.0.1
sudo afw blacklist add 1.2.3.4
sudo afw blacklist remove 1.2.3.4

# NAT / Masquerade
sudo afw nat enable
sudo afw nat disable

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

# Backup
sudo afw backup create
sudo afw backup list
sudo afw backup restore /var/lib/afw/backups/state-20240101-120000.json

# Info
sudo afw rules    # raw iptables-save output
sudo afw version
```

## Upgrade

Upgrading AFW is seamless - your configuration and rules are preserved:

```bash
# Debian / Ubuntu
sudo apt update && sudo apt upgrade -y

# RHEL / Fedora / CentOS
sudo dnf upgrade -y

# Ubuntu PPA
sudo apt update && sudo apt upgrade -y
```

After upgrade, reload to apply new features:
```bash
sudo afw reload
```

> **Note:** Conflicting firewall detection only runs on fresh install, not on upgrades. Your existing firewall state is preserved during upgrades.

## Resources

- [Package Repository](https://irtec.github.io/afw-repo/)
- [GPG Public Key](https://irtec.github.io/afw-repo/pubkey.asc)

## License

GPL © [irya](https://www.irya.dev)
