import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
from time import sleep
from threading import Thread
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO
import json
from datetime import datetime

# Check and install required packages
def install_packages():
    required = ['pillow', 'requests']
    for package in required:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", package])

install_packages()

class ADBHelperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Helper v2.0 - Enhanced")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)

        # Theme settings
        self.dark_mode = True
        self.set_theme()

        self.setup_ui()
        self.check_adb_installation()

        # Load icon (with fallback)
        try:
            icon_url = "https://raw.githubusercontent.com/mleko777/adb-helper/main/icon.png"
            response = requests.get(icon_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            photo = ImageTk.PhotoImage(img)
            self.root.iconphoto(False, photo)
        except Exception as e:
            self.print_to_console(f"Error loading icon: {str(e)}", error=True)

        # Initialize new features
        self.process_monitor_running = False
        self.resource_monitor_thread = None
        self.batch_operations = []
        self.permission_history = []

    def set_theme(self):
        """Set light/dark theme"""
        if self.dark_mode:
            self.root.tk_setPalette(background='#2d2d2d', foreground='white',
                                   activeBackground='#3d3d3d', activeForeground='white')
            style = ttk.Style()
            style.theme_use('alt')
            style.configure('.', background='#2d2d2d', foreground='white')
            style.map('.', background=[('selected', '#3d3d3d')])
        else:
            self.root.tk_setPalette(background='#f0f0f0', foreground='black',
                                   activeBackground='#e0e0e0', activeForeground='black')
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('.', background='#f0f0f0', foreground='black')
            style.map('.', background=[('selected', '#e0e0e0')])

    def check_adb_installation(self):
        """Check if ADB is installed and in PATH"""
        try:
            subprocess.run(['adb', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.print_to_console("ADB detected and working properly")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.print_to_console("ADB not found or not working properly", error=True)
            if messagebox.askyesno("ADB Not Found", "ADB is not installed or not in PATH. Would you like to install it?"):
                self.install_adb()
            return False

    def install_adb(self):
        """Install ADB on the system"""
        try:
            if sys.platform == 'win32':
                url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
            elif sys.platform == 'darwin':
                url = "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip"
            else:  # linux
                url = "https://dl.google.com/android/repository/platform-tools-latest-linux.zip"

            self.print_to_console(f"Downloading ADB from {url}")
            response = requests.get(url, stream=True)
            with open('platform-tools.zip', 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.print_to_console("Extracting ADB...")
            import zipfile
            with zipfile.ZipFile('platform-tools.zip', 'r') as zip_ref:
                zip_ref.extractall()

            # Add to PATH
            if sys.platform == 'win32':
                os.environ['PATH'] += os.pathsep + os.path.abspath('platform-tools')
                # Add to system PATH (requires admin)
                try:
                    subprocess.run(['setx', 'PATH', f'%PATH%;{os.path.abspath("platform-tools")}'], check=True, shell=True)
                except subprocess.CalledProcessError:
                    self.print_to_console("Could not add ADB to system PATH (admin required)", error=True)
            else:
                os.environ['PATH'] += os.pathsep + os.path.abspath('platform-tools')
                # Add to .bashrc or similar
                try:
                    with open(os.path.expanduser('~/.bashrc'), 'a') as f:
                        f.write(f'\nexport PATH="$PATH:{os.path.abspath("platform-tools")}"\n')
                except Exception as e:
                    self.print_to_console(f"Could not add ADB to .bashrc: {str(e)}", error=True)

            self.print_to_console("ADB installed successfully. Please restart the application.")
            messagebox.showinfo("Success", "ADB installed successfully. Please restart the application.")
            self.root.destroy()
        except Exception as e:
            self.print_to_console(f"Error installing ADB: {str(e)}", error=True)
            messagebox.showerror("Error", f"Failed to install ADB: {str(e)}")

    def print_to_console(self, message, error=False):
        """Print message to console with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.configure(state='normal')
        self.console.insert(tk.END, f"[{timestamp}] {message}\n", "error" if error else "normal")
        self.console.configure(state='disabled')
        self.console.see(tk.END)

    def run_command(self, command):
        """Run ADB command and return output"""
        try:
            result = subprocess.run(command, shell=True, check=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.print_to_console(f"Command executed: {command}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.print_to_console(f"Error executing command: {command}\n{e.stderr}", error=True)
            return None

    def setup_ui(self):
        """Setup the main UI"""
        # Menu
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        tools_menu.add_command(label="Check ADB", command=self.check_adb_installation)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_docs)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_device_tab()
        self.create_file_tab()
        self.create_apps_tab()
        self.create_logcat_tab()
        self.create_system_tab()
        self.create_backup_tab()
        self.create_settings_tab()

        # New advanced tabs
        self.create_advanced_file_tab()
        self.create_app_manager_tab()
        self.create_resource_monitor_tab()
        self.create_permission_manager_tab()
        self.create_terminal_tab()

        # Console
        console_frame = ttk.LabelFrame(main_frame, text="Console")
        console_frame.pack(fill=tk.X, padx=5, pady=5)

        self.console = scrolledtext.ScrolledText(console_frame, height=8)
        self.console.pack(fill=tk.BOTH, expand=True)
        self.console.configure(state='disabled')

    def create_device_tab(self):
        """Create device info tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Device")

        # Device info
        ttk.Label(tab, text="Device Information:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.device_info = scrolledtext.ScrolledText(tab, height=10)
        self.device_info.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.device_info.configure(state='disabled')

        # Buttons
        ttk.Button(tab, text="Refresh", command=self.update_device_info).grid(row=2, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Reboot", command=lambda: self.run_command("adb reboot")).grid(row=2, column=1, sticky=tk.EW, pady=2)

        # Connection
        ttk.Label(tab, text="Connect to Device:").grid(row=3, column=0, sticky=tk.W, pady=5)

        ttk.Label(tab, text="IP Address:").grid(row=4, column=0, sticky=tk.W)
        self.ip_entry = ttk.Entry(tab)
        self.ip_entry.grid(row=4, column=1, sticky=tk.EW)

        ttk.Button(tab, text="Connect", command=self.connect_device).grid(row=5, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Disconnect", command=lambda: self.run_command("adb disconnect")).grid(row=5, column=1, sticky=tk.EW, pady=2)

        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(1, weight=1)

    def create_file_tab(self):
        """Create file manager tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Files")

        # Local files
        ttk.Label(tab, text="Local Files:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.local_files = tk.Listbox(tab, height=12)
        self.local_files.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        ttk.Button(tab, text="Browse", command=self.browse_local_files).grid(row=2, column=0, sticky=tk.EW, pady=2)

        # Device files
        ttk.Label(tab, text="Device Files:").grid(row=0, column=1, sticky=tk.W, pady=5)
        self.device_files = tk.Listbox(tab, height=12)
        self.device_files.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

        ttk.Button(tab, text="Browse Device", command=self.browse_device_files).grid(row=2, column=1, sticky=tk.EW, pady=2)

        # File operations
        ttk.Button(tab, text="Push →", command=self.push_file).grid(row=3, column=0, sticky=tk.EW, pady=5)
        ttk.Button(tab, text="← Pull", command=self.pull_file).grid(row=3, column=1, sticky=tk.EW, pady=5)
        ttk.Button(tab, text="Delete", command=self.delete_device_file).grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=2)

        # Current path
        ttk.Label(tab, text="Current Path:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.device_path = ttk.Entry(tab)
        self.device_path.insert(0, "/sdcard/")
        self.device_path.grid(row=5, column=1, sticky=tk.EW, pady=5)

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(1, weight=1)

    def create_apps_tab(self):
        """Create apps manager tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Apps")

        # App list
        ttk.Label(tab, text="Installed Apps:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.app_list = tk.Listbox(tab, height=15)
        self.app_list.grid(row=1, column=0, rowspan=4, sticky=tk.NSEW, padx=5, pady=5)

        # App controls
        ttk.Button(tab, text="Refresh", command=self.refresh_app_list).grid(row=5, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Uninstall", command=self.uninstall_app).grid(row=6, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Launch", command=self.launch_app).grid(row=7, column=0, sticky=tk.EW, pady=2)

        # App info
        ttk.Label(tab, text="App Info:").grid(row=0, column=1, sticky=tk.W, pady=5)
        self.app_info = scrolledtext.ScrolledText(tab, height=10)
        self.app_info.grid(row=1, column=1, rowspan=3, sticky=tk.NSEW, padx=5, pady=5)
        self.app_info.configure(state='disabled')

        # App filter
        ttk.Label(tab, text="Filter:").grid(row=4, column=1, sticky=tk.W)
        self.app_filter = ttk.Entry(tab)
        self.app_filter.grid(row=4, column=1, sticky=tk.EW, padx=5)
        self.app_filter.bind('<KeyRelease>', self.filter_apps)

        # App operations
        ttk.Button(tab, text="Show Info", command=self.show_app_info).grid(row=5, column=1, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Clear Data", command=self.clear_app_data).grid(row=6, column=1, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Backup APK", command=self.backup_apk).grid(row=7, column=1, sticky=tk.EW, pady=2)

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(1, weight=1)

    def create_logcat_tab(self):
        """Create logcat viewer tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Logcat")

        # Logcat controls
        ttk.Button(tab, text="Start Logcat", command=self.start_logcat).grid(row=0, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Stop Logcat", command=self.stop_logcat).grid(row=0, column=1, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Clear", command=self.clear_logcat).grid(row=0, column=2, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Save Log", command=self.save_logcat).grid(row=0, column=3, sticky=tk.EW, pady=2)

        # Logcat filters
        ttk.Label(tab, text="Filter:").grid(row=1, column=0, sticky=tk.W)
        self.logcat_filter = ttk.Entry(tab)
        self.logcat_filter.grid(row=1, column=1, columnspan=3, sticky=tk.EW, pady=2)

        # Logcat output
        self.logcat_output = scrolledtext.ScrolledText(tab, height=20)
        self.logcat_output.grid(row=2, column=0, columnspan=4, sticky=tk.NSEW, pady=5)
        self.logcat_output.configure(state='disabled')

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(2, weight=1)
        tab.columnconfigure(3, weight=1)
        tab.rowconfigure(2, weight=1)

    def create_system_tab(self):
        """Create system tools tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="System")

        # Reboot options
        ttk.Label(tab, text="Reboot Options:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Button(tab, text="Reboot Normal", command=lambda: self.run_command("adb reboot")).grid(row=1, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Reboot Recovery", command=lambda: self.run_command("adb reboot recovery")).grid(row=2, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Reboot Bootloader", command=lambda: self.run_command("adb reboot bootloader")).grid(row=3, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Reboot Fastboot", command=lambda: self.run_command("adb reboot fastboot")).grid(row=4, column=0, sticky=tk.EW, pady=2)

        # Screenshot
        ttk.Label(tab, text="Screenshot:").grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Button(tab, text="Take Screenshot", command=self.take_screenshot).grid(row=1, column=1, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Record Screen", command=self.record_screen).grid(row=2, column=1, sticky=tk.EW, pady=2)

        # System info
        ttk.Label(tab, text="System Info:").grid(row=0, column=2, sticky=tk.W, pady=5)
        ttk.Button(tab, text="Get Prop", command=self.get_system_prop).grid(row=1, column=2, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Battery Info", command=self.get_battery_info).grid(row=2, column=2, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="CPU Info", command=self.get_cpu_info).grid(row=3, column=2, sticky=tk.EW, pady=2)

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(2, weight=1)

    def create_backup_tab(self):
        """Create backup/restore tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Backup")

        # Backup options
        ttk.Label(tab, text="Backup Options:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Button(tab, text="Full Backup", command=self.create_full_backup).grid(row=1, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Full Restore", command=self.restore_full_backup).grid(row=2, column=0, sticky=tk.EW, pady=2)

        # Partition backup
        ttk.Label(tab, text="Partition Backup:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Button(tab, text="Backup Boot", command=lambda: self.backup_partition("boot")).grid(row=4, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Backup Recovery", command=lambda: self.backup_partition("recovery")).grid(row=5, column=0, sticky=tk.EW, pady=2)

        # Backup info
        ttk.Label(tab, text="Backup Location:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.backup_path = ttk.Entry(tab)
        self.backup_path.insert(0, os.path.expanduser("~/adb_backups"))
        self.backup_path.grid(row=7, column=0, sticky=tk.EW, pady=2)

        tab.columnconfigure(0, weight=1)

    def create_settings_tab(self):
        """Create settings tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Settings")

        # ADB settings
        ttk.Label(tab, text="ADB Settings:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Button(tab, text="Kill Server", command=lambda: self.run_command("adb kill-server")).grid(row=1, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Start Server", command=lambda: self.run_command("adb start-server")).grid(row=2, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Devices", command=lambda: self.run_command("adb devices -l")).grid(row=3, column=0, sticky=tk.EW, pady=2)

        # UI settings
        ttk.Label(tab, text="UI Settings:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Button(tab, text="Toggle Theme", command=self.toggle_theme).grid(row=5, column=0, sticky=tk.EW, pady=2)

        tab.columnconfigure(0, weight=1)

    def create_advanced_file_tab(self):
        """New tab for advanced file operations"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Advanced Files")

        # Batch operations
        ttk.Label(tab, text="Batch Operations:").grid(row=0, column=0, sticky=tk.W, pady=5)

        ttk.Button(tab, text="Add Files to Batch",
                 command=self.add_to_batch).grid(row=1, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Execute Batch",
                 command=self.execute_batch).grid(row=2, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Clear Batch",
                 command=self.clear_batch).grid(row=3, column=0, sticky=tk.EW, pady=2)

        self.batch_listbox = tk.Listbox(tab, height=8)
        self.batch_listbox.grid(row=4, column=0, sticky=tk.NSEW, pady=5)

        # Permissions manager
        ttk.Label(tab, text="Permissions Manager:").grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(tab, text="Path:").grid(row=1, column=1, sticky=tk.W)
        self.perm_path_entry = ttk.Entry(tab)
        self.perm_path_entry.grid(row=1, column=2, sticky=tk.EW)

        ttk.Label(tab, text="Permissions (e.g. 755):").grid(row=2, column=1, sticky=tk.W)
        self.perm_value_entry = ttk.Entry(tab)
        self.perm_value_entry.grid(row=2, column=2, sticky=tk.EW)

        ttk.Button(tab, text="Set Permissions",
                 command=self.set_permissions).grid(row=3, column=1, columnspan=2, sticky=tk.EW)

        # File search
        ttk.Label(tab, text="File Search:").grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=5)

        ttk.Label(tab, text="Search term:").grid(row=6, column=0, sticky=tk.W)
        self.search_entry = ttk.Entry(tab)
        self.search_entry.grid(row=6, column=1, sticky=tk.EW)

        ttk.Button(tab, text="Search",
                 command=self.search_files).grid(row=6, column=2, sticky=tk.EW)

        self.search_results = scrolledtext.ScrolledText(tab, height=8)
        self.search_results.grid(row=7, column=0, columnspan=3, sticky=tk.NSEW)
        self.search_results.configure(state='disabled')

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(2, weight=1)
        tab.rowconfigure(4, weight=1)
        tab.rowconfigure(7, weight=1)

    def create_app_manager_tab(self):
        """Extended app management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Advanced Apps")

        # App backup with data
        ttk.Label(tab, text="App Backup with Data:").grid(row=0, column=0, sticky=tk.W, pady=5)

        ttk.Button(tab, text="Backup App + Data",
                 command=self.backup_app_with_data).grid(row=1, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Restore App + Data",
                 command=self.restore_app_with_data).grid(row=2, column=0, sticky=tk.EW, pady=2)

        # App migration
        ttk.Label(tab, text="App Migration:").grid(row=3, column=0, sticky=tk.W, pady=5)

        ttk.Button(tab, text="Prepare Migration",
                 command=self.prepare_migration).grid(row=4, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Complete Migration",
                 command=self.complete_migration).grid(row=5, column=0, sticky=tk.EW, pady=2)

        # App blocking
        ttk.Label(tab, text="App Control:").grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Button(tab, text="Disable App",
                 command=self.disable_app).grid(row=1, column=1, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Enable App",
                 command=self.enable_app).grid(row=2, column=1, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Force Dark Mode",
                 command=self.force_dark_mode).grid(row=3, column=1, sticky=tk.EW, pady=2)

        # Battery optimization
        ttk.Label(tab, text="Battery Optimization:").grid(row=4, column=1, sticky=tk.W, pady=5)

        ttk.Button(tab, text="Check Optimization",
                 command=self.check_battery_optimization).grid(row=5, column=1, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Disable Optimization",
                 command=self.disable_battery_optimization).grid(row=6, column=1, sticky=tk.EW, pady=2)

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)

    def create_resource_monitor_tab(self):
        """System resource monitoring tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Resource Monitor")

        # CPU Monitor
        ttk.Label(tab, text="CPU Usage:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cpu_usage_label = ttk.Label(tab, text="0%")
        self.cpu_usage_label.grid(row=0, column=1, sticky=tk.E)

        # Memory Monitor
        ttk.Label(tab, text="Memory Usage:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.memory_usage_label = ttk.Label(tab, text="0 MB / 0 MB")
        self.memory_usage_label.grid(row=1, column=1, sticky=tk.E)

        # Battery Monitor
        ttk.Label(tab, text="Battery Level:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.battery_level_label = ttk.Label(tab, text="0%")
        self.battery_level_label.grid(row=2, column=1, sticky=tk.E)

        # Controls
        ttk.Button(tab, text="Start Monitoring",
                 command=self.start_resource_monitoring).grid(row=3, column=0, pady=10, sticky=tk.EW)
        ttk.Button(tab, text="Stop Monitoring",
                 command=self.stop_resource_monitoring).grid(row=3, column=1, pady=10, sticky=tk.EW)

        # Process list
        ttk.Label(tab, text="Running Processes:").grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.process_listbox = tk.Listbox(tab, height=12)
        self.process_listbox.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW)

        # Process controls
        ttk.Button(tab, text="Refresh Processes",
                 command=self.refresh_processes).grid(row=6, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Kill Process",
                 command=self.kill_process).grid(row=6, column=1, sticky=tk.EW, pady=2)

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(5, weight=1)

    def create_permission_manager_tab(self):
        """Permissions management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Permissions")

        # App permissions
        ttk.Label(tab, text="App Permissions:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.permission_app_list = tk.Listbox(tab, height=12, selectmode=tk.SINGLE)
        self.permission_app_list.grid(row=1, column=0, rowspan=4, sticky=tk.NSEW, padx=5, pady=5)

        ttk.Button(tab, text="Refresh Apps",
                 command=self.refresh_permission_apps).grid(row=5, column=0, sticky=tk.EW, pady=2)

        # Permission details
        ttk.Label(tab, text="Permission Details:").grid(row=0, column=1, sticky=tk.W, pady=5)
        self.permission_details = scrolledtext.ScrolledText(tab, height=10)
        self.permission_details.grid(row=1, column=1, rowspan=3, sticky=tk.NSEW, padx=5, pady=5)
        self.permission_details.configure(state='disabled')

        # Permission controls
        ttk.Button(tab, text="Show Permissions",
                 command=self.show_app_permissions).grid(row=4, column=1, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Revoke Permission",
                 command=self.revoke_permission).grid(row=5, column=1, sticky=tk.EW, pady=2)

        # Dangerous permissions
        ttk.Label(tab, text="Dangerous Permissions:").grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.dangerous_perms_list = scrolledtext.ScrolledText(tab, height=6)
        self.dangerous_perms_list.grid(row=7, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        self.dangerous_perms_list.configure(state='disabled')

        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(1, weight=1)
        tab.rowconfigure(7, weight=1)

    def create_terminal_tab(self):
        """Built-in terminal tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Terminal")

        # Terminal input
        ttk.Label(tab, text="ADB Shell:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.terminal_entry = ttk.Entry(tab)
        self.terminal_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.terminal_entry.bind('<Return>', self.execute_terminal_command)

        ttk.Button(tab, text="Execute",
                 command=lambda: self.execute_terminal_command(None)).grid(row=0, column=2, sticky=tk.EW)

        # Terminal output
        self.terminal_output = scrolledtext.ScrolledText(tab, height=20)
        self.terminal_output.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, pady=5)
        self.terminal_output.configure(state='disabled')

        # History
        ttk.Button(tab, text="Clear",
                 command=self.clear_terminal).grid(row=2, column=0, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="Save Output",
                 command=self.save_terminal_output).grid(row=2, column=1, sticky=tk.EW, pady=2)
        ttk.Button(tab, text="History",
                 command=self.show_terminal_history).grid(row=2, column=2, sticky=tk.EW, pady=2)

        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(1, weight=1)

    # Device tab methods
    def update_device_info(self):
        """Update device information"""
        try:
            info = subprocess.check_output("adb shell getprop", shell=True, text=True)
            self.device_info.configure(state='normal')
            self.device_info.delete(1.0, tk.END)
            self.device_info.insert(tk.END, info)
            self.device_info.configure(state='disabled')
            self.print_to_console("Device info updated")
        except subprocess.CalledProcessError as e:
            self.print_to_console(f"Error getting device info: {str(e)}", error=True)

    def connect_device(self):
        """Connect to device via IP"""
        ip = self.ip_entry.get()
        if not ip:
            messagebox.showerror("Error", "IP address is required")
            return

        if self.run_command(f"adb connect {ip}"):
            self.print_to_console(f"Connected to {ip}")
            self.update_device_info()

    # File tab methods
    def browse_local_files(self):
        """Browse local files"""
        path = filedialog.askdirectory()
        if path:
            self.local_files.delete(0, tk.END)
            try:
                for item in os.listdir(path):
                    self.local_files.insert(tk.END, os.path.join(path, item))
            except Exception as e:
                self.print_to_console(f"Error browsing local files: {str(e)}", error=True)

    def browse_device_files(self):
        """Browse device files"""
        path = self.device_path.get()
        if not path:
            path = "/sdcard/"

        try:
            result = subprocess.check_output(f'adb shell ls "{path}"', shell=True, text=True)
            self.device_files.delete(0, tk.END)
            for line in result.split('\n'):
                if line.strip():
                    self.device_files.insert(tk.END, line)
        except subprocess.CalledProcessError as e:
            self.print_to_console(f"Error browsing device files: {str(e)}", error=True)

    def push_file(self):
        """Push file to device"""
        selection = self.local_files.curselection()
        if not selection:
            messagebox.showerror("Error", "No file selected")
            return

        local_file = self.local_files.get(selection[0])
        device_path = self.device_path.get()
        if not device_path:
            device_path = "/sdcard/"

        if self.run_command(f'adb push "{local_file}" "{device_path}"'):
            self.print_to_console(f"Pushed {local_file} to {device_path}")
            self.browse_device_files()

    def pull_file(self):
        """Pull file from device"""
        selection = self.device_files.curselection()
        if not selection:
            messagebox.showerror("Error", "No file selected")
            return

        device_file = self.device_files.get(selection[0])
        local_path = filedialog.askdirectory()
        if local_path:
            if self.run_command(f'adb pull "{device_file}" "{local_path}"'):
                self.print_to_console(f"Pulled {device_file} to {local_path}")

    def delete_device_file(self):
        """Delete file on device"""
        selection = self.device_files.curselection()
        if not selection:
            messagebox.showerror("Error", "No file selected")
            return

        device_file = self.device_files.get(selection[0])
        if messagebox.askyesno("Confirm", f"Delete {device_file}?"):
            if self.run_command(f'adb shell rm -rf "{device_file}"'):
                self.print_to_console(f"Deleted {device_file}")
                self.browse_device_files()

    # Apps tab methods
    def refresh_app_list(self):
        """Refresh list of installed apps"""
        try:
            apps = subprocess.check_output("adb shell pm list packages -3", shell=True, text=True).split('\n')
            self.app_list.delete(0, tk.END)
            for app in apps:
                if app.strip():
                    self.app_list.insert(tk.END, app.replace("package:", ""))
            self.print_to_console("App list refreshed")
        except subprocess.CalledProcessError as e:
            self.print_to_console(f"Error refreshing app list: {str(e)}", error=True)

    def filter_apps(self, event):
        """Filter apps based on search term"""
        term = self.app_filter.get().lower()
        if not term:
            self.refresh_app_list()
            return

        try:
            apps = subprocess.check_output("adb shell pm list packages -3", shell=True, text=True).split('\n')
            self.app_list.delete(0, tk.END)
            for app in apps:
                if app.strip() and term in app.lower():
                    self.app_list.insert(tk.END, app.replace("package:", ""))
        except subprocess.CalledProcessError as e:
            self.print_to_console(f"Error filtering apps: {str(e)}", error=True)

    def show_app_info(self):
        """Show info about selected app"""
        selection = self.app_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No app selected")
            return

        package = self.app_list.get(selection[0])
        try:
            info = subprocess.check_output(f"adb shell dumpsys package {package}", shell=True, text=True)
            self.app_info.configure(state='normal')
            self.app_info.delete(1.0, tk.END)
            self.app_info.insert(tk.END, info)
            self.app_info.configure(state='disabled')
            self.print_to_console(f"Showing info for {package}")
        except subprocess.CalledProcessError as e:
            self.print_to_console(f"Error getting app info: {str(e)}", error=True)

    def uninstall_app(self):
        """Uninstall selected app"""
        selection = self.app_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No app selected")
            return

        package = self.app_list.get(selection[0])
        if messagebox.askyesno("Confirm", f"Uninstall {package}?"):
            if self.run_command(f"adb uninstall {package}"):
                self.print_to_console(f"Uninstalled {package}")
                self.refresh_app_list()

    def launch_app(self):
        """Launch selected app"""
        selection = self.app_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No app selected")
            return

        package = self.app_list.get(selection[0])
        if self.run_command(f"adb shell monkey -p {package} -c android.intent.category.LAUNCHER 1"):
            self.print_to_console(f"Launched {package}")

    def clear_app_data(self):
        """Clear data for selected app"""
        selection = self.app_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No app selected")
            return

        package = self.app_list.get(selection[0])
        if messagebox.askyesno("Confirm", f"Clear data for {package}?"):
            if self.run_command(f"adb shell pm clear {package}"):
                self.print_to_console(f"Cleared data for {package}")

    def backup_apk(self):
        """Backup APK of selected app"""
        selection = self.app_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No app selected")
            return

        package = self.app_list.get(selection[0])
        filename = filedialog.asksaveasfilename(
            title=f"Backup {package} APK",
            defaultextension=".apk",
            filetypes=[("APK Files", "*.apk")]
        )

        if filename:
            if self.run_command(f"adb pull $(adb shell pm path {package} | cut -d: -f2) {filename}"):
                self.print_to_console(f"Backed up {package} to {filename}")

    # Logcat tab methods
    def start_logcat(self):
        """Start logcat in a separate thread"""
        if hasattr(self, 'logcat_process') and self.logcat_process.poll() is None:
            self.print_to_console("Logcat already running")
            return

        filter_text = self.logcat_filter.get()
        command = "adb logcat"
        if filter_text:
            command += f" | grep {filter_text}"

        self.logcat_process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        self.logcat_thread = Thread(target=self._read_logcat)
        self.logcat_thread.daemon = True
        self.logcat_thread.start()
        self.print_to_console("Logcat started")

    def _read_logcat(self):
        """Read logcat output continuously"""
        while True:
            line = self.logcat_process.stdout.readline()
            if not line:
                break

            self.root.after(0, self._update_logcat, line)

    def _update_logcat(self, line):
        """Update logcat display"""
        self.logcat_output.configure(state='normal')
        self.logcat_output.insert(tk.END, line)
        self.logcat_output.see(tk.END)
        self.logcat_output.configure(state='disabled')

    def stop_logcat(self):
        """Stop logcat process"""
        if hasattr(self, 'logcat_process'):
            self.logcat_process.terminate()
            self.print_to_console("Logcat stopped")

    def clear_logcat(self):
        """Clear logcat display"""
        self.logcat_output.configure(state='normal')
        self.logcat_output.delete(1.0, tk.END)
        self.logcat_output.configure(state='disabled')
        self.print_to_console("Logcat cleared")

    def save_logcat(self):
        """Save logcat to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Logcat",
            defaultextension=".log",
            filetypes=[("Log Files", "*.log")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.logcat_output.get(1.0, tk.END))
                self.print_to_console(f"Logcat saved to {filename}")
            except Exception as e:
                self.print_to_console(f"Error saving logcat: {str(e)}", error=True)

    # System tab methods
    def take_screenshot(self):
        """Take device screenshot"""
        filename = filedialog.asksaveasfilename(
            title="Save Screenshot",
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png")]
        )

        if filename:
            if self.run_command(f"adb exec-out screencap -p > {filename}"):
                self.print_to_console(f"Screenshot saved to {filename}")

    def record_screen(self):
        """Record device screen"""
        filename = filedialog.asksaveasfilename(
            title="Save Screen Recording",
            defaultextension=".mp4",
            filetypes=[("MP4 Files", "*.mp4")]
        )

        if filename:
            duration = simpledialog.askinteger("Duration", "Recording duration (seconds):", minvalue=1, maxvalue=300)
            if duration:
                self.print_to_console(f"Recording screen for {duration} seconds...")
                if self.run_command(f"adb shell screenrecord --verbose --time-limit {duration} /sdcard/temp.mp4"):
                    if self.run_command(f"adb pull /sdcard/temp.mp4 {filename}"):
                        self.run_command("adb shell rm /sdcard/temp.mp4")
                        self.print_to_console(f"Screen recording saved to {filename}")

    def get_system_prop(self):
        """Get system properties"""
        try:
            props = subprocess.check_output("adb shell getprop", shell=True, text=True)
            self.print_to_console("System properties:\n" + props)
        except subprocess.CalledProcessError as e:
            self.print_to_console(f"Error getting system props: {str(e)}", error=True)

    def get_battery_info(self):
        """Get battery information"""
        try:
            info = subprocess.check_output("adb shell dumpsys battery", shell=True, text=True)
            self.print_to_console("Battery info:\n" + info)
        except subprocess.CalledProcessError as e:
            self.print_to_console(f"Error getting battery info: {str(e)}", error=True)

    def get_cpu_info(self):
        """Get CPU information"""
        try:
            info = subprocess.check_output("adb shell cat /proc/cpuinfo", shell=True, text=True)
            self.print_to_console("CPU info:\n" + info)
        except subprocess.CalledProcessError as e:
            self.print_to_console(f"Error getting CPU info: {str(e)}", error=True)

    # Backup tab methods
    def create_full_backup(self):
        """Create full device backup"""
        filename = filedialog.asksaveasfilename(
            title="Save Backup",
            defaultextension=".ab",
            filetypes=[("Android Backup", "*.ab")]
        )

        if filename:
            if self.run_command(f"adb backup -apk -shared -all -f {filename}"):
                self.print_to_console(f"Full backup created: {filename}")

    def restore_full_backup(self):
        """Restore full device backup"""
        filename = filedialog.askopenfilename(
            title="Select Backup File",
            filetypes=[("Android Backup", "*.ab")]
        )

        if filename:
            if messagebox.askyesno("Confirm", "Restore backup? Device will reboot."):
                if self.run_command(f"adb restore {filename}"):
                    self.print_to_console(f"Restoring backup: {filename}")

    def backup_partition(self, partition):
        """Backup device partition"""
        filename = filedialog.asksaveasfilename(
            title=f"Save {partition.capitalize()} Backup",
            defaultextension=".img",
            filetypes=[("Image Files", "*.img")]
        )

        if filename:
            if self.run_command(f"adb shell su -c dd if=/dev/block/bootdevice/by-name/{partition} | adb shell cat > {filename}"):
                self.print_to_console(f"{partition.capitalize()} backup saved to {filename}")

    # Settings tab methods
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.dark_mode = not self.dark_mode
        self.set_theme()
        self.print_to_console(f"Theme changed to {'dark' if self.dark_mode else 'light'}")

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", "ADB Helper v2.0\n\nA made by mleko|avisdada")

    def show_docs(self):
        """Open documentation in browser"""
        webbrowser.open("https://github.com/mleko777/adb-helper")

    # New methods for advanced file operations
    def add_to_batch(self):
        """Add files to batch operations"""
        files = filedialog.askopenfilenames(title="Select files for batch operation")
        if files:
            for file in files:
                self.batch_operations.append(('push', file, "/sdcard/"))
                self.batch_listbox.insert(tk.END, f"Push: {file} → /sdcard/")
            self.print_to_console(f"Added {len(files)} files to batch")

    def execute_batch(self):
        """Execute batch operations"""
        if not self.batch_operations:
            messagebox.showwarning("Warning", "No operations in batch")
            return

        for operation in self.batch_operations:
            op_type, src, dst = operation
            if op_type == 'push':
                self.run_command(f'adb push "{src}" "{dst}"')
            elif op_type == 'pull':
                self.run_command(f'adb pull "{src}" "{dst}"')

        self.print_to_console(f"Executed {len(self.batch_operations)} batch operations")
        self.batch_operations.clear()
        self.batch_listbox.delete(0, tk.END)

    def clear_batch(self):
        """Clear batch operations list"""
        self.batch_operations.clear()
        self.batch_listbox.delete(0, tk.END)
        self.print_to_console("Cleared batch operations")

    def set_permissions(self):
        """Set permissions for file/folder"""
        path = self.perm_path_entry.get()
        perm = self.perm_value_entry.get()

        if not path or not perm:
            messagebox.showerror("Error", "Path and permissions are required")
            return

        if self.run_command(f'adb shell chmod {perm} "{path}"'):
            self.print_to_console(f"Set permissions {perm} for {path}")
            self.permission_history.append((path, perm, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def search_files(self):
        """Search for files on device"""
        term = self.search_entry.get()
        if not term:
            messagebox.showerror("Error", "Search term is required")
            return

        self.search_results.configure(state='normal')
        self.search_results.delete(1.0, tk.END)

        try:
            result = subprocess.check_output(f'adb shell find / -name "*{term}*" 2>/dev/null',
                                          shell=True, text=True)
            self.search_results.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            self.search_results.insert(tk.END, f"Error searching: {str(e)}")

        self.search_results.configure(state='disabled')

    # New methods for app management
    def backup_app_with_data(self):
        """Create app backup with data"""
        selection = self.app_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No app selected")
            return

        package = self.app_list.get(selection[0])
        filename = filedialog.asksaveasfilename(
            title=f"Backup {package} with data",
            defaultextension=".ab",
            filetypes=[("Android Backup", "*.ab")]
        )

        if filename:
            self.run_command(f"adb backup -f {filename} -apk -all {package}")
            self.print_to_console(f"Backup with data created: {filename}")

    def restore_app_with_data(self):
        """Restore app backup with data"""
        filename = filedialog.askopenfilename(
            title="Select Backup File",
            filetypes=[("Android Backup", "*.ab")]
        )

        if filename:
            package = os.path.basename(filename).replace('.ab', '')
            if messagebox.askyesno("Confirm", f"Restore {package} from backup?"):
                self.run_command(f"adb restore {filename}")
                self.print_to_console(f"Restoring {package} from backup")

    def prepare_migration(self):
        """Prepare app migration"""
        selection = self.app_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No app selected")
            return

        package = self.app_list.get(selection[0])
        filename = filedialog.asksaveasfilename(
            title=f"Prepare migration for {package}",
            defaultextension=".apk",
            filetypes=[("APK Files", "*.apk")]
        )

        if filename:
            self.run_command(f"adb shell pm install-create -r -t -S {os.path.getsize(filename)}")
            self.print_to_console(f"Prepared migration for {package}")

    def complete_migration(self):
        """Complete app migration"""
        selection = self.app_list.curselection()
        if not selection:
            messagebox.showerror("Error", "No app selected")
            return

        package = self.app_list.get(selection[0])
        self.run_command(f"adb shell pm install-commit {package}")
        self.print_to_console(f"Completed migration for {package}")

    def disable_app(self):
        """Disable selected app"""
        selection = self.app_list.curselection()
        if selection:
            package = self.app_list.get(selection[0])
            self.run_command(f"adb shell pm disable-user --user 0 {package}")
            self.print_to_console(f"Disabled app: {package}")

    def enable_app(self):
        """Enable selected app"""
        selection = self.app_list.curselection()
        if selection:
            package = self.app_list.get(selection[0])
            self.run_command(f"adb shell pm enable {package}")
            self.print_to_console(f"Enabled app: {package}")

    def force_dark_mode(self):
        """Force dark mode for app"""
        selection = self.app_list.curselection()
        if selection:
            package = self.app_list.get(selection[0])
            self.run_command(f"adb shell cmd uimode night yes")
            self.run_command(f"adb shell settings put secure ui_night_mode 2")
            self.print_to_console(f"Forced dark mode for: {package}")

    def check_battery_optimization(self):
        """Check battery optimization for app"""
        selection = self.app_list.curselection()
        if selection:
            package = self.app_list.get(selection[0])
            result = self.run_command(f"adb shell dumpsys deviceidle whitelist | grep {package}")
            if result:
                self.print_to_console(f"Battery optimization status for {package}:\n{result}")

    def disable_battery_optimization(self):
        """Disable battery optimization for app"""
        selection = self.app_list.curselection()
        if selection:
            package = self.app_list.get(selection[0])
            self.run_command(f"adb shell dumpsys deviceidle whitelist +{package}")
            self.print_to_console(f"Disabled battery optimization for: {package}")

    # New methods for resource monitoring
    def start_resource_monitoring(self):
        """Start resource monitoring"""
        if self.process_monitor_running:
            return

        self.process_monitor_running = True
        self.resource_monitor_thread = Thread(target=self._monitor_resources)
        self.resource_monitor_thread.daemon = True
        self.resource_monitor_thread.start()
        self.print_to_console("Started resource monitoring")

    def _monitor_resources(self):
        """Internal method for monitoring resources"""
        while self.process_monitor_running:
            try:
                # CPU usage
                cpu = subprocess.check_output(
                    "adb shell top -bn1 | grep -m1 -o '[0-9.]*%'",
                    shell=True, text=True
                ).strip()

                # Memory usage
                mem = subprocess.check_output(
                    "adb shell cat /proc/meminfo | grep -E 'MemTotal|MemFree'",
                    shell=True, text=True
                )
                total = int(mem.split('\n')[0].split()[1]) // 1024
                free = int(mem.split('\n')[1].split()[1]) // 1024
                used = total - free

                # Battery level
                battery = subprocess.check_output(
                    "adb shell dumpsys battery | grep level",
                    shell=True, text=True
                ).split(':')[1].strip()

                # Update UI
                self.root.after(0, self._update_resource_labels, cpu, f"{used} MB / {total} MB", f"{battery}%")

                # Refresh processes every 5 updates
                if int(datetime.now().timestamp()) % 5 == 0:
                    self.root.after(0, self.refresh_processes)

                sleep(1)
            except Exception as e:
                self.print_to_console(f"Monitoring error: {str(e)}", error=True)
                sleep(5)

    def _update_resource_labels(self, cpu, mem, battery):
        """Update resource labels"""
        self.cpu_usage_label.config(text=cpu)
        self.memory_usage_label.config(text=mem)
        self.battery_level_label.config(text=battery)

    def stop_resource_monitoring(self):
        """Stop resource monitoring"""
        self.process_monitor_running = False
        if self.resource_monitor_thread:
            self.resource_monitor_thread.join()
        self.print_to_console("Stopped resource monitoring")

    def refresh_processes(self):
        """Refresh process list"""
        try:
            processes = subprocess.check_output(
                "adb shell ps -A -o PID,NAME,USER,%CPU,%MEM",
                shell=True, text=True
            )

            self.process_listbox.delete(0, tk.END)
            for line in processes.split('\n')[1:]:  # Skip header
                if line.strip():
                    self.process_listbox.insert(tk.END, line)
        except Exception as e:
            self.print_to_console(f"Error refreshing processes: {str(e)}", error=True)

    def kill_process(self):
        """Kill selected process"""
        selection = self.process_listbox.curselection()
        if selection:
            pid = self.process_listbox.get(selection[0]).split()[0]
            self.run_command(f"adb shell kill -9 {pid}")
            self.print_to_console(f"Killed process with PID: {pid}")
            self.refresh_processes()

    # New methods for permission management
    def refresh_permission_apps(self):
        """Refresh app list for permission manager"""
        try:
            apps = subprocess.check_output(
                "adb shell pm list packages -3",
                shell=True, text=True
            ).split('\n')

            self.permission_app_list.delete(0, tk.END)
            for app in apps:
                if app.strip():
                    self.permission_app_list.insert(tk.END, app.replace("package:", ""))
        except Exception as e:
            self.print_to_console(f"Error refreshing apps: {str(e)}", error=True)

    def show_app_permissions(self):
        """Show permissions for selected app"""
        selection = self.permission_app_list.curselection()
        if not selection:
            return

        package = self.permission_app_list.get(selection[0])
        try:
            perms = subprocess.check_output(
                f"adb shell dumpsys package {package} | grep -A50 'requested permissions:'",
                shell=True, text=True
            )

            self.permission_details.configure(state='normal')
            self.permission_details.delete(1.0, tk.END)
            self.permission_details.insert(tk.END, perms)
            self.permission_details.configure(state='disabled')

            # Find dangerous permissions
            dangerous = [line for line in perms.split('\n') if "dangerous" in line]
            self.dangerous_perms_list.configure(state='normal')
            self.dangerous_perms_list.delete(1.0, tk.END)
            self.dangerous_perms_list.insert(tk.END, "\n".join(dangerous))
            self.dangerous_perms_list.configure(state='disabled')
        except Exception as e:
            self.print_to_console(f"Error getting permissions: {str(e)}", error=True)

    def revoke_permission(self):
        """Revoke permission for app"""
        selection = self.permission_app_list.curselection()
        if not selection:
            return

        package = self.permission_app_list.get(selection[0])
        perm = simpledialog.askstring("Revoke Permission", "Enter permission to revoke:")
        if perm:
            self.run_command(f"adb shell pm revoke {package} {perm}")
            self.print_to_console(f"Revoked permission {perm} for {package}")
            self.show_app_permissions()

    # New methods for terminal
    def execute_terminal_command(self, event):
        """Execute ADB shell command"""
        cmd = self.terminal_entry.get()
        if not cmd:
            return

        self.terminal_output.configure(state='normal')
        self.terminal_output.insert(tk.END, f"\n$ {cmd}\n")

        try:
            result = subprocess.check_output(
                f"adb shell {cmd}",
                shell=True, stderr=subprocess.STDOUT, text=True
            )
            self.terminal_output.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            self.terminal_output.insert(tk.END, f"Error: {e.output}")

        self.terminal_output.see(tk.END)
        self.terminal_output.configure(state='disabled')
        self.terminal_entry.delete(0, tk.END)

    def clear_terminal(self):
        """Clear terminal"""
        self.terminal_output.configure(state='normal')
        self.terminal_output.delete(1.0, tk.END)
        self.terminal_output.configure(state='disabled')

    def save_terminal_output(self):
        """Save terminal output to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Terminal Output",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.terminal_output.get(1.0, tk.END))
                self.print_to_console(f"Terminal output saved to {filename}")
            except Exception as e:
                self.print_to_console(f"Error saving terminal output: {str(e)}", error=True)

    def show_terminal_history(self):
        """Show terminal command history"""
        # To be implemented - would require storing command history
        messagebox.showinfo("Info", "Command history feature coming soon")

def main():
    root = tk.Tk()
    app = ADBHelperGUI(root)

    # Configure tags for console output
    app.console.tag_config("error", foreground="red")
    app.console.tag_config("normal", foreground="black")

    # Start with device info
    app.update_device_info()
    app.refresh_app_list()

    root.mainloop()

if __name__ == "__main__":
    main()
