# Database Management System Simulator

**Author:** Eyasu Solomon  
**Language:** Java  
**Version:** Java 8+

## Overview

An interactive Java application that simulates a database management system. Demonstrates proficiency in Object-Oriented Programming including inheritance, polymorphism, interfaces, encapsulation, and design patterns.

## Features

- **Create Tables** - Define custom tables with typed columns
- **Insert Records** - Add data with type validation
- **Select/Query** - Retrieve records with optional WHERE conditions
- **Update Records** - Modify existing data
- **Delete Records** - Remove records by condition
- **Describe Tables** - View table structure
- **SQL Query Executor** - Execute basic SQL commands

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
