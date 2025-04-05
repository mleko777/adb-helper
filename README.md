# 🔌 ADB Helper Script v1.2

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/ADB-1.0.41+-green?logo=android" alt="ADB">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey" alt="Platform">
  <img src="https://img.shields.io/github/last-commit/mleko777/adb-helper" alt="Last Commit">
</div>

A comprehensive Python toolkit for advanced Android device management via ADB, featuring both powerful utilities and harmless prank functionalities.

![ADB Helper Interface](demo.gif) *(Example interface animation)*

## 🌟 Feature Highlights

### 🚦 Device Control
- **Reboot Options**:
  - 🔄 Standard reboot
  - ⚡ Fastboot mode
  - 🔧 Recovery mode
  - 📲 Download mode
  - 🆘 EDL (Emergency Download)
  - 👶 Safe Mode

- **System Operations**:
  - 📊 CPU/Memory monitoring
  - ⚙️ Settings modification
  - 🔒 Lockscreen management

### 📁 File Management
```bash
► adb push/pull - File transfer
► adb sideload - Package installation
► screencap - Screenshot capture
► screenrecord - Screen recording (MP4)
```
+ 😄 Funny wallpaper changes
+ 🔊 Unexpected notification sounds
+ 🌍 Language switcher
+ 🔠 Giant font sizes
+ 🕰️ Hidden clock
+ 📱 Fake virus scan (visual only)

🧰 Advanced Usage
Backup Options:
# Full device backup
adb backup -apk -shared -all -f backup.ab

# App-specific backup
adb backup -apk com.example.app -f app_backup.ab

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/mleko777/adb-helper.git
   cd adb-helper
