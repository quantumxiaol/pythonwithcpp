#include <pybind11/pybind11.h>
#include <string>

// 一个简单的 C++ 函数
std::string greet() {
    return "Hello World from C++!";
}

// 一个带参数的函数
double add(double a, double b) {
    return a + b;
}

// 使用 pybind11 暴露给 Python
namespace py = pybind11;

PYBIND11_MODULE(helloworld, m) {
    m.doc() = "pybind11 example plugin"; // 模块文档

    // 绑定函数
    m.def("greet", &greet, "Return a greeting from C++");
    m.def("add", &add, "Add two numbers", 
          py::arg("a"), py::arg("b"));

    // （可选）添加常量
    m.attr("version") = "0.1.0";
}