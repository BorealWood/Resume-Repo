#!/usr/bin/env python3
"""
Network & System Data Analyzer - GUI Version
Author: Eyasu Solomon
Description: Advanced Python data analysis tool with full Tkinter GUI
Features: Real-time monitoring, charts, log analysis, network tools, report generation
"""

import os
import sys
import json
import socket
import platform
import datetime
import threading
import subprocess
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from tkinter.font import Font

# Optional imports
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not installed. Some features will be limited.")


class ModernStyle:
    """Modern color scheme and styling"""
    BG_DARK = "#1e1e2e"
    BG_MEDIUM = "#2d2d3f"
    BG_LIGHT = "#3d3d5c"
    FG_PRIMARY = "#ffffff"
    FG_SECONDARY = "#a0a0b0"
    ACCENT_BLUE = "#4fc3f7"
    ACCENT_GREEN = "#81c784"
    ACCENT_RED = "#e57373"
    ACCENT_YELLOW = "#fff176"
    ACCENT_PURPLE = "#ba68c8"


class DashboardCard(ttk.Frame):
    """Reusable dashboard card widget"""
    def __init__(self, parent, title, icon="📊", accent_color=ModernStyle.ACCENT_BLUE):
        super().__init__(parent, style="Card.TFrame")
        self.accent_color = accent_color
        
        # Header
        header = ttk.Frame(self, style="Card.TFrame")
        header.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        ttk.Label(header, text=f"{icon} {title}", 
                  font=("Segoe UI", 11, "bold"),
                  foreground=ModernStyle.FG_SECONDARY).pack(side=tk.LEFT)
        
        # Value
        self.value_var = tk.StringVar(value="--")
        self.value_label = ttk.Label(self, textvariable=self.value_var,
                                      font=("Segoe UI", 32, "bold"),
                                      foreground=accent_color)
        self.value_label.pack(padx=15, pady=5)
        
        # Subtitle
        self.subtitle_var = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.subtitle_var,
                  font=("Segoe UI", 9),
                  foreground=ModernStyle.FG_SECONDARY).pack(padx=15)
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress = ttk.Progressbar(self, variable=self.progress_var,
                                         maximum=100, length=200, mode='determinate')
        self.progress.pack(padx=15, pady=(10, 15), fill=tk.X)
    
    def update(self, value, subtitle="", progress=None):
        self.value_var.set(value)
        self.subtitle_var.set(subtitle)
        if progress is not None:
            self.progress_var.set(progress)


