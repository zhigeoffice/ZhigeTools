# ZhigeTools
[English](README.md)    |    [简体中文](README-zh.md)
## 使用说明
ZhigeTools 是一款基于 Python 的开源工具箱，主要是对日常工作中常用的一些工具的封装，方便使用。

## 安装
```
pip install zhigetools
```

## 开发

查看[开发指南](DEVELOPMENT.md)了解如何参与项目开发。

## 功能
- [x] 字符转换工具

    base_to_number
    - 将字符串转为数字，支持自定义进制和自定义进制的符号。
    ``` python
    from zhige_tools.base_converter import base_to_number
    ```
    number_to_base
    - 将数字转为字符串，支持自定义进制和自定义进制的符号。
    ``` python
    from zhige_tools.base_converter import number_to_base
    ```

- [x] INI配置文件工具
    - 读取、写入和验证INI配置文件，支持类型检查
    ``` python
    from zhige_tools.ini_reader import read_ini_file, write_ini_file, initialize_ini_file
    
    # 定义配置规则
    rules = {
        'Database': {
            'host': str,
            'port': int,
            'debug': bool
        }
    }
    
    # 使用默认值初始化
    initialize_ini_file('config.ini', rules, default_values)
    
    # 读取配置
    config = read_ini_file('config.ini')
    ```

- [x] 雪花ID生成器
    - 基于Twitter雪花算法的分布式唯一ID生成器
    - 支持多机器ID和时钟回拨校正
    - 支持十进制、十六进制和62进制输出格式
    ``` python
    from zhige_tools.snowflake import snowflake_handler
    
    # 使用不同进制初始化 (10/16/62)
    snowflake_handler.create_snowflake(machine_id=1)  # 十进制（默认）
    snowflake_handler.create_snowflake(machine_id=2, base=16)  # 十六进制
    snowflake_handler.create_snowflake(machine_id=3, base=62)  # 62进制
    
    # 生成ID
    dec_id = snowflake_handler.get_id(1)    # 例如："1234567890123456"
    hex_id = snowflake_handler.get_id(2)    # 例如："1234abcd5678"
    b62_id = snowflake_handler.get_id(3)    # 例如："Az9bXy8K"
    
    # 解析ID
    parsed = snowflake_handler.parse_id(dec_id, 1)
    print(parsed)  # {'original_id': '1234567890123456', 'decimal_id': 1234567890123456, 
                   #  'datetime': '2024-02-10 10:30:00', 'machine_id': 1, 'sequence': 0,
                   #  'base': 10, 'base_name': '十进制'}
    ```

## 更新日志
- **2024.02.10 v0.2.0**
  - 增强雪花ID生成器
    - 添加十六进制和62进制输出格式支持
    - 添加进制配置和验证
    - 改进ID解析，提供更详细信息
  - 改进INI配置文件工具
  - 更新文档和示例

- **2024.02.10 v0.1.3**
  - 添加雪花ID生成器
  - 添加INI配置文件工具

- **2021.10.25 v0.1.1**
  - 增加函数提示，修改README.md

- **2021.10.25 v0.1.0**
  - 初次发布


