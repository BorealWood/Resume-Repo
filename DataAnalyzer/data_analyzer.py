#!/usr/bin/env python3
"""
Network & System Data Analyzer
Author: Eyasu Solomon
Description: Interactive Python tool for data analysis and visualization
             demonstrating proficiency in Python, data analysis, and problem-solving.
"""

import os
import sys
import json
import socket
import platform
import datetime
import subprocess
from collections import defaultdict

# Try to import optional dependencies
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header"""
    print(f"\n{Colors.CYAN}{'═' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.YELLOW}  {title}{Colors.END}")
    print(f"{Colors.CYAN}{'═' * 60}{Colors.END}\n")

def print_menu():
    """Display the main menu"""
    clear_screen()
    print(f"""
{Colors.YELLOW}╔══════════════════════════════════════════════════════════════╗
║          NETWORK & SYSTEM DATA ANALYZER v1.0                 ║
║                Created by Eyasu Solomon                       ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
{Colors.CYAN}║  1. System Information Analysis                              ║
║  2. Network Configuration Analysis                           ║
║  3. Process Statistics & Analysis                            ║
║  4. Disk Usage Analysis with Visualization                   ║
║  5. Memory Usage Trends                                      ║
║  6. Log File Analyzer                                        ║
║  7. Port Scanner                                             ║
║  8. Generate System Report (JSON/TXT)                        ║
║  9. Exit                                                     ║{Colors.END}
{Colors.YELLOW}╚══════════════════════════════════════════════════════════════╝{Colors.END}
    """)

def create_bar(percentage, width=30):
    """Create a visual progress bar"""
    filled = int(width * percentage / 100)
    bar = '█' * filled + '░' * (width - filled)
    
    if percentage >= 90:
        color = Colors.RED
    elif percentage >= 70:
        color = Colors.YELLOW
    else:
        color = Colors.GREEN
    
    return f"{color}[{bar}]{Colors.END} {percentage:.1f}%"

def system_info_analysis():
    """Analyze and display system information"""
    print_header("SYSTEM INFORMATION ANALYSIS")
    
    info = {
        'Platform': platform.system(),
        'Platform Release': platform.release(),
        'Platform Version': platform.version(),
        'Architecture': platform.machine(),
        'Hostname': socket.gethostname(),
        'Processor': platform.processor(),
        'Python Version': platform.python_version(),
    }
    
    try:
        info['IP Address'] = socket.gethostbyname(socket.gethostname())
    except:
        info['IP Address'] = 'Unable to determine'
    
    for key, value in info.items():
        print(f"  {Colors.GREEN}{key:20}{Colors.END}: {value}")
    
    if PSUTIL_AVAILABLE:
        print(f"\n  {Colors.BOLD}Hardware Information:{Colors.END}")
        print(f"  {'CPU Cores (Physical)':20}: {psutil.cpu_count(logical=False)}")
        print(f"  {'CPU Cores (Logical)':20}: {psutil.cpu_count(logical=True)}")
        print(f"  {'CPU Frequency':20}: {psutil.cpu_freq().current:.0f} MHz")
        
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        print(f"  {'System Boot Time':20}: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  {'Uptime':20}: {uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m")

def network_analysis():
    """Analyze network configuration"""
    print_header("NETWORK CONFIGURATION ANALYSIS")
    
    if PSUTIL_AVAILABLE:
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        
        for interface, addrs in interfaces.items():
            print(f"\n  {Colors.YELLOW}{interface}{Colors.END}")
            if interface in stats:
                stat = stats[interface]
                status = f"{Colors.GREEN}UP{Colors.END}" if stat.isup else f"{Colors.RED}DOWN{Colors.END}"
                print(f"    Status: {status}, Speed: {stat.speed} Mbps")
            
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    print(f"    IPv4: {addr.address}")
                    print(f"    Netmask: {addr.netmask}")
                elif hasattr(socket, 'AF_INET6') and addr.family == socket.AF_INET6:
                    print(f"    IPv6: {addr.address}")
        
        # Network I/O statistics
        net_io = psutil.net_io_counters()
        print(f"\n  {Colors.BOLD}Network I/O Statistics:{Colors.END}")
        print(f"    Bytes Sent:     {net_io.bytes_sent / (1024**2):.2f} MB")
        print(f"    Bytes Received: {net_io.bytes_recv / (1024**2):.2f} MB")
        print(f"    Packets Sent:   {net_io.packets_sent:,}")
        print(f"    Packets Recv:   {net_io.packets_recv:,}")
    else:
        print("  psutil not installed. Install with: pip install psutil")

def process_analysis():
    """Analyze running processes"""
    print_header("PROCESS STATISTICS & ANALYSIS")
    
    if PSUTIL_AVAILABLE:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        print(f"  Total Processes: {len(processes)}")
        
        # Top memory consumers
        print(f"\n  {Colors.BOLD}Top 10 Memory Consumers:{Colors.END}")
        print(f"  {'PID':>8}  {'Name':30}  {'Memory %':>10}")
        print(f"  {'-' * 52}")
        
        sorted_by_mem = sorted(processes, key=lambda x: x['memory_percent'] or 0, reverse=True)[:10]
        for proc in sorted_by_mem:
            name = proc['name'][:28] if proc['name'] else 'N/A'
            mem = proc['memory_percent'] or 0
            print(f"  {proc['pid']:>8}  {name:30}  {mem:>10.2f}%")
        
        # Process type distribution
        print(f"\n  {Colors.BOLD}Process Analysis:{Colors.END}")
        total_mem = sum(p['memory_percent'] or 0 for p in processes)
        print(f"    Total Memory Used by Processes: {total_mem:.1f}%")
    else:
        print("  psutil not installed. Install with: pip install psutil")

def disk_analysis():
    """Analyze disk usage with visualization"""
    print_header("DISK USAGE ANALYSIS")
    
    if PSUTIL_AVAILABLE:
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"\n  {Colors.YELLOW}Drive: {partition.device}{Colors.END}")
                print(f"    Mount Point:  {partition.mountpoint}")
                print(f"    File System:  {partition.fstype}")
                print(f"    Total Size:   {usage.total / (1024**3):.2f} GB")
                print(f"    Used:         {usage.used / (1024**3):.2f} GB")
                print(f"    Free:         {usage.free / (1024**3):.2f} GB")
                print(f"    Usage:        {create_bar(usage.percent)}")
            except PermissionError:
                print(f"    {Colors.RED}Permission denied{Colors.END}")
        
        # Disk I/O
        disk_io = psutil.disk_io_counters()
        print(f"\n  {Colors.BOLD}Disk I/O Statistics:{Colors.END}")
        print(f"    Read:  {disk_io.read_bytes / (1024**3):.2f} GB ({disk_io.read_count:,} operations)")
        print(f"    Write: {disk_io.write_bytes / (1024**3):.2f} GB ({disk_io.write_count:,} operations)")
    else:
        print("  psutil not installed. Install with: pip install psutil")

def memory_analysis():
    """Analyze memory usage"""
    print_header("MEMORY USAGE ANALYSIS")
    
    if PSUTIL_AVAILABLE:
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        print(f"  {Colors.BOLD}Physical Memory (RAM):{Colors.END}")
        print(f"    Total:     {mem.total / (1024**3):.2f} GB")
        print(f"    Available: {mem.available / (1024**3):.2f} GB")
        print(f"    Used:      {mem.used / (1024**3):.2f} GB")
        print(f"    Usage:     {create_bar(mem.percent)}")
        
        print(f"\n  {Colors.BOLD}Swap Memory:{Colors.END}")
        print(f"    Total:     {swap.total / (1024**3):.2f} GB")
        print(f"    Used:      {swap.used / (1024**3):.2f} GB")
        print(f"    Free:      {swap.free / (1024**3):.2f} GB")
        print(f"    Usage:     {create_bar(swap.percent)}")
        
        # Memory breakdown
        print(f"\n  {Colors.BOLD}Memory Breakdown:{Colors.END}")
        print(f"    Cached:    {getattr(mem, 'cached', 0) / (1024**3):.2f} GB")
        print(f"    Buffers:   {getattr(mem, 'buffers', 0) / (1024**3):.2f} GB")
    else:
        print("  psutil not installed. Install with: pip install psutil")

def log_analyzer():
    """Analyze log files"""
    print_header("LOG FILE ANALYZER")
    
    print("  Enter the path to a log file to analyze")
    print("  (or press Enter for demo mode with sample data)")
    
    filepath = input(f"\n  {Colors.GREEN}File path: {Colors.END}").strip()
    
    if not filepath:
        # Demo mode with sample log data
        sample_log = """
