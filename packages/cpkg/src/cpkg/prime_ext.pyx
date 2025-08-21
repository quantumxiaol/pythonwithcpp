# prime_ext.pyx
# cython: language_level=3

# 声明外部 C 函数和结构体
cdef extern from "prime.h":
    ctypedef struct LongVector:
        long* data
        int size
        int capacity

    void long_vector_init(LongVector* vec)
    void long_vector_push(LongVector* vec, long value)
    void long_vector_free(LongVector* vec)

    void naive_prime_sieve(long n, LongVector* primes);
    void optimized_naive_prime_sieve(long n, LongVector* primes);

    void eratosthenes_sieve(long n, LongVector* primes)
    void linear_sieve(long n, LongVector* primes)
    void omp_prime_sieve(long n, LongVector* primes)

# 包装函数：返回 Python list



def py_naive_prime_sieve(long n):
    """
    使用朴素筛法生成小于 n 的素数
    """
    cdef LongVector primes
    long_vector_init(&primes)
    optimized_naive_prime_sieve(n, &primes)
    # 转为 Python list
    result = [primes.data[i] for i in range(primes.size)]

    long_vector_free(&primes)
    return result

def py_optimized_naive_prime_sieve(long n):
    """
    使用朴素筛法生成小于 n 的素数
    """
    cdef LongVector primes
    long_vector_init(&primes)
    optimized_naive_prime_sieve(n, &primes)
    # 转为 Python list
    result = [primes.data[i] for i in range(primes.size)]

    long_vector_free(&primes)
    return result

def py_eratosthenes_sieve(long n):
    """
    埃拉托斯特尼筛法：返回 2 到 n 之间的所有质数。
    """
    cdef LongVector primes
    long_vector_init(&primes)
    eratosthenes_sieve(n, &primes)

    # 转为 Python list
    result = [primes.data[i] for i in range(primes.size)]

    long_vector_free(&primes)
    return result

def py_linear_sieve(long n):
    """
    线性筛（欧拉筛）：返回 2 到 n 之间的所有质数。
    """
    cdef LongVector primes
    long_vector_init(&primes)
    linear_sieve(n, &primes)

    result = [primes.data[i] for i in range(primes.size)]
    long_vector_free(&primes)
    return result

def py_omp_prime_sieve(long n):
    """
    OpenMP 并行质数筛选。
    """
    cdef LongVector primes
    long_vector_init(&primes)
    omp_prime_sieve(n, &primes)

    result = [primes.data[i] for i in range(primes.size)]
    long_vector_free(&primes)
    return result