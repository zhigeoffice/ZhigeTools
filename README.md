# ZhigeTools
[English](README.md)    |    [简体中文](README-zh.md)
## Introduction
ZhigeTools is an open-source Python toolkit that provides a collection of utility functions for daily work. It is designed to simplify common tasks by offering easy-to-use wrappers.

## Installation
```
pip install zhigetools
```

## Development

See [Development Guide](DEVELOPMENT.md) for information about contributing to this project.

## Features
- [x] Character Conversion Tools

    base_to_number
    - Converts a string to a number, supporting custom bases and custom symbols for the base.
    ``` python
    from zhige_tools.base_converter import base_to_number
    ```
    number_to_base
    - Converts a number to a string, supporting custom bases and custom symbols for the base.
    ``` python
    from zhige_tools.base_converter import number_to_base
    ```

- [x] INI Configuration File Tools
    - Read, write and validate INI configuration files with type checking
    ``` python
    from zhige_tools.ini_reader import read_ini_file, write_ini_file, initialize_ini_file
    
    # Define configuration rules
    rules = {
        'Database': {
            'host': str,
            'port': int,
            'debug': bool
        }
    }
    
    # Initialize with default values
    initialize_ini_file('config.ini', rules, default_values)
    
    # Read configuration
    config = read_ini_file('config.ini')
    ```

- [x] Snowflake ID Generator
    - Distributed unique ID generator based on Twitter's Snowflake algorithm
    - Support multiple machine IDs and clock drift correction
    - Support decimal, hexadecimal and base62 output formats
    ``` python
    from zhige_tools.snowflake import snowflake_handler
    
    # Initialize with different bases (10/16/62)
    snowflake_handler.create_snowflake(machine_id=1)  # decimal (default)
    snowflake_handler.create_snowflake(machine_id=2, base=16)  # hexadecimal
    snowflake_handler.create_snowflake(machine_id=3, base=62)  # base62
    
    # Generate ID
    dec_id = snowflake_handler.get_id(1)    # e.g., "1234567890123456"
    hex_id = snowflake_handler.get_id(2)    # e.g., "1234abcd5678"
    b62_id = snowflake_handler.get_id(3)    # e.g., "Az9bXy8K"
    
    # Parse ID
    parsed = snowflake_handler.parse_id(dec_id, 1)
    print(parsed)  # {'original_id': '1234567890123456', 'decimal_id': 1234567890123456, 
                   #  'datetime': '2024-02-10 10:30:00', 'machine_id': 1, 'sequence': 0,
                   #  'base': 10, 'base_name': '十进制'}
    ```

## Changelog
- **2024.02.10 v0.2.0**
  - Enhanced Snowflake ID generator
    - Added support for hexadecimal and base62 output formats
    - Added base configuration and validation
    - Improved ID parsing with detailed information
  - Improved INI configuration file tools
  - Updated documentation and examples

- **2024.02.10 v0.1.3**
  - Added Snowflake ID generator
  - Added INI configuration file tools

- **2021.10.25 v0.1.1**
  - Added function hints, updated README.md

- **2021.10.25 v0.1.0**
  - Initial release