class SystemMonitorApp:
    """Main Application Class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Network & System Data Analyzer v2.0 - Eyasu Solomon")
        self.root.geometry("1280x800")
        self.root.minsize(1024, 600)
        
        # Configure styles
        self.setup_styles()
        
        # Create main container
        self.main_container = ttk.Frame(root, style="Main.TFrame")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header
        self.create_header()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_processes_tab()
        self.create_network_tab()
        self.create_disk_tab()
        self.create_logs_tab()
        self.create_tools_tab()
        
        # Create status bar
        self.create_statusbar()
        
        # Start monitoring
        self.monitoring = True
        self.start_monitoring()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        style.configure("Main.TFrame", background=ModernStyle.BG_DARK)
        style.configure("Card.TFrame", background=ModernStyle.BG_MEDIUM)
        
        # Labels
        style.configure("TLabel", background=ModernStyle.BG_DARK, 
                       foreground=ModernStyle.FG_PRIMARY)
        style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"),
                       foreground=ModernStyle.ACCENT_BLUE)
        
        # Notebook
        style.configure("TNotebook", background=ModernStyle.BG_DARK)
        style.configure("TNotebook.Tab", padding=[20, 10], font=("Segoe UI", 10))
        
        # Buttons
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Danger.TButton", foreground=ModernStyle.ACCENT_RED)
        
        # Treeview
        style.configure("Treeview", 
                       background=ModernStyle.BG_MEDIUM,
                       foreground=ModernStyle.FG_PRIMARY,
                       fieldbackground=ModernStyle.BG_MEDIUM,
                       font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        
        # Progressbar
        style.configure("TProgressbar", thickness=10)
    
    def create_header(self):
        """Create application header"""
        header = ttk.Frame(self.main_container, style="Main.TFrame")
        header.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        ttk.Label(header, text="🖥️ Network & System Data Analyzer",
                  style="Header.TLabel").pack(side=tk.LEFT)
        
        # Quick actions
        actions = ttk.Frame(header, style="Main.TFrame")
        actions.pack(side=tk.RIGHT)
        
        ttk.Button(actions, text="🔄 Refresh All", 
                  command=self.refresh_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="📊 Export Report", 
                  command=self.export_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(actions, text="ℹ️ About", 
                  command=self.show_about).pack(side=tk.LEFT, padx=5)
    
    def create_dashboard_tab(self):
        """Create main dashboard tab"""
        tab = ttk.Frame(self.notebook, style="Main.TFrame")
        self.notebook.add(tab, text="📊 Dashboard")
        
        # Stats cards row
        cards_frame = ttk.Frame(tab, style="Main.TFrame")
        cards_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # CPU Card
        self.cpu_card = DashboardCard(cards_frame, "CPU Usage", "⚡", ModernStyle.ACCENT_BLUE)
        self.cpu_card.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH)
        
        # Memory Card
        self.memory_card = DashboardCard(cards_frame, "Memory Usage", "🧠", ModernStyle.ACCENT_PURPLE)
        self.memory_card.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH)
        
        # Disk Card
        self.disk_card = DashboardCard(cards_frame, "Disk Usage", "💾", ModernStyle.ACCENT_YELLOW)
        self.disk_card.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH)
        
        # Network Card
        self.network_card = DashboardCard(cards_frame, "Network", "🌐", ModernStyle.ACCENT_GREEN)
        self.network_card.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.BOTH)
        
        # Bottom section
        bottom = ttk.Frame(tab, style="Main.TFrame")
        bottom.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # System Info Panel
        info_frame = ttk.LabelFrame(bottom, text="System Information", padding=15)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.system_info_text = scrolledtext.ScrolledText(
            info_frame, height=15, font=("Consolas", 10),
            bg=ModernStyle.BG_MEDIUM, fg=ModernStyle.FG_PRIMARY,
            insertbackground=ModernStyle.FG_PRIMARY
        )
        self.system_info_text.pack(fill=tk.BOTH, expand=True)
        self.load_system_info()
        
        # Quick Stats Panel
        stats_frame = ttk.LabelFrame(bottom, text="Quick Statistics", padding=15)
        stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.stats_tree = ttk.Treeview(stats_frame, columns=("Metric", "Value"), 
                                        show="headings", height=12)
        self.stats_tree.heading("Metric", text="Metric")
        self.stats_tree.heading("Value", text="Value")
        self.stats_tree.column("Metric", width=200)
        self.stats_tree.column("Value", width=150)
        self.stats_tree.pack(fill=tk.BOTH, expand=True)
        self.load_quick_stats()
    
    def create_processes_tab(self):
        """Create processes management tab"""
        tab = ttk.Frame(self.notebook, style="Main.TFrame")
        self.notebook.add(tab, text="⚙️ Processes")
        
        # Toolbar
        toolbar = ttk.Frame(tab, style="Main.TFrame")
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(toolbar, text="Search:").pack(side=tk.LEFT, padx=5)
        self.process_search_var = tk.StringVar()
        self.process_search_var.trace('w', lambda *args: self.filter_processes())
        search_entry = ttk.Entry(toolbar, textvariable=self.process_search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(toolbar, text="Sort by:").pack(side=tk.LEFT, padx=(20, 5))
        self.sort_var = tk.StringVar(value="name")
        sort_combo = ttk.Combobox(toolbar, textvariable=self.sort_var, 
                                  values=["name", "pid", "memory", "cpu"], width=10)
        sort_combo.pack(side=tk.LEFT, padx=5)
        sort_combo.bind("<<ComboboxSelected>>", lambda e: self.load_processes())
        
        ttk.Button(toolbar, text="🔄 Refresh", 
                  command=self.load_processes).pack(side=tk.LEFT, padx=20)
        ttk.Button(toolbar, text="❌ End Task", style="Danger.TButton",
                  command=self.kill_selected_process).pack(side=tk.LEFT, padx=5)
        
        # Process list
        columns = ("Name", "PID", "CPU %", "Memory (MB)", "Threads", "Status")
        self.process_tree = ttk.Treeview(tab, columns=columns, show="headings")
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=120)
        self.process_tree.column("Name", width=200)
        
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        self.process_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.load_processes()
    
    def create_network_tab(self):
        """Create network analysis tab"""
        tab = ttk.Frame(self.notebook, style="Main.TFrame")
        self.notebook.add(tab, text="🌐 Network")
        
        # Top section - Network interfaces
        interfaces_frame = ttk.LabelFrame(tab, text="Network Interfaces", padding=10)
        interfaces_frame.pack(fill=tk.X, padx=10, pady=10)
        
        columns = ("Name", "Status", "Type", "Speed", "IP Address", "MAC")
        self.interface_tree = ttk.Treeview(interfaces_frame, columns=columns, 
                                           show="headings", height=6)
        for col in columns:
            self.interface_tree.heading(col, text=col)
            self.interface_tree.column(col, width=150)
        self.interface_tree.pack(fill=tk.X)
        self.load_network_interfaces()
        
        # Bottom section
        bottom = ttk.Frame(tab, style="Main.TFrame")
        bottom.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Ping Tool
        ping_frame = ttk.LabelFrame(bottom, text="Ping Tool", padding=15)
        ping_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        ping_input = ttk.Frame(ping_frame)
        ping_input.pack(fill=tk.X)
        
        self.ping_host_var = tk.StringVar(value="google.com")
        ttk.Entry(ping_input, textvariable=self.ping_host_var, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(ping_input, text="🏓 Ping", command=self.run_ping).pack(side=tk.LEFT, padx=5)
        ttk.Button(ping_input, text="📍 Traceroute", command=self.run_traceroute).pack(side=tk.LEFT, padx=5)
        
        self.ping_output = scrolledtext.ScrolledText(
            ping_frame, height=12, font=("Consolas", 9),
            bg="#1a1a2e", fg="#00ff88"
        )
        self.ping_output.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Port Scanner
        port_frame = ttk.LabelFrame(bottom, text="Port Scanner", padding=15)
        port_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        port_input = ttk.Frame(port_frame)
        port_input.pack(fill=tk.X)
        
        ttk.Label(port_input, text="Host:").pack(side=tk.LEFT)
        self.scan_host_var = tk.StringVar(value="127.0.0.1")
        ttk.Entry(port_input, textvariable=self.scan_host_var, width=15).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(port_input, text="Ports:").pack(side=tk.LEFT, padx=(10, 0))
        self.scan_ports_var = tk.StringVar(value="1-1024")
        ttk.Entry(port_input, textvariable=self.scan_ports_var, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(port_input, text="🔍 Scan", command=self.run_port_scan).pack(side=tk.LEFT, padx=10)
        
        self.port_output = scrolledtext.ScrolledText(
            port_frame, height=12, font=("Consolas", 9),
            bg="#1a1a2e", fg="#00ff88"
        )
        self.port_output.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def create_disk_tab(self):
        """Create disk analysis tab"""
        tab = ttk.Frame(self.notebook, style="Main.TFrame")
        self.notebook.add(tab, text="💾 Disk")
        
        # Drive overview
        drives_frame = ttk.LabelFrame(tab, text="Drives", padding=10)
        drives_frame.pack(fill=tk.X, padx=10, pady=10)
        
        columns = ("Drive", "Label", "Type", "File System", "Total", "Free", "Used", "Usage %")
        self.disk_tree = ttk.Treeview(drives_frame, columns=columns, show="headings", height=5)
        for col in columns:
            self.disk_tree.heading(col, text=col)
            self.disk_tree.column(col, width=100)
        self.disk_tree.column("Drive", width=60)
        self.disk_tree.pack(fill=tk.X)
        self.load_disk_info()
        
        # Folder analyzer
        analyzer_frame = ttk.LabelFrame(tab, text="Folder Size Analyzer", padding=10)
        analyzer_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        toolbar = ttk.Frame(analyzer_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        self.folder_path_var = tk.StringVar(value=os.path.expanduser("~"))
        ttk.Entry(toolbar, textvariable=self.folder_path_var, width=60).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="📁 Browse", command=self.browse_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🔍 Analyze", command=self.analyze_folder).pack(side=tk.LEFT, padx=5)
        
        columns = ("Name", "Type", "Size", "Files", "Modified")
        self.folder_tree = ttk.Treeview(analyzer_frame, columns=columns, show="headings")
        for col in columns:
            self.folder_tree.heading(col, text=col)
        self.folder_tree.column("Name", width=300)
        self.folder_tree.column("Type", width=80)
        self.folder_tree.column("Size", width=100)
        self.folder_tree.column("Files", width=80)
        self.folder_tree.column("Modified", width=150)
        
        scrollbar = ttk.Scrollbar(analyzer_frame, orient=tk.VERTICAL, command=self.folder_tree.yview)
        self.folder_tree.configure(yscrollcommand=scrollbar.set)
        
        self.folder_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_logs_tab(self):
        """Create log analysis tab"""
        tab = ttk.Frame(self.notebook, style="Main.TFrame")
        self.notebook.add(tab, text="📋 Log Analyzer")
        
        # Controls
        controls = ttk.Frame(tab, style="Main.TFrame")
        controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(controls, text="📂 Load Log File", 
                  command=self.load_log_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="📊 Analyze", 
                  command=self.analyze_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="🧹 Clear", 
                  command=lambda: self.log_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(controls, text="Filter:").pack(side=tk.LEFT, padx=(20, 5))
        self.log_filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(controls, textvariable=self.log_filter_var,
                                    values=["All", "ERROR", "WARNING", "INFO", "DEBUG"],
                                    width=10)
        filter_combo.pack(side=tk.LEFT, padx=5)
        
        # Main content
        paned = ttk.PanedWindow(tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Log content
        log_frame = ttk.LabelFrame(paned, text="Log Content", padding=10)
        paned.add(log_frame, weight=2)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, font=("Consolas", 9),
            bg=ModernStyle.BG_MEDIUM, fg=ModernStyle.FG_PRIMARY
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Tag configurations for log levels
        self.log_text.tag_configure("ERROR", foreground="#ff6b6b")
        self.log_text.tag_configure("WARNING", foreground="#feca57")
        self.log_text.tag_configure("INFO", foreground="#54a0ff")
        self.log_text.tag_configure("DEBUG", foreground="#a0a0a0")
        
        # Analysis results
        analysis_frame = ttk.LabelFrame(paned, text="Analysis Results", padding=10)
        paned.add(analysis_frame, weight=1)
        
        self.analysis_text = scrolledtext.ScrolledText(
            analysis_frame, font=("Segoe UI", 10),
            bg=ModernStyle.BG_MEDIUM, fg=ModernStyle.FG_PRIMARY
        )
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
    
    def create_tools_tab(self):
        """Create additional tools tab"""
        tab = ttk.Frame(self.notebook, style="Main.TFrame")
        self.notebook.add(tab, text="🛠️ Tools")
        
        # Tools grid
        tools_frame = ttk.Frame(tab, style="Main.TFrame")
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tools = [
            ("🔐", "Password Generator", self.password_generator),
            ("📋", "Clipboard Manager", self.clipboard_manager),
            ("🔢", "Base Converter", self.base_converter),
            ("📏", "Unit Converter", self.unit_converter),
            ("🎨", "Color Picker", self.color_picker),
            ("⏱️", "Stopwatch", self.stopwatch),
            ("📊", "System Benchmark", self.system_benchmark),
            ("💾", "Memory Cleaner", self.memory_cleaner),
        ]
        
        for i, (icon, name, command) in enumerate(tools):
            row, col = divmod(i, 4)
            btn = ttk.Button(tools_frame, text=f"{icon}\n{name}", 
                           command=command, width=20)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            tools_frame.columnconfigure(col, weight=1)
    
    def create_statusbar(self):
        """Create status bar"""
        self.statusbar = ttk.Frame(self.main_container, style="Main.TFrame")
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.statusbar, textvariable=self.status_var).pack(side=tk.LEFT)
        
        self.time_var = tk.StringVar()
        ttk.Label(self.statusbar, textvariable=self.time_var).pack(side=tk.RIGHT)
        self.update_time()
    
    def update_time(self):
        """Update status bar time"""
        self.time_var.set(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    # Data loading methods
    def load_system_info(self):
        """Load system information"""
        self.system_info_text.delete(1.0, tk.END)
        info = f"""
