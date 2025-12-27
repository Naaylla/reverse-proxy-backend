# VPS Deployment Guide - Reverse Proxy Showcase

This guide shows how to deploy the full reverse proxy architecture on a VPS to demonstrate the pattern for your hackathon.

## 🏗️ Architecture (Full Reverse Proxy)

```
Internet → VPS:80 (NGINX) → Gateway:8000 → External APIs
                                           ├─ CoinGecko
                                           ├─ Open-Meteo
                                           └─ Open-Meteo AQ
```

## 📋 Prerequisites

- SSH access to VPS
- VPS running Ubuntu 20.04+ or Debian
- Root or sudo access
- Domain name (optional, can use IP)

## 🚀 Quick Deploy

### 1. Connect to VPS

```bash
ssh your-username@your-vps-ip
```

### 2. Install Docker & Docker Compose

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Clone & Configure

```bash
# Clone repository
git clone https://github.com/Naaylla/reverse-proxy-backend.git
cd reverse-proxy-backend

# Create environment file
cp .env.example .env

# Edit if needed
nano .env
```

### 4. Deploy with Docker Compose

```bash
# Build and start
docker-compose up -d --build

# Check logs
docker-compose logs -f

# Verify services
docker-compose ps
```

### 5. Configure Firewall

```bash
# Allow HTTP traffic
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp  # For future HTTPS
sudo ufw enable
```

### 6. Test Deployment

```bash
# Health check
curl http://your-vps-ip/api/health

# Test state endpoint
curl -X POST http://your-vps-ip/api/state \
  -H "Content-Type: application/json" \
  -d '{
    "economy": {"asset": "btc"},
    "weather": {"country": "algeria"},
    "air": {"country": "algeria"}
  }'
```

## 🎯 Hackathon Demo Points

### Show the Reverse Proxy Pattern

1. **Single Entry Point**
   ```bash
   # All requests go through NGINX on port 80
   curl http://your-vps-ip/api/state
   ```

2. **NGINX Routes to Backend**
   ```bash
   # Check NGINX config
   docker-compose exec gateway cat /etc/nginx/nginx.conf
   ```

3. **Backend Aggregates Multiple APIs**
   ```bash
   # Show logs of parallel API calls
   docker-compose logs -f gateway
   ```

### Key Features to Highlight

✅ **NGINX as Reverse Proxy** - Single public endpoint  
✅ **Backend as API Gateway** - Aggregates 3 external APIs  
✅ **Parallel Processing** - All APIs called concurrently  
✅ **Clean Architecture** - Frontend never calls external APIs  
✅ **Scalable Design** - Easy to add new data sources  

## 📊 Monitoring

```bash
# View logs
docker-compose logs -f

# Check resource usage
docker stats

# Restart services
docker-compose restart

# View NGINX access logs
docker-compose exec gateway tail -f /var/log/nginx/access.log
```

## 🔧 Troubleshooting

### Port 80 Already in Use

```bash
# Check what's using port 80
sudo lsof -i :80

# Stop existing service
sudo systemctl stop apache2  # or nginx
sudo systemctl disable apache2
```

### Services Not Starting

```bash
# Check logs
docker-compose logs gateway

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Cannot Access from Browser

```bash
# Check firewall
sudo ufw status

# Allow port 80
sudo ufw allow 80/tcp
```

## 🌐 Optional: Add Domain Name

### 1. Point Domain to VPS

Add an A record in your DNS:
```
A    @    your-vps-ip
A    api  your-vps-ip
```

### 2. Update NGINX Config

```nginx
server_name yourdomain.com api.yourdomain.com;
```

### 3. Add SSL with Certbot

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

## 📱 Update Frontend

Point your frontend to:
```javascript
const API_URL = 'http://your-vps-ip/api/state';
// or with domain:
const API_URL = 'https://api.yourdomain.com/api/state';
```

## 🎓 Explaining to Judges

### The Problem
"Frontends calling multiple APIs directly creates complexity, CORS issues, and exposes API keys."

### Your Solution
"We use NGINX as a reverse proxy to create a single API gateway that aggregates multiple external APIs behind one endpoint."

### The Flow
1. Frontend makes ONE request to `/api/state`
2. NGINX receives and routes to gateway service
3. Gateway calls 3 external APIs in parallel
4. Gateway aggregates and returns clean data
5. Frontend receives normalized response

### Benefits
- ✅ Single point of entry (security)
- ✅ No CORS issues (same origin)
- ✅ Parallel API calls (performance)
- ✅ Clean separation (maintainability)
- ✅ Easy to extend (scalability)

## 🚀 Quick Commands Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Logs
docker-compose logs -f

# Rebuild
docker-compose up -d --build

# Check status
docker-compose ps

# Update code
git pull
docker-compose up -d --build
```

## 📞 Support

If you encounter issues during deployment:
1. Check logs: `docker-compose logs -f`
2. Verify ports: `sudo lsof -i :80`
3. Test locally: `curl http://localhost/api/health`
4. Check firewall: `sudo ufw status`

Your reverse proxy is ready to impress the judges! 🏆