import time
import sys
from typing import List

# 从编译好的 cpppkg 扩展模块导入 C++ 实现的筛法
try:
    from cpkg import (
        naive_sieve,
        eratosthenes_sieve,
        linear_sieve,
        omp_prime_sieve,
        optimized_naive_sieve,
    )
except ImportError as e:
    print("Failed to import 'prime' module. Did you compile it?")
    print("Hint: Use pybind11 + CMake or setuptools to build the extension.")
    raise e

def main(n: int, compare_naive: bool = False):
    print(f"Search Primes in [2, {n}]")
    print("-" * 60)

    results = {}

    # 1. Naive Prime Sieve (C++ optimized version)
    if compare_naive:
        start = time.perf_counter()
        results['naive'] = naive_sieve(n)
        end = time.perf_counter()
        print(f"Naive Prime Sieve:{int((end - start) * 1000):4d} ms")
    else:
        print("Naive Prime Sieve: Skipped (disabled)")

    # 2. Optimized Naive (C++ 版)
    start = time.perf_counter()
    results['optimized_naive'] = optimized_naive_sieve(n)
    end = time.perf_counter()
    print(f"Optimized Naive Prime Sieve:{int((end - start) * 1000):4d} ms")

    # 3. OpenMP 并行筛法
    start = time.perf_counter()
    results['omp'] = omp_prime_sieve(n)
    end = time.perf_counter()
    print(f"OpenMP Prime Sieve:{int((end - start) * 1000):4d} ms")

    # 4. 埃拉托斯特尼筛法
    start = time.perf_counter()
    results['eratosthenes'] = eratosthenes_sieve(n)
    end = time.perf_counter()
    print(f"Eratosthenes Sieve:{int((end - start) * 1000):4d} ms")

    # 5. 线性筛法（欧拉筛）
    start = time.perf_counter()
    results['linear'] = linear_sieve(n)
    end = time.perf_counter()
    print(f"Linear Sieve:{int((end - start) * 1000):4d} ms")

    print("-" * 60)

    
    ref = results['linear']
    # 验证结果一致性（可选）
    # for name, res in results.items():
    #     if len(res) != len(ref):
    #         print(f"{name} has different count: {len(res)} vs {len(ref)}")
    #     elif res != ref:
    #         print(f"{name} differs from linear sieve")
    #     else:
    #         print(f"{name} matches linear sieve")

    # 输出前 100 个质数
    m = 100
    sample = ref[:m]
    print(f"\nFirst {m} primes:")
    for idx, p in enumerate(sample):
        print(f"{p:6d}", end=" ")
        if (idx + 1) % 10 == 0:
            print()
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(" Usage: python tests/test_c_prime.py <n> [compare_naive: 0/1]")
        print(" Example: python tests/test_c_prime.py 100000 1")
        sys.exit(1)

    n = int(sys.argv[1])
    compare_naive = len(sys.argv) == 3 and sys.argv[2] == '1'

    if n < 2:
        print("No primes less than 2.")
        sys.exit(0)

    main(n, compare_naive)