#!/bin/bash

# Database Setup Script for VPS
# This script sets up the database with sample data on the VPS

VPS_IP="10.11.1.207"
VPS_USER="soc-ai"
SSH_TARGET="${VPS_USER}@${VPS_IP}"

echo "🗄️ Setting up database on VPS..."

# Upload the database script
echo "📤 Uploading database insertion script..."
scp insert_data.py ${SSH_TARGET}:/tmp/

# Create Latest folder and upload CSV files if they exist
if [ -d "Latest" ]; then
    echo "📊 Uploading CSV data files..."
    scp -r Latest/ ${SSH_TARGET}:/tmp/
fi

# Execute database setup on VPS
echo "🔧 Setting up database on VPS..."
ssh ${SSH_TARGET} << 'ENDSSH'
set -e

echo "🏠 Setting up database environment..."
cd /home/soc-ai/tani-ai

# Copy database script
cp /tmp/insert_data.py .

# Copy CSV files if they exist
if [ -d "/tmp/Latest" ]; then
    cp -r /tmp/Latest .
fi

# Install Python dependencies for database script
echo "📦 Installing Python dependencies..."
pip3 install pandas sqlalchemy psycopg2-binary

# Wait for database to be ready
echo "⏳ Waiting for database container to be ready..."
sleep 10

# Run database insertion script
echo "🗄️ Running database insertion script..."
python3 insert_data.py

echo "✅ Database setup completed!"

ENDSSH

echo "🎉 Database setup on VPS completed!"