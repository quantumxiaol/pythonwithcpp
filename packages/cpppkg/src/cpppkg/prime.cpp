#include <pybind11/pybind11.h>
#include <pybind11/stl.h> 

//prime.cpp 质数筛选
//给定数字n，输出从1到n之间的所有质数
//
//
// MacOS
// /opt/homebrew/opt/llvm/bin/clang++ -o output/primeNumber primeNumber/primeNumber.cpp -O2 -fopenmp -std=c++17
// run ./output/prime 1000000 1 
#include <iostream>
#include <vector>
#include <chrono>
#include <omp.h>
#include <cstdlib>
namespace py = pybind11;
// 定义筛选质数的函数
void naive_prime_sieve(long int n, std::vector<long int>& PrimeNumber);
void optimized_naive_prime_sieve(long int n, std::vector<long int>& PrimeNumber);
void omp_prime_sieve(long int n, std::vector<long int>& PrimeNumber);
void eratosthenes_sieve(long int n, std::vector<long int>& PrimeNumber);
void linear_sieve(long int n, std::vector<long int>& PrimeNumber);

void naive_prime_sieve(long int n, std::vector<long int>& PrimeNumber) {
    for (long int i = 2; i <= n; ++i) {
        bool is_prime = true;
        for (long int j = 2; j < i; ++j) {
            if (i % j == 0) {
                is_prime = false;
                break;
            }
        }
        if (is_prime) {
            PrimeNumber.push_back(i);
        }
    }
}

void optimized_naive_prime_sieve(long int n, std::vector<long int>& PrimeNumber) {
    for (long int i = 2; i <= n; ++i) {
        bool is_prime = true;
        for (long int j = 2; j * j <= i; ++j) {
            if (i % j == 0) {
                is_prime = false;
                break;
            }
        }
        if (is_prime) {
            PrimeNumber.push_back(i);
        }
    }
}

void omp_prime_sieve(long int n, std::vector<long int>& PrimeNumber) {
#pragma omp parallel
    {
        std::vector<long int> threadLocalPrimes;
#pragma omp for
        for (long int i = 2; i <= n; ++i) {
            bool is_prime = true;
            for (long int j = 2; j * j <= i; ++j) {
                if (i % j == 0) {
                    is_prime = false;
                    break;
                }
            }
            if (is_prime) {
                threadLocalPrimes.push_back(i);
            }
        }

#pragma omp critical
        for (long int prime : threadLocalPrimes) {
            PrimeNumber.push_back(prime);
        }
    }
}

void eratosthenes_sieve(long int n, std::vector<long int>& PrimeNumber) {
    std::vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (long int i = 2; i * i <= n; ++i) {
        if (is_prime[i]) {
            for (long int j = i * i; j <= n; j += i) {
                is_prime[j] = false;
            }
        }
    }
    for (long int i = 2; i <= n; ++i) {
        if (is_prime[i]) {
            PrimeNumber.push_back(i);
        }
    }
}

void linear_sieve(long int n, std::vector<long int>& PrimeNumber) {
    std::vector<long int> min_prime(n + 1, 0);
    for (long int i = 2; i <= n; ++i) {
        if (min_prime[i] == 0) {
            min_prime[i] = i;
            PrimeNumber.push_back(i);
        }
        for (long int j = 0; j < PrimeNumber.size() && i * PrimeNumber[j] <= n; ++j) {
            min_prime[i * PrimeNumber[j]] = PrimeNumber[j];
            if (i % PrimeNumber[j] == 0) {
                break;
            }
        }
    }
}

std::vector<long int> wrap_naive(long int n){
    std::vector<long int> result;
    naive_prime_sieve(n, result);
    return result;
}


std::vector<long int> wrap_eratosthenes(long int n) {
    std::vector<long int> result;
    eratosthenes_sieve(n, result);
    return result;
}

std::vector<long int> wrap_linear_sieve(long int n) {
    std::vector<long int> result;
    linear_sieve(n, result);
    return result;
}

std::vector<long int> wrap_omp_sieve(long int n) {
    std::vector<long int> result;
    omp_prime_sieve(n, result);
    return result;
}

std::vector<long int> wrap_optimized_naive(long int n) {
    std::vector<long int> result;
    optimized_naive_prime_sieve(n, result);
    return result;
}

PYBIND11_MODULE(prime, m) {
    m.doc() = "Prime number sieve algorithms with OpenMP support";

    m.def("naive_sieve", &wrap_naive,
        "Naive prime number sieve algorithm",py::arg("n"));

    m.def("eratosthenes_sieve", &wrap_eratosthenes,
          "Sieve of Eratosthenes", py::arg("n"));

    m.def("linear_sieve", &wrap_linear_sieve,
          "Linear sieve (optimal)", py::arg("n"));

    m.def("omp_prime_sieve", &wrap_omp_sieve,
          "Parallel sieve using OpenMP", py::arg("n"));

    m.def("optimized_naive_sieve", &wrap_optimized_naive,
          "Optimized trial division", py::arg("n"));

    m.attr("__version__") = "0.1.0";
}