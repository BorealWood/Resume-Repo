# IT Dashboard Pro - Web Application

**Author:** Eyasu Solomon  
**Version:** 2.0  
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

### Real-Time Monitoring
- **CPU Usage** - Animated progress bar with live updates
- **Memory Usage** - Visual bar with GB breakdown
- **Disk Usage** - Color-coded usage indicator
- **Network Status** - Speed (Mbps) and latency display

### Network Activity Chart
- 12-hour bar chart with upload/download visualization
- Interactive hover effects with tooltips

### Process Manager
- Top 5 processes with CPU/memory stats
- Process icons and PID display

### Services Grid
- 6 service cards with status indicators
- Online/Warning/Offline states with glow effects

### Network Tools Suite
- **Ping Tool** - Test connectivity with simulated responses
- **Port Scanner** - Scan multiple ports with results
- **DNS Lookup** - Query A, MX, NS records
- **Subnet Calculator** - CIDR calculations

### Interactive Terminal
- Built-in command-line interface
- Commands: help, date, whoami, uptime, neofetch, ps, df, clear

### Quick Actions
- Speed Test simulation
- Clear Cache utility
- Export System Report (JSON)
- Password Generator

## How to Run

Simply open `index.html` in any modern web browser:

```bash
# Option 1: Open directly
start index.html

# Option 2: Use a local server
python -m http.server 8000
# Then visit http://localhost:8000
```

## Design Features

- **Dark Theme** - Modern dark UI with gradient backgrounds
- **Responsive Layout** - Works on desktop and mobile devices
- **CSS Grid** - Flexible dashboard layout
- **Glassmorphism** - Frosted glass card effects
- **Smooth Animations** - CSS transitions and keyframe animations
- **No Dependencies** - Pure HTML, CSS, and JavaScript

## Screenshot

```
╔═══════════════════════════════════════════════════════════════╗
║                    🖥️ IT Dashboard                            ║
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
