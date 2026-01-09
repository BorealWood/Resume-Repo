import java.util.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Database Management System Simulator
 * Author: Eyasu Solomon
 * 
 * A Java application demonstrating Object-Oriented Programming concepts
 * including inheritance, polymorphism, interfaces, and encapsulation.
 */
public class DatabaseManager {
    
    public static void main(String[] args) {
        DatabaseManager app = new DatabaseManager();
        app.run();
    }
    
    private Database database;
    private Scanner scanner;
    
    public DatabaseManager() {
        this.database = new Database("MainDB");
        this.scanner = new Scanner(System.in);
    }
    
    public void run() {
        System.out.println("\n" + Colors.CYAN + "═".repeat(60) + Colors.RESET);
        System.out.println(Colors.YELLOW + Colors.BOLD + 
            "      DATABASE MANAGEMENT SYSTEM SIMULATOR" + Colors.RESET);
        System.out.println(Colors.CYAN + "           Created by Eyasu Solomon" + Colors.RESET);
        System.out.println(Colors.CYAN + "═".repeat(60) + Colors.RESET);
        
        boolean running = true;
        while (running) {
            printMenu();
            String choice = scanner.nextLine().trim();
            
            switch (choice) {
                case "1": createTable(); break;
                case "2": insertRecord(); break;
                case "3": selectRecords(); break;
                case "4": updateRecord(); break;
                case "5": deleteRecord(); break;
                case "6": showTables(); break;
                case "7": describeTable(); break;
                case "8": executeSQL(); break;
                case "9": 
                    System.out.println("\n" + Colors.GREEN + "Thank you for using Database Manager!" + Colors.RESET);
                    running = false; 
                    break;
                default:
                    System.out.println(Colors.RED + "Invalid option. Please try again." + Colors.RESET);
            }
        }
    }
    
    private void printMenu() {
        System.out.println("\n" + Colors.YELLOW + "╔══════════════════════════════════════╗" + Colors.RESET);
        System.out.println(Colors.YELLOW + "║          MAIN MENU                   ║" + Colors.RESET);
        System.out.println(Colors.YELLOW + "╠══════════════════════════════════════╣" + Colors.RESET);
        System.out.println(Colors.CYAN + "║  1. Create Table                     ║" + Colors.RESET);
        System.out.println(Colors.CYAN + "║  2. Insert Record                    ║" + Colors.RESET);
        System.out.println(Colors.CYAN + "║  3. Select Records (Query)           ║" + Colors.RESET);
        System.out.println(Colors.CYAN + "║  4. Update Record                    ║" + Colors.RESET);
        System.out.println(Colors.CYAN + "║  5. Delete Record                    ║" + Colors.RESET);
        System.out.println(Colors.CYAN + "║  6. Show All Tables                  ║" + Colors.RESET);
        System.out.println(Colors.CYAN + "║  7. Describe Table                   ║" + Colors.RESET);
        System.out.println(Colors.CYAN + "║  8. Execute SQL Query                ║" + Colors.RESET);
        System.out.println(Colors.CYAN + "║  9. Exit                             ║" + Colors.RESET);
        System.out.println(Colors.YELLOW + "╚══════════════════════════════════════╝" + Colors.RESET);
        System.out.print("\nSelect an option: ");
    }
    
    private void createTable() {
        System.out.println("\n" + Colors.GREEN + "=== CREATE TABLE ===" + Colors.RESET);
        System.out.print("Enter table name: ");
        String tableName = scanner.nextLine().trim();
        
        List<Column> columns = new ArrayList<>();
        System.out.println("Enter columns (format: name:type, type can be: STRING, INTEGER, DOUBLE, BOOLEAN, DATE)");
        System.out.println("Enter 'done' when finished:");
        
        while (true) {
            System.out.print("  Column: ");
            String input = scanner.nextLine().trim();
            if (input.equalsIgnoreCase("done")) break;
            
            String[] parts = input.split(":");
            if (parts.length == 2) {
                try {
                    DataType type = DataType.valueOf(parts[1].toUpperCase());
                    columns.add(new Column(parts[0], type));
                    System.out.println(Colors.GREEN + "    Added: " + parts[0] + " (" + type + ")" + Colors.RESET);
                } catch (IllegalArgumentException e) {
                    System.out.println(Colors.RED + "    Invalid data type: " + parts[1] + Colors.RESET);
                }
            } else {
                System.out.println(Colors.RED + "    Invalid format. Use: name:type" + Colors.RESET);
            }
        }
        
        if (!columns.isEmpty()) {
            Table table = new Table(tableName, columns);
            database.addTable(table);
            System.out.println(Colors.GREEN + "\nTable '" + tableName + "' created successfully!" + Colors.RESET);
        }
    }
    
