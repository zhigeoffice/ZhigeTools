# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@File    : setup.py
@Time    : 2024/8/19 16:02
@Author  : zhige
@Email   : zhigeoffice@gmail.com
@Software: PyCharm
"""
from setuptools import setup, find_packages

setup(
    name='zhige_tools',
    version='0.1.0',
    packages=find_packages(include=['zhige_tools', 'zhige_tools.*']),
    install_requires=[
        # 在这里列出你的依赖包
    ],
    test_suite='tools_test',
    tests_require=[
        # 在这里列出你的测试依赖包
    ],
    author='Zhige office',
    author_email='zhigeoffice@gmail.com',
    description='zhige office的个人工具箱',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/zhigeoffice/ZhigeTools/',
    license='MIT',  # 或者其他适合你的许可证
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
