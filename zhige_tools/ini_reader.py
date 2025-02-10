# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@File    : ini_reader.py
@Time    : 2025-2-10 17:09:37
@Author  : zhige
@Email   : zhigeoffice@gmail.com
@Software: PyCharm
"""
import configparser
import os
from typing import Dict, Any, Optional


def read_ini_file(file_path: str) -> Dict[str, Dict[str, Any]]:
    """
    读取config文件，返回配置数据字典

    Args:
        file_path (str): INI文件路径

    Returns:
        Dict[str, Dict[str, Any]]: 包含所有配置的嵌套字典
        
    Raises:
        FileNotFoundError: 文件不存在时抛出
        configparser.Error: 解析配置文件出错时抛出
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件不存在: {file_path}")

    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    
    result = {}
    for section in config.sections():
        result[section] = dict(config[section])
    
    return result


def write_ini_file(file_path: str, data: Dict[str, Dict[str, Any]]) -> None:
    """
    写入config文件

    Args:
        file_path (str): INI文件路径
        data (Dict[str, Dict[str, Any]]): 要写入的配置数据

    Raises:
        IOError: 写入文件失败时抛出
    """
    config = configparser.ConfigParser()
    
    for section, values in data.items():
        config[section] = values
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            config.write(f)
    except IOError as e:
        raise IOError(f"写入配置文件失败: {str(e)}")


def initialize_ini_file(file_path: str, rules: Dict[str, Dict[str, type]], 
                       default_values: Dict[str, Dict[str, Any]]) -> None:
    """
    config初始化，如果文件不存在则创建并写入默认值，如果存在则验证格式

    Args:
        file_path (str): INI文件路径
        rules (Dict[str, Dict[str, type]]): 配置规则，定义每个配置项的数据类型
        default_values (Dict[str, Dict[str, Any]]): 默认配置值

    Raises:
        ValueError: 默认值不符合规则时抛出
    """
    if not os.path.exists(file_path):
        # 验证默认值是否符合规则
        if verify_config_file(default_values, rules):
            write_ini_file(file_path, default_values)
    else:
        current_config = read_ini_file(file_path)
        if verify_config_file(current_config, rules):
            # 检查是否有缺失的配置项，如有则补充默认值
            for section, values in default_values.items():
                if section not in current_config:
                    current_config[section] = {}
                for key, value in values.items():
                    if key not in current_config[section]:
                        current_config[section][key] = value
            
            write_ini_file(file_path, current_config)


def verify_config_file(config_data: Dict[str, Dict[str, Any]], 
                      rules: Dict[str, Dict[str, type]]) -> bool:
    """
    config文件校验器，检查配置是否符合规则

    Args:
        config_data (Dict[str, Dict[str, Any]]): 配置数据
        rules (Dict[str, Dict[str, type]]): 配置规则

    Returns:
        bool: 验证通过返回True，否则抛出异常

    Raises:
        ValueError: 配置不符合规则时抛出
    """
    for section, section_rules in rules.items():
        if section not in config_data:
            raise ValueError(f"缺少必需的配置节: {section}")
        
        for key, expected_type in section_rules.items():
            if key not in config_data[section]:
                raise ValueError(f"在节 {section} 中缺少必需的配置项: {key}")
            
            value = config_data[section][key]
            try:
                # 尝试类型转换
                if expected_type == bool:
                    # 特殊处理布尔值
                    if isinstance(value, str):
                        if value.lower() not in ('true', 'false', '1', '0'):
                            raise ValueError
                else:
                    expected_type(value)
            except ValueError:
                raise ValueError(
                    f"配置项 [{section}]{key} 的值 {value} 不是预期的类型 {expected_type.__name__}"
                )
    
    return True
