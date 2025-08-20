# Python with Cpp

对比c++和python实现的相同功能的代码的运行效率

c++使用了OpenMP来实现多线程加速。对于python来说，由于python的GIL机制，多线程实现效果有限。

## System

### MacOS(arm64,Apple Silicon)

mac上使用llvm+openmp，不使用默认的clang编译

在 MacOS 上，OpenMP 的支持不像在 Linux 或 Windows 上那样直接可用，因为 macOS 的默认编译器（Apple Clang）并不默认包含对 OpenMP 的支持。

需要安装带有 OpenMP 支持的 LLVM：

    brew install llvm

安装libomp

    brew install libomp

llvm提供了 C、C++ 和 Objective-C 的编译器。libomp则可以让C++程序使用OpenMP。

如果使用CMake，在 CMake 中可以这样做：

    set(CMAKE_C_COMPILER "/usr/local/opt/llvm/bin/clang")
    set(CMAKE_CXX_COMPILER "/usr/local/opt/llvm/bin/clang++")
    find_package(OpenMP REQUIRED)
    if(OPENMP_FOUND)
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    endif()

### Ubuntu(x86_64,Intel)

### Winodws(x86_64,Intel)

## Environment

    uv venv
    source .venv/bin/activate
    uv lock
    uv sync


## 测试项目

### 质数筛选

这只是一个小范围内的玩具性质的测试，对于很大的质数不适用。

    python tests/test_cpp_prime.py 10000 1
    python tests/test_python_prime.py 10000 1 

这会分别使用c++和python实现质数筛选，筛选方法的算法一致；在[2,10000]范围内寻找质数，将结果写入List，统计每种方法运行的时间。

显而易见的，对于相同的$n$来说，c++的运行时间要少于python。