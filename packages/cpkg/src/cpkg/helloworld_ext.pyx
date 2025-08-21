# helloworld_wrapper.pyx

# 声明外部 C 函数
cdef extern from "helloworld.h":
    const char* greet()
    double add_numbers(double a, double b)

# 包装成 Python 可调用函数

def py_greet():
    """Return a greeting from C."""
    return greet()  # 自动将 const char* 转为 Python str

# 暴露给 Python 的函数
def py_add(double a, double b):
    """Add two numbers."""
    return add_numbers(a, b)