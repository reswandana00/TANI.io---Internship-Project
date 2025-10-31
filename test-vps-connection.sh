#!/bin/bash

# Test VPS Connection Script
# Tests SSH connection and basic requirements

VPS_IP="10.11.1.207"
VPS_USER="soc-ai"
SSH_TARGET="${VPS_USER}@${VPS_IP}"

echo "🔍 Testing connection to VPS..."
echo "Target: ${SSH_TARGET}"

# Test SSH connection
echo "📡 Testing SSH connection..."
if ssh -o ConnectTimeout=10 ${SSH_TARGET} "echo 'SSH connection successful'"; then
    echo "✅ SSH connection: OK"
else
    echo "❌ SSH connection: FAILED"
    exit 1
fi

# Check Docker installation
echo "🐳 Checking Docker installation..."
if ssh ${SSH_TARGET} "docker --version"; then
    echo "✅ Docker: OK"
else
    echo "❌ Docker: NOT INSTALLED"
fi

# Check Docker Compose installation
echo "🐙 Checking Docker Compose installation..."
if ssh ${SSH_TARGET} "docker-compose --version"; then
    echo "✅ Docker Compose: OK"
else
    echo "❌ Docker Compose: NOT INSTALLED"
fi

# Check available disk space
echo "💾 Checking disk space..."
ssh ${SSH_TARGET} "df -h /"

# Check if ports are available
echo "🔌 Checking port availability..."
for port in 8011 8012 8013 8080 5432; do
    if ssh ${SSH_TARGET} "sudo netstat -tlnp | grep :${port}"; then
        echo "⚠️  Port ${port}: IN USE"
    else
        echo "✅ Port ${port}: AVAILABLE"
    fi
done

# Test internet connectivity from VPS
echo "🌐 Testing internet connectivity from VPS..."
if ssh ${SSH_TARGET} "curl -s https://www.google.com > /dev/null"; then
    echo "✅ Internet connectivity: OK"
else
    echo "❌ Internet connectivity: FAILED"
fi

echo "🎯 Connection test completed!"