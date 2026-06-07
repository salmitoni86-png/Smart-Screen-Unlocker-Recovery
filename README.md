<!-- README.md -->
<div align="center">

<img src="frontend/static/images/logo.svg" alt="Smart Recovery Logo" width="200"/>

# 🔓 Smart Recovery Platform

### Professional Android Recovery & FRP Bypass Suite

[![Python](https://img.shields.io/badge/Python-3.8+-orange.svg?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-black.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.0.0-black.svg?style=for-the-badge)]()

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [API](#-api) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

**Smart Recovery Platform** is a comprehensive Android device recovery tool that combines **screen lock removal**, **FRP bypass**, and **remote device control** in a beautiful, modern interface. Built with cutting-edge technologies including real-time camera tracking, glassmorphism UI, and AI-powered recovery methods.

### Why Choose Smart Recovery?

- 🚀 **Multi-Platform**: Web, CLI, and API access
- 🎨 **Beautiful UI**: Black & Orange glassmorphism design
- 📱 **Camera Tracking**: Control interface with finger movements
- 💰 **Coin System**: Earn rewards through referrals and successful recoveries
- 🔧 **All Samsung Methods**: Including Exynos-specific exploits
- 🖥️ **Built-in scrcpy**: Remote device control from browser
- 🔒 **Secure**: Enterprise-grade authentication and encryption

---

## ✨ Features

### 📱 Device Recovery
- **Screen Lock Removal** (PIN/Pattern/Password)
- **FRP Bypass** for all major brands
- **Samsung Specialized Methods**
  - Exynos 8890-990 exploits
  - Combination firmware bypass
  - TrustZone vulnerabilities
  - DeKnox method
  - Download mode exploits
- **Android 5-14 Support**
- **Automatic method selection**

### 🎮 Remote Control
- **Full scrcpy integration**
- **Real-time screen streaming**
- **Touch control from browser**
- **Keyboard/mouse input**
- **Screen recording**

### 👁️ Camera Tracking
- **Finger movement detection**
- **Hand gesture controls**
- **Face tracking for security**
- **Motion-reactive UI elements**

### 💰 Economy System
- **Earn coins** through:
  - Successful recoveries (10 coins)
  - Referral program (50 coins)
  - Daily bonuses
  - Watching ads
- **Spend coins on**:
  - Premium FRP methods
  - scrcpy sessions
  - Priority support

### 🎨 UI/UX
- **Glassmorphism design**
- **Animated FRP symbols**
- **Particle effects**
- **Responsive layout**
- **Dark mode optimized**
- **Real-time notifications**

### 🔧 Technical
- **REST API** with FastAPI
- **WebSocket** for real-time control
- **JWT Authentication**
- **SQLite/PostgreSQL** database
- **Docker support**
- **CLI tool** included

---

## 📋 Supported Devices

| Brand | Screen Lock | FRP Bypass | Special Methods |
|-------|------------|------------|-----------------|
| **Samsung** | ✅ | ✅ | Exynos, Knox, FMM |
| **Xiaomi** | ✅ | ✅ | Mi Account bypass |
| **Google** | ✅ | ✅ | Account Manager |
| **OnePlus** | ✅ | ✅ | OxygenOS methods |
| **Motorola** | ✅ | ✅ | - |
| **LG** | ✅ | ✅ | - |
| **Huawei** | ✅ | ✅ | HiSuite exploit |
| **OPPO/Vivo** | ✅ | ✅ | - |
| **Realme** | ✅ | ✅ | - |

## Samsung Exynos Support Matrix

| Exynos Model | Devices | Methods Available |
|--------------|---------|-------------------|
| **8890** | S7, S7 Edge | Download Mode, TZ Exploit |
| **8895** | S8, S8+, Note 8 | Download Mode, Comb. FW |
| **9810** | S9, S9+, Note 9 | Comb. FW, DeKnox |
| **9820/9825** | S10, Note 10 | Comb. FW, Knox Reset |
| **990** | S20, Note 20 | Comb. FW, Security Patch |

---

## 🚀 Installation

### Quick Install (Linux/Termux/Mac)

```bash
# Clone repository
git clone https://github.com/salmitoni86-png/Smart-Screen-Unlocker-Recovery.git
cd Smart-Screen-Unlocker-Recovery

# Run installer
chmod +x install.sh
./install.sh

Manual Installation
<details> <summary><b>Termux (Android)</b></summary>
bash
# Update packages
pkg update && pkg upgrade

# Install dependencies
pkg install python android-tools scrcpy git openssl

# Install Python packages
pip install -r requirements.txt

# Run server
python backend/main.py
</details><details> <summary><b>Linux/Chromebook</b></summary>
bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip android-tools-adb scrcpy

# Install Python packages
pip3 install -r requirements.txt

# Run server
python3 backend/main.py
</details><details> <summary><b>Windows</b></summary>
powershell
# Install Python 3.8+ from python.org
# Install ADB from Google Platform Tools

# Clone and install
git clone https://github.com/salmitoni86-png/Smart-Screen-Unlocker-Recovery.git
cd Smart-Screen-Unlocker-Recovery
pip install -r requirements.txt

# Run server
python backend/main.py
</details><details> <summary><b>Docker</b></summary>
bash
# Build and run with Docker
docker-compose up -d

# Access at http://localhost:8000
</details>
💻 Usage
Web Interface
Start the server:

bash
python backend/main.py
Open browser: http://localhost:8000

Register account / Login

Connect device via USB

Select recovery method or use Auto-Recovery

CLI Tool
bash
# List connected devices
python cli/smart_recovery_cli.py devices

# Get device info
python cli/smart_recovery_cli.py info <serial>

# Auto-recovery
python cli/smart_recovery_cli.py recover <serial> --type auto

# Samsung FRP bypass
python cli/smart_recovery_cli.py samsung-frp <serial>

# Start scrcpy
python cli/smart_recovery_cli.py scrcpy <serial>
API Access
python
import requests

# Login
response = requests.post('http://localhost:8000/api/login', json={
    'username': 'your_username',
    'password': 'your_password'
})
token = response.json()['access_token']

# Start recovery
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:8000/api/recovery/start', 
    headers=headers,
    json={
        'device_serial': 'YOUR_DEVICE_SERIAL',
        'recovery_type': 'frp_bypass',
        'method': 'auto'
    }
)
📸 Screenshots
<div align="center">
🎨 Glassmorphism Dashboard
https://screenshots/dashboard.png

📱 Device Control with scrcpy
https://screenshots/device_control.png

💰 Coin System
https://screenshots/coin_system.png

🎯 Recovery Process
https://screenshots/recovery.png

</div>
🏗️ Architecture
text
┌─────────────────────────────────────────────────────────┐
│                    Frontend (HTML/CSS/JS)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Dashboard │  │ Device   │  │ Recovery │  │  Admin   │ │
│  │          │  │ Control  │  │  Tools   │  │  Panel   │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                    WebSocket│REST API
                            │
┌─────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │   Auth   │  │   ADB    │  │   FRP    │  │  Coin    │ │
│  │  System  │  │ Manager  │  │ Methods  │  │  System  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ scrcpy   │  │ Samsung  │  │  Camera  │  │ Database │ │
│  │ Manager  │  │  Exynos  │  │ Tracker  │  │  (SQL)   │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            │ ADB
                            │
┌─────────────────────────────────────────────────────────┐
│                   Android Device                         │
│         ┌──────────────────────────────┐                │
│         │    Target Phone/Tablet       │                │
│         │  (Locked / FRP Protected)    │                │
│         └──────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
🔐 Security
JWT Authentication with token expiration

Password hashing with SHA-256 + salt

HTTPS support (configurable)

Rate limiting on API endpoints

CORS configuration

Input validation with Pydantic

SQL injection prevention

XSS protection

⚙️ Configuration
Create .env file:

env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Security
SECRET_KEY=your-secret-key-here
JWT_EXPIRY=60

# Database
DATABASE_URL=sqlite:///data/recovery.db

# Coin System
WELCOME_BONUS=10
REFERRAL_REWARD=50
PREMIUM_COST=20

# Ads
ADS_ENABLED=true
AD_REWARD=5

# Camera Tracking
CAMERA_ENABLED=false
CAMERA_DEVICE=0

# scrcpy
SCRCPY_PATH=/usr/bin/scrcpy
SCRCPY_MAX_BITRATE=8M
🧪 Testing
bash
# Run tests
python -m pytest tests/

# Test with coverage
python -m pytest --cov=backend tests/
🤝 Contributing
We welcome contributions! See CONTRIBUTING.md

Development Setup
bash
# Fork and clone
git clone https://github.com/YOUR_USER/Smart-Screen-Unlocker-Recovery.git
cd Smart-Screen-Unlocker-Recovery

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Run in development mode
python backend/main.py --reload
⚠️ Legal Disclaimer
This tool is intended for legitimate purposes only:

✅ Recovering YOUR OWN device

✅ IT support with EXPLICIT permission

✅ Forensic investigations with legal authorization

❌ Unauthorized access to others' devices

❌ Illegal activities

❌ Violating privacy laws

You are responsible for complying with all applicable laws.

📄 License
This project is licensed under the MIT License - see LICENSE file.

🙏 Acknowledgments
scrcpy - Genymobile's awesome screen mirroring

MOBILedit Forensic - Research inspiration

Oxygen Forensics - Method research

Android Debug Bridge - Google's ADB tool

FastAPI - Amazing Python framework

📞 Support
📧 Email: support@smartrecovery.io

💬 Discord: Join our server

🐦 Twitter: @SmartRecovery

📖 Docs: docs.smartrecovery.io

⭐ Star History
https://api.star-history.com/svg?repos=salmitoni86-png/Smart-Screen-Unlocker-Recovery&type=Date

<div align="center">
Made with ❤️ by the Smart Recovery Team
⬆ Back to Top

</div> 