╔══════════════════════════════════════════════════════════╗
║                    SYSTEM INFORMATION                     ║
╚══════════════════════════════════════════════════════════╝

  Computer Name:    {socket.gethostname()}
  Platform:         {platform.system()} {platform.release()}
  Version:          {platform.version()}
  Architecture:     {platform.machine()}
  Processor:        {platform.processor()}
  Python Version:   {platform.python_version()}
"""
        if PSUTIL_AVAILABLE:
            info += f"""
  CPU Cores:        {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count()} logical
  CPU Frequency:    {psutil.cpu_freq().current:.0f} MHz
  
  Total RAM:        {psutil.virtual_memory().total / (1024**3):.1f} GB
  Boot Time:        {datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M')}
"""
        self.system_info_text.insert(1.0, info)
    
    def load_quick_stats(self):
        """Load quick statistics"""
        self.stats_tree.delete(*self.stats_tree.get_children())
        
        stats = [
            ("Platform", platform.system()),
            ("Hostname", socket.gethostname()),
            ("Python Version", platform.python_version()),
        ]
        
        if PSUTIL_AVAILABLE:
            stats.extend([
                ("Running Processes", str(len(psutil.pids()))),
                ("CPU Cores", str(psutil.cpu_count())),
                ("Network Interfaces", str(len(psutil.net_if_addrs()))),
                ("Disk Partitions", str(len(psutil.disk_partitions()))),
            ])
        
        for metric, value in stats:
            self.stats_tree.insert("", tk.END, values=(metric, value))
    
    def load_processes(self):
        """Load process list"""
        self.process_tree.delete(*self.process_tree.get_children())
        
        if not PSUTIL_AVAILABLE:
            self.process_tree.insert("", tk.END, values=("psutil not installed", "", "", "", "", ""))
            return
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'num_threads', 'status']):
            try:
                info = proc.info
                processes.append((
                    info['name'],
                    info['pid'],
                    info['cpu_percent'] or 0,
                    info['memory_info'].rss / (1024*1024) if info['memory_info'] else 0,
                    info['num_threads'],
                    info['status']
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort
        sort_key = self.sort_var.get()
        sort_idx = {"name": 0, "pid": 1, "cpu": 2, "memory": 3}.get(sort_key, 0)
        processes.sort(key=lambda x: x[sort_idx], reverse=(sort_key in ["cpu", "memory"]))
        
        for proc in processes[:200]:  # Limit to 200
            self.process_tree.insert("", tk.END, values=(
                proc[0], proc[1], f"{proc[2]:.1f}", f"{proc[3]:.1f}", proc[4], proc[5]
            ))
        
        self.status_var.set(f"Loaded {len(processes)} processes")
    
    def load_network_interfaces(self):
        """Load network interfaces"""
        self.interface_tree.delete(*self.interface_tree.get_children())
        
        if not PSUTIL_AVAILABLE:
            return
        
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        for name, addr_list in addrs.items():
            stat = stats.get(name)
            ipv4 = next((a.address for a in addr_list 
                        if a.family == socket.AF_INET), "--")
            mac = next((a.address for a in addr_list 
                       if a.family == psutil.AF_LINK), "--")
            
            self.interface_tree.insert("", tk.END, values=(
                name,
                "Up" if stat and stat.isup else "Down",
                stat.speed if stat else 0,
                f"{stat.speed} Mbps" if stat else "--",
                ipv4,
                mac
            ))
    
    def load_disk_info(self):
        """Load disk information"""
        self.disk_tree.delete(*self.disk_tree.get_children())
        
        if not PSUTIL_AVAILABLE:
            return
        
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                percent = usage.percent
                
                self.disk_tree.insert("", tk.END, values=(
                    part.device,
                    part.mountpoint,
                    part.fstype,
                    part.fstype,
                    self.format_bytes(usage.total),
                    self.format_bytes(usage.free),
                    self.format_bytes(usage.used),
                    f"{percent:.1f}%"
                ))
            except (PermissionError, OSError):
                pass
    
    # Monitoring
    def start_monitoring(self):
        """Start background monitoring"""
        def monitor():
            while self.monitoring:
                try:
                    if PSUTIL_AVAILABLE:
                        # CPU
                        cpu = psutil.cpu_percent(interval=1)
                        self.root.after(0, lambda c=cpu: self.cpu_card.update(
                            f"{c:.0f}%", f"{psutil.cpu_count()} cores", c))
                        
                        # Memory
                        mem = psutil.virtual_memory()
                        self.root.after(0, lambda m=mem: self.memory_card.update(
                            f"{m.percent:.0f}%", 
                            f"{m.used/(1024**3):.1f} / {m.total/(1024**3):.1f} GB",
                            m.percent))
                        
                        # Disk
                        disk = psutil.disk_usage('/')
                        self.root.after(0, lambda d=disk: self.disk_card.update(
                            f"{d.percent:.0f}%",
                            f"{d.free/(1024**3):.1f} GB free",
                            d.percent))
                        
                        # Network
                        net = psutil.net_io_counters()
                        self.root.after(0, lambda n=net: self.network_card.update(
                            "Online",
                            f"↑ {n.bytes_sent/(1024**2):.1f} MB | ↓ {n.bytes_recv/(1024**2):.1f} MB",
                            50))
                except Exception as e:
                    pass
        
        self.monitor_thread = threading.Thread(target=monitor, daemon=True)
        self.monitor_thread.start()
    
    # Action handlers
    def filter_processes(self):
        """Filter process list"""
        search = self.process_search_var.get().lower()
        for item in self.process_tree.get_children():
            values = self.process_tree.item(item, 'values')
            if search in values[0].lower():
                self.process_tree.reattach(item, '', tk.END)
            else:
                self.process_tree.detach(item)
    
    def kill_selected_process(self):
        """Kill selected process"""
        selection = self.process_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a process")
            return
        
        item = self.process_tree.item(selection[0])
        pid = int(item['values'][1])
        name = item['values'][0]
        
        if messagebox.askyesno("Confirm", f"End process '{name}' (PID: {pid})?"):
            try:
                psutil.Process(pid).terminate()
                self.load_processes()
                messagebox.showinfo("Success", f"Process {name} terminated")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def run_ping(self):
        """Run ping command"""
        host = self.ping_host_var.get()
        self.ping_output.delete(1.0, tk.END)
        self.ping_output.insert(tk.END, f"Pinging {host}...\n\n")
        
        def ping():
            try:
                for i in range(4):
                    start = datetime.datetime.now()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((host, 80))
                    elapsed = (datetime.datetime.now() - start).total_seconds() * 1000
                    sock.close()
                    
                    if result == 0:
                        self.root.after(0, lambda t=elapsed: self.ping_output.insert(
                            tk.END, f"Reply from {host}: time={t:.0f}ms\n"))
                    else:
                        self.root.after(0, lambda: self.ping_output.insert(
                            tk.END, "Request timed out\n"))
            except Exception as e:
                self.root.after(0, lambda: self.ping_output.insert(tk.END, f"Error: {e}\n"))
        
        threading.Thread(target=ping, daemon=True).start()
    
    def run_traceroute(self):
        """Run traceroute (placeholder)"""
        self.ping_output.insert(tk.END, "\nTraceroute feature - requires admin privileges\n")
    
    def run_port_scan(self):
        """Run port scanner"""
        host = self.scan_host_var.get()
        port_range = self.scan_ports_var.get()
        
        self.port_output.delete(1.0, tk.END)
        self.port_output.insert(tk.END, f"Scanning {host}...\n\n")
        
        def scan():
            try:
                start, end = map(int, port_range.split("-"))
                end = min(end, start + 100)  # Limit scan range
                
                common_ports = {
                    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
                    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
                    443: "HTTPS", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL"
                }
                
                for port in range(start, end + 1):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((host, port))
                    if result == 0:
                        service = common_ports.get(port, "Unknown")
                        self.root.after(0, lambda p=port, s=service: self.port_output.insert(
                            tk.END, f"Port {p} OPEN - {s}\n"))
                    sock.close()
                
                self.root.after(0, lambda: self.port_output.insert(tk.END, "\nScan complete.\n"))
            except Exception as e:
                self.root.after(0, lambda: self.port_output.insert(tk.END, f"Error: {e}\n"))
        
        threading.Thread(target=scan, daemon=True).start()
    
    def browse_folder(self):
        """Browse for folder"""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path_var.set(folder)
    
    def analyze_folder(self):
        """Analyze folder contents"""
        path = self.folder_path_var.get()
        self.folder_tree.delete(*self.folder_tree.get_children())
        
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    if os.path.isdir(item_path):
                        size = sum(os.path.getsize(os.path.join(dp, f)) 
                                  for dp, dn, fn in os.walk(item_path) for f in fn)
                        files = sum(len(fn) for dp, dn, fn in os.walk(item_path))
                        item_type = "Folder"
                    else:
                        size = os.path.getsize(item_path)
                        files = 1
                        item_type = os.path.splitext(item)[1] or "File"
                    
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
                    
                    self.folder_tree.insert("", tk.END, values=(
                        item, item_type, self.format_bytes(size), files, 
                        mtime.strftime("%Y-%m-%d %H:%M")
                    ))
                except (PermissionError, OSError):
                    pass
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_log_file(self):
        """Load log file"""
        filepath = filedialog.askopenfilename(
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', errors='ignore') as f:
                    content = f.read()
                self.log_text.delete(1.0, tk.END)
                
                for line in content.split('\n'):
                    if 'ERROR' in line.upper():
                        self.log_text.insert(tk.END, line + '\n', 'ERROR')
                    elif 'WARNING' in line.upper():
                        self.log_text.insert(tk.END, line + '\n', 'WARNING')
                    elif 'INFO' in line.upper():
                        self.log_text.insert(tk.END, line + '\n', 'INFO')
                    elif 'DEBUG' in line.upper():
                        self.log_text.insert(tk.END, line + '\n', 'DEBUG')
                    else:
                        self.log_text.insert(tk.END, line + '\n')
                        
                self.status_var.set(f"Loaded {filepath}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def analyze_logs(self):
        """Analyze loaded logs"""
        content = self.log_text.get(1.0, tk.END)
        lines = content.split('\n')
        
        levels = defaultdict(int)
        for line in lines:
            for level in ['ERROR', 'WARNING', 'INFO', 'DEBUG']:
                if level in line.upper():
                    levels[level] += 1
                    break
        
        total = sum(levels.values()) or 1
        
        analysis = f"""
╔══════════════════════════════════════╗
║           LOG ANALYSIS               ║
╚══════════════════════════════════════╝

Total Lines: {len(lines)}

Log Level Distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        for level in ['ERROR', 'WARNING', 'INFO', 'DEBUG']:
            count = levels[level]
            pct = count / total * 100
            bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
            analysis += f"  {level:10} [{bar}] {count:5} ({pct:.1f}%)\n"
        
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, analysis)
    
    # Tool functions
    def password_generator(self):
        """Generate password"""
        import string
        import random
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(16))
        
        top = tk.Toplevel(self.root)
        top.title("Password Generator")
        top.geometry("400x150")
        
        ttk.Label(top, text="Generated Password:", font=("Segoe UI", 12)).pack(pady=10)
        
        entry = ttk.Entry(top, font=("Consolas", 14), width=30)
        entry.insert(0, password)
        entry.pack(pady=5)
        
        ttk.Button(top, text="Copy to Clipboard", 
                  command=lambda: [self.root.clipboard_clear(), 
                                  self.root.clipboard_append(password),
                                  messagebox.showinfo("Copied", "Password copied!")]).pack(pady=10)
    
    def clipboard_manager(self):
        messagebox.showinfo("Clipboard", f"Current clipboard:\n\n{self.root.clipboard_get()}")
    
    def base_converter(self):
        """Number base converter"""
        top = tk.Toplevel(self.root)
        top.title("Base Converter")
        top.geometry("350x200")
        
        ttk.Label(top, text="Enter number:").pack(pady=5)
        entry = ttk.Entry(top, width=30)
        entry.pack()
        
        result = ttk.Label(top, text="", font=("Consolas", 10))
        result.pack(pady=10)
        
        def convert():
            try:
                n = int(entry.get())
                result.config(text=f"Binary: {bin(n)}\nOctal: {oct(n)}\nHex: {hex(n)}")
            except:
                result.config(text="Invalid number")
        
        ttk.Button(top, text="Convert", command=convert).pack(pady=5)
    
    def unit_converter(self):
        messagebox.showinfo("Unit Converter", "Unit converter - Coming soon!")
    
    def color_picker(self):
        from tkinter.colorchooser import askcolor
        color = askcolor()
        if color[1]:
            messagebox.showinfo("Color", f"Selected: {color[1]}\nRGB: {color[0]}")
    
    def stopwatch(self):
        """Simple stopwatch"""
        top = tk.Toplevel(self.root)
        top.title("Stopwatch")
        top.geometry("300x150")
        
        time_var = tk.StringVar(value="00:00:00")
        running = [False]
        elapsed = [0]
        
        ttk.Label(top, textvariable=time_var, font=("Segoe UI", 36)).pack(pady=20)
        
        def update():
            if running[0]:
                elapsed[0] += 1
                hours, rem = divmod(elapsed[0], 3600)
                mins, secs = divmod(rem, 60)
                time_var.set(f"{hours:02d}:{mins:02d}:{secs:02d}")
                top.after(1000, update)
        
        def toggle():
            running[0] = not running[0]
            if running[0]:
                update()
        
        def reset():
            running[0] = False
            elapsed[0] = 0
            time_var.set("00:00:00")
        
        btns = ttk.Frame(top)
        btns.pack()
        ttk.Button(btns, text="Start/Stop", command=toggle).pack(side=tk.LEFT, padx=5)
        ttk.Button(btns, text="Reset", command=reset).pack(side=tk.LEFT, padx=5)
    
    def system_benchmark(self):
        messagebox.showinfo("Benchmark", "System benchmark - Coming soon!")
    
    def memory_cleaner(self):
        if PSUTIL_AVAILABLE:
            before = psutil.virtual_memory().available
            import gc
            gc.collect()
            after = psutil.virtual_memory().available
            freed = (after - before) / (1024*1024)
            messagebox.showinfo("Memory Cleaner", f"Freed approximately {freed:.1f} MB")
        else:
            messagebox.showinfo("Memory Cleaner", "psutil required")
    
    def refresh_all(self):
        """Refresh all data"""
        self.load_system_info()
        self.load_quick_stats()
        self.load_processes()
        self.load_network_interfaces()
        self.load_disk_info()
        self.status_var.set("All data refreshed")
    
    def export_report(self):
        """Export system report"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Text", "*.txt")]
        )
        if filepath:
            report = {
                "generated_at": datetime.datetime.now().isoformat(),
                "system": {
                    "hostname": socket.gethostname(),
                    "platform": platform.system(),
                    "version": platform.version(),
                    "processor": platform.processor()
                }
            }
            
            if PSUTIL_AVAILABLE:
                report["cpu"] = {"percent": psutil.cpu_percent(), "count": psutil.cpu_count()}
                report["memory"] = dict(psutil.virtual_memory()._asdict())
            
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            messagebox.showinfo("Export", f"Report saved to {filepath}")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
            "Network & System Data Analyzer v2.0\n\n"
            "Created by Eyasu Solomon\n\n"
            "A comprehensive system monitoring and\n"
            "network analysis tool built with Python.")
    
    def format_bytes(self, bytes):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024
        return f"{bytes:.1f} PB"
    
    def on_closing(self):
        """Handle window close"""
        self.monitoring = False
        self.root.destroy()


def main():
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
