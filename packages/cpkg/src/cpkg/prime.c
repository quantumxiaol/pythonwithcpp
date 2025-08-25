// prime.c
#include "prime.h"
#include <stdlib.h>
#include <math.h>
#include <omp.h>

// 初始化动态数组
void long_vector_init(LongVector* vec) {
    vec->size = 0;
    vec->capacity = 16;
    vec->data = (long*)malloc(vec->capacity * sizeof(long));
    if (!vec->data) exit(1); // 简单错误处理
}

// 扩容
void long_vector_reserve(LongVector* vec, int new_capacity) {
    if (new_capacity > vec->capacity) {
        vec->data = (long*)realloc(vec->data, new_capacity * sizeof(long));
        if (!vec->data) exit(1);
        vec->capacity = new_capacity;
    }
}

// 添加元素
void long_vector_push(LongVector* vec, long value) {
    if (vec->size >= vec->capacity) {
        long_vector_reserve(vec, vec->capacity * 2);
    }
    vec->data[vec->size++] = value;
}

// 释放
void long_vector_free(LongVector* vec) {
    free(vec->data);
    vec->data = NULL;
    vec->size = vec->capacity = 0;
}

// 1. 暴力法：检查每个数是否被小于它的数整除
void naive_prime_sieve(long n, LongVector* primes) {
    for (long i = 2; i <= n; ++i) {
        bool is_prime = true;
        for (long j = 2; j < i; ++j) {
            if (i % j == 0) {
                is_prime = false;
                break;
            }
        }
        if (is_prime) {
            long_vector_push(primes, i);
        }
    }
}

// 2. 优化暴力法：只检查到 sqrt(i)
void optimized_naive_prime_sieve(long n, LongVector* primes) {
    for (long i = 2; i <= n; ++i) {
        bool is_prime = true;
        long limit = (long)sqrt(i);
        for (long j = 2; j <= limit; ++j) {
            if (i % j == 0) {
                is_prime = false;
                break;
            }
        }
        if (is_prime) {
            long_vector_push(primes, i);
        }
    }
}

// 3. OpenMP 并行版本
void omp_prime_sieve(long n, LongVector* primes) {
    #pragma omp parallel
    {
        LongVector thread_primes;
        long_vector_init(&thread_primes);

        long int i,k;
        #pragma omp for
        for (i = 2; i <= n; ++i) {
            bool is_prime = true;
            long limit = (long)sqrt(i);
            for (long j = 2; j <= limit; ++j) {
                if (i % j == 0) {
                    is_prime = false;
                    break;
                }
            }
            if (is_prime) {
                long_vector_push(&thread_primes, i);
            }
        }

        // 合并结果
        #pragma omp critical
        {
            for (k = 0; k < thread_primes.size; ++k) {
                long_vector_push(primes, thread_primes.data[k]);
            }
        }

        long_vector_free(&thread_primes);
    }
}

// 4. 埃拉托斯特尼筛法
void eratosthenes_sieve(long n, LongVector* primes) {
    bool* is_prime = (bool*)calloc(n + 1, sizeof(bool));
    for (long i = 2; i <= n; ++i) is_prime[i] = true;

    for (long i = 2; i * i <= n; ++i) {
        if (is_prime[i]) {
            for (long j = i * i; j <= n; j += i) {
                is_prime[j] = false;
            }
        }
    }

    for (long i = 2; i <= n; ++i) {
        if (is_prime[i]) {
            long_vector_push(primes, i);
        }
    }

    free(is_prime);
}

// 5. 线性筛（欧拉筛）
void linear_sieve(long n, LongVector* primes) {
    long* min_prime = (long*)calloc(n + 1, sizeof(long)); // 记录最小质因数

    for (long i = 2; i <= n; ++i) {
        if (min_prime[i] == 0) {
            min_prime[i] = i;
            long_vector_push(primes, i);
        }
        // 筛去所有已知质数与 i 的乘积
        for (int j = 0; j < primes->size; ++j) {
            long p = primes->data[j];
            long next = i * p;
            if (next > n) break;
            min_prime[next] = p;
            if (i % p == 0) break; // 保证每个数只被最小质因数筛一次
        }
    }

    free(min_prime);
}