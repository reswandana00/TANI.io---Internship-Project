#!/bin/bash

# Quick Update Deployment Script for VPS
# Updates the existing deployment with new code

VPS_IP="10.11.1.207"
VPS_USER="soc-ai"
SSH_TARGET="${VPS_USER}@${VPS_IP}"

echo "🔄 Updating TANI.io deployment on VPS..."

# Execute update on VPS
ssh ${SSH_TARGET} << 'ENDSSH'
set -e

echo "📍 Navigating to project directory..."
cd /home/soc-ai/tani-ai

echo "🛑 Stopping current services..."
docker-compose -f docker-compose.production.yml down

echo "📥 Extracting updated code..."
sudo tar -xzf /tmp/tani-ai-deployment-updated.tar.gz
sudo chown -R soc-ai:soc-ai /home/soc-ai/tani-ai

echo "🔄 Copying VPS environment configuration..."
cp .env.vps .env

echo "🔨 Starting updated services..."
docker-compose -f docker-compose.production.yml up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 20

echo "🔍 Checking service status..."
docker-compose -f docker-compose.production.yml ps

echo "✅ Update completed!"
echo "🌐 Access your application at: http://10.11.1.207:8013"

ENDSSH

echo "🎉 VPS update completed successfully!"