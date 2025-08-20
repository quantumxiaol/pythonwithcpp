import math
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List


def naive_prime_sieve(n: int) -> List[int]:
    """朴素试除法：检查每个数是否能被小于它的数整除"""
    primes = []
    for i in range(2, n + 1):
        is_prime = True
        for j in range(2, i):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes


def optimized_naive_prime_sieve(n: int) -> List[int]:
    """优化试除法：只检查到 sqrt(i)"""
    primes = []
    for i in range(2, n + 1):
        if i == 2:
            primes.append(i)
            continue
        if i % 2 == 0:
            continue
        is_prime = True
        for j in range(2, int(math.isqrt(i)) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes


def _is_prime_single(i: int) -> int:
    """辅助函数：判断单个数是否为质数（用于多线程）"""
    if i < 2:
        return None
    if i == 2:
        return i
    if i % 2 == 0:
        return None
    for j in range(3, int(math.isqrt(i)) + 1, 2):
        if i % j == 0:
            return None
    return i


def omp_prime_sieve(n: int) -> List[int]:
    """模拟 OpenMP 多线程试除法"""
    primes = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(_is_prime_single, i) for i in range(2, n + 1)]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                primes.append(result)
    primes.sort()  # 保证顺序
    return primes


def eratosthenes_sieve(n: int) -> List[int]:
    """埃拉托斯特尼筛法"""
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i in range(2, n + 1) if is_prime[i]]


def linear_sieve(n: int) -> List[int]:
    """线性筛法（欧拉筛）"""
    if n < 2:
        return []
    min_prime = [0] * (n + 1)  # min_prime[i] 表示 i 的最小质因数
    primes = []
    for i in range(2, n + 1):
        if min_prime[i] == 0:
            min_prime[i] = i
            primes.append(i)
        j = 0
        while j < len(primes) and i * primes[j] <= n:
            min_prime[i * primes[j]] = primes[j]
            if i % primes[j] == 0:
                break
            j += 1
    return primes

