# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@File    : base_converter
@Time    : 2024/8/19 16:02
@Author  : zhige
@Email   : zhigeoffice@gmail.com
@Software: PyCharm
"""

import string


def _get_alphabet(base, custom_alphabet=None):
    """Helper function to get the alphabet based on base or custom alphabet."""
    base64_alphabet = string.digits + string.ascii_lowercase + string.ascii_uppercase + '+/'

    if custom_alphabet:
        if len(custom_alphabet) != base:
            raise ValueError(f"custom_alphabet length must be equal to base: {base}")
        alphabet = custom_alphabet
    else:
        if base <= 64:
            alphabet = base64_alphabet[:base]
        else:
            raise ValueError(f"Unsupported base: {base}. Supported bases are 2, 8, 10, 16, 24, 36, 62, 64.")

    if ' ' in alphabet:
        raise ValueError("custom_alphabet cannot contain spaces")

    return alphabet


def number_to_base(number, base=16, custom_alphabet=None) -> str:
    """
    Convert a number to a string in a given base(将数字转换为指定进制的字符串).
    Args:
        number (int): The number to convert(需要转换的数字).
        base (int): The base to use for the conversion(进制).
        custom_alphabet (str): A custom alphabet to use for the conversion(自定义字符集).
    Returns:
        str: The string representation of the number in the given base(指定进制的数字字符串表示).
    """
    if type(number) is not int:
        raise TypeError("number must be an integer")
    if base < 2:
        raise ValueError("base must be greater than or equal to 2")
    # 使用Python内置的转换函数对于常见进制进行优化
    if base == 16:
        return hex(number)[2:] if number >= 0 else '-' + hex(number)[3:]
    elif base == 8:
        return oct(number)[2:] if number >= 0 else '-' + oct(number)[3:]
    elif base == 2:
        return bin(number)[2:] if number >= 0 else '-' + bin(number)[3:]

    alphabet = _get_alphabet(base, custom_alphabet)

    is_negative = number < 0
    number = abs(number)

    if number == 0:
        return '-' + alphabet[0] if is_negative else alphabet[0]

    digits = []
    while number:
        digits.append(alphabet[number % base])
        number //= base

    result = ''.join(reversed(digits))
    return '-' + result if is_negative else result


def base_to_number(encoded_str: str, base: int=16, custom_alphabet: str=None) -> int:
    """
    Convert a string in a given base to an integer(将给定的字符串从给定的进制转换为整数值).
    Args:
        encoded_str (str): The string to convert(需要转换的字符串).
        base (int): The base of the string(字符串的进制).
        custom_alphabet (str): A custom alphabet to use for the conversion(自定义字符集).
    Returns:
        int: The integer value of the string(字符串对应的整数值).
    """
    # 使用Python内置的转换函数对于常见进制进行优化
    if not encoded_str.startswith('-'):
        if base == 16:
            return int(encoded_str, 16)
        elif base == 8:
            return int(encoded_str, 8)
        elif base == 2:
            return int(encoded_str, 2)

    alphabet = _get_alphabet(base, custom_alphabet)

    # 处理负数
    is_negative = encoded_str[0] == '-'
    if is_negative:
        encoded_str = encoded_str[1:]

    if '-' in encoded_str:
        raise ValueError("- only allowed as first character in encoded_str")

    # 处理空字符串
    if len(encoded_str) == 0:
        return 0
    number = 0
    for char in encoded_str:
        if char not in alphabet:
            raise ValueError(f"Invalid character: {char}")
        value = alphabet.index(char)
        number = number * base + value

    return -number if is_negative else number
