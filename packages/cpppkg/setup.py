# CppPkg_hello/setup.py
from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
import pybind11
import os
import subprocess
import sys
import platform

# ===== 平台检测 =====
def is_macos():
    return sys.platform == "darwin"

def is_linux():
    return sys.platform.startswith("linux")

def is_windows():
    return sys.platform == "win32" or sys.platform == "cygwin"

# ===== 获取编译和链接参数 =====
def get_build_args():
    extra_compile_args = []
    extra_link_args = []

    if is_macos():
        # macOS (Apple Silicon) —— 使用你LLVM的OpenMP
        print("🔧 Detected macOS. Using Homebrew LLVM for OpenMP support.")

        # 强制使用 Homebrew 的 clang++
        os.environ["CXX"] = "/opt/homebrew/opt/llvm/bin/clang++"
        os.environ["CC"] = "/opt/homebrew/opt/llvm/bin/clang"

        extra_compile_args = ["-O2", "-fopenmp", "-std=c++17"]
        extra_link_args = ["-fopenmp"]  # 自动链接 libomp

        # 可选：添加 rpath，确保运行时能找到 libomp.dylib
        extra_link_args += [
            "-Wl,-rpath,/opt/homebrew/lib",
            "-L/opt/homebrew/lib"
        ]

    elif is_linux():
        # Linux —— 使用 g++/clang++ 支持 OpenMP
        print("🔧 Detected Linux. Using -fopenmp with default compiler.")
        extra_compile_args = ["-O2", "-fopenmp", "-std=c++17"]
        extra_link_args = ["-fopenmp"]

    elif is_windows():
        # Windows —— MSVC 使用 /openmp
        print("🔧 Detected Windows. Using MSVC /openmp.")
        extra_compile_args = ["/O2", "/openmp", "/utf-8"]
        # MSVC 通常自动链接，无需额外 link args
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")

    return extra_compile_args, extra_link_args


# ===== 构建扩展 =====
extra_compile_args, extra_link_args = get_build_args()

ext_modules = [
    Pybind11Extension(
        "cpppkg.helloworld",
        [   
            "src/cpppkg/helloworld.cpp",
        ],
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
    Pybind11Extension(
        "cpppkg.prime",
        [   
            "src/cpppkg/prime.cpp",
        ],
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    name="cpppkg",
    version="0.1.0",
    author="quantumxiaol",
    description="A simple pybind11 example",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)