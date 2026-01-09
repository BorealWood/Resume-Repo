#!/bin/bash
#===============================================================================
#
#          FILE:  sysadmin_toolkit.sh
#
#         USAGE:  ./sysadmin_toolkit.sh [command]
#
#   DESCRIPTION:  System Administration Automation Toolkit
#                 A collection of useful scripts for IT professionals
#
#        AUTHOR:  Eyasu Solomon
#       VERSION:  1.0
#       CREATED:  2025
#
#===============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

#===============================================================================
# UTILITY FUNCTIONS
#===============================================================================

print_header() {
    echo -e "\n${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${YELLOW}  $1${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

#===============================================================================
# SYSTEM INFORMATION
#===============================================================================

system_info() {
    print_header "SYSTEM INFORMATION"
    
    echo -e "${BOLD}Operating System:${NC}"
    echo "  Hostname:     $(hostname)"
    echo "  OS:           $(uname -o 2>/dev/null || echo 'Unknown')"
    echo "  Kernel:       $(uname -r)"
    echo "  Architecture: $(uname -m)"
    
    echo -e "\n${BOLD}Hardware:${NC}"
    if command -v nproc &> /dev/null; then
        echo "  CPU Cores:    $(nproc)"
    fi
    
    if [ -f /proc/meminfo ]; then
        total_mem=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
        total_mem_gb=$(echo "scale=2; $total_mem / 1024 / 1024" | bc 2>/dev/null || echo "N/A")
        echo "  Total RAM:    ${total_mem_gb} GB"
    fi
    
    echo -e "\n${BOLD}Current User:${NC}"
    echo "  Username:     $(whoami)"
    echo "  Home:         $HOME"
    echo "  Shell:        $SHELL"
    
    echo -e "\n${BOLD}System Uptime:${NC}"
    uptime -p 2>/dev/null || uptime
}

#===============================================================================
# DISK USAGE ANALYZER
#===============================================================================

disk_usage() {
    print_header "DISK USAGE ANALYSIS"
    
    echo -e "${BOLD}Filesystem Usage:${NC}\n"
    df -h | head -1
    echo "------------------------------------------------------------"
    df -h | tail -n +2 | while read line; do
        usage=$(echo $line | awk '{print $5}' | sed 's/%//')
        if [ ! -z "$usage" ] && [ "$usage" -ge 90 ] 2>/dev/null; then
            echo -e "${RED}$line${NC}"
        elif [ ! -z "$usage" ] && [ "$usage" -ge 70 ] 2>/dev/null; then
            echo -e "${YELLOW}$line${NC}"
        else
            echo "$line"
        fi
    done
    
    echo -e "\n${BOLD}Top 10 Largest Directories in Home:${NC}\n"
    du -h "$HOME" 2>/dev/null | sort -rh | head -10
}

#===============================================================================
# NETWORK DIAGNOSTICS
#===============================================================================

network_diagnostics() {
    print_header "NETWORK DIAGNOSTICS"
    
    echo -e "${BOLD}Network Interfaces:${NC}\n"
    if command -v ip &> /dev/null; then
        ip addr show 2>/dev/null | grep -E "^[0-9]+:|inet " | sed 's/^/  /'
    else
        ifconfig 2>/dev/null | grep -E "^[a-z]|inet " | sed 's/^/  /'
    fi
    
    echo -e "\n${BOLD}DNS Servers:${NC}"
    if [ -f /etc/resolv.conf ]; then
        grep nameserver /etc/resolv.conf | sed 's/^/  /'
    fi
    
    echo -e "\n${BOLD}Connectivity Test:${NC}"
    for host in "8.8.8.8" "1.1.1.1" "google.com"; do
        if ping -c 1 -W 2 $host &> /dev/null; then
            print_success "  $host - Reachable"
        else
            print_error "  $host - Unreachable"
        fi
    done
    
    echo -e "\n${BOLD}Active Connections:${NC}"
    if command -v ss &> /dev/null; then
        ss -tuln 2>/dev/null | head -15
    else
        netstat -tuln 2>/dev/null | head -15
    fi
}

#===============================================================================
# PROCESS MANAGER
#===============================================================================

process_manager() {
    print_header "PROCESS MANAGER"
    
    echo -e "${BOLD}Top 10 CPU Consumers:${NC}\n"
    ps aux --sort=-%cpu | head -11 | awk '{printf "  %-10s %-8s %5s%% %5s%%  %s\n", $1, $2, $3, $4, $11}'
    
    echo -e "\n${BOLD}Top 10 Memory Consumers:${NC}\n"
    ps aux --sort=-%mem | head -11 | awk '{printf "  %-10s %-8s %5s%% %5s%%  %s\n", $1, $2, $3, $4, $11}'
    
    echo -e "\n${BOLD}Process Count by User:${NC}"
    ps aux | awk '{print $1}' | sort | uniq -c | sort -rn | head -5 | sed 's/^/  /'
    
    echo -e "\n${BOLD}Total Running Processes:${NC} $(ps aux | wc -l)"
}

#===============================================================================
# SERVICE MANAGER
#===============================================================================

service_manager() {
    print_header "SERVICE MANAGER"
    
    if command -v systemctl &> /dev/null; then
        echo -e "${BOLD}Active Services:${NC}\n"
        systemctl list-units --type=service --state=running 2>/dev/null | head -20
        
        echo -e "\n${BOLD}Failed Services:${NC}\n"
        failed=$(systemctl list-units --type=service --state=failed 2>/dev/null | grep -c "failed")
        if [ "$failed" -gt 0 ]; then
            systemctl list-units --type=service --state=failed 2>/dev/null | head -10
        else
            print_success "No failed services"
        fi
    else
        print_warning "systemctl not available. Using service command."
        service --status-all 2>/dev/null | head -20
    fi
}

#===============================================================================
# LOG ANALYZER
#===============================================================================

log_analyzer() {
    print_header "LOG ANALYZER"
    
    log_file="${1:-/var/log/syslog}"
    
    if [ ! -f "$log_file" ]; then
        log_file="/var/log/messages"
    fi
    
    if [ -f "$log_file" ]; then
        echo -e "${BOLD}Analyzing: $log_file${NC}\n"
        
        echo -e "${BOLD}Error Count:${NC}"
        error_count=$(grep -ci "error" "$log_file" 2>/dev/null || echo "0")
        warning_count=$(grep -ci "warning" "$log_file" 2>/dev/null || echo "0")
        critical_count=$(grep -ci "critical\|fatal" "$log_file" 2>/dev/null || echo "0")
        
        echo "  Errors:    $error_count"
        echo "  Warnings:  $warning_count"
        echo "  Critical:  $critical_count"
        
        echo -e "\n${BOLD}Last 10 Errors:${NC}\n"
        grep -i "error" "$log_file" 2>/dev/null | tail -10 | sed 's/^/  /'
    else
        print_warning "No standard log file found. Specify path as argument."
    fi
}

#===============================================================================
# BACKUP UTILITY
#===============================================================================

backup_utility() {
    print_header "BACKUP UTILITY"
    
    source_dir="${1:-$HOME}"
    backup_dir="${2:-$HOME/backups}"
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_name="backup_${timestamp}.tar.gz"
    
    mkdir -p "$backup_dir"
    
    echo -e "${BOLD}Creating backup...${NC}"
    echo "  Source:      $source_dir"
    echo "  Destination: $backup_dir/$backup_name"
    
    if tar -czf "$backup_dir/$backup_name" -C "$(dirname "$source_dir")" "$(basename "$source_dir")" 2>/dev/null; then
        size=$(du -h "$backup_dir/$backup_name" | cut -f1)
        print_success "Backup created successfully ($size)"
    else
        print_error "Backup failed"
    fi
    
    echo -e "\n${BOLD}Recent Backups:${NC}"
    ls -lh "$backup_dir"/*.tar.gz 2>/dev/null | tail -5 | sed 's/^/  /'
}

#===============================================================================
# SECURITY AUDIT
#===============================================================================

security_audit() {
    print_header "SECURITY AUDIT"
    
    echo -e "${BOLD}User Accounts:${NC}"
    echo "  Total users:       $(wc -l < /etc/passwd)"
    echo "  Users with shell:  $(grep -v '/nologin\|/false' /etc/passwd | wc -l)"
    echo "  Root login:        $(if grep -q "^root:" /etc/shadow 2>/dev/null; then echo "Enabled"; else echo "Check manually"; fi)"
    
    echo -e "\n${BOLD}Password Policy:${NC}"
    if [ -f /etc/login.defs ]; then
        echo "  Max age:  $(grep ^PASS_MAX_DAYS /etc/login.defs 2>/dev/null | awk '{print $2}') days"
        echo "  Min age:  $(grep ^PASS_MIN_DAYS /etc/login.defs 2>/dev/null | awk '{print $2}') days"
        echo "  Min len:  $(grep ^PASS_MIN_LEN /etc/login.defs 2>/dev/null | awk '{print $2}') chars"
    fi
    
    echo -e "\n${BOLD}SSH Configuration:${NC}"
    if [ -f /etc/ssh/sshd_config ]; then
        echo "  Root login:     $(grep -i "^PermitRootLogin" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}' || echo "default")"
        echo "  Password auth:  $(grep -i "^PasswordAuthentication" /etc/ssh/sshd_config 2>/dev/null | awk '{print $2}' || echo "default")"
    fi
    
    echo -e "\n${BOLD}Open Ports:${NC}"
    if command -v ss &> /dev/null; then
        ss -tuln | grep LISTEN | awk '{print $5}' | sed 's/.*://' | sort -n | uniq | head -10 | tr '\n' ' '
        echo ""
    fi
    
    echo -e "\n${BOLD}Last 5 Failed Login Attempts:${NC}"
    if [ -f /var/log/auth.log ]; then
        grep "Failed password" /var/log/auth.log 2>/dev/null | tail -5 | sed 's/^/  /'
    elif [ -f /var/log/secure ]; then
        grep "Failed password" /var/log/secure 2>/dev/null | tail -5 | sed 's/^/  /'
    fi
}

#===============================================================================
# CLEANUP UTILITY
#===============================================================================

cleanup_utility() {
    print_header "SYSTEM CLEANUP"
    
    echo -e "${BOLD}Cleaning temporary files...${NC}\n"
    
    # Calculate space before
    before=$(df / | tail -1 | awk '{print $4}')
    
    # Clean common temp directories
    temp_dirs=("/tmp" "$HOME/.cache" "/var/tmp")
    
    for dir in "${temp_dirs[@]}"; do
        if [ -d "$dir" ]; then
            count=$(find "$dir" -type f 2>/dev/null | wc -l)
            print_info "Found $count files in $dir"
        fi
    done
    
    echo ""
    read -p "  Do you want to clean these directories? (y/n): " confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        # Clean user cache (older than 7 days)
        if [ -d "$HOME/.cache" ]; then
            find "$HOME/.cache" -type f -atime +7 -delete 2>/dev/null
            print_success "Cleaned ~/.cache (files older than 7 days)"
        fi
        
        after=$(df / | tail -1 | awk '{print $4}')
        freed=$((after - before))
        print_success "Freed approximately ${freed}K of disk space"
    else
        print_info "Cleanup cancelled"
    fi
}

#===============================================================================
# MAIN MENU
#===============================================================================

show_menu() {
    clear
    echo -e "${YELLOW}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║       SYSTEM ADMINISTRATION TOOLKIT v1.0                     ║"
    echo "║              Created by Eyasu Solomon                         ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo -e "${CYAN}"
    echo "║  1. System Information                                       ║"
    echo "║  2. Disk Usage Analysis                                      ║"
    echo "║  3. Network Diagnostics                                      ║"
    echo "║  4. Process Manager                                          ║"
    echo "║  5. Service Manager                                          ║"
    echo "║  6. Log Analyzer                                             ║"
    echo "║  7. Backup Utility                                           ║"
    echo "║  8. Security Audit                                           ║"
    echo "║  9. System Cleanup                                           ║"
    echo "║  0. Exit                                                     ║"
    echo -e "${YELLOW}"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

main() {
    # If argument provided, run that function directly
    if [ $# -gt 0 ]; then
        case "$1" in
            sysinfo)     system_info ;;
            disk)        disk_usage ;;
            network)     network_diagnostics ;;
            process)     process_manager ;;
            service)     service_manager ;;
            log)         log_analyzer "$2" ;;
            backup)      backup_utility "$2" "$3" ;;
            security)    security_audit ;;
            cleanup)     cleanup_utility ;;
            *)           echo "Usage: $0 {sysinfo|disk|network|process|service|log|backup|security|cleanup}" ;;
        esac
        exit 0
    fi
    
    # Interactive menu mode
    while true; do
        show_menu
        read -p "  Select an option: " choice
        
        case $choice in
            1) system_info ;;
            2) disk_usage ;;
            3) network_diagnostics ;;
            4) process_manager ;;
            5) service_manager ;;
            6) log_analyzer ;;
            7) backup_utility ;;
            8) security_audit ;;
            9) cleanup_utility ;;
            0) echo -e "\n${GREEN}Thank you for using SysAdmin Toolkit!${NC}\n"; exit 0 ;;
            *) print_error "Invalid option. Please try again." ;;
        esac
        
        echo ""
        read -p "  Press Enter to continue..."
    done
}

# Run main function
main "$@"
