# Cpp Python 包构建

使用C++ 构建C++ Python 包

## Tools

pybind11: 将 C++ 类/函数绑定到 Python

setuptools: 构建扩展模块

uv / pip: 安装包

Clang/GCC: 编译 C++ 代码

## setup.py

```python
# CppPkg_hello/setup.py
from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
import pybind11

ext_modules = [
    Pybind11Extension(
        "cpp_hello",               # 模块名，必须与 PYBIND11_MODULE 一致
        ["cpp_hello.cpp"],         # C++ 源文件
        language="c++"
    ),
]

setup(
    name="CppPkg_hello",
    version="0.1.0",
    description="A C++ extension using pybind11",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
```

## pyproject.toml

```toml
[build-system]
requires = ["setuptools", "pybind11"]
build-backend = "setuptools.build_meta"

[project]
name = "cpppkg"
version = "0.1.0"
description = "A pybind11 example"
```

## Uasge

更新后使用

    cd ./packages
    uv pip uninstall ./cpppkg
    uv pip install -e ./cpppkg

重新编译.so和egg-info文件