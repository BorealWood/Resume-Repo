using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net.NetworkInformation;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Management;
using System.ServiceProcess;

namespace SystemAdminToolGUI
{
    /// <summary>
    /// Advanced System Administration Tool with Full Windows Forms GUI
    /// Author: Eyasu Solomon
    /// Features: Real-time monitoring, process management, network tools, service control
    /// </summary>
    public class MainForm : Form
    {
        // UI Components
        private TabControl tabControl;
        private TabPage tabDashboard, tabProcesses, tabNetwork, tabServices, tabDisk, tabEventLog;
        private System.Windows.Forms.Timer refreshTimer;
        private StatusStrip statusStrip;
        private ToolStripStatusLabel statusLabel;
        private MenuStrip menuStrip;
        
        // Dashboard components
        private ProgressBar cpuProgressBar, memoryProgressBar, diskProgressBar;
        private Label lblCpuValue, lblMemoryValue, lblDiskValue;
        private Label lblSystemInfo, lblUptime;
        private ListView lvQuickStats;
        
        // Process tab components
        private ListView lvProcesses;
        private TextBox txtProcessSearch;
        private Button btnKillProcess, btnRefreshProcesses;
        private ComboBox cmbSortBy;
        
        // Network tab components
        private ListView lvNetworkInterfaces;
        private TextBox txtPingHost;
        private Button btnPing;
        private RichTextBox rtbPingResults;
        private ListView lvConnections;
        
        // Services tab components
        private ListView lvServices;
        private Button btnStartService, btnStopService, btnRestartService;
        private TextBox txtServiceSearch;
        private ComboBox cmbServiceFilter;
        
        // Disk tab components
        private ListView lvDisks;
        private TreeView tvFolderBrowser;
        private ListView lvFolderContents;
        private Label lblSelectedPath;
        
        // Event Log tab components
        private ListView lvEventLog;
        private ComboBox cmbLogType;
        private DateTimePicker dtpFromDate, dtpToDate;
        private Button btnFilterLogs;
        private ComboBox cmbLogLevel;
        
        // Performance counters
        private PerformanceCounter cpuCounter, ramCounter;
        
        public MainForm()
        {
            InitializeComponent();
            InitializePerformanceCounters();
            LoadInitialData();
            StartMonitoring();
        }
        
        private void InitializeComponent()
        {
            this.Text = "System Administration Tool v2.0 - Eyasu Solomon";
            this.Size = new Size(1200, 800);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.Icon = SystemIcons.Application;
            this.MinimumSize = new Size(900, 600);
            
            // Menu Strip
            menuStrip = new MenuStrip();
            var fileMenu = new ToolStripMenuItem("File");
            fileMenu.DropDownItems.Add("Export Report", null, ExportReport_Click);
            fileMenu.DropDownItems.Add(new ToolStripSeparator());
            fileMenu.DropDownItems.Add("Exit", null, (s, e) => Application.Exit());
            
            var toolsMenu = new ToolStripMenuItem("Tools");
            toolsMenu.DropDownItems.Add("Refresh All", null, (s, e) => RefreshAll());
            toolsMenu.DropDownItems.Add("System Information", null, ShowSystemInfo_Click);
            toolsMenu.DropDownItems.Add("Network Speed Test", null, NetworkSpeedTest_Click);
            
            var helpMenu = new ToolStripMenuItem("Help");
            helpMenu.DropDownItems.Add("About", null, ShowAbout_Click);
            
            menuStrip.Items.AddRange(new ToolStripItem[] { fileMenu, toolsMenu, helpMenu });
            this.MainMenuStrip = menuStrip;
            this.Controls.Add(menuStrip);
            
            // Status Strip
            statusStrip = new StatusStrip();
            statusLabel = new ToolStripStatusLabel("Ready");
            var lblTime = new ToolStripStatusLabel();
            lblTime.Alignment = ToolStripItemAlignment.Right;
            
            var clockTimer = new System.Windows.Forms.Timer { Interval = 1000 };
            clockTimer.Tick += (s, e) => lblTime.Text = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            clockTimer.Start();
            
            statusStrip.Items.AddRange(new ToolStripItem[] { statusLabel, new ToolStripStatusLabel { Spring = true }, lblTime });
            this.Controls.Add(statusStrip);
            
            // Tab Control
            tabControl = new TabControl();
            tabControl.Dock = DockStyle.Fill;
            tabControl.Font = new Font("Segoe UI", 10);
            
            InitializeDashboardTab();
            InitializeProcessesTab();
            InitializeNetworkTab();
            InitializeServicesTab();
            InitializeDiskTab();
            InitializeEventLogTab();
            
            tabControl.TabPages.AddRange(new TabPage[] { 
                tabDashboard, tabProcesses, tabNetwork, tabServices, tabDisk, tabEventLog 
            });
            
            this.Controls.Add(tabControl);
            tabControl.BringToFront();
        }
        
