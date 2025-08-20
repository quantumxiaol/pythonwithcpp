import cpppkg

print("✅ 模块导入成功！")
print("📁 位置:", cpppkg.__file__)
print("🔍 内容:", dir(cpppkg))

print(cpppkg.greet())
print(cpppkg.add(111.1, 222.2))
print(cpppkg.__version__)