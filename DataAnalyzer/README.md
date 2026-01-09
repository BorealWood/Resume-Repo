# System Monitor Pro

**Author:** Eyasu Solomon  
**Version:** 2.0  
**Language:** Python 3  
**Framework:** Tkinter  
**Dependencies:** psutil

## Overview

A modern GUI system monitoring application built with Tkinter. Features a dark theme, real-time updates, and comprehensive tools for system analysis and network diagnostics.

## Files

| File | Description |
|------|-------------|
| `data_analyzer.py` | Original console version |
| `data_analyzer_gui.py` | **Full Tkinter GUI application** |

## Features

### Dashboard Tab
- Real-time CPU, Memory, Disk cards
- Network status with speed display
- Auto-refresh with threading
- Dark modern theme

### Process Manager Tab
- Live process listing with search
- CPU and Memory columns
- Kill process button
- Refresh functionality

### Network Tools Tab
- **Ping Tool** - Test connectivity with results
- **Port Scanner** - Multi-threaded port scanning
- Results display panel

### Disk Analyzer Tab
- Folder browser TreeView
- File listing with sizes
- Current path display
- Size calculations

### Log Analyzer Tab
- Log file viewer
- Level-based filtering
- Search functionality
- Syntax highlighting

### Tools Tab
- Password Generator
- Stopwatch utility
- Quick system actions

## Installation

```bash
# Install optional dependencies for full functionality
pip install psutil

# Run the application
python data_analyzer.py
```

## Usage

Run the script and select options from the interactive menu:

```
╔══════════════════════════════════════════════════════════════╗
║          NETWORK & SYSTEM DATA ANALYZER v1.0                 ║
║                Created by Eyasu Solomon                       ║
╠══════════════════════════════════════════════════════════════╣
║  1. System Information Analysis                              ║
║  2. Network Configuration Analysis                           ║
║  3. Process Statistics & Analysis                            ║
║  4. Disk Usage Analysis with Visualization                   ║
║  5. Memory Usage Trends                                      ║
║  6. Log File Analyzer                                        ║
║  7. Port Scanner                                             ║
║  8. Generate System Report (JSON/TXT)                        ║
║  9. Exit                                                     ║
╚══════════════════════════════════════════════════════════════╝
```

## Skills Demonstrated

- Python Programming
- Data Analysis & Visualization
- Network Programming
- System Administration
- JSON/File I/O Operations
- Object-Oriented Design
