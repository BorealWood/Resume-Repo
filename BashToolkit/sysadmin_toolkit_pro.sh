#!/bin/bash

#############################################################
#  SysAdmin Toolkit Pro - Interactive TUI Edition
#  Created by Eyasu Solomon
#  
#  A comprehensive system administration toolkit with
#  dialog-based menus for Linux/Unix systems.
#
#  Features:
#  - Interactive menu navigation
#  - System monitoring and health checks
#  - Network diagnostics and tools
#  - User and service management
#  - Disk analysis and cleanup
#  - Security auditing
#  - Log analysis
#  - Backup utilities
#############################################################

# Configuration
VERSION="2.0"
AUTHOR="Eyasu Solomon"
LOG_FILE="/tmp/sysadmin_toolkit.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Symbols
CHECK="${GREEN}✓${NC}"
CROSS="${RED}✗${NC}"
ARROW="${CYAN}➤${NC}"
INFO="${BLUE}ℹ${NC}"
WARN="${YELLOW}⚠${NC}"

# Check if running as root for certain operations
check_root() {
    if [[ $EUID -ne 0 ]]; then
        return 1
    fi
    return 0
}

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Print styled header
print_header() {
    clear
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                                                                  ║"
    echo "║     ███████╗██╗   ██╗███████╗ █████╗ ██████╗ ███╗   ███╗        ║"
    echo "║     ██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗██╔══██╗████╗ ████║        ║"
    echo "║     ███████╗ ╚████╔╝ ███████╗███████║██║  ██║██╔████╔██║        ║"
    echo "║     ╚════██║  ╚██╔╝  ╚════██║██╔══██║██║  ██║██║╚██╔╝██║        ║"
    echo "║     ███████║   ██║   ███████║██║  ██║██████╔╝██║ ╚═╝ ██║        ║"
    echo "║     ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝        ║"
    echo "║                                                                  ║"
    echo "║              SysAdmin Toolkit Pro v${VERSION}                         ║"
    echo "║              Created by ${AUTHOR}                        ║"
    echo "║                                                                  ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Print section header
section_header() {
    echo ""
    echo -e "${CYAN}┌──────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC} ${WHITE}$1${NC}"
    echo -e "${CYAN}└──────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
}

# Print menu option
menu_option() {
    echo -e "  ${YELLOW}[$1]${NC} $2"
}

# Wait for keypress
wait_key() {
    echo ""
    echo -e "${CYAN}Press any key to continue...${NC}"
    read -n 1 -s
}

# System Information
show_system_info() {
    section_header "📊 System Information"
    
    echo -e "${WHITE}Hostname:${NC}      $(hostname)"
    echo -e "${WHITE}OS:${NC}            $(uname -s) $(uname -r)"
    echo -e "${WHITE}Architecture:${NC}  $(uname -m)"
    echo -e "${WHITE}Kernel:${NC}        $(uname -r)"
    
    if [ -f /etc/os-release ]; then
        echo -e "${WHITE}Distribution:${NC}  $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '"')"
    fi
    
    echo -e "${WHITE}Uptime:${NC}        $(uptime -p 2>/dev/null || uptime | awk '{print $3,$4}' | tr -d ',')"
    echo -e "${WHITE}Current User:${NC}  $USER"
    echo -e "${WHITE}Shell:${NC}         $SHELL"
    echo -e "${WHITE}Date/Time:${NC}     $(date '+%Y-%m-%d %H:%M:%S %Z')"
    
    log "Displayed system information"
}

# CPU Information
show_cpu_info() {
    section_header "🖥️  CPU Information"
    
    if [ -f /proc/cpuinfo ]; then
        echo -e "${WHITE}Model:${NC}         $(grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)"
        echo -e "${WHITE}Cores:${NC}         $(grep -c processor /proc/cpuinfo)"
        echo -e "${WHITE}Architecture:${NC}  $(uname -m)"
        
        # CPU Usage
        cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 2>/dev/null || echo "N/A")
        echo -e "${WHITE}Usage:${NC}         ${cpu_usage}%"
        
        # Load Average
        load_avg=$(cat /proc/loadavg | awk '{print $1, $2, $3}')
        echo -e "${WHITE}Load Avg:${NC}      $load_avg"
    else
        echo -e "${YELLOW}CPU information not available on this system${NC}"
    fi
    
    log "Displayed CPU information"
}

