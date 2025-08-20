# src/cpppkg/__init__.py

"""
CppPkg - A Python package with optimized C++ extensions.

This package provides high-performance functions for basic operations 
and prime number calculations, powered by pybind11.
"""
__version__ = "0.1.0"
__author__ = "quantumxiaol"

# 导入编译好的 C++ 扩展模块
# (假设 setup.py 已正确安装或 build_ext --inplace 生成了这些模块)
try:
    from . import helloworld
    from . import prime
except ImportError as e:
    # 更好的错误信息
    raise ImportError(f"Failed to import C++ extensions. Make sure they are compiled. Original error: {e}")

# --- 直接重新导出 C++ 函数到包顶层 ---

greet = helloworld.greet
add = helloworld.add
version = helloworld.version

eratosthenes_sieve = prime.eratosthenes_sieve
linear_sieve = prime.linear_sieve
omp_prime_sieve = prime.omp_prime_sieve
optimized_naive_sieve = prime.optimized_naive_sieve
naive_sieve= prime.naive_sieve
__prime_version__ = prime.__version__
