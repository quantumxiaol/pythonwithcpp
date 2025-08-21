import cpkg

print("✅ 模块导入成功！")
print("📁 位置:", cpkg.__file__)
print("🔍 内容:", dir(cpkg))

print(cpkg.greet())
print(cpkg.add(111.1, 222.2))
print(cpkg.__version__)