    private void insertRecord() {
        System.out.println("\n" + Colors.GREEN + "=== INSERT RECORD ===" + Colors.RESET);
        showTables();
        System.out.print("Enter table name: ");
        String tableName = scanner.nextLine().trim();
        
        Table table = database.getTable(tableName);
        if (table == null) {
            System.out.println(Colors.RED + "Table not found: " + tableName + Colors.RESET);
            return;
        }
        
        Map<String, Object> values = new HashMap<>();
        for (Column col : table.getColumns()) {
            System.out.print("  Enter " + col.getName() + " (" + col.getType() + "): ");
            String input = scanner.nextLine().trim();
            values.put(col.getName(), parseValue(input, col.getType()));
        }
        
        table.insert(values);
        System.out.println(Colors.GREEN + "\nRecord inserted successfully!" + Colors.RESET);
    }
    
    private void selectRecords() {
        System.out.println("\n" + Colors.GREEN + "=== SELECT RECORDS ===" + Colors.RESET);
        showTables();
        System.out.print("Enter table name: ");
        String tableName = scanner.nextLine().trim();
        
        Table table = database.getTable(tableName);
        if (table == null) {
            System.out.println(Colors.RED + "Table not found: " + tableName + Colors.RESET);
            return;
        }
        
        System.out.print("Enter WHERE condition (column=value) or press Enter for all: ");
        String condition = scanner.nextLine().trim();
        
        List<Record> results;
        if (condition.isEmpty()) {
            results = table.selectAll();
        } else {
            String[] parts = condition.split("=");
            if (parts.length == 2) {
                results = table.selectWhere(parts[0].trim(), parts[1].trim());
            } else {
                results = table.selectAll();
            }
        }
        
        table.printRecords(results);
    }
    
    private void updateRecord() {
        System.out.println("\n" + Colors.GREEN + "=== UPDATE RECORD ===" + Colors.RESET);
        showTables();
        System.out.print("Enter table name: ");
        String tableName = scanner.nextLine().trim();
        
        Table table = database.getTable(tableName);
        if (table == null) {
            System.out.println(Colors.RED + "Table not found: " + tableName + Colors.RESET);
            return;
        }
        
        System.out.print("Enter WHERE condition (column=value): ");
        String condition = scanner.nextLine().trim();
        String[] condParts = condition.split("=");
        
        if (condParts.length != 2) {
            System.out.println(Colors.RED + "Invalid condition format" + Colors.RESET);
            return;
        }
        
        System.out.print("Enter SET values (column=value): ");
        String setValue = scanner.nextLine().trim();
        String[] setParts = setValue.split("=");
        
        if (setParts.length != 2) {
            System.out.println(Colors.RED + "Invalid SET format" + Colors.RESET);
            return;
        }
        
        int updated = table.update(condParts[0].trim(), condParts[1].trim(), 
                                   setParts[0].trim(), setParts[1].trim());
        System.out.println(Colors.GREEN + "\n" + updated + " record(s) updated!" + Colors.RESET);
    }
    
    private void deleteRecord() {
        System.out.println("\n" + Colors.GREEN + "=== DELETE RECORD ===" + Colors.RESET);
        showTables();
        System.out.print("Enter table name: ");
        String tableName = scanner.nextLine().trim();
        
        Table table = database.getTable(tableName);
        if (table == null) {
            System.out.println(Colors.RED + "Table not found: " + tableName + Colors.RESET);
            return;
        }
        
        System.out.print("Enter WHERE condition (column=value): ");
        String condition = scanner.nextLine().trim();
        String[] parts = condition.split("=");
        
        if (parts.length != 2) {
            System.out.println(Colors.RED + "Invalid condition format" + Colors.RESET);
            return;
        }
        
        int deleted = table.delete(parts[0].trim(), parts[1].trim());
        System.out.println(Colors.GREEN + "\n" + deleted + " record(s) deleted!" + Colors.RESET);
    }
    
    private void showTables() {
        System.out.println("\n" + Colors.CYAN + "Tables in database '" + database.getName() + "':" + Colors.RESET);
        for (String name : database.getTableNames()) {
            Table t = database.getTable(name);
            System.out.println("  - " + name + " (" + t.getRecordCount() + " records)");
        }
    }
    
    private void describeTable() {
        System.out.print("\nEnter table name: ");
        String tableName = scanner.nextLine().trim();
        
        Table table = database.getTable(tableName);
        if (table == null) {
            System.out.println(Colors.RED + "Table not found: " + tableName + Colors.RESET);
            return;
        }
        
        table.describe();
    }
    
