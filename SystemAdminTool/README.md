# System Administration Tool Pro

**Author:** Eyasu Solomon  
**Version:** 2.0  
**Language:** C#  
**Framework:** .NET 6.0 (Windows Forms)

## Overview

A full-featured Windows Forms GUI application for system administration. Demonstrates proficiency in C#, Windows APIs, GUI development, and system management.

## Files

| File | Description |
|------|-------------|
| `SystemAdminTool.cs` | Original console version |
| `SystemAdminToolGUI.cs` | **Full Windows Forms GUI** |

## Features

### Dashboard Tab
- Real-time CPU and RAM gauges
- System uptime display
- Live refresh every 2 seconds

### Process Manager Tab
- DataGridView with all processes
- Search/filter by name
- Kill process functionality
- CPU/Memory usage columns

### Network Tab
- Network interface listing
- Ping tool with results
- IP address display
- Bytes sent/received stats

### Services Tab
- Windows services listing
- Start/Stop/Restart buttons
- Status filtering (Running/Stopped/All)
- Service search

### Disk Analyzer Tab
- TreeView folder browser
- Disk space breakdown
- File listing with sizes
- Drive selection

### Event Log Tab
- Application/System/Security logs
- Date range filtering
- Level filtering (Info/Warning/Error)
- Message details view

## How to Run

```bash
# Build the project
dotnet build

# Run the application
dotnet run
```

## Screenshots

```
╔════════════════════════════════════════════════════════════╗
║         SYSTEM ADMINISTRATION TOOL v1.0                    ║
║              Created by Eyasu Solomon                      ║
╠════════════════════════════════════════════════════════════╣
║  1. System Information                                     ║
║  2. Network Diagnostics                                    ║
║  3. Process Manager                                        ║
║  4. Disk Space Analyzer                                    ║
║  5. Service Manager                                        ║
║  6. Event Log Viewer                                       ║
║  7. Performance Monitor                                    ║
║  8. Exit                                                   ║
╚════════════════════════════════════════════════════════════╝
```

## Skills Demonstrated

- C# Programming
- Windows System APIs
- Network Programming
- Process Management
- Performance Monitoring
- Console UI Design
