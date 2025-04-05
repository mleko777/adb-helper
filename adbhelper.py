import os

def print_header(text):
    print(f"\033[4m{text}\033[0m")

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

def push_file():
    src = input("Path to file on your computer: ")
    dst = input("Path on the device (e.g., /sdcard/): ")
    os.system(f'adb push "{src}" "{dst}"')

def pull_file():
    src = input("Path on the device (e.g., /sdcard/file.txt): ")
    dst = input("Destination path on your computer: ")
    os.system(f'adb pull "{src}" "{dst}"')

def install_apk():
    path = input("Path to APK file: ")
    os.system(f'adb install "{path}"')

def uninstall_app():
    package = input("Package name to uninstall (e.g., com.example.app): ")
    os.system(f'adb uninstall "{package}"')

def sideload_file():
    path = input("Path to ZIP file for sideloading: ")
    os.system(f'adb sideload "{path}"')

def adb_tcpip():
    port = input("Port (e.g., 5555): ")
    os.system(f"adb tcpip {port}")

def adb_connect():
    ip = input("Device IP (e.g., 192.168.1.100:5555): ")
    os.system(f"adb connect {ip}")

def list_installed_apps():
    print_header("== List of Installed Apps ==")
    os.system("adb shell pm list packages")

def screenshot():
    filename = input("Filename to save (e.g., screenshot.png): ")
    os.system(f'adb exec-out screencap -p > "{filename}"')
    print(f"Saved screenshot as: {filename}")

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

def backup_data():
    destination = input("Path to backup folder (e.g., /home/user/backup): ")
    os.system(f"adb backup -apk -shared -all -f {destination}/backup.ab")
    print(f"Backup saved to: {destination}/backup.ab")

def restore_data():
    backup_file = input("Choose backup file (e.g., backup.ab): ")
    os.system(f"adb restore {backup_file}")
    print("Restoring data from backup...")

def main():
    while True:
        print_header("== MAIN MENU ==")
        print("1. adb reboot...")
        print("2. Show connected devices")
        print("3. adb shell")
        print("4. adb push (send file to device)")
        print("5. adb pull (get file from device)")
        print("6. adb install (install APK)")
        print("7. adb uninstall (uninstall app)")
        print("8. adb sideload (flash ZIP)")
        print("9. adb tcpip (network connection)")
        print("10. adb connect (connect by IP)")
        print("11. adb logcat (logs)")
        print("12. adb logcat -c (clear logs)")
        print("13. Logcat filtering")
        print("14. List installed apps")
        print("15. Take screenshot")
        print("16. Backup data")
        print("17. Restore from backup")
        print("18. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            reboot_menu()
        elif choice == "2":
            os.system("adb devices")
        elif choice == "3":
            os.system("adb shell")
        elif choice == "4":
            push_file()
        elif choice == "5":
            pull_file()
        elif choice == "6":
            install_apk()
        elif choice == "7":
            uninstall_app()
        elif choice == "8":
            sideload_file()
        elif choice == "9":
            adb_tcpip()
        elif choice == "10":
            adb_connect()
        elif choice == "11":
            os.system("adb logcat")
        elif choice == "12":
            os.system("adb logcat -c")
        elif choice == "13":
            logcat_filter()
        elif choice == "14":
            list_installed_apps()
        elif choice == "15":
            screenshot()
        elif choice == "16":
            backup_data()
        elif choice == "17":
            restore_data()
        elif choice == "18":
            print("Closing...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

