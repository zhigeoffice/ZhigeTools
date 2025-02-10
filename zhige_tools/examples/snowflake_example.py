# -*- encoding: utf-8 -*-
"""
雪花ID生成器使用示例
"""
import os
import sys
import time
# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from zhige_tools.snowflake import snowflake_handler

def main():
    try:
        # 1. 初始化不同进制的雪花ID生成器
        print("初始化雪花ID生成器...")
        snowflake_handler.create_snowflake(machine_id=1)  # 默认10进制
        snowflake_handler.create_snowflake(machine_id=2, base=16)  # 16进制
        snowflake_handler.create_snowflake(machine_id=3, base=62)  # 62进制

        # 测试进制冲突
        try:
            print("\n测试进制冲突...")
            # 尝试用不同的进制初始化已存在的生成器
            snowflake_handler.create_snowflake(machine_id=1, base=16)
        except ValueError as e:
            print(f"预期的进制冲突错误: {e}")

        # 2. 生成一些ID
        print("\n生成ID:")
        for i in range(5):
            # 从不同机器生成不同进制的ID
            id1 = snowflake_handler.get_id(1)  # 10进制
            id2 = snowflake_handler.get_id(2)  # 16进制
            id3 = snowflake_handler.get_id(3)  # 62进制
            print(f"机器1生成ID(10进制): {id1}，长度为{len(str(id1))}")
            print(f"机器2生成ID(16进制): {id2}，长度为{len(id2)}")
            print(f"机器3生成ID(62进制): {id3}，长度为{len(id3)}")

        # 3. 解析不同进制的ID
        print("\n解析最后生成的ID:")
        parsed1 = snowflake_handler.parse_id(id1, 1)
        parsed2 = snowflake_handler.parse_id(id2, 2)
        parsed3 = snowflake_handler.parse_id(id3, 3)
        
        for machine_id, parsed in [(1, parsed1), (2, parsed2), (3, parsed3)]:
            print(f"\n机器{machine_id}生成的ID解析结果:")
            print(f"原始ID: {parsed['original_id']} ({parsed['base_name']})")
            print(f"十进制值: {parsed['decimal_id']}")
            print(f"生成时间: {parsed['datetime']}")
            print(f"机器ID: {parsed['machine_id']}")
            print(f"序列号: {parsed['sequence']}")

        # 4. 性能测试
        print("\n生成1000000个ID，并计算耗时:")
        for machine_id in (1, 2, 3):
            start_time = time.time()
            for i in range(1000000):
                snowflake_handler.get_id(machine_id)
            end_time = time.time()
            print(f"机器{machine_id}生成1000000个ID耗时: {end_time - start_time}秒")

    except ValueError as e:
        print(f"参数错误: {e}")
    except KeyError as e:
        print(f"初始化错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == '__main__':
    main() 