# Memory Information
show_memory_info() {
    section_header "🧠 Memory Information"
    
    if command -v free &> /dev/null; then
        echo -e "${WHITE}Memory Usage:${NC}"
        free -h | head -2
        echo ""
        
        # Memory percentage
        mem_used=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100}')
        echo -e "${WHITE}Used:${NC} ${mem_used}%"
        
        # Visual bar
        bar_width=50
        filled=$(echo "$mem_used * $bar_width / 100" | bc 2>/dev/null || echo 25)
        bar=""
        for ((i=0; i<bar_width; i++)); do
            if [ $i -lt ${filled:-25} ]; then
                bar+="█"
            else
                bar+="░"
            fi
        done
        echo -e "${WHITE}[${GREEN}${bar}${NC}${WHITE}]${NC}"
    else
        echo -e "${YELLOW}free command not available${NC}"
    fi
    
    log "Displayed memory information"
}

# Disk Usage
show_disk_usage() {
    section_header "💾 Disk Usage"
    
    echo -e "${WHITE}Filesystem      Size  Used  Avail  Use%  Mounted on${NC}"
    echo "────────────────────────────────────────────────────────"
    
    df -h | grep -E '^/dev/' | while read line; do
        usage=$(echo "$line" | awk '{print $5}' | tr -d '%')
        if [ "$usage" -gt 90 ]; then
            color=$RED
        elif [ "$usage" -gt 70 ]; then
            color=$YELLOW
        else
            color=$GREEN
        fi
        echo -e "${color}$line${NC}"
    done
    
    echo ""
    echo -e "${WHITE}Total Disk Space:${NC}"
    df -h --total 2>/dev/null | grep total || df -h | tail -1
    
    log "Displayed disk usage"
}

# Network Information
show_network_info() {
    section_header "🌐 Network Information"
    
    echo -e "${WHITE}Hostname:${NC}      $(hostname)"
    
    # IP Addresses
    echo -e "\n${WHITE}IP Addresses:${NC}"
    if command -v ip &> /dev/null; then
        ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print "  " $2 " on " $NF}'
    elif command -v ifconfig &> /dev/null; then
        ifconfig | grep "inet " | grep -v "127.0.0.1" | awk '{print "  " $2}'
    fi
    
    # Default Gateway
    echo -e "\n${WHITE}Default Gateway:${NC}"
    ip route | grep default | awk '{print "  " $3}'
    
    # DNS Servers
    echo -e "\n${WHITE}DNS Servers:${NC}"
    if [ -f /etc/resolv.conf ]; then
        grep nameserver /etc/resolv.conf | awk '{print "  " $2}'
    fi
    
    # Active Connections
    echo -e "\n${WHITE}Active Connections:${NC}"
    if command -v ss &> /dev/null; then
        ss -tuln 2>/dev/null | head -10
    elif command -v netstat &> /dev/null; then
        netstat -tuln 2>/dev/null | head -10
    fi
    
    log "Displayed network information"
}

# Process Manager
show_processes() {
    section_header "⚙️  Process Manager"
    
    echo -e "${WHITE}Top 15 Processes by CPU:${NC}"
    echo ""
    ps aux --sort=-%cpu 2>/dev/null | head -16 || ps aux | head -16
    
    echo ""
    echo -e "${WHITE}Process Count:${NC} $(ps aux | wc -l)"
    
    log "Displayed process list"
}

# Service Manager
show_services() {
    section_header "🔧 Service Manager"
    
    if command -v systemctl &> /dev/null; then
        echo -e "${WHITE}Active Services:${NC}"
        systemctl list-units --type=service --state=running 2>/dev/null | head -20
    elif command -v service &> /dev/null; then
        echo -e "${WHITE}Services:${NC}"
        service --status-all 2>/dev/null | head -20
    else
        echo -e "${YELLOW}Service manager not found${NC}"
    fi
    
    log "Displayed services"
}

