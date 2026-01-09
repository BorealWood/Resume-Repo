import javax.swing.*;
import javax.swing.border.*;
import javax.swing.table.*;
import javax.swing.tree.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.util.List;
import java.text.SimpleDateFormat;

/**
 * Database Manager Pro - A GUI Database Management System Simulator
 * Created by Eyasu Solomon
 * 
 * Features:
 * - Modern dark theme UI with gradient headers
 * - Database browser with tree structure
 * - SQL Query editor with syntax highlighting simulation
 * - Query results in table format
 * - Create/Edit/Delete tables and records
 * - Import/Export functionality
 * - Query history tracking
 * - Connection management
 */
public class DatabaseManagerGUI extends JFrame {
    
    // Color scheme
    private static final Color DARK_BG = new Color(18, 18, 24);
    private static final Color DARKER_BG = new Color(13, 13, 17);
    private static final Color CARD_BG = new Color(30, 30, 40);
    private static final Color ACCENT = new Color(99, 102, 241);
    private static final Color ACCENT_DARK = new Color(79, 70, 229);
    private static final Color SUCCESS = new Color(34, 197, 94);
    private static final Color WARNING = new Color(245, 158, 11);
    private static final Color DANGER = new Color(239, 68, 68);
    private static final Color TEXT_PRIMARY = new Color(241, 245, 249);
    private static final Color TEXT_SECONDARY = new Color(148, 163, 184);
    private static final Color BORDER_COLOR = new Color(55, 55, 70);
    
    // Components
    private JTree databaseTree;
    private JTextArea queryEditor;
    private JTable resultsTable;
    private JTextArea consoleOutput;
    private JList<String> historyList;
    private DefaultListModel<String> historyModel;
    private DefaultMutableTreeNode rootNode;
    private DefaultTreeModel treeModel;
    private JLabel statusLabel;
    private JLabel connectionStatus;
    private JProgressBar progressBar;
    
    // Data storage (simulated database)
    private Map<String, Map<String, List<Map<String, Object>>>> databases;
    private String currentDatabase = "sample_db";
    
    public DatabaseManagerGUI() {
        initializeData();
        initializeUI();
    }
    
    private void initializeData() {
        databases = new HashMap<>();
        
        // Create sample database
        Map<String, List<Map<String, Object>>> sampleDb = new HashMap<>();
        
        // Users table
        List<Map<String, Object>> users = new ArrayList<>();
        users.add(createRow(1, "John Doe", "john@email.com", "Admin", "2024-01-15"));
        users.add(createRow(2, "Jane Smith", "jane@email.com", "User", "2024-01-20"));
        users.add(createRow(3, "Bob Wilson", "bob@email.com", "User", "2024-02-01"));
        users.add(createRow(4, "Alice Brown", "alice@email.com", "Manager", "2024-02-10"));
        users.add(createRow(5, "Charlie Davis", "charlie@email.com", "User", "2024-02-15"));
        sampleDb.put("users", users);
        
        // Products table
        List<Map<String, Object>> products = new ArrayList<>();
        products.add(createProductRow(1, "Laptop Pro", "Electronics", 1299.99, 50));
        products.add(createProductRow(2, "Wireless Mouse", "Accessories", 49.99, 200));
        products.add(createProductRow(3, "USB-C Hub", "Accessories", 79.99, 150));
        products.add(createProductRow(4, "Monitor 4K", "Electronics", 599.99, 30));
        products.add(createProductRow(5, "Keyboard RGB", "Accessories", 129.99, 100));
        sampleDb.put("products", products);
        
        // Orders table
        List<Map<String, Object>> orders = new ArrayList<>();
        orders.add(createOrderRow(1001, 1, 1, 1, 1299.99, "Completed"));
        orders.add(createOrderRow(1002, 2, 2, 3, 149.97, "Shipped"));
        orders.add(createOrderRow(1003, 3, 4, 1, 599.99, "Processing"));
        orders.add(createOrderRow(1004, 1, 3, 2, 159.98, "Completed"));
        sampleDb.put("orders", orders);
        
        databases.put("sample_db", sampleDb);
        
        // Create another database
        Map<String, List<Map<String, Object>>> testDb = new HashMap<>();
        testDb.put("test_table", new ArrayList<>());
        databases.put("test_db", testDb);
    }
    
    private Map<String, Object> createRow(int id, String name, String email, String role, String created) {
        Map<String, Object> row = new LinkedHashMap<>();
        row.put("id", id);
        row.put("name", name);
        row.put("email", email);
        row.put("role", role);
        row.put("created_at", created);
        return row;
    }
    
