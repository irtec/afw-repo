#!/bin/bash
# AFW Firewall - APT Repository Setup (Debian / Ubuntu)
# Usage: curl -fsSL https://irtec.github.io/afw-repo/setup-apt.sh | sudo bash

set -e

echo "🔥 AFW Firewall - Setting up APT repository..."

# Download and install GPG key
curl -fsSL https://irtec.github.io/afw-repo/pubkey.asc | gpg --dearmor -o /usr/share/keyrings/afw.gpg

# Add repository
ARCH=$(dpkg --print-architecture)
echo "deb [arch=${ARCH} signed-by=/usr/share/keyrings/afw.gpg] https://irtec.github.io/afw-repo stable main" > /etc/apt/sources.list.d/afw.list

# Update and install
apt-get update
apt-get install -y afw

echo "✅ AFW Firewall installed successfully!"
echo "   Run 'sudo afw' to start the interactive TUI"
echo "   Run 'sudo afw setup --interface eth0 --ssh-port 22' for initial setup"