    private void executeSQL() {
        System.out.println("\n" + Colors.GREEN + "=== SQL QUERY EXECUTOR ===" + Colors.RESET);
        System.out.println("Supported: SELECT * FROM table, INSERT INTO table VALUES (...), etc.");
        System.out.print("SQL> ");
        String sql = scanner.nextLine().trim();
        
        // Simple SQL parser (demonstration)
        SQLParser parser = new SQLParser(database);
        parser.execute(sql);
    }
    
    private Object parseValue(String input, DataType type) {
        try {
            switch (type) {
                case INTEGER: return Integer.parseInt(input);
                case DOUBLE: return Double.parseDouble(input);
                case BOOLEAN: return Boolean.parseBoolean(input);
                case DATE: return input;
                default: return input;
            }
        } catch (Exception e) {
            return input;
        }
    }
}

// ============================================================================
// ENUMS
// ============================================================================

enum DataType {
    STRING, INTEGER, DOUBLE, BOOLEAN, DATE
}

// ============================================================================
// INTERFACES
// ============================================================================

interface Queryable {
    List<Record> selectAll();
    List<Record> selectWhere(String column, String value);
}

interface Modifiable {
    void insert(Map<String, Object> values);
    int update(String whereCol, String whereVal, String setCol, String setVal);
    int delete(String column, String value);
}

// ============================================================================
// CLASSES
// ============================================================================

class Colors {
    public static final String RESET = "\u001B[0m";
    public static final String RED = "\u001B[31m";
    public static final String GREEN = "\u001B[32m";
    public static final String YELLOW = "\u001B[33m";
    public static final String BLUE = "\u001B[34m";
    public static final String CYAN = "\u001B[36m";
    public static final String BOLD = "\u001B[1m";
}

class Column {
    private String name;
    private DataType type;
    private boolean nullable;
    
    public Column(String name, DataType type) {
        this.name = name;
        this.type = type;
        this.nullable = true;
    }
    
    public String getName() { return name; }
    public DataType getType() { return type; }
    public boolean isNullable() { return nullable; }
}

class Record {
    private int id;
    private Map<String, Object> data;
    private LocalDateTime createdAt;
    
    public Record(int id, Map<String, Object> data) {
        this.id = id;
        this.data = new HashMap<>(data);
        this.createdAt = LocalDateTime.now();
    }
    
    public int getId() { return id; }
    public Object get(String column) { return data.get(column); }
    public void set(String column, Object value) { data.put(column, value); }
    public Map<String, Object> getData() { return data; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}

class Table implements Queryable, Modifiable {
    private String name;
    private List<Column> columns;
    private List<Record> records;
    private int nextId;
    
    public Table(String name, List<Column> columns) {
        this.name = name;
        this.columns = new ArrayList<>(columns);
        this.records = new ArrayList<>();
        this.nextId = 1;
    }
    
    public String getName() { return name; }
    public List<Column> getColumns() { return columns; }
    public int getRecordCount() { return records.size(); }
    
    @Override
    public void insert(Map<String, Object> values) {
        Record record = new Record(nextId++, values);
        records.add(record);
    }
    
    @Override
    public List<Record> selectAll() {
        return new ArrayList<>(records);
    }
    
    @Override
    public List<Record> selectWhere(String column, String value) {
        List<Record> results = new ArrayList<>();
        for (Record r : records) {
            Object val = r.get(column);
            if (val != null && val.toString().equals(value)) {
                results.add(r);
            }
        }
        return results;
    }
    
    @Override
    public int update(String whereCol, String whereVal, String setCol, String setVal) {
        int count = 0;
        for (Record r : records) {
            Object val = r.get(whereCol);
            if (val != null && val.toString().equals(whereVal)) {
                r.set(setCol, setVal);
                count++;
            }
        }
        return count;
    }
    
    @Override
    public int delete(String column, String value) {
        int count = 0;
        Iterator<Record> it = records.iterator();
        while (it.hasNext()) {
            Record r = it.next();
            Object val = r.get(column);
            if (val != null && val.toString().equals(value)) {
                it.remove();
                count++;
            }
        }
        return count;
    }
    
    public void describe() {
        System.out.println("\n" + Colors.CYAN + "Table: " + name + Colors.RESET);
        System.out.println(Colors.CYAN + "─".repeat(50) + Colors.RESET);
        System.out.printf("%-20s %-15s %-10s%n", "Column", "Type", "Nullable");
        System.out.println("─".repeat(50));
        for (Column col : columns) {
            System.out.printf("%-20s %-15s %-10s%n", 
                col.getName(), col.getType(), col.isNullable() ? "YES" : "NO");
        }
        System.out.println("\nTotal Records: " + records.size());
    }
    
