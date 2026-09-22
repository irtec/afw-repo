# 🔥 AFW Firewall v2.3.1

**Advanced Firewall Management & Integrated WireGuard VPN for Linux Servers**

## Features

## Built-in Security

- **WireGuard AES-GCM Key Encryption** — private keys encrypted at rest (`0600` key file)
- **IPv6 filtering** — full ip6tables ruleset, enabled automatically on hosts that use IPv6
- **SYN flood protection** — rate limited with logging
- **Ping of death protection** — ICMP rate limiting
- **Port scan detection** — RST packet analysis
- **IP spoofing defense** — bogon/reserved-range blocking on WAN
- **Windows port blocking** — 135,137,138,139,445 in FORWARD
- **SSH brute-force** — `recent` module rate limiting
- **Input sanitization** — all user input cleaned (no shell injection)

## 🔐 Integrated WireGuard VPN

AFW includes full road-warrior WireGuard VPN management natively built-in:

- 📱 **QR Code Export**: Easily connect mobile devices by scanning terminal QR codes.
- 🔑 **Encrypted at Rest**: Server and client private keys are encrypted with AES-GCM in `/etc/afw/state.json`.
- 🌐 **Auto Firewall Integration**: Automatically opens UDP listen ports, manages masquerading, and mirrors access rules to `wg0`.
- ⚡ **Optimized MTU (1380)**: Prevents MTU issues over NATs and mobile carriers.

## 🌐 IPv6 Filtering

IPv6 is filtered by default whenever the host actually uses it, so it can never become a bypass around your IPv4 rules.

- **auto** (default) — AFW checks whether IPv6 is disabled at the kernel and whether any interface holds a global IPv6 address. If yes, the dual-stack engine (`iptables` + `ip6tables`) is used; if not, IPv4 alone.
- **on** — force IPv6 filtering on.
- **off** — force IPv6 filtering off (IPv4 only).

```bash
sudo afw config                        # show current mode and the decision
sudo afw config set ipv6_mode auto     # auto | on | off
sudo afw reload                        # apply
```

## 🐳 Docker & Kubernetes Compatible

AFW intelligently preserves external firewall rules!

When you run `afw reload`, AFW will:

- Preserve Docker container networking rules
- Keep Kubernetes pod/service rules intact
- Maintain libvirt/KVM virtual machine networking
- Auto-reload rules when Docker daemon restarts (`docker.service` hook)

**How it works:**

- AFW uses **selective flush** — only removes its own chains
- External rules (Docker, K8s, libvirt) are never removed by AFW's flush, so they survive every reload
- Container ports are rate-limited directly inside the `DOCKER-USER` chain

## Installation

### Debian / Ubuntu (APT)

```bash
curl -fsSL https://irtec.github.io/afw-repo/pubkey.asc | sudo gpg --dearmor -o /usr/share/keyrings/afw.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/afw.gpg] https://irtec.github.io/afw-repo stable main" | sudo tee /etc/apt/sources.list.d/afw.list
sudo apt update
sudo apt install afw
```

Or one-liner:

```bash
curl -fsSL https://irtec.github.io/afw-repo/setup-apt.sh | sudo bash
```

### Ubuntu PPA (alternative)

```bash
sudo add-apt-repository ppa:irya31/afw
sudo apt update
sudo apt install afw
```

### RHEL / Fedora / CentOS (YUM/DNF)

```bash
sudo curl -fsSL https://irtec.github.io/afw-repo/afw.repo -o /etc/yum.repos.d/afw.repo
sudo rpm --import https://irtec.github.io/afw-repo/pubkey.asc
sudo dnf install afw    # or: sudo yum install afw
```

Or one-liner:

```bash
curl -fsSL https://irtec.github.io/afw-repo/setup-yum.sh | sudo bash
```

### Binary (any Linux)

```bash
curl -sL https://github.com/irtec/afw-firewall/releases/latest/download/afw_2.3.0_linux_amd64.tar.gz | tar xz
sudo mv afw /usr/sbin/
sudo afw setup --interface eth0 --ssh-port 22
```

### From Source

```bash
git clone https://github.com/irtec/afw-firewall.git
cd afw-firewall
go build -o afw .
sudo mv afw /usr/sbin/
```

*After installation, your firewall is automatically configured and active!*

## Upgrade

Upgrading AFW is seamless — your configuration and rules are preserved:

```bash
# Debian / Ubuntu
sudo apt update && sudo apt upgrade -y

# RHEL / Fedora / CentOS
sudo dnf upgrade -y
```

*After upgrade, reload to apply new features:* `sudo afw reload`

## Usage

### Interactive TUI

```bash
sudo afw
```

Launches the interactive TUI with master-detail layout, telemetry header, rules overview, and category panels (TCP/UDP, Protect, Ranges, Whitelist, Blacklist, NAT, IGMP, WireGuard VPN).

### Manual Reconfiguration (Optional)

```bash
# Only needed on a fresh, unconfigured install — a configured
# install is preserved and  is a safe no-op.
sudo afw setup --interface eth0 --ssh-port 22
```

### CLI Commands

```bash
# Port management
sudo afw port tcp add 80
sudo afw port udp add 53
sudo afw port tcp add 8080 -s 10.0.0.5   # IP-restricted
sudo afw port tcp range 3000 4000        # range
sudo afw port tcp remove 80
sudo afw port list

# Port protection (rate limiting)
sudo afw protect add 22 --rate 10 --per 60
sudo afw protect remove 22

# WireGuard VPN Server (Road-Warrior)
sudo afw wg install                      # Install wireguard-tools
sudo afw wg server up                    # Start WireGuard server
sudo afw wg peer add phone               # Add client device
sudo afw wg client export phone --qr     # Export config as QR code
sudo afw wg server show                  # Show live status & peers
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

# Settings (IPv6 filtering mode)
sudo afw config
sudo afw config set ipv6_mode auto

# Factory reset
sudo afw reset                           # Wipe all rules, state & WireGuard

# Info
sudo afw version
```

## Systemd Service

```bash
sudo systemctl enable afw       # Auto-start on boot
sudo systemctl start afw        # Start firewall
sudo systemctl stop afw         # Stop firewall
sudo systemctl reload afw       # Reload rules
sudo systemctl status afw       # Check status
```

## State File

Rules and WireGuard server state are stored as JSON at `/etc/afw/state.json`:

```
{
  "version": "2.3.0",
  "active": true,
  "interface": "eth0",
  "ssh_port": 22,
  "masquerade": false,
  "rules": [
    {
      "id": "tcp-80",
      "type": "tcp",
      "action": "ACCEPT",
      "protocol": "tcp",
      "port": 80,
      "enabled": true
    }
  ]
}
```

Behavioural settings live separately in `/etc/afw/config.json`:

```
{
  "backend": "iptables",
  "preserve_external_rules": true,
  "log_level": "info",
  "auto_backup": true,
  "max_backups": 10,
  "ipv6_mode": "auto"
}
```

## Paths

## Resources

- [GPG Public Key](https://irtec.github.io/afw-repo/pubkey.asc)
- [Package Repository](https://irtec.github.io/afw-repo/)
- [Ubuntu PPA](https://launchpad.net/~irya31/+archive/ubuntu/afw)

## License

**GNU General Public License v3.0 or later** (GPL-3.0-or-later) — Copyright © 2024–2026 [IRTech](https://www.irya.dev).
