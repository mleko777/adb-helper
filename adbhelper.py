import os

def print_header(text):
    print(f"\033[4m{text}\033[0m")

# == REBOOT MENU ==
def reboot_menu():
    print_header("== REBOOT MENU ==")
    print("1. fastboot")
    print("2. bootloader")
    print("3. system")
    print("4. recovery")
    print("5. download")
    print("6. Back")

    choice = input("Choose an option: ")

    if choice == "1":
        os.system("adb reboot fastboot")
    elif choice == "2":
        os.system("adb reboot bootloader")
    elif choice == "3":
        os.system("adb reboot")
    elif choice == "4":
        os.system("adb reboot recovery")
    elif choice == "5":
        os.system("adb reboot download")
    elif choice == "6":
        return
    else:
        print("Invalid choice.")
        reboot_menu()

# == FILE OPERATIONS MENU ==
def file_operations_menu():
    print_header("== FILE OPERATIONS MENU ==")
    print("1. adb push (send file to device)")
    print("2. adb pull (get file from device)")
    print("3. adb sideload (flash ZIP)")
    print("4. Back")

    choice = input("Choose an option: ")

    if choice == "1":
        push_file()
    elif choice == "2":
        pull_file()
    elif choice == "3":
        sideload_file()
    elif choice == "4":
        return
    else:
        print("Invalid choice.")
        file_operations_menu()

def push_file():
    src = input("Path to file on your computer: ")
    dst = input("Path on the device (e.g., /sdcard/): ")
    os.system(f'adb push "{src}" "{dst}"')

def pull_file():
    src = input("Path on the device (e.g., /sdcard/file.txt): ")
    dst = input("Destination path on your computer: ")
    os.system(f'adb pull "{src}" "{dst}"')

def sideload_file():
    path = input("Path to ZIP file for sideloading: ")
    os.system(f'adb sideload "{path}"')

# == NETWORK MENU ==
def network_operations_menu():
    print_header("== NETWORK MENU ==")
    print("1. adb tcpip (set device in TCP/IP mode)")
    print("2. adb connect (connect by IP)")
    print("3. Back")

    choice = input("Choose an option: ")

    if choice == "1":
        adb_tcpip()
    elif choice == "2":
        adb_connect()
    elif choice == "3":
        return
    else:
        print("Invalid choice.")
        network_operations_menu()

def adb_tcpip():
    port = input("Port (e.g., 5555): ")
    os.system(f"adb tcpip {port}")

def adb_connect():
    ip = input("Device IP (e.g., 192.168.1.100:5555): ")
    os.system(f"adb connect {ip}")

# == INSTALLED APPS MENU ==
def installed_apps_menu():
    print_header("== INSTALLED APPS MENU ==")
    print("1. List installed apps")
    print("2. Uninstall app")
    print("3. Install APK")
    print("4. Back")

    choice = input("Choose an option: ")

    if choice == "1":
        list_installed_apps()
    elif choice == "2":
        uninstall_app()
    elif choice == "3":
        install_apk()
    elif choice == "4":
        return
    else:
        print("Invalid choice.")
        installed_apps_menu()

def list_installed_apps():
    print_header("== List of Installed Apps ==")
    os.system("adb shell pm list packages")

def install_apk():
    path = input("Path to APK file: ")
    os.system(f'adb install "{path}"')

def uninstall_app():
    package = input("Package name to uninstall (e.g., com.example.app): ")
    os.system(f'adb uninstall "{package}"')

# == LOGCAT MENU ==
def logcat_menu():
    print_header("== LOGCAT MENU ==")
    print("1. Show logcat")
    print("2. Clear logcat")
    print("3. Filter logcat")
    print("4. Back")

    choice = input("Choose an option: ")

    if choice == "1":
        os.system("adb logcat")
    elif choice == "2":
        os.system("adb logcat -c")
    elif choice == "3":
        logcat_filter()
    elif choice == "4":
        return
    else:
        print("Invalid choice.")
        logcat_menu()

def logcat_filter():
    filter_type = input("Log filter: [E]rrors, [W]arnings, [I]nfo, [D]ebug, [V]erbose (default: All): ").upper()
    if filter_type == "E":
        os.system("adb logcat *:E")
    elif filter_type == "W":
        os.system("adb logcat *:W")
    elif filter_type == "I":
        os.system("adb logcat *:I")
    elif filter_type == "D":
        os.system("adb logcat *:D")
    elif filter_type == "V":
        os.system("adb logcat *:V")
    else:
        os.system("adb logcat")

# == SYSTEM OPERATIONS MENU ==
def system_operations_menu():
    print_header("== SYSTEM OPERATIONS MENU ==")
    print("1. Change system settings")
    print("2. Monitor CPU usage")
    print("3. Disable system app")
    print("4. Clear app data")
    print("5. Check memory status")
    print("6. Set lockscreen password")
    print("7. Back")

    choice = input("Choose an option: ")

    if choice == "1":
        change_system_settings()
    elif choice == "2":
        monitor_cpu_usage()
    elif choice == "3":
        disable_system_app()
    elif choice == "4":
        clear_app_data()
    elif choice == "5":
        check_memory_status()
    elif choice == "6":
        set_lockscreen_password()
    elif choice == "7":
        return
    else:
        print("Invalid choice.")
        system_operations_menu()

def change_system_settings():
    print_header("== Change System Settings ==")
    setting = input("Enter setting to change (e.g., 'screen_brightness'): ")
    value = input(f"Enter value for {setting}: ")
    os.system(f"adb shell settings put system {setting} {value}")
    print(f"Changed {setting} to {value}")

def monitor_cpu_usage():
    print_header("== Monitor CPU Usage ==")
    os.system("adb shell top -n 1")

def disable_system_app():
    package = input("Package name to disable (e.g., com.example.app): ")
    os.system(f'adb shell pm disable-user --user 0 "{package}"')
    print(f"Disabled app: {package}")

def clear_app_data():
    package = input("Package name to clear data (e.g., com.example.app): ")
    os.system(f'adb shell pm clear "{package}"')
    print(f"Cleared data for app: {package}")

def check_memory_status():
    print_header("== Check Memory Status ==")
    os.system("adb shell free")

def set_lockscreen_password():
    password = input("Enter lock screen password: ")
    os.system(f'adb shell lockscreen {password}')
    print("Lockscreen password set.")

# == BACKUP MENU ==
def backup_data():
    destination = input("Path to backup folder (e.g., /home/user/backup): ")
    os.system(f"adb backup -apk -shared -all -f {destination}/backup.ab")
    print(f"Backup saved to: {destination}/backup.ab")

def restore_data():
    backup_file = input("Choose backup file (e.g., backup.ab): ")
    os.system(f"adb restore {backup_file}")
    print("Restoring data from backup...")

# == MAIN MENU ==
def main():
    while True:
        print_header("== MAIN MENU ==")
        print("1. adb reboot...")
        print("2. Show connected devices")
        print("3. adb shell")
        print("4. File operations")
        print("5. Installed apps")
        print("6. Logcat operations")
        print("7. System operations")
        print("8. Backup data")
        print("9. Restore from backup")
        print("10. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            reboot_menu()
        elif choice == "2":
            os.system("adb devices")
        elif choice == "3":
            os.system("adb shell")
        elif choice == "4":
            file_operations_menu()
        elif choice == "5":
            installed_apps_menu()
        elif choice == "6":
            logcat_menu()
        elif choice == "7":
            system_operations_menu()
        elif choice == "8":
            backup_data()
        elif choice == "9":
            restore_data()
        elif choice == "10":
            print("Closing...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
