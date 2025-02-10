# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@File    : snowflake
@Time    : 2025/2/10 16:02
@Author  : zhige
@Email   : zhigeoffice@gmail.com
@Software: PyCharm
"""
import os
import time
from typing import Optional, Union
from .ini_reader import initialize_ini_file, read_ini_file, write_ini_file
from .base_converter import number_to_base

class Snowflake:
    # 64位ID的划分
    TIMESTAMP_BITS = 41  # 时间戳占用位数
    MACHINE_ID_BITS = 10  # 机器ID占用位数
    SEQUENCE_BITS = 12  # 序列号占用位数

    # 最大取值
    MAX_MACHINE_ID = -1 ^ (-1 << MACHINE_ID_BITS)  # 1023
    MAX_SEQUENCE = -1 ^ (-1 << SEQUENCE_BITS)  # 4095

    # 位移
    MACHINE_ID_SHIFT = SEQUENCE_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + MACHINE_ID_BITS

    def __init__(self, machine_id: int = 0, config_path: Optional[str] = None, base: Union[int, str] = 10):
        """
        初始化雪花ID生成器
        
        Args:
            machine_id: 机器ID (0-1023)
            config_path: 配置文件路径，如果为None则使用默认路径
            base: 返回ID的进制，支持:
                - 10: 十进制 (默认)
                - 16: 十六进制
                - 62: 62进制 (0-9a-zA-Z)
                - 'hex': 十六进制
                - '62': 62进制
        """
        if not 0 <= machine_id <= self.MAX_MACHINE_ID:
            raise ValueError(f"机器ID必须在0-{self.MAX_MACHINE_ID}之间")

        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1
        
        # 设置进制
        if isinstance(base, str):
            if base.lower() == 'hex':
                self.base = 16
            elif base == '62':
                self.base = 62
            else:
                raise ValueError("base参数只支持'hex'或'62'字符串值")
        elif isinstance(base, int):
            if base not in (10, 16, 62):
                raise ValueError("base参数只支持10、16或62进制")
            self.base = base
        else:
            raise ValueError("base参数类型必须是int或str")
        
        # 初始化配置
        self.config = self._get_config(machine_id, config_path)
        self.epoch = int(self.config['Snowflake']['epoch'])

    def _get_config(self, machine_id: int, config_path: Optional[str]) -> dict:
        """获取或初始化配置"""
        if config_path is None:
            # 确保配置目录存在
            config_dir = os.path.join(os.getcwd(), 'config', 'snowflake')
            os.makedirs(config_dir, exist_ok=True)
            config_path = os.path.join(config_dir, f'{machine_id}.ini')

        # 定义配置规则
        rules = {
            'Snowflake': {
                'machine_id': int,
                'epoch': int,
                'base': int,  # 新增进制配置
            }
        }

        # 默认配置
        # 使用2020-01-01 00:00:00 作为默认epoch
        default_epoch = int(time.mktime(time.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")) * 1000)
        
        default_values = {
            'Snowflake': {
                'machine_id': str(machine_id),
                'epoch': str(default_epoch),
                'base': str(self.base),  # 保存进制设置
            }
        }

        if os.path.exists(config_path):
            # 如果配置文件已存在，验证进制设置
            current_config = read_ini_file(config_path)
            current_base = int(current_config['Snowflake']['base'])
            if current_base != self.base:
                raise ValueError(
                    f"进制设置冲突：配置文件中为{current_base}进制，"
                    f"但参数指定为{self.base}进制。请使用相同的进制设置。"
                )
        
        # 初始化配置文件
        initialize_ini_file(config_path, rules, default_values)
        
        return read_ini_file(config_path)

    def _gen_timestamp(self) -> int:
        """获取当前时间戳"""
        return int(time.time() * 1000) - self.epoch

    def _time_back_correct(self, timestamp: int) -> int:
        """
        时钟回拨校正
        当检测到时钟回拨时，等待直到时间追上来
        """
        while timestamp < self.last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

    def get_id(self) -> Union[int, str]:
        """
        生成下一个ID
        
        Returns:
            Union[int, str]: 根据指定进制返回ID
                - base=10: 返回整数
                - base=16: 返回小写十六进制字符串
                - base=62: 返回62进制字符串
        
        Raises:
            RuntimeError: 当序列号用尽时抛出
        """
        decimal_id = self._generate_id()
        
        if self.base == 10:
            return decimal_id
        else:
            return number_to_base(decimal_id, self.base)

    def _generate_id(self) -> int:
        """生成原始十进制ID"""
        timestamp = self._gen_timestamp()
        
        # 时钟回拨检测和校正
        if timestamp < self.last_timestamp:
            timestamp = self._time_back_correct(timestamp)

        # 同一毫秒
        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
            # 同一毫秒序列号用尽
            if self.sequence == 0:
                timestamp = self._time_back_correct(self.last_timestamp + 1)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # 组合ID
        return (timestamp << self.TIMESTAMP_SHIFT) | \
               (self.machine_id << self.MACHINE_ID_SHIFT) | \
               self.sequence

    def parse_id(self, snowflake_id: Union[int, str]) -> dict:
        """
        解析雪花ID
        
        Args:
            snowflake_id: 雪花ID，可以是整数或字符串（16进制或62进制）
            
        Returns:
            dict: 包含时间戳、机器ID、序列号和进制信息的字典
        """
        # 如果输入是字符串，先转换为十进制整数
        original_id = snowflake_id  # 保存原始ID用于返回
        if isinstance(snowflake_id, str):
            from .base_converter import base_to_number
            if self.base == 16:
                decimal_id = int(snowflake_id, 16)
            elif self.base == 62:
                decimal_id = base_to_number(snowflake_id, 62)
            else:
                decimal_id = int(snowflake_id)
        else:
            decimal_id = snowflake_id

        timestamp = (decimal_id >> self.TIMESTAMP_SHIFT) + self.epoch
        machine_id = (decimal_id >> self.MACHINE_ID_SHIFT) & self.MAX_MACHINE_ID
        sequence = decimal_id & self.MAX_SEQUENCE
        
        # 添加进制信息到返回结果
        base_info = {
            10: "十进制",
            16: "十六进制",
            62: "62进制"
        }
        
        return {
            'original_id': original_id,  # 原始格式的ID
            'decimal_id': decimal_id,    # 十进制格式的ID
            'timestamp': timestamp,
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp/1000)),
            'machine_id': machine_id,
            'sequence': sequence,
            'base': self.base,
            'base_name': base_info.get(self.base, f"{self.base}进制")
        }


class SnowflakeHandler:
    """
    雪花ID生成器管理类（单例模式）
    """
    _instance = None
    _snowflakes = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SnowflakeHandler, cls).__new__(cls)
        return cls._instance

    def create_snowflake(self, machine_id: int = 0, config_path: Optional[str] = None, 
                        base: Union[int, str] = 10) -> None:
        """
        创建或获取雪花ID生成器
        
        Args:
            machine_id: 机器ID
            config_path: 配置文件路径
            base: 返回ID的进制 (10, 16, 62, 'hex', '62')
        """
        if machine_id not in self._snowflakes:
            self._snowflakes[machine_id] = Snowflake(machine_id, config_path, base)

    def get_id(self, machine_id: int = 0) -> Union[int, str]:
        """
        获取下一个ID
        
        Args:
            machine_id: 机器ID
            
        Returns:
            Union[int, str]: 根据指定进制返回ID
                - base=10: 返回整数
                - base=16: 返回小写十六进制字符串
                - base=62: 返回62进制字符串
            
        Raises:
            KeyError: 如果指定的机器ID未初始化
        """
        if machine_id not in self._snowflakes:
            raise KeyError(f"机器ID {machine_id} 未初始化，请先调用 create_snowflake()")
        return self._snowflakes[machine_id].get_id()

    def parse_id(self, snowflake_id: Union[int, str], machine_id: int = 0) -> dict:
        """
        解析雪花ID
        
        Args:
            snowflake_id: 雪花ID，可以是整数或字符串（16进制或62进制）
            machine_id: 机器ID
            
        Returns:
            dict: 解析结果
            
        Raises:
            KeyError: 如果指定的机器ID未初始化
        """
        if machine_id not in self._snowflakes:
            raise KeyError(f"机器ID {machine_id} 未初始化，请先调用 create_snowflake()")
        return self._snowflakes[machine_id].parse_id(snowflake_id)


# 全局单例实例
snowflake_handler = SnowflakeHandler()

