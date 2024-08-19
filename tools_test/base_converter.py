# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@File    : base_converter.py
@Time    : 2024/8/19 16:07
@Author  : zhige
@Email   : zhigeoffice@gmail.com
@Software: PyCharm
"""
from zhige_tools import base_converter  # 确保导入路径正确


class BaseConverterTest(object):
    def __init__(self):
        print("--- base_converter.base_to_number ---")
        self.test_base_to_number()
        print()
        print("--- base_converter.number_to_base ---")
        self.test_number_to_base()

    def test_base_to_number(self):
        # Test cases for base_to_number function
        test_cases = [
            ('101010', 2, 42),  # Binary to decimal
            ('2a', 16, 42),  # Hexadecimal to decimal
            ('52', 8, 42),  # Octal to decimal
            ('-2a', 16, -42),  # Negative hexadecimal to decimal
            ('1G7U', 64, 434680),  # Base64 to decimal
            ('abc', 36, 13368),  # Base36 to decimal
        ]

        custom_alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
        custom_base36 = custom_alphabet[:36]
        custom_base64 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789*+'

        # Custom alphabet base conversion
        test_cases.extend([
            ('d', 36, 3, custom_base36),  # Base36 to decimal
            ('1d', 36, 975, custom_base36),  # Base36 to decimal
            ('-*+', 64, -4031, custom_base64),  # Base64 to decimal
            ('**', 64, 4030, custom_base64),  # Custom base64 to decimal
        ])

        for base_str, base, expected, *custom_alphabet in test_cases:
            if custom_alphabet:
                num = base_converter.base_to_number(base_str, base, custom_alphabet[0])
            else:
                num = base_converter.base_to_number(base_str, base)
            print(f'{base}:{base_str} >>> {num} (Expected: {expected})')

    def test_number_to_base(self):
        # Test cases for number_to_base function
        test_cases = [
            (42, 2, '101010'),  # Decimal to binary
            (42, 16, '2a'),  # Decimal to hexadecimal
            (42, 8, '52'),  # Decimal to octal
            (-42, 16, '-2a'),  # Decimal to negative hexadecimal
            (1234567, 64, '4Jq7'),  # Decimal to base64
            (123456, 36, '2n9c'),  # Decimal to base36
        ]

        custom_alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
        custom_base36 = custom_alphabet[:36]
        custom_base64 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789*+'

        # Custom alphabet base conversion
        test_cases.extend([
            (13, 36, 'd', custom_base36),  # Decimal to base36
            (49, 36, '1d', custom_base36),  # Decimal to base36
            (-4031, 64, '-*+', custom_base64),  # Decimal to base64
            (4030, 64, '**', custom_base64),  # Decimal to base64
        ])

        for number, base, expected, *custom_alphabet in test_cases:
            if custom_alphabet:
                base_str = base_converter.number_to_base(number, base, custom_alphabet[0])
            else:
                base_str = base_converter.number_to_base(number, base)
            print(f'{number} >>> {base}:{base_str} (Expected: {expected})')


if __name__ == '__main__':
    BaseConverterTest()