# Network Tools Menu
network_tools_menu() {
    while true; do
        print_header
        section_header "🔧 Network Tools"
        
        menu_option "1" "Ping Host"
        menu_option "2" "Port Scanner"
        menu_option "3" "DNS Lookup"
        menu_option "4" "Traceroute"
        menu_option "5" "Network Statistics"
        menu_option "6" "ARP Table"
        menu_option "7" "Check Internet Speed"
        menu_option "0" "Back to Main Menu"
        
        echo ""
        echo -ne "${ARROW} Enter your choice: "
        read choice
        
        case $choice in
            1) ping_host ;;
            2) port_scanner ;;
            3) dns_lookup ;;
            4) trace_route ;;
            5) network_stats ;;
            6) show_arp ;;
            7) speed_test ;;
            0) return ;;
            *) echo -e "${CROSS} Invalid option" ;;
        esac
        
        wait_key
    done
}

# Ping Host
ping_host() {
    echo ""
    echo -ne "${ARROW} Enter hostname or IP: "
    read host
    
    if [ -n "$host" ]; then
        section_header "Pinging $host"
        ping -c 5 "$host" 2>&1
        log "Pinged $host"
    fi
}

# Port Scanner
port_scanner() {
    echo ""
    echo -ne "${ARROW} Enter hostname or IP: "
    read host
    echo -ne "${ARROW} Enter ports (comma-separated, e.g., 22,80,443): "
    read ports
    
    if [ -n "$host" ] && [ -n "$ports" ]; then
        section_header "Scanning $host"
        
        IFS=',' read -ra PORT_ARRAY <<< "$ports"
        for port in "${PORT_ARRAY[@]}"; do
            port=$(echo "$port" | tr -d ' ')
            if timeout 2 bash -c "echo >/dev/tcp/$host/$port" 2>/dev/null; then
                echo -e "${CHECK} Port $port: ${GREEN}OPEN${NC}"
            else
                echo -e "${CROSS} Port $port: ${RED}CLOSED${NC}"
            fi
        done
        
        log "Scanned ports on $host"
    fi
}

# DNS Lookup
dns_lookup() {
    echo ""
    echo -ne "${ARROW} Enter domain: "
    read domain
    
    if [ -n "$domain" ]; then
        section_header "DNS Lookup: $domain"
        
        if command -v nslookup &> /dev/null; then
            nslookup "$domain"
        elif command -v dig &> /dev/null; then
            dig "$domain"
        elif command -v host &> /dev/null; then
            host "$domain"
        else
            echo -e "${YELLOW}No DNS lookup tool available${NC}"
        fi
        
        log "DNS lookup for $domain"
    fi
}

# Traceroute
trace_route() {
    echo ""
    echo -ne "${ARROW} Enter hostname or IP: "
    read host
    
    if [ -n "$host" ]; then
        section_header "Traceroute to $host"
        
        if command -v traceroute &> /dev/null; then
            traceroute "$host" 2>&1
        elif command -v tracepath &> /dev/null; then
            tracepath "$host" 2>&1
        else
            echo -e "${YELLOW}Traceroute not available${NC}"
        fi
        
        log "Traceroute to $host"
    fi
}

# Network Statistics
network_stats() {
    section_header "Network Statistics"
    
    if command -v ss &> /dev/null; then
        echo -e "${WHITE}Socket Summary:${NC}"
        ss -s
    fi
    
    echo ""
    echo -e "${WHITE}Interface Statistics:${NC}"
    if command -v ip &> /dev/null; then
        ip -s link | head -30
    fi
}

# ARP Table
show_arp() {
    section_header "ARP Table"
    
    if command -v arp &> /dev/null; then
        arp -a
    elif command -v ip &> /dev/null; then
        ip neigh
    fi
}

