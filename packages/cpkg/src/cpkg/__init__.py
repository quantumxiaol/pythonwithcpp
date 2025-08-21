# src/cpkg/__init__.py

"""
CPkg - A Python package with  C extensions.

This package provides high-performance functions for basic operations 
and prime number calculations, powered by Cython.
"""
__version__ = "0.1.0"
__author__ = "quantumxiaol"

# 导入编译好的 C++ 扩展模块
# (假设 setup.py 已正确安装或 build_ext --inplace 生成了这些模块)
try:
    from . import helloworld_ext
    from . import prime_ext
except ImportError as e:
    # 更好的错误信息
    raise ImportError(f"Failed to import C extensions. Make sure they are compiled. Original error: {e}")

# --- 直接重新导出 C++ 函数到包顶层 ---

greet = helloworld_ext.py_greet
add = helloworld_ext.py_add
# version = helloworld_ext.version

eratosthenes_sieve = prime_ext.py_eratosthenes_sieve
linear_sieve = prime_ext.py_linear_sieve
omp_prime_sieve = prime_ext.py_omp_prime_sieve
naive_sieve= prime_ext.py_naive_prime_sieve
optimized_naive_sieve = prime_ext.py_optimized_naive_prime_sieve