    public void printRecords(List<Record> recs) {
        if (recs.isEmpty()) {
            System.out.println(Colors.YELLOW + "\nNo records found." + Colors.RESET);
            return;
        }
        
        // Print header
        System.out.println();
        System.out.print(String.format("%-5s", "ID"));
        for (Column col : columns) {
            System.out.print(String.format("%-15s", col.getName()));
        }
        System.out.println();
        System.out.println("─".repeat(5 + columns.size() * 15));
        
        // Print records
        for (Record r : recs) {
            System.out.print(String.format("%-5d", r.getId()));
            for (Column col : columns) {
                Object val = r.get(col.getName());
                String strVal = val != null ? val.toString() : "NULL";
                if (strVal.length() > 12) strVal = strVal.substring(0, 12) + "..";
                System.out.print(String.format("%-15s", strVal));
            }
            System.out.println();
        }
        System.out.println("\n" + Colors.GREEN + recs.size() + " record(s) returned." + Colors.RESET);
    }
}

class Database {
    private String name;
    private Map<String, Table> tables;
    
    public Database(String name) {
        this.name = name;
        this.tables = new HashMap<>();
        initSampleData();
    }
    
    private void initSampleData() {
        // Create sample Employees table
        List<Column> empCols = Arrays.asList(
            new Column("name", DataType.STRING),
            new Column("department", DataType.STRING),
            new Column("salary", DataType.DOUBLE),
            new Column("active", DataType.BOOLEAN)
        );
        Table employees = new Table("employees", empCols);
        
        Map<String, Object> emp1 = new HashMap<>();
        emp1.put("name", "John Smith");
        emp1.put("department", "IT");
        emp1.put("salary", 75000.0);
        emp1.put("active", true);
        employees.insert(emp1);
        
        Map<String, Object> emp2 = new HashMap<>();
        emp2.put("name", "Jane Doe");
        emp2.put("department", "HR");
        emp2.put("salary", 65000.0);
        emp2.put("active", true);
        employees.insert(emp2);
        
        Map<String, Object> emp3 = new HashMap<>();
        emp3.put("name", "Bob Wilson");
        emp3.put("department", "IT");
        emp3.put("salary", 80000.0);
        emp3.put("active", false);
        employees.insert(emp3);
        
        tables.put("employees", employees);
        
        // Create sample Products table
        List<Column> prodCols = Arrays.asList(
            new Column("product_name", DataType.STRING),
            new Column("price", DataType.DOUBLE),
            new Column("quantity", DataType.INTEGER)
        );
        Table products = new Table("products", prodCols);
        
        Map<String, Object> prod1 = new HashMap<>();
        prod1.put("product_name", "Laptop");
        prod1.put("price", 999.99);
        prod1.put("quantity", 50);
        products.insert(prod1);
        
        Map<String, Object> prod2 = new HashMap<>();
        prod2.put("product_name", "Mouse");
        prod2.put("price", 29.99);
        prod2.put("quantity", 200);
        products.insert(prod2);
        
        tables.put("products", products);
    }
    
    public String getName() { return name; }
    
    public void addTable(Table table) {
        tables.put(table.getName().toLowerCase(), table);
    }
    
    public Table getTable(String name) {
        return tables.get(name.toLowerCase());
    }
    
    public Set<String> getTableNames() {
        return tables.keySet();
    }
}

class SQLParser {
    private Database database;
    
    public SQLParser(Database database) {
        this.database = database;
    }
    
    public void execute(String sql) {
        sql = sql.trim().toUpperCase();
        
        if (sql.startsWith("SELECT")) {
            executeSelect(sql);
        } else if (sql.startsWith("SHOW TABLES")) {
            for (String name : database.getTableNames()) {
                System.out.println("  " + name);
            }
        } else if (sql.startsWith("DESC") || sql.startsWith("DESCRIBE")) {
            String[] parts = sql.split("\\s+");
            if (parts.length >= 2) {
                Table t = database.getTable(parts[1]);
                if (t != null) t.describe();
                else System.out.println(Colors.RED + "Table not found" + Colors.RESET);
            }
        } else {
            System.out.println(Colors.YELLOW + "Query executed (simulation mode)" + Colors.RESET);
        }
    }
    
    private void executeSelect(String sql) {
        // Simple SELECT * FROM table parser
        if (sql.contains("FROM")) {
            String[] parts = sql.split("FROM");
            if (parts.length >= 2) {
                String tableName = parts[1].trim().split("\\s+")[0];
                Table table = database.getTable(tableName);
                if (table != null) {
                    table.printRecords(table.selectAll());
                } else {
                    System.out.println(Colors.RED + "Table not found: " + tableName + Colors.RESET);
                }
            }
        }
    }
}
