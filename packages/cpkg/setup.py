from setuptools import setup, Extension

def build_extensions():
    from Cython.Build import cythonize
    extensions = [
        Extension(
            "cpkg.helloworld_ext",
            sources=["src/cpkg/helloworld_ext.pyx", "src/cpkg/helloworld.c"],
            include_dirs=["src/cpkg/hello.h"],
            language="c"
        )
    ]
    return cythonize(extensions, compiler_directives={'language_level': 3})

setup(
    name="cpkg",
    ext_modules=build_extensions(),  # 延迟调用
    zip_safe=False,
)