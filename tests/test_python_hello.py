import pythonpkg

print("✅ 模块导入成功！")
print("📁 位置:", pythonpkg.__file__)
print("🔍 内容:", dir(pythonpkg))

print(pythonpkg.helloworld.greet())
print(pythonpkg.helloworld.add(111.1, 222.2))
print(pythonpkg.__version__)