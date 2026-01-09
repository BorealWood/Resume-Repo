# IT Dashboard - Web Application

**Author:** Eyasu Solomon  
**Languages:** HTML5, CSS3, JavaScript  
**Type:** Single-Page Application

## Overview

An interactive web-based IT dashboard for monitoring system resources and network status. Demonstrates proficiency in front-end web development, UI/UX design, and JavaScript programming.

## Features

### Real-Time Monitoring
- **CPU Usage** - Live animated progress bar with color-coded warnings
- **Memory Usage** - Displays used/total RAM with percentage
- **Disk Usage** - Storage monitoring with visual indicator
- **Network Status** - Upload/download speeds and latency

### Network Activity Chart
- Visual bar chart showing hourly network activity
- Interactive hover effects with detailed tooltips

### System Services Table
- Display of running services with status indicators
- Shows uptime, CPU, and memory usage per service
- Color-coded status badges (Online/Warning/Offline)

### Interactive Tools
- **Ping Tool** - Simulate network connectivity tests
- **DNS Lookup** - Query domain name records
- **Port Scanner** - Check for open ports
- **Subnet Calculator** - IP address calculations
- **Password Generator** - Create secure passwords

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