# Speed Test (simplified)
speed_test() {
    section_header "Internet Speed Test"
    
    echo -e "${INFO} Testing download speed..."
    
    if command -v curl &> /dev/null; then
        # Simple speed test using curl
        start_time=$(date +%s.%N)
        curl -s -o /dev/null http://speedtest.tele2.net/1MB.zip 2>/dev/null
        end_time=$(date +%s.%N)
        
        duration=$(echo "$end_time - $start_time" | bc)
        speed=$(echo "scale=2; 1 / $duration * 8" | bc)
        
        echo -e "${CHECK} Download speed: ~${GREEN}${speed} Mbps${NC}"
        echo -e "${INFO} (Based on 1MB test file)"
    else
        echo -e "${YELLOW}curl not available for speed test${NC}"
    fi
}

# Security Menu
security_menu() {
    while true; do
        print_header
        section_header "🔒 Security Tools"
        
        menu_option "1" "Check Open Ports"
        menu_option "2" "Failed Login Attempts"
        menu_option "3" "Active SSH Sessions"
        menu_option "4" "Firewall Status"
        menu_option "5" "User Login History"
        menu_option "6" "Password Policy Check"
        menu_option "7" "Security Audit"
        menu_option "0" "Back to Main Menu"
        
        echo ""
        echo -ne "${ARROW} Enter your choice: "
        read choice
        
        case $choice in
            1) check_open_ports ;;
            2) failed_logins ;;
            3) ssh_sessions ;;
            4) firewall_status ;;
            5) login_history ;;
            6) password_policy ;;
            7) security_audit ;;
            0) return ;;
            *) echo -e "${CROSS} Invalid option" ;;
        esac
        
        wait_key
    done
}

# Check Open Ports
check_open_ports() {
    section_header "Open Ports"
    
    if command -v ss &> /dev/null; then
        ss -tuln | grep LISTEN
    elif command -v netstat &> /dev/null; then
        netstat -tuln | grep LISTEN
    fi
}

# Failed Logins
failed_logins() {
    section_header "Failed Login Attempts"
    
    if [ -f /var/log/auth.log ]; then
        grep "Failed password" /var/log/auth.log 2>/dev/null | tail -20
    elif [ -f /var/log/secure ]; then
        grep "Failed password" /var/log/secure 2>/dev/null | tail -20
    else
        echo -e "${YELLOW}Auth log not accessible${NC}"
    fi
}

# SSH Sessions
ssh_sessions() {
    section_header "Active SSH Sessions"
    
    who | grep pts
    echo ""
    echo -e "${WHITE}Current connections:${NC}"
    ss -tn | grep :22 || echo "No SSH connections"
}

# Firewall Status
firewall_status() {
    section_header "Firewall Status"
    
    if command -v ufw &> /dev/null; then
        echo -e "${WHITE}UFW Status:${NC}"
        sudo ufw status 2>/dev/null || echo "Run as root to view"
    fi
    
    if command -v iptables &> /dev/null; then
        echo -e "\n${WHITE}IPTables Rules:${NC}"
        sudo iptables -L -n 2>/dev/null | head -20 || echo "Run as root to view"
    fi
}

# Login History
login_history() {
    section_header "Login History"
    
    if command -v last &> /dev/null; then
        last -20
    fi
}

# Password Policy
password_policy() {
    section_header "Password Policy Check"
    
    if [ -f /etc/login.defs ]; then
        echo -e "${WHITE}Password Aging Settings:${NC}"
        grep -E "^PASS_MAX_DAYS|^PASS_MIN_DAYS|^PASS_WARN_AGE|^PASS_MIN_LEN" /etc/login.defs
    fi
    
    if [ -f /etc/pam.d/common-password ]; then
        echo -e "\n${WHITE}PAM Password Requirements:${NC}"
        grep -v "^#" /etc/pam.d/common-password | head -10
    fi
}

# Security Audit
security_audit() {
    section_header "Security Audit Report"
    
    echo -e "${WHITE}1. SUID Files:${NC}"
    find / -perm -4000 -type f 2>/dev/null | head -10
    
    echo -e "\n${WHITE}2. World-Writable Files:${NC}"
    find /etc -perm -2 -type f 2>/dev/null | head -5
    
    echo -e "\n${WHITE}3. Users with UID 0:${NC}"
    awk -F: '($3 == "0") {print $1}' /etc/passwd
    
    echo -e "\n${WHITE}4. Users without passwords:${NC}"
    awk -F: '($2 == "" || $2 == "!") {print $1}' /etc/shadow 2>/dev/null || echo "Access denied"
    
    echo -e "\n${WHITE}5. Listening Services:${NC}"
    ss -tuln | grep LISTEN | wc -l
    echo " services listening"
    
    log "Security audit completed"
}

