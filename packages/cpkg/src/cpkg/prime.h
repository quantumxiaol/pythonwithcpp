// prime.h
#ifndef PRIME_H
#define PRIME_H

#include <stdbool.h>

// 动态数组结构
typedef struct {
    long* data;
    int size;
    int capacity;
} LongVector;

// 初始化
void long_vector_init(LongVector* vec);

// 添加元素
void long_vector_push(LongVector* vec, long value);

// 释放内存
void long_vector_free(LongVector* vec);

// 质数筛选函数
void naive_prime_sieve(long n, LongVector* primes);
void optimized_naive_prime_sieve(long n, LongVector* primes);
void omp_prime_sieve(long n, LongVector* primes);
void eratosthenes_sieve(long n, LongVector* primes);
void linear_sieve(long n, LongVector* primes);

#endif