        private void InitializeDashboardTab()
        {
            tabDashboard = new TabPage("📊 Dashboard");
            tabDashboard.BackColor = Color.FromArgb(240, 240, 245);
            
            // Header Panel
            var headerPanel = new Panel {
                Dock = DockStyle.Top,
                Height = 80,
                BackColor = Color.FromArgb(0, 120, 215)
            };
            
            var titleLabel = new Label {
                Text = "System Dashboard",
                Font = new Font("Segoe UI", 24, FontStyle.Bold),
                ForeColor = Color.White,
                AutoSize = true,
                Location = new Point(20, 20)
            };
            headerPanel.Controls.Add(titleLabel);
            
            // Stats Panel
            var statsPanel = new FlowLayoutPanel {
                Location = new Point(20, 100),
                Size = new Size(1140, 200),
                FlowDirection = FlowDirection.LeftToRight
            };
            
            // CPU Card
            var cpuCard = CreateStatCard("CPU Usage", out cpuProgressBar, out lblCpuValue, Color.FromArgb(0, 150, 136));
            
            // Memory Card
            var memoryCard = CreateStatCard("Memory Usage", out memoryProgressBar, out lblMemoryValue, Color.FromArgb(156, 39, 176));
            
            // Disk Card  
            var diskCard = CreateStatCard("Disk Usage", out diskProgressBar, out lblDiskValue, Color.FromArgb(255, 152, 0));
            
            statsPanel.Controls.AddRange(new Control[] { cpuCard, memoryCard, diskCard });
            
            // System Info Panel
            var infoPanel = new GroupBox {
                Text = "System Information",
                Location = new Point(20, 320),
                Size = new Size(550, 350),
                Font = new Font("Segoe UI", 10)
            };
            
            lblSystemInfo = new Label {
                Location = new Point(15, 30),
                Size = new Size(520, 300),
                Font = new Font("Consolas", 9)
            };
            infoPanel.Controls.Add(lblSystemInfo);
            
            // Quick Stats Panel
            var quickStatsPanel = new GroupBox {
                Text = "Quick Statistics",
                Location = new Point(590, 320),
                Size = new Size(570, 350),
                Font = new Font("Segoe UI", 10)
            };
            
            lvQuickStats = new ListView {
                Location = new Point(15, 30),
                Size = new Size(540, 300),
                View = View.Details,
                FullRowSelect = true,
                GridLines = true
            };
            lvQuickStats.Columns.Add("Metric", 250);
            lvQuickStats.Columns.Add("Value", 270);
            quickStatsPanel.Controls.Add(lvQuickStats);
            
            tabDashboard.Controls.AddRange(new Control[] { headerPanel, statsPanel, infoPanel, quickStatsPanel });
        }
        
        private Panel CreateStatCard(string title, out ProgressBar progressBar, out Label valueLabel, Color accentColor)
        {
            var card = new Panel {
                Size = new Size(350, 180),
                BackColor = Color.White,
                Margin = new Padding(10),
                Padding = new Padding(20)
            };
            card.Paint += (s, e) => {
                e.Graphics.DrawRectangle(new Pen(Color.LightGray), 0, 0, card.Width - 1, card.Height - 1);
            };
            
            var titleLbl = new Label {
                Text = title,
                Font = new Font("Segoe UI", 12, FontStyle.Bold),
                ForeColor = Color.FromArgb(60, 60, 60),
                Location = new Point(20, 15),
                AutoSize = true
            };
            
            valueLabel = new Label {
                Text = "0%",
                Font = new Font("Segoe UI", 36, FontStyle.Bold),
                ForeColor = accentColor,
                Location = new Point(20, 45),
                AutoSize = true
            };
            
            progressBar = new ProgressBar {
                Location = new Point(20, 130),
                Size = new Size(310, 25),
                Style = ProgressBarStyle.Continuous
            };
            
            card.Controls.AddRange(new Control[] { titleLbl, valueLabel, progressBar });
            return card;
        }
        
