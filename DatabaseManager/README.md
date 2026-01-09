# Database Manager Pro

**Author:** Eyasu Solomon  
**Version:** 2.0  
**Language:** Java  
**Framework:** Java Swing

## Overview

A full-featured GUI database management application built with Java Swing. Features a modern dark theme, SQL editor, database browser, and query execution. Demonstrates advanced OOP, GUI development, and database concepts.

## Files

| File | Description |
|------|-------------|
| `DatabaseManager.java` | Original console version |
| `DatabaseManagerGUI.java` | **Full Swing GUI application** |

## Features

### Database Explorer (Left Panel)
- Tree view of databases and tables
- Double-click table to auto-query
- Expandable/collapsible nodes
- Query history with click-to-restore

### SQL Query Editor (Center)
- Syntax-aware text area
- Line numbers
- Tab-based multiple queries
- Query formatting (Ctrl+Shift+F)

### Results Panel (Bottom)
- JTable with sortable columns
- Console output tab
- Timestamped execution logs
- Row count display

### SQL Support
- SELECT with WHERE clause filtering
- INSERT INTO (simulated)
- UPDATE (simulated)
- DELETE (simulated)
- CREATE TABLE

### Menu Bar
- **File**: New Connection, Open, Import SQL, Export
- **Edit**: Undo, Redo, Cut, Copy, Paste
- **Query**: Execute (F5), Format, Clear
- **Database**: Create Database, Create Table, Refresh
- **Help**: Documentation, About

## Data Types Supported

- `STRING` - Text data
- `INTEGER` - Whole numbers
- `DOUBLE` - Decimal numbers
- `BOOLEAN` - True/False values
- `DATE` - Date strings

## How to Compile and Run

```bash
# Compile
javac DatabaseManager.java

# Run
java DatabaseManager
```

## Usage Example

```
╔══════════════════════════════════════╗
║          MAIN MENU                   ║
╠══════════════════════════════════════╣
║  1. Create Table                     ║
║  2. Insert Record                    ║
║  3. Select Records (Query)           ║
║  4. Update Record                    ║
║  5. Delete Record                    ║
║  6. Show All Tables                  ║
║  7. Describe Table                   ║
║  8. Execute SQL Query                ║
║  9. Exit                             ║
╚══════════════════════════════════════╝
```

## Sample Data

The application comes pre-loaded with sample tables:

### Employees Table
| ID | Name       | Department | Salary  | Active |
|----|------------|------------|---------|--------|
| 1  | John Smith | IT         | 75000.0 | true   |
| 2  | Jane Doe   | HR         | 65000.0 | true   |
| 3  | Bob Wilson | IT         | 80000.0 | false  |

### Products Table
| ID | Product Name | Price  | Quantity |
|----|--------------|--------|----------|
| 1  | Laptop       | 999.99 | 50       |
| 2  | Mouse        | 29.99  | 200      |

## OOP Concepts Demonstrated

- **Encapsulation** - Private fields with getters/setters
- **Inheritance** - Class hierarchies
- **Polymorphism** - Interface implementations
- **Interfaces** - `Queryable` and `Modifiable` interfaces
- **Generics** - Collections with type parameters
- **Enums** - `DataType` enumeration
- **Exception Handling** - Input validation
- **Design Patterns** - Command pattern for SQL execution

## Skills Demonstrated

- Java Programming
- Object-Oriented Design
- Data Structures
- Database Concepts
- User Interface Design
- Input Validation
