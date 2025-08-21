# C Python 包构建

使用Cython 构建C Python 包

一个python包需要有setup.py或者pyproject.toml文件，其中后者是现代python的标准。

## Tools

Cython: 将 .pyx 转为 C 代码

setuptools: 构建和安装扩展

uv / pip: 包管理与安装

## setup.py

```python
rom setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "CythonPkg_hello.hello_ext",           # 模块全路径
        ["hello_ext.pyx"],                     # 源文件
        language="c"
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={'language_level': 3}  
    ),
    zip_safe=False,
)
```

## pyproject.toml
```toml
[project]
name = "CythonPkg_hello"
version = "0.1.0"
description = "C python package test"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "cython>=3.1.3",

]

[build-system]
requires = [
    "setuptools>=45",
    "wheel",
    "Cython>=3.1.3"
]
build-backend = "setuptools.build_meta"

[[tool.setuptools.ext-modules]]
name = "hello_ext"
sources = ["hello_ext.pyx", "hello.c"]
include-dirs = ["."]

[tool.setuptools.packages.find]
where = ["."]
include = ["*"]
```

## Uasge

更新后使用

    cd packages
    uv pip uninstall ./cpkg
    uv pip install -e ./cpkg

重新编译.so和egg-info文件