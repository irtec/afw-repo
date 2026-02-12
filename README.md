# 🔥 AFW Firewall - Package Repository

Advanced Firewall Management for Linux Servers

## Installation

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

## Resources

- [Package Repository](https://irtec.github.io/afw-repo/)
- [GPG Public Key](https://irtec.github.io/afw-repo/pubkey.asc)
