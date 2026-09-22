#!/bin/bash
# AFW Firewall - YUM/DNF Repository Setup (RHEL / Fedora / CentOS)
# Usage: curl -fsSL https://irtec.github.io/afw-repo/setup-yum.sh | sudo bash

set -e

echo "🔥 AFW Firewall - Setting up YUM repository..."

# Add repository config
curl -fsSL https://irtec.github.io/afw-repo/afw.repo -o /etc/yum.repos.d/afw.repo

# Import GPG key
rpm --import https://irtec.github.io/afw-repo/pubkey.asc

# Install
if command -v dnf &>/dev/null; then
    dnf install -y afw
else
    yum install -y afw
fi

echo "✅ AFW Firewall installed successfully!"
echo "   Run 'sudo afw' to start the interactive TUI"
echo "   Run 'sudo afw setup --interface eth0 --ssh-port 22' for initial setup"