# Backup Menu
backup_menu() {
    while true; do
        print_header
        section_header "💾 Backup Utilities"
        
        menu_option "1" "Backup Directory"
        menu_option "2" "Backup to Remote (SCP)"
        menu_option "3" "Schedule Backup (Cron)"
        menu_option "4" "Restore from Backup"
        menu_option "5" "List Backups"
        menu_option "0" "Back to Main Menu"
        
        echo ""
        echo -ne "${ARROW} Enter your choice: "
        read choice
        
        case $choice in
            1) backup_directory ;;
            2) backup_remote ;;
            3) schedule_backup ;;
            4) restore_backup ;;
            5) list_backups ;;
            0) return ;;
            *) echo -e "${CROSS} Invalid option" ;;
        esac
        
        wait_key
    done
}

# Backup Directory
backup_directory() {
    echo ""
    echo -ne "${ARROW} Enter source directory: "
    read src
    echo -ne "${ARROW} Enter backup destination: "
    read dest
    
    if [ -d "$src" ]; then
        backup_name="backup_$(date +%Y%m%d_%H%M%S).tar.gz"
        
        echo -e "${INFO} Creating backup..."
        tar -czf "${dest}/${backup_name}" "$src" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo -e "${CHECK} Backup created: ${dest}/${backup_name}"
            log "Backup created: ${dest}/${backup_name}"
        else
            echo -e "${CROSS} Backup failed"
        fi
    else
        echo -e "${CROSS} Source directory not found"
    fi
}

# Backup to Remote
backup_remote() {
    echo ""
    echo -ne "${ARROW} Enter local file/directory: "
    read src
    echo -ne "${ARROW} Enter remote destination (user@host:/path): "
    read dest
    
    if [ -e "$src" ]; then
        echo -e "${INFO} Copying to remote..."
        scp -r "$src" "$dest"
        
        if [ $? -eq 0 ]; then
            echo -e "${CHECK} Transfer complete"
            log "Remote backup to $dest completed"
        else
            echo -e "${CROSS} Transfer failed"
        fi
    fi
}

# Schedule Backup
schedule_backup() {
    echo ""
    echo -e "${INFO} To schedule a backup, add this to crontab:"
    echo ""
    echo "# Daily backup at 2 AM"
    echo "0 2 * * * /path/to/sysadmin_toolkit.sh --backup /source /dest"
    echo ""
    echo "Use 'crontab -e' to edit your cron jobs"
}

# Restore Backup
restore_backup() {
    echo ""
    echo -ne "${ARROW} Enter backup file path: "
    read backup
    echo -ne "${ARROW} Enter restore destination: "
    read dest
    
    if [ -f "$backup" ]; then
        echo -e "${INFO} Restoring..."
        tar -xzf "$backup" -C "$dest" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo -e "${CHECK} Restore complete"
            log "Restored from $backup to $dest"
        else
            echo -e "${CROSS} Restore failed"
        fi
    else
        echo -e "${CROSS} Backup file not found"
    fi
}