        private void InitializeProcessesTab()
        {
            tabProcesses = new TabPage("⚙️ Processes");
            tabProcesses.BackColor = Color.White;
            
            // Toolbar
            var toolbar = new Panel {
                Dock = DockStyle.Top,
                Height = 50,
                BackColor = Color.FromArgb(250, 250, 250),
                Padding = new Padding(10)
            };
            
            txtProcessSearch = new TextBox {
                Location = new Point(10, 12),
                Size = new Size(200, 25),
                PlaceholderText = "Search processes..."
            };
            txtProcessSearch.TextChanged += (s, e) => FilterProcesses();
            
            cmbSortBy = new ComboBox {
                Location = new Point(220, 12),
                Size = new Size(150, 25),
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            cmbSortBy.Items.AddRange(new[] { "Name", "PID", "CPU %", "Memory", "Status" });
            cmbSortBy.SelectedIndex = 0;
            cmbSortBy.SelectedIndexChanged += (s, e) => SortProcesses();
            
            btnRefreshProcesses = new Button {
                Text = "🔄 Refresh",
                Location = new Point(400, 10),
                Size = new Size(100, 30)
            };
            btnRefreshProcesses.Click += (s, e) => LoadProcesses();
            
            btnKillProcess = new Button {
                Text = "❌ End Task",
                Location = new Point(510, 10),
                Size = new Size(100, 30),
                BackColor = Color.FromArgb(220, 53, 69),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnKillProcess.Click += KillProcess_Click;
            
            toolbar.Controls.AddRange(new Control[] { txtProcessSearch, cmbSortBy, btnRefreshProcesses, btnKillProcess });
            
            // Process List
            lvProcesses = new ListView {
                Dock = DockStyle.Fill,
                View = View.Details,
                FullRowSelect = true,
                GridLines = true,
                Font = new Font("Segoe UI", 9)
            };
            lvProcesses.Columns.Add("Name", 200);
            lvProcesses.Columns.Add("PID", 70);
            lvProcesses.Columns.Add("CPU %", 80);
            lvProcesses.Columns.Add("Memory (MB)", 100);
            lvProcesses.Columns.Add("Threads", 70);
            lvProcesses.Columns.Add("Status", 100);
            lvProcesses.Columns.Add("User", 120);
            lvProcesses.Columns.Add("Start Time", 150);
            
            tabProcesses.Controls.Add(lvProcesses);
            tabProcesses.Controls.Add(toolbar);
        }
        
        private void InitializeNetworkTab()
        {
            tabNetwork = new TabPage("🌐 Network");
            tabNetwork.BackColor = Color.White;
            
            var splitContainer = new SplitContainer {
                Dock = DockStyle.Fill,
                Orientation = Orientation.Horizontal,
                SplitterDistance = 250
            };
            
            // Top: Network Interfaces
            var topPanel = new GroupBox {
                Text = "Network Interfaces",
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10)
            };
            
            lvNetworkInterfaces = new ListView {
                Dock = DockStyle.Fill,
                View = View.Details,
                FullRowSelect = true,
                GridLines = true
            };
            lvNetworkInterfaces.Columns.Add("Name", 200);
            lvNetworkInterfaces.Columns.Add("Status", 80);
            lvNetworkInterfaces.Columns.Add("Type", 120);
            lvNetworkInterfaces.Columns.Add("Speed", 100);
            lvNetworkInterfaces.Columns.Add("IP Address", 150);
            lvNetworkInterfaces.Columns.Add("MAC Address", 150);
            topPanel.Controls.Add(lvNetworkInterfaces);
            
            // Bottom: Ping Tool & Connections
            var bottomSplit = new SplitContainer {
                Dock = DockStyle.Fill,
                Orientation = Orientation.Vertical,
                SplitterDistance = 400
            };
            
            // Ping Tool
            var pingPanel = new GroupBox {
                Text = "Ping Tool",
                Dock = DockStyle.Fill
            };
            
            txtPingHost = new TextBox {
                Location = new Point(15, 30),
                Size = new Size(250, 25),
                Text = "google.com"
            };
            
            btnPing = new Button {
                Text = "Ping",
                Location = new Point(275, 28),
                Size = new Size(80, 27)
            };
            btnPing.Click += Ping_Click;
            
            rtbPingResults = new RichTextBox {
                Location = new Point(15, 65),
                Size = new Size(360, 200),
                ReadOnly = true,
                Font = new Font("Consolas", 9),
                BackColor = Color.FromArgb(30, 30, 30),
                ForeColor = Color.LightGreen
            };
            
            pingPanel.Controls.AddRange(new Control[] { txtPingHost, btnPing, rtbPingResults });
            
            // Active Connections
            var connPanel = new GroupBox {
                Text = "Active Connections",
                Dock = DockStyle.Fill
            };
            
            lvConnections = new ListView {
                Dock = DockStyle.Fill,
                View = View.Details,
                FullRowSelect = true,
                GridLines = true
            };
            lvConnections.Columns.Add("Local Address", 150);
            lvConnections.Columns.Add("Local Port", 80);
            lvConnections.Columns.Add("Remote Address", 150);
            lvConnections.Columns.Add("Remote Port", 80);
            lvConnections.Columns.Add("State", 100);
            connPanel.Controls.Add(lvConnections);
            
            bottomSplit.Panel1.Controls.Add(pingPanel);
            bottomSplit.Panel2.Controls.Add(connPanel);
            
            splitContainer.Panel1.Controls.Add(topPanel);
            splitContainer.Panel2.Controls.Add(bottomSplit);
            
            tabNetwork.Controls.Add(splitContainer);
        }
        
        private void InitializeServicesTab()
        {
            tabServices = new TabPage("🔧 Services");
            tabServices.BackColor = Color.White;
            
            // Toolbar
            var toolbar = new Panel {
                Dock = DockStyle.Top,
                Height = 60,
                BackColor = Color.FromArgb(250, 250, 250),
                Padding = new Padding(10)
            };
            
            txtServiceSearch = new TextBox {
                Location = new Point(10, 18),
                Size = new Size(200, 25),
                PlaceholderText = "Search services..."
            };
            txtServiceSearch.TextChanged += (s, e) => FilterServices();
            
            cmbServiceFilter = new ComboBox {
                Location = new Point(220, 18),
                Size = new Size(120, 25),
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            cmbServiceFilter.Items.AddRange(new[] { "All", "Running", "Stopped", "Paused" });
            cmbServiceFilter.SelectedIndex = 0;
            cmbServiceFilter.SelectedIndexChanged += (s, e) => FilterServices();
            
            btnStartService = new Button {
                Text = "▶ Start",
                Location = new Point(400, 15),
                Size = new Size(90, 30),
                BackColor = Color.FromArgb(40, 167, 69),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnStartService.Click += StartService_Click;
            
            btnStopService = new Button {
                Text = "⏹ Stop",
                Location = new Point(500, 15),
                Size = new Size(90, 30),
                BackColor = Color.FromArgb(220, 53, 69),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnStopService.Click += StopService_Click;
            
            btnRestartService = new Button {
                Text = "🔄 Restart",
                Location = new Point(600, 15),
                Size = new Size(90, 30),
                BackColor = Color.FromArgb(0, 123, 255),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnRestartService.Click += RestartService_Click;
            
            toolbar.Controls.AddRange(new Control[] { 
                txtServiceSearch, cmbServiceFilter, btnStartService, btnStopService, btnRestartService 
            });
            
            // Services List
            lvServices = new ListView {
                Dock = DockStyle.Fill,
                View = View.Details,
                FullRowSelect = true,
                GridLines = true,
                Font = new Font("Segoe UI", 9)
            };
            lvServices.Columns.Add("Display Name", 300);
            lvServices.Columns.Add("Service Name", 180);
            lvServices.Columns.Add("Status", 100);
            lvServices.Columns.Add("Start Type", 100);
            lvServices.Columns.Add("Account", 150);
            
            tabServices.Controls.Add(lvServices);
            tabServices.Controls.Add(toolbar);
        }
        
        private void InitializeDiskTab()
        {
            tabDisk = new TabPage("💾 Disk");
            tabDisk.BackColor = Color.White;
            
            var splitContainer = new SplitContainer {
                Dock = DockStyle.Fill,
                Orientation = Orientation.Horizontal,
                SplitterDistance = 200
            };
            
            // Top: Drive Overview
            var drivePanel = new GroupBox {
                Text = "Drives",
                Dock = DockStyle.Fill
            };
            
            lvDisks = new ListView {
                Dock = DockStyle.Fill,
                View = View.Details,
                FullRowSelect = true,
                GridLines = true
            };
            lvDisks.Columns.Add("Drive", 60);
            lvDisks.Columns.Add("Label", 150);
            lvDisks.Columns.Add("Type", 100);
            lvDisks.Columns.Add("File System", 80);
            lvDisks.Columns.Add("Total Size", 100);
            lvDisks.Columns.Add("Free Space", 100);
            lvDisks.Columns.Add("Used", 80);
            lvDisks.Columns.Add("Usage %", 80);
            drivePanel.Controls.Add(lvDisks);
            
            // Bottom: File Browser
            var browserSplit = new SplitContainer {
                Dock = DockStyle.Fill,
                SplitterDistance = 300
            };
            
            var folderPanel = new GroupBox {
                Text = "Folders",
                Dock = DockStyle.Fill
            };
            
            tvFolderBrowser = new TreeView {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 9)
            };
            tvFolderBrowser.AfterSelect += FolderBrowser_AfterSelect;
            folderPanel.Controls.Add(tvFolderBrowser);
            
            var contentsPanel = new GroupBox {
                Text = "Contents",
                Dock = DockStyle.Fill
            };
            
            lblSelectedPath = new Label {
                Dock = DockStyle.Top,
                Height = 25,
                Font = new Font("Segoe UI", 9),
                BackColor = Color.FromArgb(240, 240, 240),
                Padding = new Padding(5)
            };
            
            lvFolderContents = new ListView {
                Dock = DockStyle.Fill,
                View = View.Details,
                FullRowSelect = true,
                GridLines = true
            };
            lvFolderContents.Columns.Add("Name", 250);
            lvFolderContents.Columns.Add("Type", 100);
            lvFolderContents.Columns.Add("Size", 100);
            lvFolderContents.Columns.Add("Modified", 150);
            
            contentsPanel.Controls.Add(lvFolderContents);
            contentsPanel.Controls.Add(lblSelectedPath);
            
            browserSplit.Panel1.Controls.Add(folderPanel);
            browserSplit.Panel2.Controls.Add(contentsPanel);
            
            splitContainer.Panel1.Controls.Add(drivePanel);
            splitContainer.Panel2.Controls.Add(browserSplit);
            
            tabDisk.Controls.Add(splitContainer);
        }
        
        private void InitializeEventLogTab()
        {
            tabEventLog = new TabPage("📋 Event Log");
            tabEventLog.BackColor = Color.White;
            
            // Toolbar
            var toolbar = new Panel {
                Dock = DockStyle.Top,
                Height = 60,
                BackColor = Color.FromArgb(250, 250, 250)
            };
            
            var lblLogType = new Label { Text = "Log:", Location = new Point(10, 20), AutoSize = true };
            cmbLogType = new ComboBox {
                Location = new Point(50, 17),
                Size = new Size(120, 25),
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            cmbLogType.Items.AddRange(new[] { "Application", "System", "Security" });
            cmbLogType.SelectedIndex = 0;
            
            var lblLevel = new Label { Text = "Level:", Location = new Point(190, 20), AutoSize = true };
            cmbLogLevel = new ComboBox {
                Location = new Point(235, 17),
                Size = new Size(100, 25),
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            cmbLogLevel.Items.AddRange(new[] { "All", "Error", "Warning", "Information" });
            cmbLogLevel.SelectedIndex = 0;
            
            var lblFrom = new Label { Text = "From:", Location = new Point(360, 20), AutoSize = true };
            dtpFromDate = new DateTimePicker {
                Location = new Point(405, 17),
                Size = new Size(130, 25),
                Value = DateTime.Now.AddDays(-7)
            };
            
            var lblTo = new Label { Text = "To:", Location = new Point(550, 20), AutoSize = true };
            dtpToDate = new DateTimePicker {
                Location = new Point(580, 17),
                Size = new Size(130, 25)
            };
            
            btnFilterLogs = new Button {
                Text = "🔍 Filter",
                Location = new Point(730, 15),
                Size = new Size(80, 28)
            };
            btnFilterLogs.Click += FilterLogs_Click;
            
            toolbar.Controls.AddRange(new Control[] { 
                lblLogType, cmbLogType, lblLevel, cmbLogLevel, 
                lblFrom, dtpFromDate, lblTo, dtpToDate, btnFilterLogs 
            });
            
            // Event Log List
            lvEventLog = new ListView {
                Dock = DockStyle.Fill,
                View = View.Details,
                FullRowSelect = true,
                GridLines = true,
                Font = new Font("Segoe UI", 9)
            };
            lvEventLog.Columns.Add("Level", 80);
            lvEventLog.Columns.Add("Date/Time", 150);
            lvEventLog.Columns.Add("Source", 150);
            lvEventLog.Columns.Add("Event ID", 80);
            lvEventLog.Columns.Add("Message", 500);
            
            tabEventLog.Controls.Add(lvEventLog);
            tabEventLog.Controls.Add(toolbar);
        }
        
        private void InitializePerformanceCounters()
        {
            try
            {
                cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
                ramCounter = new PerformanceCounter("Memory", "Available MBytes");
            }
            catch { }
        }
        
        private void LoadInitialData()
        {
            LoadSystemInfo();
            LoadProcesses();
            LoadNetworkInterfaces();
            LoadServices();
            LoadDiskInfo();
            LoadEventLogs();
            LoadFolderTree();
        }
        
        private void LoadSystemInfo()
        {
            var info = new System.Text.StringBuilder();
            info.AppendLine($"Computer Name:    {Environment.MachineName}");
            info.AppendLine($"User Name:        {Environment.UserName}");
            info.AppendLine($"OS Version:       {Environment.OSVersion}");
            info.AppendLine($"64-bit OS:        {Environment.Is64BitOperatingSystem}");
            info.AppendLine($"Processor Count:  {Environment.ProcessorCount}");
            info.AppendLine($"CLR Version:      {Environment.Version}");
            info.AppendLine($"System Directory: {Environment.SystemDirectory}");
            
            lblSystemInfo.Text = info.ToString();
            
            // Quick stats
            lvQuickStats.Items.Clear();
            lvQuickStats.Items.Add(new ListViewItem(new[] { "Running Processes", Process.GetProcesses().Length.ToString() }));
            lvQuickStats.Items.Add(new ListViewItem(new[] { "Total Services", ServiceController.GetServices().Length.ToString() }));
            lvQuickStats.Items.Add(new ListViewItem(new[] { "Network Interfaces", NetworkInterface.GetAllNetworkInterfaces().Length.ToString() }));
            lvQuickStats.Items.Add(new ListViewItem(new[] { "Drives", DriveInfo.GetDrives().Count(d => d.IsReady).ToString() }));
        }
        
        private void LoadProcesses()
        {
            lvProcesses.Items.Clear();
            foreach (var proc in Process.GetProcesses().OrderBy(p => p.ProcessName))
            {
                try
                {
                    var item = new ListViewItem(proc.ProcessName);
                    item.SubItems.Add(proc.Id.ToString());
                    item.SubItems.Add("--");
                    item.SubItems.Add((proc.WorkingSet64 / 1024.0 / 1024.0).ToString("F1"));
                    item.SubItems.Add(proc.Threads.Count.ToString());
                    item.SubItems.Add(proc.Responding ? "Running" : "Not Responding");
                    item.SubItems.Add("--");
                    try { item.SubItems.Add(proc.StartTime.ToString("g")); } catch { item.SubItems.Add("--"); }
                    item.Tag = proc.Id;
                    lvProcesses.Items.Add(item);
                }
                catch { }
            }
            statusLabel.Text = $"Loaded {lvProcesses.Items.Count} processes";
        }
        
        private void LoadNetworkInterfaces()
        {
            lvNetworkInterfaces.Items.Clear();
            foreach (var ni in NetworkInterface.GetAllNetworkInterfaces())
            {
                var item = new ListViewItem(ni.Name);
                item.SubItems.Add(ni.OperationalStatus.ToString());
                item.SubItems.Add(ni.NetworkInterfaceType.ToString());
                item.SubItems.Add($"{ni.Speed / 1_000_000} Mbps");
                
                var ipProps = ni.GetIPProperties();
                var ipv4 = ipProps.UnicastAddresses
                    .FirstOrDefault(a => a.Address.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork);
                item.SubItems.Add(ipv4?.Address.ToString() ?? "--");
                item.SubItems.Add(ni.GetPhysicalAddress().ToString());
                
                item.ForeColor = ni.OperationalStatus == OperationalStatus.Up ? Color.Green : Color.Gray;
                lvNetworkInterfaces.Items.Add(item);
            }
        }
        
        private void LoadServices()
        {
            lvServices.Items.Clear();
            foreach (var svc in ServiceController.GetServices().OrderBy(s => s.DisplayName))
            {
                var item = new ListViewItem(svc.DisplayName);
                item.SubItems.Add(svc.ServiceName);
                item.SubItems.Add(svc.Status.ToString());
                item.SubItems.Add(svc.StartType.ToString());
                item.SubItems.Add("--");
                item.Tag = svc.ServiceName;
                
                item.ForeColor = svc.Status == ServiceControllerStatus.Running ? Color.Green :
                                 svc.Status == ServiceControllerStatus.Stopped ? Color.Red : Color.Orange;
                lvServices.Items.Add(item);
            }
        }
        
        private void LoadDiskInfo()
        {
            lvDisks.Items.Clear();
            foreach (var drive in DriveInfo.GetDrives().Where(d => d.IsReady))
            {
                var used = drive.TotalSize - drive.TotalFreeSpace;
                var usagePercent = (double)used / drive.TotalSize * 100;
                
                var item = new ListViewItem(drive.Name);
                item.SubItems.Add(drive.VolumeLabel);
                item.SubItems.Add(drive.DriveType.ToString());
                item.SubItems.Add(drive.DriveFormat);
                item.SubItems.Add(FormatBytes(drive.TotalSize));
                item.SubItems.Add(FormatBytes(drive.TotalFreeSpace));
                item.SubItems.Add(FormatBytes(used));
                item.SubItems.Add($"{usagePercent:F1}%");
                
                item.ForeColor = usagePercent > 90 ? Color.Red : usagePercent > 70 ? Color.Orange : Color.Black;
                lvDisks.Items.Add(item);
            }
        }
        
        private void LoadEventLogs()
        {
            lvEventLog.Items.Clear();
            try
            {
                var log = new EventLog(cmbLogType.SelectedItem?.ToString() ?? "Application");
                var entries = log.Entries.Cast<EventLogEntry>()
                    .Where(e => e.TimeGenerated >= dtpFromDate.Value && e.TimeGenerated <= dtpToDate.Value)
                    .OrderByDescending(e => e.TimeGenerated)
                    .Take(500);
                
                foreach (var entry in entries)
                {
                    var item = new ListViewItem(entry.EntryType.ToString());
                    item.SubItems.Add(entry.TimeGenerated.ToString("g"));
                    item.SubItems.Add(entry.Source);
                    item.SubItems.Add(entry.EventID.ToString());
                    var msg = entry.Message?.Replace("\r\n", " ").Replace("\n", " ");
                    item.SubItems.Add(msg?.Length > 200 ? msg.Substring(0, 200) + "..." : msg ?? "");
                    
                    item.ForeColor = entry.EntryType == EventLogEntryType.Error ? Color.Red :
                                     entry.EntryType == EventLogEntryType.Warning ? Color.Orange : Color.Black;
                    lvEventLog.Items.Add(item);
                }
            }
            catch { }
        }
        
        private void LoadFolderTree()
        {
            tvFolderBrowser.Nodes.Clear();
            foreach (var drive in DriveInfo.GetDrives().Where(d => d.IsReady))
            {
                var node = new TreeNode(drive.Name) { Tag = drive.Name };
                node.Nodes.Add(new TreeNode("Loading..."));
                tvFolderBrowser.Nodes.Add(node);
            }
            tvFolderBrowser.BeforeExpand += (s, e) => {
                if (e.Node.Nodes.Count == 1 && e.Node.Nodes[0].Text == "Loading...")
                {
                    e.Node.Nodes.Clear();
                    try
                    {
                        foreach (var dir in Directory.GetDirectories(e.Node.Tag.ToString()))
                        {
                            var node = new TreeNode(Path.GetFileName(dir)) { Tag = dir };
                            node.Nodes.Add(new TreeNode("Loading..."));
                            e.Node.Nodes.Add(node);
                        }
                    }
                    catch { }
                }
            };
        }
        
        private void StartMonitoring()
        {
            refreshTimer = new System.Windows.Forms.Timer { Interval = 2000 };
            refreshTimer.Tick += (s, e) => UpdateDashboard();
            refreshTimer.Start();
        }
        
        private void UpdateDashboard()
        {
            try
            {
                // CPU
                var cpu = cpuCounter?.NextValue() ?? 0;
                cpuProgressBar.Value = Math.Min(100, (int)cpu);
                lblCpuValue.Text = $"{cpu:F0}%";
                
                // Memory
                var totalMem = new Microsoft.VisualBasic.Devices.ComputerInfo().TotalPhysicalMemory / 1024.0 / 1024.0;
                var availMem = ramCounter?.NextValue() ?? 0;
                var usedMem = totalMem - availMem;
                var memPercent = usedMem / totalMem * 100;
                memoryProgressBar.Value = Math.Min(100, (int)memPercent);
                lblMemoryValue.Text = $"{memPercent:F0}%";
                
                // Disk (first drive)
                var drive = DriveInfo.GetDrives().FirstOrDefault(d => d.IsReady);
                if (drive != null)
                {
                    var diskPercent = (double)(drive.TotalSize - drive.TotalFreeSpace) / drive.TotalSize * 100;
                    diskProgressBar.Value = Math.Min(100, (int)diskPercent);
                    lblDiskValue.Text = $"{diskPercent:F0}%";
                }
                
                // Uptime
                var uptime = TimeSpan.FromMilliseconds(Environment.TickCount64);
                lvQuickStats.Items[0].SubItems[1].Text = Process.GetProcesses().Length.ToString();
            }
            catch { }
        }
        
        // Event Handlers
        private void KillProcess_Click(object sender, EventArgs e)
        {
            if (lvProcesses.SelectedItems.Count > 0)
            {
                var pid = (int)lvProcesses.SelectedItems[0].Tag;
                if (MessageBox.Show($"End process {lvProcesses.SelectedItems[0].Text}?", "Confirm", 
                    MessageBoxButtons.YesNo, MessageBoxIcon.Warning) == DialogResult.Yes)
                {
                    try
                    {
                        Process.GetProcessById(pid).Kill();
                        LoadProcesses();
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Error: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }
        
        private async void Ping_Click(object sender, EventArgs e)
        {
            rtbPingResults.Clear();
            rtbPingResults.AppendText($"Pinging {txtPingHost.Text}...\n\n");
            
            var ping = new Ping();
            for (int i = 0; i < 4; i++)
            {
                try
                {
                    var reply = await ping.SendPingAsync(txtPingHost.Text, 1000);
                    if (reply.Status == IPStatus.Success)
                        rtbPingResults.AppendText($"Reply from {reply.Address}: time={reply.RoundtripTime}ms TTL={reply.Options?.Ttl}\n");
                    else
                        rtbPingResults.AppendText($"Request timed out.\n");
                }
                catch (Exception ex)
                {
                    rtbPingResults.AppendText($"Error: {ex.Message}\n");
                }
                await Task.Delay(500);
            }
        }
        
        private void StartService_Click(object sender, EventArgs e) => ControlService("start");
        private void StopService_Click(object sender, EventArgs e) => ControlService("stop");
        private void RestartService_Click(object sender, EventArgs e) => ControlService("restart");
        
        private void ControlService(string action)
        {
            if (lvServices.SelectedItems.Count > 0)
            {
                var serviceName = lvServices.SelectedItems[0].Tag.ToString();
                try
                {
                    var svc = new ServiceController(serviceName);
                    switch (action)
                    {
                        case "start": svc.Start(); break;
                        case "stop": svc.Stop(); break;
                        case "restart": svc.Stop(); svc.WaitForStatus(ServiceControllerStatus.Stopped); svc.Start(); break;
                    }
                    svc.WaitForStatus(action == "stop" ? ServiceControllerStatus.Stopped : ServiceControllerStatus.Running, TimeSpan.FromSeconds(10));
                    LoadServices();
                    MessageBox.Show($"Service {action} successful!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error: {ex.Message}\nAdministrator privileges may be required.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
        }
        
        private void FolderBrowser_AfterSelect(object sender, TreeViewEventArgs e)
        {
            var path = e.Node.Tag?.ToString();
            if (string.IsNullOrEmpty(path)) return;
            
            lblSelectedPath.Text = path;
            lvFolderContents.Items.Clear();
            
            try
            {
                foreach (var dir in Directory.GetDirectories(path))
                {
                    var info = new DirectoryInfo(dir);
                    var item = new ListViewItem(info.Name);
                    item.SubItems.Add("Folder");
                    item.SubItems.Add("--");
                    item.SubItems.Add(info.LastWriteTime.ToString("g"));
                    lvFolderContents.Items.Add(item);
                }
                
                foreach (var file in Directory.GetFiles(path))
                {
                    var info = new FileInfo(file);
                    var item = new ListViewItem(info.Name);
                    item.SubItems.Add(info.Extension);
                    item.SubItems.Add(FormatBytes(info.Length));
                    item.SubItems.Add(info.LastWriteTime.ToString("g"));
                    lvFolderContents.Items.Add(item);
                }
            }
            catch { }
        }
        
        private void FilterLogs_Click(object sender, EventArgs e) => LoadEventLogs();
        private void FilterProcesses() { /* Implement search filtering */ }
        private void SortProcesses() { /* Implement sorting */ }
        private void FilterServices() { /* Implement service filtering */ }
        private void RefreshAll() { LoadInitialData(); }
        private void ExportReport_Click(object sender, EventArgs e) { /* Export to file */ }
        private void ShowSystemInfo_Click(object sender, EventArgs e) { /* Show detailed info */ }
        private void NetworkSpeedTest_Click(object sender, EventArgs e) { /* Speed test */ }
        private void ShowAbout_Click(object sender, EventArgs e)
        {
            MessageBox.Show("System Administration Tool v2.0\nCreated by Eyasu Solomon\n\nA comprehensive system management application.", 
                "About", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        
        private string FormatBytes(long bytes)
        {
            string[] sizes = { "B", "KB", "MB", "GB", "TB" };
            double size = bytes;
            int order = 0;
            while (size >= 1024 && order < sizes.Length - 1) { order++; size /= 1024; }
            return $"{size:F1} {sizes[order]}";
        }
        
        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }
}
