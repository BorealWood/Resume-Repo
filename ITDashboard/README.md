# IT Dashboard Pro - Web Application

**Author:** Eyasu Solomon  
**Version:** 2.1  
**Languages:** HTML5, CSS3, JavaScript  
**Type:** Single-Page Application

## Overview

A professional web-based IT dashboard with modern glassmorphism UI, real-time monitoring, interactive tools, and a built-in terminal. Demonstrates advanced front-end development, UI/UX design, and JavaScript programming.

## Files

| File | Description |
|------|-------------|
| `index.html` | Original dashboard version |
| `index_pro.html` | **Enhanced Pro version with full features** |

## Features

### Modern UI
- Glassmorphism dark theme with animated backgrounds
- Sidebar navigation with section highlighting
- Responsive design for all screen sizes
- Smooth CSS transitions and animations
- **Theme customization** (Dark, Light, Midnight Blue)
- **Accent color picker**

### Real-Time Monitoring
- **CPU Usage** - Animated progress bar with live updates
- **Memory Usage** - Visual bar with GB breakdown
- **Disk Usage** - Color-coded usage indicator
- **Network Status** - Speed (Mbps) and latency display
- **Configurable refresh rate** (1s, 2s, 5s, 10s)
- **Alert thresholds** for CPU and memory

### Network Activity Chart
- 12-hour bar chart with upload/download visualization
- Interactive hover effects with tooltips

### Process Manager
- **Full process table** with PID, Name, CPU%, Memory, Status
- **Search/filter** processes by name
- **End process** functionality
- **Refresh** process list

### Service Manager
- **Services table** with Name, Status, Startup Type
- **Filter** by status (All, Running, Stopped)
- **Start/Stop** individual services
- **Restart** service functionality

### System Logs Viewer
- **Log type** selection (System, Application, Security, etc.)
- **Log level** filtering (All, Info, Warning, Error)
- **Formatted entries** with timestamps and color-coded levels
- **Export logs** to text file

### Network Interfaces
- **Interface cards** showing eth0, wlan0, docker0, lo
- **IP addresses** and connection speeds
- **Active connections table** (Local, Remote, Status, Process)

### Network Tools Suite
- **Ping Tool** - Test connectivity with simulated responses
- **Port Scanner** - Scan multiple ports with results
- **DNS Lookup** - Query A, MX, NS records
- **Subnet Calculator** - CIDR calculations

### Interactive Terminal
- Built-in command-line interface
- Commands: help, date, whoami, uptime, neofetch, ps, df, clear

### Settings Modal
- **Theme selection** - Switch between Dark, Light, Midnight Blue
- **Accent color** - Custom color picker
- **Refresh rate** - Control monitoring update frequency
- **Auto-refresh toggle** - Enable/disable live updates
- **Alert thresholds** - Configure CPU and memory warning levels
- **Reset to defaults** - Restore original settings

### Quick Actions
- Speed Test simulation
- Clear Cache utility
- Export System Report (JSON)
- Password Generator

## Navigation

| Button | Section |
|--------|---------|
| Dashboard | Main monitoring view with stats and charts |
| Processes | Process Manager with table and controls |
| Network | Network interfaces and active connections |
| Services | Service Manager with start/stop controls |
| Tools | Network tools (Ping, Port Scan, DNS, Subnet) |
| Terminal | Interactive command-line interface |
| Logs | System log viewer with filtering |
| Settings | Theme, refresh rate, and alert configuration |
| About | Application information modal |

## How to Run

Simply open `index_pro.html` in any modern web browser:

```bash
# Option 1: Open directly
start index_pro.html

# Option 2: Use a local server
python -m http.server 8000
# Then visit http://localhost:8000/index_pro.html
```

## Design Features

- **Dark Theme** - Modern dark UI with gradient backgrounds
- **Multiple Themes** - Dark, Light, and Midnight Blue options
- **Responsive Layout** - Works on desktop and mobile devices
- **CSS Grid** - Flexible dashboard layout
- **Glassmorphism** - Frosted glass card effects
- **Smooth Animations** - CSS transitions and keyframe animations
- **No Dependencies** - Pure HTML, CSS, and JavaScript

## Screenshot

```
╔═══════════════════════════════════════════════════════════════╗
║                    🖥️ IT Dashboard Pro                        ║
╠═══════════════════════════════════════════════════════════════╣
║  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐              ║
║  │ CPU 45% │ │ RAM 62% │ │Disk 73% │ │ Online  │              ║
║  │ [█████░]│ │ [██████]│ │ [██████]│ │ 15ms    │              ║
║  └─────────┘ └─────────┘ └─────────┘ └─────────┘              ║
║                                                                ║
║  ┌──────────────────────────────────────────────────────────┐ ║
║  │                Network Activity Chart                     │ ║
║  │   █ █   █   █ █ █   █ █ █   █ █                          │ ║
║  └──────────────────────────────────────────────────────────┘ ║
╚═══════════════════════════════════════════════════════════════╝
```

## Skills Demonstrated

- HTML5 Semantic Markup
- CSS3 (Grid, Flexbox, Animations)
- JavaScript (DOM Manipulation, Event Handling)
- Responsive Web Design
- UI/UX Design Principles
- Data Visualization
