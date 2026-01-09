# SysAdmin Toolkit Pro

**Author:** Eyasu Solomon  
**Version:** 2.0  
**Language:** Bash  
**Platform:** Linux/Unix/Git Bash

## Overview

A comprehensive interactive TUI-based system administration toolkit for Linux/Unix systems. Features color-coded menus, ASCII art headers, and modular tools for system monitoring, network diagnostics, security auditing, and more.

## Features

### Main Dashboard
- **System Information** - OS, hostname, kernel, uptime, user details
- **CPU Information** - Model, cores, usage, load average
- **Memory Information** - Usage with visual progress bar
- **Disk Usage** - Color-coded warnings (green/yellow/red)
- **Network Information** - IP addresses, gateway, DNS, active connections
- **Process Manager** - Top 15 processes by CPU
- **Service Manager** - View and manage systemd services

### Network Tools Submenu
- **Ping Tool** - Test connectivity to any host
- **Port Scanner** - Scan specific ports on remote hosts
- **DNS Lookup** - Query DNS records
- **Traceroute** - Trace packet route
- **Network Statistics** - Socket and interface stats
- **Speed Test** - Download speed measurement

### Security Tools Submenu
- **Open Ports** - Check listening ports
- **Failed Login Attempts** - View auth log
- **SSH Sessions** - Monitor SSH connections
- **Firewall Status** - UFW/IPTables status
- **Security Audit** - SUID files, world-writable, UID 0 users

### Backup Utilities
- **Backup Directory** - Create tar.gz backups
- **Remote Backup (SCP)** - Copy to remote server
- **Restore Backup** - Extract from archive

### Log Analyzer
- **System/Auth/Kernel Logs** - View log files
- **Search Logs** - Grep across log files
- **Real-time Monitor** - tail -f on logs

## Files

| File | Description |
|------|-------------|
| `sysadmin_toolkit.sh` | Original console version |
| `sysadmin_toolkit_pro.sh` | **Enhanced TUI version** |

## Usage

```bash
chmod +x sysadmin_toolkit_pro.sh
./sysadmin_toolkit_pro.sh
```

## Menu Preview

```
╔══════════════════════════════════════════════════════════════════╗
║     ███████╗██╗   ██╗███████╗ █████╗ ██████╗ ███╗   ███╗        ║
║     ██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗██╔══██╗████╗ ████║        ║
║     ███████╗ ╚████╔╝ ███████╗███████║██║  ██║██╔████╔██║        ║
║              SysAdmin Toolkit Pro v2.0                           ║
╚══════════════════════════════════════════════════════════════════╝

  [1] System Information     [8] Network Tools     →
  [2] CPU Information        [9] Security Tools    →
  [3] Memory Information     [10] Backup Utilities →
  [4] Disk Usage             [11] Log Analyzer     →
  ...
```

## Skills Demonstrated

- Advanced Bash Scripting
- Interactive TUI Design
- System Administration
- Network Diagnostics
- Security Auditing
- Backup/Restore Operations
