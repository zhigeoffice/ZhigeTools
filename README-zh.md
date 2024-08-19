# ZhigeTools
[English](README.md)    |    [简体中文](README-zh.md)
## 使用说明
ZhigeTools 是一款基于 Python 的开源工具箱，主要是对日常工作中常用的一些工具的封装，方便使用。

## 安装
```
pip install zhigetools
```

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

## 更新日志
- **2021.10.25 v0.1.0**

  初次发布

- **2021.10.25：v0.1.1**

   增加函数提示，修改README.md


