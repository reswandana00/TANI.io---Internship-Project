@echo off
setlocal enabledelayedexpansion

REM TANI.io VPS Deployment Script for Windows
REM Target: VPS at 10.11.1.207

echo 🚀 Starting TANI.io deployment to VPS...

REM Configuration
set VPS_IP=10.11.1.207
set VPS_USER=soc-ai
set SSH_TARGET=%VPS_USER%@%VPS_IP%
set PROJECT_DIR=/home/%VPS_USER%/tani-ai

echo 📋 Deployment Configuration:
echo    VPS IP: %VPS_IP%
echo    SSH Target: %SSH_TARGET%
echo    Remote Directory: %PROJECT_DIR%

REM Check if ssh and scp are available
where ssh >nul 2>nul
if errorlevel 1 (
    echo ❌ SSH not found. Please install OpenSSH or use WSL.
    pause
    exit /b 1
)

REM Create deployment package using PowerShell (excluding database data)
echo 📦 Creating deployment package...
powershell -Command "
$excludePaths = @('.\ApiDB\pgdata\*', '.\.git\*', '.\node_modules\*', '.\__pycache__\*', '.\.next\*', '*.pyc')
Get-ChildItem -Path '.\*' -Recurse | Where-Object { 
    $item = $_
    $exclude = $false
    foreach ($pattern in $excludePaths) {
        if ($item.FullName -like $pattern) {
            $exclude = $true
            break
        }
    }
    -not $exclude
} | Compress-Archive -DestinationPath '.\tani-ai-deployment.zip' -Force -CompressionLevel Optimal
"

if not exist "tani-ai-deployment.zip" (
    echo ❌ Failed to create deployment package
    pause
    exit /b 1
)

echo ✅ Deployment package created: tani-ai-deployment.zip

REM Copy files to VPS
echo 📤 Uploading files to VPS...
scp tani-ai-deployment.zip %SSH_TARGET%:/tmp/

if errorlevel 1 (
    echo ❌ Failed to upload files to VPS
    pause
    exit /b 1
)

REM Execute deployment on VPS
echo 🔧 Executing deployment on VPS...
ssh %SSH_TARGET% "
set -e
echo '🏠 Setting up project directory...'
sudo mkdir -p /home/soc-ai/tani-ai
cd /home/soc-ai/tani-ai

echo '📥 Extracting deployment package...'
sudo unzip -o /tmp/tani-ai-deployment.zip
sudo chown -R soc-ai:soc-ai /home/soc-ai/tani-ai

echo '🔄 Copying production environment...'
cp .env.vps .env

echo '🐳 Stopping existing containers...'
docker-compose -f docker-compose.production.yml down --remove-orphans || true

echo '🧹 Cleaning up Docker resources...'
docker system prune -f || true

echo '🔨 Building and starting services...'
docker-compose -f docker-compose.production.yml up --build -d

echo '⏳ Waiting for services to be ready...'
sleep 30

echo '🔍 Checking service status...'
docker-compose -f docker-compose.production.yml ps

echo '🩺 Running health checks...'
echo 'Checking Tool API...'
curl -f http://localhost:8011/health || echo 'Tool API health check failed'

echo 'Checking Chatbot API...'
curl -f http://localhost:8012/health || echo 'Chatbot API health check failed'

echo 'Checking Frontend...'
curl -f http://localhost:8013 || echo 'Frontend health check failed'

echo '🎉 Deployment completed!'
echo '📱 Services available at:'
echo '   Frontend: http://10.11.1.207:8013'
echo '   Tool API: http://10.11.1.207:8011'
echo '   Chatbot API: http://10.11.1.207:8012'
echo '   PgAdmin: http://10.11.1.207:8080'
"

if errorlevel 1 (
    echo ❌ Deployment failed on VPS
    pause
    exit /b 1
)

REM Clean up local deployment package
del tani-ai-deployment.zip

echo ✅ VPS deployment completed successfully!
echo 🌐 Access your application at: http://10.11.1.207:8013
pause