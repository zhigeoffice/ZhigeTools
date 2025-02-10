# -*- encoding: utf-8 -*-
"""
INI配置文件读写组件使用示例
"""
import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from zhige_tools.ini_reader import (
    read_ini_file,
    write_ini_file,
    initialize_ini_file,
    verify_config_file
)

def main():
    # 1. 定义配置规则
    rules = {
        'Database': {
            'host': str,
            'port': int,
            'enable_ssl': bool,
            'max_connections': int
        },
        'App': {
            'debug': bool,
            'log_level': str,
            'max_threads': int
        }
    }

    # 2. 定义默认配置
    default_values = {
        'Database': {
            'host': 'localhost',
            'port': '5432',
            'enable_ssl': 'True',
            'max_connections': '100'
        },
        'App': {
            'debug': 'False',
            'log_level': 'INFO',
            'max_threads': '4'
        }
    }

    config_path = 'config.ini'

    try:
        # 3. 初始化配置文件
        print("正在初始化配置文件...")
        initialize_ini_file(config_path, rules, default_values)
        print("配置文件初始化成功！")

        # 4. 读取配置
        print("\n读取当前配置:")
        config = read_ini_file(config_path)
        for section, values in config.items():
            print(f"\n[{section}]")
            for key, value in values.items():
                print(f"{key} = {value}")

        # 5. 修改配置
        print("\n修改配置...")
        config['Database']['host'] = 'db.example.com'
        config['App']['debug'] = 'True'
        
        # 6. 验证修改后的配置
        if verify_config_file(config, rules):
            write_ini_file(config_path, config)
            print("配置更新成功！")

        # 7. 再次读取确认更改
        print("\n更新后的配置:")
        updated_config = read_ini_file(config_path)
        for section, values in updated_config.items():
            print(f"\n[{section}]")
            for key, value in values.items():
                print(f"{key} = {value}")

    except FileNotFoundError as e:
        print(f"错误: {e}")
    except ValueError as e:
        print(f"配置验证错误: {e}")
    except IOError as e:
        print(f"IO错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == '__main__':
    main() 