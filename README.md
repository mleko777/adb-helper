# ADB Utility Script

A powerful and modular Python script designed to manage Android devices via ADB. This tool allows for various device operations like rebooting, file transfers, managing installed apps, system operations, and even some harmless prank functionalities.

## Features

### 1. **Reboot Menu**
   - Reboot the device into different modes:
     - **fastboot**: Reboot into fastboot mode.
     - **bootloader**: Reboot into bootloader mode.
     - **system**: Reboot into the system.
     - **recovery**: Reboot into recovery mode.
     - **download**: Reboot into download mode.

### 2. **File Operations Menu**
   - **Push File**: Transfer a file from your computer to the device.
   - **Pull File**: Transfer a file from the device to your computer.
   - **Sideload File**: Sideload a ZIP file onto the device.

### 3. **Network Operations Menu**
   - **adb tcpip**: Enable ADB over TCP/IP (for wireless ADB).
   - **adb connect**: Connect to a device over TCP/IP using its IP address.

### 4. **Installed Apps Menu**
   - **List Installed Apps**: Display a list of all apps installed on the device.
   - **Install APK**: Install an APK file onto the device.
   - **Uninstall App**: Uninstall an app by package name.

### 5. **Logcat Menu**
   - **Show Logcat**: Display the device's logcat output.
   - **Clear Logcat**: Clear the current logcat buffer.
   - **Filter Logcat**: Filter the logcat output by log level (Error, Warning, Info, Debug, Verbose).

### 6. **System Operations Menu**
   - **Change System Settings**: Modify system settings such as screen brightness.
   - **Monitor CPU Usage**: Monitor CPU usage on the device.
   - **Disable System App**: Disable a system app.
   - **Clear App Data**: Clear the data of a specified app.
   - **Check Memory Status**: Check the device's memory usage.
   - **Set Lockscreen Password**: Set or change the lock screen password on the device.

### 7. **Backup Menu**
   - **Backup Data**: Backup device data to a specified location.
   - **Restore Data**: Restore data from a backup file.

### 8. **Trolling/Pranking Options (Harmless and Reversible)**
   - **Change Wallpaper**: Change the device wallpaper to a funny image.
   - **Change Notification Sound**: Modify the notification sound to something unusual.
   - **Change Device Name**: Rename the device to something humorous.
   - **Enable Vibration**: Enable vibration for every action.
   - **Enable Touch Sound**: Enable sound on touch events.
   - **Change Language**: Change the device's system language to something unexpected (e.g., Chinese).
   - **Change App Icon**: Change the icon of any app (if supported).
   - **Change Font Size**: Increase the font size to the maximum.
   - **Hide Clock**: Hide the clock in the notification bar.
   - **Change Settings Background**: Change the background of the Settings app (if supported).

## Requirements

- **Python 3.x**: Make sure you have Python installed on your system.
- **ADB**: Ensure that Android Debug Bridge (ADB) is installed and configured on your system.
- **Device with USB Debugging enabled**: USB Debugging should be enabled on the Android device.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/mleko777/adb-utility-script.git
   cd adb-utility-script