2025-01-08 10:15:23 INFO Application started
2025-01-08 10:15:24 DEBUG Loading configuration
2025-01-08 10:15:25 INFO Database connected
2025-01-08 10:16:00 WARNING High memory usage detected
2025-01-08 10:17:30 ERROR Failed to connect to external API
2025-01-08 10:18:00 INFO Retry successful
2025-01-08 10:20:00 ERROR Database timeout
2025-01-08 10:21:00 WARNING CPU usage above 80%
2025-01-08 10:25:00 INFO Scheduled task completed
2025-01-08 10:30:00 DEBUG Cache cleared
        """.strip().split('\n')
        
        print(f"\n  {Colors.YELLOW}Demo Mode - Analyzing sample log data{Colors.END}\n")
        lines = sample_log
    else:
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"\n  {Colors.RED}Error: File not found{Colors.END}")
            return
        except Exception as e:
            print(f"\n  {Colors.RED}Error: {e}{Colors.END}")
            return
    
    # Analyze log levels
    levels = defaultdict(int)
    keywords = ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']
    
    for line in lines:
        for keyword in keywords:
            if keyword in line.upper():
                levels[keyword] += 1
                break
    
    print(f"  {Colors.BOLD}Log Level Distribution:{Colors.END}")
    total = sum(levels.values()) or 1
    
    level_colors = {
        'INFO': Colors.BLUE,
        'DEBUG': Colors.CYAN,
        'WARNING': Colors.YELLOW,
        'ERROR': Colors.RED,
        'CRITICAL': Colors.RED
    }
    
    for level in keywords:
        count = levels[level]
        percentage = (count / total) * 100
        color = level_colors.get(level, Colors.END)
        bar = '█' * int(percentage / 5) + '░' * (20 - int(percentage / 5))
        print(f"    {color}{level:10}{Colors.END} [{bar}] {count:5} ({percentage:.1f}%)")
    
    print(f"\n  Total lines analyzed: {len(lines)}")

def port_scanner():
    """Simple port scanner"""
    print_header("PORT SCANNER")
    
    target = input(f"  Enter target IP/hostname (default: localhost): ").strip()
    if not target:
        target = "127.0.0.1"
    
    start_port = input("  Start port (default: 1): ").strip()
    start_port = int(start_port) if start_port else 1
    
    end_port = input("  End port (default: 1024): ").strip()
    end_port = int(end_port) if end_port else 1024
    
    print(f"\n  {Colors.YELLOW}Scanning {target} from port {start_port} to {end_port}...{Colors.END}\n")
    
    open_ports = []
    common_ports = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
        53: 'DNS', 80: 'HTTP', 110: 'POP3', 143: 'IMAP',
        443: 'HTTPS', 3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL'
    }
    
    for port in range(start_port, min(end_port + 1, start_port + 100)):  # Limit to 100 ports
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            service = common_ports.get(port, 'Unknown')
            open_ports.append((port, service))
            print(f"  {Colors.GREEN}Port {port:5} OPEN{Colors.END} - {service}")
        sock.close()
    
    print(f"\n  Scan complete. Found {len(open_ports)} open ports.")

def generate_report():
    """Generate a comprehensive system report"""
    print_header("GENERATING SYSTEM REPORT")
    
    report = {
        'generated_at': datetime.datetime.now().isoformat(),
        'system': {
            'platform': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'architecture': platform.machine(),
            'hostname': socket.gethostname(),
            'processor': platform.processor(),
        }
    }
    
    if PSUTIL_AVAILABLE:
        mem = psutil.virtual_memory()
        report['memory'] = {
            'total_gb': round(mem.total / (1024**3), 2),
            'available_gb': round(mem.available / (1024**3), 2),
            'percent_used': mem.percent
        }
        
        report['cpu'] = {
            'physical_cores': psutil.cpu_count(logical=False),
            'logical_cores': psutil.cpu_count(logical=True),
            'frequency_mhz': round(psutil.cpu_freq().current, 2),
            'usage_percent': psutil.cpu_percent(interval=1)
        }
        
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'percent_used': usage.percent
                })
            except:
                pass
        report['disks'] = disks
    
    # Save as JSON
    json_path = 'system_report.json'
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"  {Colors.GREEN}JSON report saved to: {json_path}{Colors.END}")
    
    # Save as TXT
    txt_path = 'system_report.txt'
    with open(txt_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("SYSTEM REPORT\n")
        f.write(f"Generated: {report['generated_at']}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("SYSTEM INFORMATION\n")
        f.write("-" * 30 + "\n")
        for key, value in report['system'].items():
            f.write(f"{key}: {value}\n")
        
        if PSUTIL_AVAILABLE:
            f.write("\nMEMORY\n")
            f.write("-" * 30 + "\n")
            for key, value in report['memory'].items():
                f.write(f"{key}: {value}\n")
            
            f.write("\nCPU\n")
            f.write("-" * 30 + "\n")
            for key, value in report['cpu'].items():
                f.write(f"{key}: {value}\n")
    
    print(f"  {Colors.GREEN}Text report saved to: {txt_path}{Colors.END}")

def main():
    """Main application loop"""
    while True:
        print_menu()
        choice = input("  Select an option: ").strip()
        
        if choice == '1':
            system_info_analysis()
        elif choice == '2':
            network_analysis()
        elif choice == '3':
            process_analysis()
        elif choice == '4':
            disk_analysis()
        elif choice == '5':
            memory_analysis()
        elif choice == '6':
            log_analyzer()
        elif choice == '7':
            port_scanner()
        elif choice == '8':
            generate_report()
        elif choice == '9':
            print(f"\n  {Colors.GREEN}Thank you for using Network & System Data Analyzer!{Colors.END}\n")
            break
        else:
            print(f"\n  {Colors.RED}Invalid option. Please try again.{Colors.END}")
        
        input(f"\n  {Colors.CYAN}Press Enter to continue...{Colors.END}")

if __name__ == "__main__":
    main()
