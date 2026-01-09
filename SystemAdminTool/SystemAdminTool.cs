using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net.NetworkInformation;
using System.Management;

namespace SystemAdminTool
{
    /// <summary>
    /// Interactive System Administration Tool
    /// Author: Eyasu Solomon
    /// Description: A comprehensive C# console application for system administration tasks
    /// demonstrating proficiency in C#, system management, and problem-solving.
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            Console.Title = "System Administration Tool v1.0 - Eyasu Solomon";
            Console.ForegroundColor = ConsoleColor.Cyan;
            
            while (true)
            {
                DisplayMainMenu();
                string choice = Console.ReadLine();
                
                switch (choice)
                {
                    case "1":
                        DisplaySystemInfo();
                        break;
                    case "2":
                        NetworkDiagnostics();
                        break;
                    case "3":
                        ProcessManager();
                        break;
                    case "4":
                        DiskAnalyzer();
                        break;
                    case "5":
                        ServiceManager();
                        break;
                    case "6":
                        EventLogViewer();
                        break;
                    case "7":
                        PerformanceMonitor();
                        break;
                    case "8":
                        Console.WriteLine("\nThank you for using System Admin Tool!");
                        return;
                    default:
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("\nInvalid option. Please try again.");
                        Console.ForegroundColor = ConsoleColor.Cyan;
                        break;
                }
                
                Console.WriteLine("\nPress any key to continue...");
                Console.ReadKey();
            }
        }

        static void DisplayMainMenu()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine("╔════════════════════════════════════════════════════════════╗");
            Console.WriteLine("║         SYSTEM ADMINISTRATION TOOL v1.0                    ║");
            Console.WriteLine("║              Created by Eyasu Solomon                      ║");
            Console.WriteLine("╠════════════════════════════════════════════════════════════╣");
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("║  1. System Information                                     ║");
            Console.WriteLine("║  2. Network Diagnostics                                    ║");
            Console.WriteLine("║  3. Process Manager                                        ║");
            Console.WriteLine("║  4. Disk Space Analyzer                                    ║");
            Console.WriteLine("║  5. Service Manager                                        ║");
            Console.WriteLine("║  6. Event Log Viewer                                       ║");
            Console.WriteLine("║  7. Performance Monitor                                    ║");
            Console.WriteLine("║  8. Exit                                                   ║");
            Console.WriteLine("╚════════════════════════════════════════════════════════════╝");
            Console.Write("\nSelect an option: ");
        }

        static void DisplaySystemInfo()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n═══════════════ SYSTEM INFORMATION ═══════════════\n");
            
            Console.WriteLine($"  Computer Name:     {Environment.MachineName}");
            Console.WriteLine($"  User Name:         {Environment.UserName}");
            Console.WriteLine($"  OS Version:        {Environment.OSVersion}");
            Console.WriteLine($"  64-bit OS:         {Environment.Is64BitOperatingSystem}");
            Console.WriteLine($"  Processor Count:   {Environment.ProcessorCount}");
            Console.WriteLine($"  System Directory:  {Environment.SystemDirectory}");
            Console.WriteLine($"  CLR Version:       {Environment.Version}");
            Console.WriteLine($"  System Uptime:     {GetSystemUptime()}");
            
            // Get memory info
            try
            {
                var computerInfo = new Microsoft.VisualBasic.Devices.ComputerInfo();
                Console.WriteLine($"  Total RAM:         {FormatBytes((long)computerInfo.TotalPhysicalMemory)}");
                Console.WriteLine($"  Available RAM:     {FormatBytes((long)computerInfo.AvailablePhysicalMemory)}");
            }
            catch
            {
                Console.WriteLine("  RAM Info:          Requires Microsoft.VisualBasic reference");
            }
        }

        static void NetworkDiagnostics()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n═══════════════ NETWORK DIAGNOSTICS ═══════════════\n");
            
            // Display network interfaces
            Console.WriteLine("  Network Interfaces:");
            Console.WriteLine("  -------------------");
            
            foreach (NetworkInterface ni in NetworkInterface.GetAllNetworkInterfaces())
            {
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine($"\n  Name: {ni.Name}");
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine($"    Description:  {ni.Description}");
                Console.WriteLine($"    Status:       {ni.OperationalStatus}");
                Console.WriteLine($"    Type:         {ni.NetworkInterfaceType}");
                Console.WriteLine($"    Speed:        {ni.Speed / 1000000} Mbps");
                
                var ipProps = ni.GetIPProperties();
                foreach (var ip in ipProps.UnicastAddresses)
                {
                    Console.WriteLine($"    IP Address:   {ip.Address}");
                }
            }
            
            // Ping test
            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.Write("\n  Enter host to ping (or press Enter for google.com): ");
            string host = Console.ReadLine();
            if (string.IsNullOrEmpty(host)) host = "google.com";
            
            try
            {
                Ping ping = new Ping();
                Console.WriteLine($"\n  Pinging {host}...");
                
                for (int i = 0; i < 4; i++)
                {
                    PingReply reply = ping.Send(host, 1000);
                    if (reply.Status == IPStatus.Success)
                    {
                        Console.ForegroundColor = ConsoleColor.Green;
                        Console.WriteLine($"    Reply from {reply.Address}: time={reply.RoundtripTime}ms TTL={reply.Options?.Ttl}");
                    }
                    else
                    {
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine($"    Request timed out.");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"  Error: {ex.Message}");
            }
        }

        static void ProcessManager()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n═══════════════ PROCESS MANAGER ═══════════════\n");
            
            Console.WriteLine("  1. List all processes");
            Console.WriteLine("  2. Search for a process");
            Console.WriteLine("  3. Kill a process");
            Console.WriteLine("  4. Top memory consumers");
            Console.Write("\n  Select option: ");
            
            string choice = Console.ReadLine();
            Process[] processes = Process.GetProcesses();
            
            switch (choice)
            {
                case "1":
                    Console.WriteLine("\n  {0,-30} {1,-10} {2,-15}", "Process Name", "PID", "Memory (MB)");
                    Console.WriteLine("  " + new string('-', 55));
                    foreach (var proc in processes)
                    {
                        try
                        {
                            Console.WriteLine("  {0,-30} {1,-10} {2,-15:F2}", 
                                proc.ProcessName.Length > 28 ? proc.ProcessName.Substring(0, 28) : proc.ProcessName, 
                                proc.Id, 
                                proc.WorkingSet64 / 1024.0 / 1024.0);
                        }
                        catch { }
                    }
                    break;
                    
                case "2":
                    Console.Write("\n  Enter process name to search: ");
                    string searchName = Console.ReadLine().ToLower();
                    Console.WriteLine("\n  {0,-30} {1,-10} {2,-15}", "Process Name", "PID", "Memory (MB)");
                    Console.WriteLine("  " + new string('-', 55));
                    foreach (var proc in processes)
                    {
                        if (proc.ProcessName.ToLower().Contains(searchName))
                        {
                            try
                            {
                                Console.WriteLine("  {0,-30} {1,-10} {2,-15:F2}", 
                                    proc.ProcessName, proc.Id, proc.WorkingSet64 / 1024.0 / 1024.0);
                            }
                            catch { }
                        }
                    }
                    break;
                    
                case "3":
                    Console.Write("\n  Enter PID to kill: ");
                    if (int.TryParse(Console.ReadLine(), out int pid))
                    {
                        try
                        {
                            Process.GetProcessById(pid).Kill();
                            Console.ForegroundColor = ConsoleColor.Green;
                            Console.WriteLine($"  Process {pid} terminated successfully.");
                        }
                        catch (Exception ex)
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine($"  Error: {ex.Message}");
                        }
                    }
                    break;
                    
                case "4":
                    Console.WriteLine("\n  Top 10 Memory Consumers:");
                    Console.WriteLine("  {0,-30} {1,-10} {2,-15}", "Process Name", "PID", "Memory (MB)");
                    Console.WriteLine("  " + new string('-', 55));
                    var sorted = new List<Process>(processes);
                    sorted.Sort((a, b) => {
                        try { return b.WorkingSet64.CompareTo(a.WorkingSet64); }
                        catch { return 0; }
                    });
                    for (int i = 0; i < Math.Min(10, sorted.Count); i++)
                    {
                        try
                        {
                            Console.WriteLine("  {0,-30} {1,-10} {2,-15:F2}", 
                                sorted[i].ProcessName, sorted[i].Id, sorted[i].WorkingSet64 / 1024.0 / 1024.0);
                        }
                        catch { }
                    }
                    break;
            }
        }

        static void DiskAnalyzer()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n═══════════════ DISK SPACE ANALYZER ═══════════════\n");
            
            DriveInfo[] drives = DriveInfo.GetDrives();
            
            foreach (DriveInfo drive in drives)
            {
                if (drive.IsReady)
                {
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.WriteLine($"  Drive {drive.Name}");
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine($"    Label:        {drive.VolumeLabel}");
                    Console.WriteLine($"    Type:         {drive.DriveType}");
                    Console.WriteLine($"    Format:       {drive.DriveFormat}");
                    Console.WriteLine($"    Total Size:   {FormatBytes(drive.TotalSize)}");
                    Console.WriteLine($"    Free Space:   {FormatBytes(drive.TotalFreeSpace)}");
                    Console.WriteLine($"    Used Space:   {FormatBytes(drive.TotalSize - drive.TotalFreeSpace)}");
                    
                    // Visual bar
                    double usedPercent = (double)(drive.TotalSize - drive.TotalFreeSpace) / drive.TotalSize * 100;
                    Console.Write("    Usage:        [");
                    int filled = (int)(usedPercent / 5);
                    Console.ForegroundColor = usedPercent > 90 ? ConsoleColor.Red : 
                                              usedPercent > 70 ? ConsoleColor.Yellow : ConsoleColor.Green;
                    Console.Write(new string('█', filled));
                    Console.ForegroundColor = ConsoleColor.DarkGray;
                    Console.Write(new string('░', 20 - filled));
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine($"] {usedPercent:F1}%\n");
                }
            }
        }

        static void ServiceManager()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n═══════════════ SERVICE MANAGER ═══════════════\n");
            Console.WriteLine("  Note: Some operations require administrator privileges.\n");
            
            Console.WriteLine("  1. List running services");
            Console.WriteLine("  2. List stopped services");
            Console.WriteLine("  3. Search for a service");
            Console.Write("\n  Select option: ");
            
            string choice = Console.ReadLine();
            
            try
            {
                System.ServiceProcess.ServiceController[] services = 
                    System.ServiceProcess.ServiceController.GetServices();
                
                Console.WriteLine("\n  {0,-40} {1,-15}", "Service Name", "Status");
                Console.WriteLine("  " + new string('-', 55));
                
                foreach (var service in services)
                {
                    bool show = false;
                    if (choice == "1" && service.Status == System.ServiceProcess.ServiceControllerStatus.Running)
                        show = true;
                    else if (choice == "2" && service.Status == System.ServiceProcess.ServiceControllerStatus.Stopped)
                        show = true;
                    else if (choice == "3")
                    {
                        Console.Write("  Enter service name to search: ");
                        string search = Console.ReadLine().ToLower();
                        if (service.ServiceName.ToLower().Contains(search) || 
                            service.DisplayName.ToLower().Contains(search))
                            show = true;
                    }
                    
                    if (show || choice == "3")
                    {
                        Console.ForegroundColor = service.Status == System.ServiceProcess.ServiceControllerStatus.Running 
                            ? ConsoleColor.Green : ConsoleColor.Red;
                        Console.WriteLine("  {0,-40} {1,-15}", 
                            service.DisplayName.Length > 38 ? service.DisplayName.Substring(0, 38) : service.DisplayName,
                            service.Status);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine($"  Error: {ex.Message}");
                Console.WriteLine("  Make sure to add reference to System.ServiceProcess");
            }
        }

        static void EventLogViewer()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n═══════════════ EVENT LOG VIEWER ═══════════════\n");
            
            Console.WriteLine("  1. Application Log");
            Console.WriteLine("  2. System Log");
            Console.WriteLine("  3. Security Log");
            Console.Write("\n  Select log type: ");
            
            string[] logTypes = { "Application", "System", "Security" };
            if (int.TryParse(Console.ReadLine(), out int logChoice) && logChoice >= 1 && logChoice <= 3)
            {
                try
                {
                    EventLog eventLog = new EventLog(logTypes[logChoice - 1]);
                    Console.WriteLine($"\n  Last 20 entries from {logTypes[logChoice - 1]} log:\n");
                    
                    int count = 0;
                    for (int i = eventLog.Entries.Count - 1; i >= 0 && count < 20; i--, count++)
                    {
                        EventLogEntry entry = eventLog.Entries[i];
                        Console.ForegroundColor = entry.EntryType == EventLogEntryType.Error ? ConsoleColor.Red :
                                                  entry.EntryType == EventLogEntryType.Warning ? ConsoleColor.Yellow :
                                                  ConsoleColor.Cyan;
                        Console.WriteLine($"  [{entry.TimeGenerated}] {entry.EntryType}: {entry.Source}");
                        Console.ForegroundColor = ConsoleColor.Gray;
                        string msg = entry.Message.Length > 80 ? entry.Message.Substring(0, 80) + "..." : entry.Message;
                        Console.WriteLine($"    {msg.Replace("\n", " ").Replace("\r", "")}\n");
                    }
                }
                catch (Exception ex)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine($"  Error: {ex.Message}");
                    Console.WriteLine("  Administrator privileges may be required.");
                }
            }
        }

        static void PerformanceMonitor()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("\n═══════════════ PERFORMANCE MONITOR ═══════════════\n");
            Console.WriteLine("  Monitoring system performance (Press any key to stop)...\n");
            
            PerformanceCounter cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            PerformanceCounter ramCounter = new PerformanceCounter("Memory", "Available MBytes");
            
            while (!Console.KeyAvailable)
            {
                float cpuUsage = cpuCounter.NextValue();
                float availableRam = ramCounter.NextValue();
                
                Console.SetCursorPosition(0, 5);
                
                // CPU Usage Bar
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.Write("  CPU Usage:    [");
                int cpuFilled = (int)(cpuUsage / 5);
                Console.ForegroundColor = cpuUsage > 90 ? ConsoleColor.Red : 
                                          cpuUsage > 70 ? ConsoleColor.Yellow : ConsoleColor.Green;
                Console.Write(new string('█', Math.Min(cpuFilled, 20)));
                Console.ForegroundColor = ConsoleColor.DarkGray;
                Console.Write(new string('░', Math.Max(0, 20 - cpuFilled)));
                Console.ForegroundColor = ConsoleColor.Cyan;
                Console.WriteLine($"] {cpuUsage:F1}%   ");
                
                // RAM Available
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine($"\n  Available RAM: {availableRam:F0} MB   ");
                
                System.Threading.Thread.Sleep(1000);
            }
            Console.ReadKey(true);
        }

        static string GetSystemUptime()
        {
            TimeSpan uptime = TimeSpan.FromMilliseconds(Environment.TickCount64);
            return $"{uptime.Days}d {uptime.Hours}h {uptime.Minutes}m {uptime.Seconds}s";
        }

        static string FormatBytes(long bytes)
        {
            string[] sizes = { "B", "KB", "MB", "GB", "TB" };
            int order = 0;
            double size = bytes;
            while (size >= 1024 && order < sizes.Length - 1)
            {
                order++;
                size /= 1024;
            }
            return $"{size:F2} {sizes[order]}";
        }
    }
}