# List Backups
list_backups() {
    echo ""
    echo -ne "${ARROW} Enter backup directory to search: "
    read dir
    
    if [ -d "$dir" ]; then
        section_header "Available Backups"
        ls -lh "$dir"/*.tar.gz 2>/dev/null || echo "No backups found"
    fi
}

# Log Analyzer Menu
log_menu() {
    while true; do
        print_header
        section_header "📋 Log Analyzer"
        
        menu_option "1" "View System Log"
        menu_option "2" "View Auth Log"
        menu_option "3" "View Kernel Log"
        menu_option "4" "Search Logs"
        menu_option "5" "Real-time Log Monitor"
        menu_option "6" "Log Statistics"
        menu_option "0" "Back to Main Menu"
        
        echo ""
        echo -ne "${ARROW} Enter your choice: "
        read choice
        
        case $choice in
            1) view_syslog ;;
            2) view_authlog ;;
            3) view_kernlog ;;
            4) search_logs ;;
            5) realtime_log ;;
            6) log_stats ;;
            0) return ;;
            *) echo -e "${CROSS} Invalid option" ;;
        esac
        
        wait_key
    done
}

# View Syslog
view_syslog() {
    section_header "System Log (last 50 lines)"
    
    if [ -f /var/log/syslog ]; then
        tail -50 /var/log/syslog
    elif [ -f /var/log/messages ]; then
        tail -50 /var/log/messages
    else
        echo -e "${YELLOW}System log not found${NC}"
    fi
}

# View Auth Log
view_authlog() {
    section_header "Authentication Log (last 50 lines)"
    
    if [ -f /var/log/auth.log ]; then
        tail -50 /var/log/auth.log
    elif [ -f /var/log/secure ]; then
        tail -50 /var/log/secure
    else
        echo -e "${YELLOW}Auth log not found${NC}"
    fi
}

# View Kernel Log
view_kernlog() {
    section_header "Kernel Log"
    dmesg | tail -50
}

# Search Logs
search_logs() {
    echo ""
    echo -ne "${ARROW} Enter search pattern: "
    read pattern
    
    if [ -n "$pattern" ]; then
        section_header "Search Results for: $pattern"
        grep -r "$pattern" /var/log/*.log 2>/dev/null | head -30
    fi
}

# Real-time Log
realtime_log() {
    echo ""
    echo -e "${INFO} Press Ctrl+C to stop"
    echo ""
    
    if [ -f /var/log/syslog ]; then
        tail -f /var/log/syslog
    elif [ -f /var/log/messages ]; then
        tail -f /var/log/messages
    fi
}

# Log Statistics
log_stats() {
    section_header "Log Statistics"
    
    echo -e "${WHITE}Log File Sizes:${NC}"
    ls -lh /var/log/*.log 2>/dev/null | head -10
    
    echo -e "\n${WHITE}Total Log Space:${NC}"
    du -sh /var/log 2>/dev/null
    
    echo -e "\n${WHITE}Error Count (last 24h):${NC}"
    grep -c -i "error" /var/log/syslog 2>/dev/null || echo "N/A"
}

# Main Menu
main_menu() {
    while true; do
        print_header
        
        menu_option "1" "System Information"
        menu_option "2" "CPU Information"
        menu_option "3" "Memory Information"
        menu_option "4" "Disk Usage"
        menu_option "5" "Network Information"
        menu_option "6" "Process Manager"
        menu_option "7" "Service Manager"
        echo ""
        menu_option "8" "Network Tools     ${CYAN}→${NC}"
        menu_option "9" "Security Tools    ${CYAN}→${NC}"
        menu_option "10" "Backup Utilities  ${CYAN}→${NC}"
        menu_option "11" "Log Analyzer      ${CYAN}→${NC}"
        echo ""
        menu_option "0" "Exit"
        
        echo ""
        echo -ne "${ARROW} Enter your choice: "
        read choice
        
        case $choice in
            1) show_system_info; wait_key ;;
            2) show_cpu_info; wait_key ;;
            3) show_memory_info; wait_key ;;
            4) show_disk_usage; wait_key ;;
            5) show_network_info; wait_key ;;
            6) show_processes; wait_key ;;
            7) show_services; wait_key ;;
            8) network_tools_menu ;;
            9) security_menu ;;
            10) backup_menu ;;
            11) log_menu ;;
            0) 
                echo ""
                echo -e "${GREEN}Thank you for using SysAdmin Toolkit Pro!${NC}"
                echo -e "${CYAN}Created by ${AUTHOR}${NC}"
                echo ""
                log "Session ended"
                exit 0
                ;;
            *)
                echo -e "${CROSS} Invalid option"
                sleep 1
                ;;
        esac
    done
}

# Start
log "Session started"
main_menu
