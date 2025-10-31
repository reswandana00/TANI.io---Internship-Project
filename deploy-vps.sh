#!/bin/bash

# TANI.io VPS Deployment Script
# Target: VPS at 10.11.1.207

set -e

echo "🚀 Starting TANI.io deployment to VPS..."

# Configuration
VPS_IP="10.11.1.207"
VPS_USER="soc-ai"
SSH_TARGET="${VPS_USER}@${VPS_IP}"
PROJECT_DIR="/home/${VPS_USER}/tani-ai"
LOCAL_DIR="."

echo "📋 Deployment Configuration:"
echo "   VPS IP: ${VPS_IP}"
echo "   SSH Target: ${SSH_TARGET}"
echo "   Remote Directory: ${PROJECT_DIR}"

# Create deployment package
echo "📦 Creating deployment package..."
tar --exclude='.git' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.next' \
    --exclude='ApiDB/pgdata' \
    -czf tani-ai-deployment.tar.gz .

echo "✅ Deployment package created: tani-ai-deployment.tar.gz"

# Copy files to VPS
echo "📤 Uploading files to VPS..."
scp tani-ai-deployment.tar.gz ${SSH_TARGET}:/tmp/

# Execute deployment on VPS
echo "🔧 Executing deployment on VPS..."
ssh ${SSH_TARGET} << 'ENDSSH'
set -e

echo "🏠 Setting up project directory..."
sudo mkdir -p /home/soc-ai/tani-ai
cd /home/soc-ai/tani-ai

echo "📥 Extracting deployment package..."
sudo tar -xzf /tmp/tani-ai-deployment.tar.gz -C . --strip-components=0
sudo chown -R soc-ai:soc-ai /home/soc-ai/tani-ai

echo "🔄 Copying production environment..."
cp .env.vps .env

echo "🐳 Stopping existing containers..."
docker-compose -f docker-compose.production.yml down --remove-orphans || true

echo "🧹 Cleaning up Docker resources..."
docker system prune -f || true

echo "🔨 Building and starting services..."
docker-compose -f docker-compose.production.yml up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 30

echo "🔍 Checking service status..."
docker-compose -f docker-compose.production.yml ps

echo "🩺 Running health checks..."
echo "Checking Tool API..."
curl -f http://localhost:8011/health || echo "Tool API health check failed"

echo "Checking Chatbot API..."
curl -f http://localhost:8012/health || echo "Chatbot API health check failed"

echo "Checking Frontend..."
curl -f http://localhost:8013 || echo "Frontend health check failed"

echo "🎉 Deployment completed!"
echo "📱 Services available at:"
echo "   Frontend: http://10.11.1.207:8013"
echo "   Tool API: http://10.11.1.207:8011"
echo "   Chatbot API: http://10.11.1.207:8012"
echo "   PgAdmin: http://10.11.1.207:8080"

ENDSSH

# Clean up local deployment package
rm tani-ai-deployment.tar.gz

echo "✅ VPS deployment completed successfully!"
echo "🌐 Access your application at: http://10.11.1.207:8013"