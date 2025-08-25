import time
import sys
from typing import List

from pythonpkg.prime import (
    naive_prime_sieve,
    optimized_naive_prime_sieve,
    omp_prime_sieve,
    omp_prime_sieve_multiprocessing,
    eratosthenes_sieve,
    linear_sieve     
)

def main(n: int, compare_naive: bool = False):
    print(f"Search Primes in [ 2 , {n} ]")
    print("-" * 60)
    # 执行五种方法并计时
    results = {}

    # 1. Naive (可选)
    if compare_naive:
        start = time.perf_counter()
        results['naive'] = naive_prime_sieve(n)
        end = time.perf_counter()
        print(f"Naive Prime Sieve: {int((end - start) * 1000)}ms")
    else:
        print("Naive Prime Sieve: Skipped (disabled)")

    # 2. Optimized Naive
    start = time.perf_counter()
    results['optimized_naive'] = optimized_naive_prime_sieve(n)
    end = time.perf_counter()
    print(f"Optimized Naive Prime Sieve: {int((end - start) * 1000)}ms")

    # 3. OpenMP模拟
    start = time.perf_counter()
    results['omp_thearding'] = omp_prime_sieve(n)
    end = time.perf_counter()
    print(f"OpenMP Prime Sieve: {int((end - start) * 1000)}ms")

    # # 3. OpenMP多线程
    # start = time.perf_counter()
    # results['omp_multiprocessing'] = omp_prime_sieve_multiprocessing(n)
    # end = time.perf_counter()
    # print(f"OpenMP Prime Sieve(Multiprocessing): {int((end - start) * 1000)}ms")

    # 4. 埃氏筛
    start = time.perf_counter()
    results['eratosthenes'] = eratosthenes_sieve(n)
    end = time.perf_counter()
    print(f"Eratosthenes Sieve: {int((end - start) * 1000)}ms")

    # 5. 线性筛
    start = time.perf_counter()
    results['linear'] = linear_sieve(n)
    end = time.perf_counter()
    print(f"Linear Sieve: {int((end - start) * 1000)}ms")

    print("-" * 60)

    # 输出前100个质数
    m = 100
    sample = results['optimized_naive'][:m]
    print("Prime Sieve: ")
    for idx, p in enumerate(sample):
        print(f"{p:6d}", end=" ")
        if (idx + 1) % 10 == 0:
            print()
    print()


if __name__ == "__main__":

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python tests/test_python_prime.py <n> [compare_naive:0/1]")
        print("Example: python tests/test_python_prime.py 100000 1")
        sys.exit(1)

    n = int(sys.argv[1])
    compare_naive = len(sys.argv) == 3 and sys.argv[2] == '1'

    main(n, compare_naive)