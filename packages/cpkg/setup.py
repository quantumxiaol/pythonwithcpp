from setuptools import setup, Extension
# from Cython.Build import cythonize
import os
import subprocess
import sys

# ===== 平台检测 =====
def is_macos():
    return sys.platform == "darwin"

def is_linux():
    return sys.platform.startswith("linux")

def is_windows():
    return sys.platform == "win32" or sys.platform == "cygwin"

# ===== 检查 Homebrew LLVM（macOS）=====
def check_homebrew_llvm():
    if is_macos():
        clangpp = "/opt/homebrew/opt/llvm/bin/clang"
        if not os.path.exists(clangpp):
            raise RuntimeError(
                "Homebrew LLVM not found! Install with: brew install llvm"
            )
        try:
            result = subprocess.run([clangpp, "--version"], capture_output=True, text=True)
            print(f"🔧 Using Clang: {result.stdout.strip().splitlines()[0]}")
        except Exception as e:
            raise RuntimeError(f"Failed to run clang: {e}")

# ===== 获取编译参数 =====
def get_build_args():
    extra_compile_args = []
    extra_link_args = []

    if is_macos():
        print("🔧 Detected macOS. Using Homebrew LLVM for OpenMP.")

        # 强制使用 Homebrew 的 clang（C 编译器）
        os.environ["CC"] = "/opt/homebrew/opt/llvm/bin/clang"
        os.environ["CXX"] = "/opt/homebrew/opt/llvm/bin/clang++"  # 兼容 C++

        extra_compile_args = ["-O2", "-fopenmp", "-std=c11"]
        extra_link_args = ["-fopenmp"]

        # 确保链接时能找到 libomp.dylib
        extra_link_args += [
            "-L/opt/homebrew/lib",
            "-Wl,-rpath,/opt/homebrew/lib"
        ]

    elif is_linux():
        print("🔧 Detected Linux. Using -fopenmp.")
        extra_compile_args = ["-O2", "-fopenmp", "-std=c11"]
        extra_link_args = ["-fopenmp", "-lomp"]  # 某些发行版需显式链接

    elif is_windows():
        print("🔧 Detected Windows. Using MSVC /openmp.")
        extra_compile_args = ["/O2", "/openmp", "/utf-8"]
        # MSVC 自动链接

    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")

    return extra_compile_args, extra_link_args

# ===== 智能查找 OpenMP 路径 =====
def find_omp_include_dirs():
    """查找包含 omp.h 的目录"""
    candidates = [
        # macOS Homebrew
        "/opt/homebrew/opt/llvm/include",      # Apple Silicon
        "/usr/local/opt/llvm/include",         # Intel Mac
        "/usr/local/include",                  # 通用 Homebrew
        # Linux
        "/usr/include",                        # 系统默认
        "/usr/local/include",
        # Conda
        os.path.join(sys.prefix, "include"),
        # 自定义环境变量
        os.environ.get("LLVM_INCLUDE_DIR"),
    ]
    for path in candidates:
        if path and os.path.exists(os.path.join(path, "omp.h")):
            print(f"Found omp.h at: {path}")
            return [path]
    print("Warning: omp.h not found in common paths. Proceeding anyway.")
    return []

def find_omp_library_dirs():
    """查找包含 libomp.so/.dylib/.dll 的目录"""
    candidates = [
        # macOS
        "/opt/homebrew/lib",
        "/usr/local/opt/llvm/lib",
        "/usr/local/lib",
        # Linux
        "/usr/lib/x86_64-linux-gnu",
        "/usr/lib64",
        "/usr/lib",
        # Conda
        os.path.join(sys.prefix, "lib"),
        os.environ.get("LLVM_LIB_DIR"),
    ]
    for path in candidates:
        if not path:
            continue
        # 检查常见库文件
        if (os.path.exists(os.path.join(path, "libomp.dylib")) or  # macOS
            os.path.exists(os.path.join(path, "libgomp.so")) or    # Linux GCC
            os.path.exists(os.path.join(path, "libomp.so")) or     # LLVM
            os.path.exists(os.path.join(path, "vcomp.lib"))):      # Windows MSVC
            print(f"Found OpenMP library at: {path}")
            return [path]
    print("Warning: OpenMP library dir not found.")
    return []

# ===== 检查依赖 =====
# check_homebrew_llvm()

# ===== 获取编译参数 =====
extra_compile_args, extra_link_args = get_build_args()

# ===== 智能查找路径 =====
omp_include_dirs = find_omp_include_dirs()
omp_library_dirs = find_omp_library_dirs()
# ===== 构建扩展 =====
extensions = [
    Extension(
        "cpkg.helloworld_ext",
        sources=["src/cpkg/helloworld_ext.pyx", "src/cpkg/helloworld.c"],
        include_dirs=[
            "src/cpkg",  # 项目头文件
        ] + omp_include_dirs,  # 动态添加 omp.h 路径
        library_dirs=omp_library_dirs,  # 动态库路径
        language="c",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
    Extension(
        "cpkg.prime_ext",
        sources=["src/cpkg/prime_ext.pyx", "src/cpkg/prime.c"],
        include_dirs=[
            "src/cpkg",
        ] + omp_include_dirs,
        library_dirs=omp_library_dirs,
        language="c",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    name="cpkg",
    ext_modules=extensions,  # 延迟调用
    zip_safe=False,
)