    private Map<String, Object> createProductRow(int id, String name, String category, double price, int stock) {
        Map<String, Object> row = new LinkedHashMap<>();
        row.put("id", id);
        row.put("name", name);
        row.put("category", category);
        row.put("price", price);
        row.put("stock", stock);
        return row;
    }
    
    private Map<String, Object> createOrderRow(int orderId, int userId, int productId, int qty, double total, String status) {
        Map<String, Object> row = new LinkedHashMap<>();
        row.put("order_id", orderId);
        row.put("user_id", userId);
        row.put("product_id", productId);
        row.put("quantity", qty);
        row.put("total", total);
        row.put("status", status);
        return row;
    }
    
    private void initializeUI() {
        setTitle("Database Manager Pro | Eyasu Solomon");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1400, 900);
        setLocationRelativeTo(null);
        
        // Set dark look
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        // Main panel
        JPanel mainPanel = new JPanel(new BorderLayout());
        mainPanel.setBackground(DARK_BG);
        
        // Add components
        mainPanel.add(createToolBar(), BorderLayout.NORTH);
        mainPanel.add(createMainContent(), BorderLayout.CENTER);
        mainPanel.add(createStatusBar(), BorderLayout.SOUTH);
        
        setContentPane(mainPanel);
        
        // Menu bar
        setJMenuBar(createMenuBar());
    }
    
    private JMenuBar createMenuBar() {
        JMenuBar menuBar = new JMenuBar();
        menuBar.setBackground(DARKER_BG);
        menuBar.setBorder(BorderFactory.createMatteBorder(0, 0, 1, 0, BORDER_COLOR));
        
        // File menu
        JMenu fileMenu = createMenu("File");
        fileMenu.add(createMenuItem("New Connection", "ctrl N", e -> showNewConnectionDialog()));
        fileMenu.add(createMenuItem("Open Database", "ctrl O", e -> openDatabase()));
        fileMenu.addSeparator();
        fileMenu.add(createMenuItem("Import SQL", "ctrl I", e -> importSQL()));
        fileMenu.add(createMenuItem("Export Database", "ctrl E", e -> exportDatabase()));
        fileMenu.addSeparator();
        fileMenu.add(createMenuItem("Exit", "alt F4", e -> System.exit(0)));
        menuBar.add(fileMenu);
        
        // Edit menu
        JMenu editMenu = createMenu("Edit");
        editMenu.add(createMenuItem("Undo", "ctrl Z", e -> {}));
        editMenu.add(createMenuItem("Redo", "ctrl Y", e -> {}));
        editMenu.addSeparator();
        editMenu.add(createMenuItem("Cut", "ctrl X", e -> queryEditor.cut()));
        editMenu.add(createMenuItem("Copy", "ctrl C", e -> queryEditor.copy()));
        editMenu.add(createMenuItem("Paste", "ctrl V", e -> queryEditor.paste()));
        menuBar.add(editMenu);
        
        // Query menu
        JMenu queryMenu = createMenu("Query");
        queryMenu.add(createMenuItem("Execute Query", "F5", e -> executeQuery()));
        queryMenu.add(createMenuItem("Format Query", "ctrl shift F", e -> formatQuery()));
        queryMenu.addSeparator();
        queryMenu.add(createMenuItem("Clear Editor", null, e -> queryEditor.setText("")));
        queryMenu.add(createMenuItem("Clear Results", null, e -> clearResults()));
        menuBar.add(queryMenu);
        
        // Database menu
        JMenu dbMenu = createMenu("Database");
        dbMenu.add(createMenuItem("Create Database", null, e -> createNewDatabase()));
        dbMenu.add(createMenuItem("Create Table", null, e -> showCreateTableDialog()));
        dbMenu.addSeparator();
        dbMenu.add(createMenuItem("Refresh", "F5", e -> refreshTree()));
        menuBar.add(dbMenu);
        
        // Help menu
        JMenu helpMenu = createMenu("Help");
        helpMenu.add(createMenuItem("Documentation", "F1", e -> showDocumentation()));
        helpMenu.add(createMenuItem("About", null, e -> showAbout()));
        menuBar.add(helpMenu);
        
        return menuBar;
    }
    
    private JMenu createMenu(String title) {
        JMenu menu = new JMenu(title);
        menu.setForeground(TEXT_PRIMARY);
        return menu;
    }
    
    private JMenuItem createMenuItem(String text, String shortcut, ActionListener action) {
        JMenuItem item = new JMenuItem(text);
        item.addActionListener(action);
        if (shortcut != null) {
            item.setAccelerator(KeyStroke.getKeyStroke(shortcut));
        }
        return item;
    }
    
    private JPanel createToolBar() {
        JPanel toolBar = new JPanel(new BorderLayout());
        toolBar.setBackground(DARKER_BG);
        toolBar.setBorder(BorderFactory.createMatteBorder(0, 0, 1, 0, BORDER_COLOR));
        toolBar.setPreferredSize(new Dimension(0, 50));
        
        // Left buttons
        JPanel leftPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 5, 8));
        leftPanel.setOpaque(false);
        
        leftPanel.add(createToolButton("New", "➕", e -> showNewConnectionDialog()));
        leftPanel.add(createToolButton("Open", "📂", e -> openDatabase()));
        leftPanel.add(createToolButton("Save", "💾", e -> saveQuery()));
        leftPanel.add(Box.createHorizontalStrut(10));
        leftPanel.add(createToolButton("Run", "▶", e -> executeQuery()));
        leftPanel.add(createToolButton("Stop", "⏹", e -> stopQuery()));
        leftPanel.add(Box.createHorizontalStrut(10));
        leftPanel.add(createToolButton("Format", "📝", e -> formatQuery()));
        leftPanel.add(createToolButton("Clear", "🗑", e -> clearAll()));
        
        toolBar.add(leftPanel, BorderLayout.WEST);
        
        // Right panel - connection status
        JPanel rightPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 8));
        rightPanel.setOpaque(false);
        
        connectionStatus = new JLabel("● Connected to: sample_db");
        connectionStatus.setForeground(SUCCESS);
        connectionStatus.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        rightPanel.add(connectionStatus);
        
        toolBar.add(rightPanel, BorderLayout.EAST);
        
        return toolBar;
    }
    
    private JButton createToolButton(String tooltip, String icon, ActionListener action) {
        JButton button = new JButton(icon);
        button.setToolTipText(tooltip);
        button.setFont(new Font("Segoe UI Emoji", Font.PLAIN, 14));
        button.setForeground(TEXT_PRIMARY);
        button.setBackground(CARD_BG);
        button.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(BORDER_COLOR),
            BorderFactory.createEmptyBorder(5, 12, 5, 12)
        ));
        button.setFocusPainted(false);
        button.addActionListener(action);
        button.addMouseListener(new MouseAdapter() {
            public void mouseEntered(MouseEvent e) {
                button.setBackground(ACCENT);
            }
            public void mouseExited(MouseEvent e) {
                button.setBackground(CARD_BG);
            }
        });
        return button;
    }
    
    private JPanel createMainContent() {
        JPanel mainContent = new JPanel(new BorderLayout());
        mainContent.setBackground(DARK_BG);
        
        // Create split pane for left sidebar and main area
        JSplitPane mainSplit = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        mainSplit.setDividerLocation(250);
        mainSplit.setBorder(null);
        mainSplit.setDividerSize(3);
        
        // Left sidebar - Database explorer
        mainSplit.setLeftComponent(createDatabaseExplorer());
        
        // Right side - Editor and results
        JSplitPane rightSplit = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
        rightSplit.setDividerLocation(350);
        rightSplit.setBorder(null);
        rightSplit.setDividerSize(3);
        
        rightSplit.setTopComponent(createQueryEditor());
        rightSplit.setBottomComponent(createResultsPanel());
        
        mainSplit.setRightComponent(rightSplit);
        mainContent.add(mainSplit, BorderLayout.CENTER);
        
        return mainContent;
    }
    
    private JPanel createDatabaseExplorer() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(DARKER_BG);
        panel.setBorder(BorderFactory.createMatteBorder(0, 0, 0, 1, BORDER_COLOR));
        
        // Header
        JLabel header = new JLabel("  📁 Database Explorer");
        header.setFont(new Font("Segoe UI", Font.BOLD, 13));
        header.setForeground(TEXT_PRIMARY);
        header.setBackground(CARD_BG);
        header.setOpaque(true);
        header.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createMatteBorder(0, 0, 1, 0, BORDER_COLOR),
            BorderFactory.createEmptyBorder(10, 5, 10, 5)
        ));
        panel.add(header, BorderLayout.NORTH);
        
        // Tree
        rootNode = new DefaultMutableTreeNode("Databases");
        treeModel = new DefaultTreeModel(rootNode);
        databaseTree = new JTree(treeModel);
        databaseTree.setBackground(DARKER_BG);
        databaseTree.setForeground(TEXT_PRIMARY);
        databaseTree.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        databaseTree.setRowHeight(24);
        
        // Custom renderer
        databaseTree.setCellRenderer(new DefaultTreeCellRenderer() {
            @Override
            public Component getTreeCellRendererComponent(JTree tree, Object value, boolean sel,
                    boolean expanded, boolean leaf, int row, boolean hasFocus) {
                super.getTreeCellRendererComponent(tree, value, sel, expanded, leaf, row, hasFocus);
                setBackground(sel ? ACCENT : DARKER_BG);
                setForeground(TEXT_PRIMARY);
                setOpaque(sel);
                
                String text = value.toString();
                if (text.equals("Databases")) {
                    setIcon(null);
                    setText("🗄️ " + text);
                } else if (text.endsWith("_db")) {
                    setText("📁 " + text);
                } else {
                    setText("📋 " + text);
                }
                return this;
            }
        });
        
        databaseTree.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 2) {
                    TreePath path = databaseTree.getPathForLocation(e.getX(), e.getY());
                    if (path != null && path.getPathCount() == 3) {
                        String table = path.getLastPathComponent().toString();
                        String db = path.getPathComponent(1).toString();
                        queryEditor.setText("SELECT * FROM " + table + ";");
                        currentDatabase = db;
                        executeQuery();
                    }
                }
            }
        });
        
        populateTree();
        
        JScrollPane scrollPane = new JScrollPane(databaseTree);
        scrollPane.setBorder(null);
        scrollPane.getViewport().setBackground(DARKER_BG);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        // History panel
        JPanel historyPanel = new JPanel(new BorderLayout());
        historyPanel.setBackground(DARKER_BG);
        historyPanel.setBorder(BorderFactory.createMatteBorder(1, 0, 0, 0, BORDER_COLOR));
        historyPanel.setPreferredSize(new Dimension(0, 150));
        
        JLabel historyLabel = new JLabel("  📜 Query History");
        historyLabel.setFont(new Font("Segoe UI", Font.BOLD, 12));
        historyLabel.setForeground(TEXT_SECONDARY);
        historyLabel.setBorder(BorderFactory.createEmptyBorder(8, 0, 8, 0));
        historyPanel.add(historyLabel, BorderLayout.NORTH);
        
        historyModel = new DefaultListModel<>();
        historyModel.addElement("SELECT * FROM users");
        historyModel.addElement("SELECT * FROM products");
        
        historyList = new JList<>(historyModel);
        historyList.setBackground(DARKER_BG);
        historyList.setForeground(TEXT_SECONDARY);
        historyList.setFont(new Font("Consolas", Font.PLAIN, 11));
        historyList.setSelectionBackground(ACCENT);
        historyList.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (e.getClickCount() == 2) {
                    String query = historyList.getSelectedValue();
                    if (query != null) {
                        queryEditor.setText(query);
                    }
                }
            }
        });
        
        JScrollPane historyScroll = new JScrollPane(historyList);
        historyScroll.setBorder(null);
        historyPanel.add(historyScroll, BorderLayout.CENTER);
        
        panel.add(historyPanel, BorderLayout.SOUTH);
        
        return panel;
    }
    
    private void populateTree() {
        rootNode.removeAllChildren();
        
        for (String dbName : databases.keySet()) {
            DefaultMutableTreeNode dbNode = new DefaultMutableTreeNode(dbName);
            Map<String, List<Map<String, Object>>> tables = databases.get(dbName);
            
            for (String tableName : tables.keySet()) {
                dbNode.add(new DefaultMutableTreeNode(tableName));
            }
            rootNode.add(dbNode);
        }
        
        treeModel.reload();
        
        // Expand all
        for (int i = 0; i < databaseTree.getRowCount(); i++) {
            databaseTree.expandRow(i);
        }
    }
    
    private JPanel createQueryEditor() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(CARD_BG);
        
        // Header with tabs
        JPanel header = new JPanel(new BorderLayout());
        header.setBackground(CARD_BG);
        header.setBorder(BorderFactory.createMatteBorder(0, 0, 1, 0, BORDER_COLOR));
        
        JPanel tabs = new JPanel(new FlowLayout(FlowLayout.LEFT, 0, 0));
        tabs.setOpaque(false);
        
        JButton queryTab = createTabButton("Query Editor", true);
        tabs.add(queryTab);
        tabs.add(createTabButton("New Query +", false));
        
        header.add(tabs, BorderLayout.WEST);
        panel.add(header, BorderLayout.NORTH);
        
        // Query editor
        queryEditor = new JTextArea();
        queryEditor.setBackground(new Color(22, 22, 30));
        queryEditor.setForeground(TEXT_PRIMARY);
        queryEditor.setCaretColor(TEXT_PRIMARY);
        queryEditor.setFont(new Font("Consolas", Font.PLAIN, 14));
        queryEditor.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
        queryEditor.setLineWrap(true);
        queryEditor.setText("-- Write your SQL query here\nSELECT * FROM users WHERE role = 'Admin';");
        
        // Line numbers
        JTextArea lineNumbers = new JTextArea("1\n2\n3\n");
        lineNumbers.setBackground(new Color(18, 18, 24));
        lineNumbers.setForeground(TEXT_SECONDARY);
        lineNumbers.setFont(new Font("Consolas", Font.PLAIN, 14));
        lineNumbers.setBorder(BorderFactory.createEmptyBorder(15, 10, 15, 10));
        lineNumbers.setEditable(false);
        
        queryEditor.addKeyListener(new KeyAdapter() {
            @Override
            public void keyReleased(KeyEvent e) {
                updateLineNumbers(lineNumbers);
            }
        });
        
        JPanel editorPanel = new JPanel(new BorderLayout());
        editorPanel.add(lineNumbers, BorderLayout.WEST);
        editorPanel.add(queryEditor, BorderLayout.CENTER);
        
        JScrollPane scrollPane = new JScrollPane(editorPanel);
        scrollPane.setBorder(null);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JButton createTabButton(String text, boolean active) {
        JButton button = new JButton(text);
        button.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        button.setForeground(active ? TEXT_PRIMARY : TEXT_SECONDARY);
        button.setBackground(active ? CARD_BG : DARKER_BG);
        button.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createMatteBorder(0, 0, active ? 2 : 0, 0, ACCENT),
            BorderFactory.createEmptyBorder(10, 20, 10, 20)
        ));
        button.setFocusPainted(false);
        return button;
    }
    
    private void updateLineNumbers(JTextArea lineNumbers) {
        String[] lines = queryEditor.getText().split("\n");
        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= Math.max(lines.length, 10); i++) {
            sb.append(i).append("\n");
        }
        lineNumbers.setText(sb.toString());
    }
    
    private JPanel createResultsPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(CARD_BG);
        
        // Tabbed pane for results
        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.setBackground(CARD_BG);
        tabbedPane.setForeground(TEXT_PRIMARY);
        
        // Results tab
        resultsTable = new JTable();
        resultsTable.setBackground(CARD_BG);
        resultsTable.setForeground(TEXT_PRIMARY);
        resultsTable.setGridColor(BORDER_COLOR);
        resultsTable.setSelectionBackground(ACCENT);
        resultsTable.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        resultsTable.setRowHeight(28);
        resultsTable.getTableHeader().setBackground(DARKER_BG);
        resultsTable.getTableHeader().setForeground(TEXT_PRIMARY);
        resultsTable.getTableHeader().setFont(new Font("Segoe UI", Font.BOLD, 12));
        
        JScrollPane tableScroll = new JScrollPane(resultsTable);
        tableScroll.setBorder(null);
        tableScroll.getViewport().setBackground(CARD_BG);
        
        tabbedPane.addTab("📊 Results", tableScroll);
        
        // Console tab
        consoleOutput = new JTextArea();
        consoleOutput.setBackground(new Color(13, 13, 17));
        consoleOutput.setForeground(TEXT_SECONDARY);
        consoleOutput.setFont(new Font("Consolas", Font.PLAIN, 12));
        consoleOutput.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        consoleOutput.setEditable(false);
        consoleOutput.setText("[" + getTimestamp() + "] Database Manager Pro started\n");
        consoleOutput.append("[" + getTimestamp() + "] Connected to sample_db\n");
        
        JScrollPane consoleScroll = new JScrollPane(consoleOutput);
        consoleScroll.setBorder(null);
        
        tabbedPane.addTab("📝 Console", consoleScroll);
        
        panel.add(tabbedPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JPanel createStatusBar() {
        JPanel statusBar = new JPanel(new BorderLayout());
        statusBar.setBackground(DARKER_BG);
        statusBar.setBorder(BorderFactory.createMatteBorder(1, 0, 0, 0, BORDER_COLOR));
        statusBar.setPreferredSize(new Dimension(0, 28));
        
        JPanel leftPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 4));
        leftPanel.setOpaque(false);
        
        statusLabel = new JLabel("Ready");
        statusLabel.setForeground(TEXT_SECONDARY);
        statusLabel.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        leftPanel.add(statusLabel);
        
        statusBar.add(leftPanel, BorderLayout.WEST);
        
        JPanel rightPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 4));
        rightPanel.setOpaque(false);
        
        progressBar = new JProgressBar();
        progressBar.setPreferredSize(new Dimension(100, 12));
        progressBar.setVisible(false);
        rightPanel.add(progressBar);
        
        JLabel dbInfo = new JLabel("Database: sample_db | Tables: 3 | Rows: 13");
        dbInfo.setForeground(TEXT_SECONDARY);
        dbInfo.setFont(new Font("Segoe UI", Font.PLAIN, 11));
        rightPanel.add(dbInfo);
        
        statusBar.add(rightPanel, BorderLayout.EAST);
        
        return statusBar;
    }
    
    // Action methods
    private void executeQuery() {
        String query = queryEditor.getText().trim();
        if (query.isEmpty()) {
            showMessage("Please enter a query", "Warning", JOptionPane.WARNING_MESSAGE);
            return;
        }
        
        statusLabel.setText("Executing query...");
        consoleOutput.append("[" + getTimestamp() + "] Executing: " + query + "\n");
        
        // Add to history
        if (!historyModel.contains(query)) {
            historyModel.add(0, query);
            if (historyModel.size() > 10) {
                historyModel.remove(historyModel.size() - 1);
            }
        }
        
        // Parse and execute
        String upperQuery = query.toUpperCase();
        
        try {
            if (upperQuery.startsWith("SELECT")) {
                executeSelect(query);
            } else if (upperQuery.startsWith("INSERT")) {
                executeInsert(query);
            } else if (upperQuery.startsWith("UPDATE")) {
                executeUpdate(query);
            } else if (upperQuery.startsWith("DELETE")) {
                executeDelete(query);
            } else if (upperQuery.startsWith("CREATE TABLE")) {
                executeCreateTable(query);
            } else {
                consoleOutput.append("[" + getTimestamp() + "] Unknown query type\n");
            }
            
            statusLabel.setText("Query executed successfully");
            consoleOutput.append("[" + getTimestamp() + "] Query completed\n");
        } catch (Exception e) {
            statusLabel.setText("Query failed: " + e.getMessage());
            consoleOutput.append("[" + getTimestamp() + "] Error: " + e.getMessage() + "\n");
        }
    }
    
    private void executeSelect(String query) {
        // Parse table name
        String tableName = extractTableName(query, "FROM");
        if (tableName == null) {
            throw new RuntimeException("Invalid SELECT query");
        }
        
        Map<String, List<Map<String, Object>>> db = databases.get(currentDatabase);
        if (db == null || !db.containsKey(tableName)) {
            throw new RuntimeException("Table not found: " + tableName);
        }
        
        List<Map<String, Object>> data = db.get(tableName);
        if (data.isEmpty()) {
            showMessage("No data found", "Info", JOptionPane.INFORMATION_MESSAGE);
            return;
        }
        
        // Apply WHERE clause if exists
        String whereClause = extractWhereClause(query);
        List<Map<String, Object>> filteredData = data;
        
        if (whereClause != null) {
            filteredData = applyWhereFilter(data, whereClause);
        }
        
        // Populate table
        String[] columns = data.get(0).keySet().toArray(new String[0]);
        Object[][] rowData = new Object[filteredData.size()][columns.length];
        
        for (int i = 0; i < filteredData.size(); i++) {
            Map<String, Object> row = filteredData.get(i);
            for (int j = 0; j < columns.length; j++) {
                rowData[i][j] = row.get(columns[j]);
            }
        }
        
        resultsTable.setModel(new DefaultTableModel(rowData, columns));
        consoleOutput.append("[" + getTimestamp() + "] " + filteredData.size() + " rows returned\n");
    }
    
    private List<Map<String, Object>> applyWhereFilter(List<Map<String, Object>> data, String whereClause) {
        List<Map<String, Object>> filtered = new ArrayList<>();
        
        // Simple parsing for column = 'value'
        String[] parts = whereClause.split("=");
        if (parts.length == 2) {
            String column = parts[0].trim();
            String value = parts[1].trim().replace("'", "").replace(";", "");
            
            for (Map<String, Object> row : data) {
                Object cellValue = row.get(column);
                if (cellValue != null && cellValue.toString().equalsIgnoreCase(value)) {
                    filtered.add(row);
                }
            }
        }
        
        return filtered.isEmpty() ? data : filtered;
    }
    
    private void executeInsert(String query) {
        consoleOutput.append("[" + getTimestamp() + "] INSERT executed (simulated)\n");
        consoleOutput.append("[" + getTimestamp() + "] 1 row affected\n");
        showMessage("1 row inserted successfully", "Success", JOptionPane.INFORMATION_MESSAGE);
    }
    
    private void executeUpdate(String query) {
        consoleOutput.append("[" + getTimestamp() + "] UPDATE executed (simulated)\n");
        consoleOutput.append("[" + getTimestamp() + "] Rows affected\n");
        showMessage("Rows updated successfully", "Success", JOptionPane.INFORMATION_MESSAGE);
    }
    
    private void executeDelete(String query) {
        consoleOutput.append("[" + getTimestamp() + "] DELETE executed (simulated)\n");
        showMessage("Rows deleted successfully", "Success", JOptionPane.INFORMATION_MESSAGE);
    }
    
    private void executeCreateTable(String query) {
        String tableName = extractTableName(query, "TABLE");
        if (tableName != null) {
            Map<String, List<Map<String, Object>>> db = databases.get(currentDatabase);
            db.put(tableName, new ArrayList<>());
            populateTree();
            consoleOutput.append("[" + getTimestamp() + "] Table '" + tableName + "' created\n");
            showMessage("Table created successfully", "Success", JOptionPane.INFORMATION_MESSAGE);
        }
    }
    
    private String extractTableName(String query, String keyword) {
        String upper = query.toUpperCase();
        int idx = upper.indexOf(keyword);
        if (idx == -1) return null;
        
        String rest = query.substring(idx + keyword.length()).trim();
        String[] parts = rest.split("\\s+|;|\\(");
        return parts.length > 0 ? parts[0].trim() : null;
    }
    
    private String extractWhereClause(String query) {
        String upper = query.toUpperCase();
        int idx = upper.indexOf("WHERE");
        if (idx == -1) return null;
        return query.substring(idx + 5).replace(";", "").trim();
    }
    
    private void formatQuery() {
        String query = queryEditor.getText();
        // Simple formatting
        query = query.replaceAll("(?i)\\bSELECT\\b", "SELECT")
                     .replaceAll("(?i)\\bFROM\\b", "\nFROM")
                     .replaceAll("(?i)\\bWHERE\\b", "\nWHERE")
                     .replaceAll("(?i)\\bAND\\b", "\n  AND")
                     .replaceAll("(?i)\\bOR\\b", "\n  OR")
                     .replaceAll("(?i)\\bORDER BY\\b", "\nORDER BY")
                     .replaceAll("(?i)\\bGROUP BY\\b", "\nGROUP BY")
                     .replaceAll("(?i)\\bLIMIT\\b", "\nLIMIT");
        queryEditor.setText(query);
        consoleOutput.append("[" + getTimestamp() + "] Query formatted\n");
    }
    
    private void clearResults() {
        resultsTable.setModel(new DefaultTableModel());
    }
    
    private void clearAll() {
        queryEditor.setText("");
        clearResults();
        consoleOutput.setText("");
    }
    
    private void stopQuery() {
        statusLabel.setText("Query stopped");
        consoleOutput.append("[" + getTimestamp() + "] Query execution stopped\n");
    }
    
    private void refreshTree() {
        populateTree();
        consoleOutput.append("[" + getTimestamp() + "] Database explorer refreshed\n");
    }
    
    private void showNewConnectionDialog() {
        JPanel panel = new JPanel(new GridLayout(5, 2, 10, 10));
        
        panel.add(new JLabel("Host:"));
        JTextField hostField = new JTextField("localhost");
        panel.add(hostField);
        
        panel.add(new JLabel("Port:"));
        JTextField portField = new JTextField("3306");
        panel.add(portField);
        
        panel.add(new JLabel("Database:"));
        JTextField dbField = new JTextField("sample_db");
        panel.add(dbField);
        
        panel.add(new JLabel("Username:"));
        JTextField userField = new JTextField("root");
        panel.add(userField);
        
        panel.add(new JLabel("Password:"));
        JPasswordField passField = new JPasswordField();
        panel.add(passField);
        
        int result = JOptionPane.showConfirmDialog(this, panel, "New Connection", JOptionPane.OK_CANCEL_OPTION);
        if (result == JOptionPane.OK_OPTION) {
            connectionStatus.setText("● Connected to: " + dbField.getText());
            currentDatabase = dbField.getText();
            consoleOutput.append("[" + getTimestamp() + "] Connected to " + dbField.getText() + "\n");
        }
    }
    
    private void openDatabase() {
        JFileChooser chooser = new JFileChooser();
        if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            consoleOutput.append("[" + getTimestamp() + "] Opened: " + chooser.getSelectedFile().getName() + "\n");
        }
    }
    
    private void saveQuery() {
        JFileChooser chooser = new JFileChooser();
        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            consoleOutput.append("[" + getTimestamp() + "] Query saved to: " + chooser.getSelectedFile().getName() + "\n");
        }
    }
    
    private void importSQL() {
        JFileChooser chooser = new JFileChooser();
        if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
            consoleOutput.append("[" + getTimestamp() + "] SQL imported from: " + chooser.getSelectedFile().getName() + "\n");
        }
    }
    
    private void exportDatabase() {
        JFileChooser chooser = new JFileChooser();
        if (chooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
            consoleOutput.append("[" + getTimestamp() + "] Database exported to: " + chooser.getSelectedFile().getName() + "\n");
            showMessage("Database exported successfully!", "Export Complete", JOptionPane.INFORMATION_MESSAGE);
        }
    }
    
    private void createNewDatabase() {
        String name = JOptionPane.showInputDialog(this, "Enter database name:");
        if (name != null && !name.isEmpty()) {
            databases.put(name, new HashMap<>());
            populateTree();
            consoleOutput.append("[" + getTimestamp() + "] Database '" + name + "' created\n");
        }
    }
    
    private void showCreateTableDialog() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        
        JTextField nameField = new JTextField(20);
        JTextArea columnsArea = new JTextArea(5, 30);
        columnsArea.setText("id INT PRIMARY KEY,\nname VARCHAR(100),\nemail VARCHAR(255)");
        
        JPanel topPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        topPanel.add(new JLabel("Table Name:"));
        topPanel.add(nameField);
        
        panel.add(topPanel, BorderLayout.NORTH);
        panel.add(new JLabel("Columns:"), BorderLayout.CENTER);
        panel.add(new JScrollPane(columnsArea), BorderLayout.SOUTH);
        
        int result = JOptionPane.showConfirmDialog(this, panel, "Create Table", JOptionPane.OK_CANCEL_OPTION);
        if (result == JOptionPane.OK_OPTION) {
            String tableName = nameField.getText();
            if (!tableName.isEmpty()) {
                Map<String, List<Map<String, Object>>> db = databases.get(currentDatabase);
                db.put(tableName, new ArrayList<>());
                populateTree();
                consoleOutput.append("[" + getTimestamp() + "] Table '" + tableName + "' created\n");
            }
        }
    }
    
    private void showDocumentation() {
        JTextArea doc = new JTextArea();
        doc.setText("Database Manager Pro - Documentation\n\n" +
                   "SQL Commands Supported:\n" +
                   "- SELECT * FROM table_name WHERE condition;\n" +
                   "- INSERT INTO table_name VALUES (...);\n" +
                   "- UPDATE table_name SET column = value;\n" +
                   "- DELETE FROM table_name WHERE condition;\n" +
                   "- CREATE TABLE table_name (columns);\n\n" +
                   "Shortcuts:\n" +
                   "- F5: Execute Query\n" +
                   "- Ctrl+N: New Connection\n" +
                   "- Ctrl+S: Save Query\n" +
                   "- Ctrl+Shift+F: Format Query\n\n" +
                   "Tips:\n" +
                   "- Double-click a table to view all rows\n" +
                   "- Double-click history to restore query\n");
        doc.setEditable(false);
        doc.setFont(new Font("Segoe UI", Font.PLAIN, 12));
        
        JScrollPane scroll = new JScrollPane(doc);
        scroll.setPreferredSize(new Dimension(400, 300));
        
        JOptionPane.showMessageDialog(this, scroll, "Documentation", JOptionPane.INFORMATION_MESSAGE);
    }
    
    private void showAbout() {
        String about = "Database Manager Pro v1.0\n\n" +
                      "Created by Eyasu Solomon\n\n" +
                      "A powerful GUI-based database management\n" +
                      "system simulator built with Java Swing.\n\n" +
                      "Features:\n" +
                      "• Database browser with tree view\n" +
                      "• SQL query editor with formatting\n" +
                      "• Results display in table format\n" +
                      "• Query history tracking\n" +
                      "• Import/Export functionality\n" +
                      "• Dark modern theme";
        
        JOptionPane.showMessageDialog(this, about, "About Database Manager Pro", JOptionPane.INFORMATION_MESSAGE);
    }
    
    private void showMessage(String message, String title, int type) {
        JOptionPane.showMessageDialog(this, message, title, type);
    }
    
    private String getTimestamp() {
        return new SimpleDateFormat("HH:mm:ss").format(new Date());
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            DatabaseManagerGUI app = new DatabaseManagerGUI();
            app.setVisible(true);
        });
    }
}
