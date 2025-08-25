# Python Package

python中异步、多线程等相关的示例

## 1. GIL (Global Interpreter Lock)

全局解释器锁，是 CPython 解释器的一个互斥锁，确保同一时刻只有一个线程执行 Python 字节码，可以保护 Python 对象的内存管理，避免竞态条件

### GIL 的释放时机
- I/O 操作时（网络请求、文件读写等）
- C 扩展调用时
- 定期释放（每执行一定数量的字节码）

## 2. Threading（多线程）

### 特点
- 并发模型：多线程
- 是否受 GIL 影响：是
- 内存空间：共享内存
- 资源开销：低
- 适合任务：I/O 密集型

### 优势
- 线程间通信简单（共享内存）
- 创建和切换开销小
- 适合处理 I/O 等待

### 劣势
- CPU 密集型任务无法真正并行
- 容易出现竞态条件
- 需要手动处理同步问题

### 适用场景
```python
# I/O 密集型任务
import threading
import requests

def download_url(url):
    response = requests.get(url)  # I/O 操作会释放 GIL
    return response.text

# 文件读写
def process_file(filename):
    with open(filename, 'r') as f:
        data = f.read()  # I/O 操作释放 GIL
    return data
```
## 3. Multiprocessing（多进程）

### 特点

- 并发模型：多进程
- 是否受 GIL 影响：否
- 内存空间：独立内存
- 资源开销：高
- 适合任务：CPU 密集型

### 优势

- 真正的并行执行
- 可以充分利用多核 CPU
- 避免 GIL 限制

### 劣势

- 进程创建和通信开销大
- 内存占用高
- 数据共享需要序列化

### 场景

```python
# CPU 密集型任务
import multiprocessing

def cpu_intensive_task(n):
    # 大量数学计算
    result = 0
    for i in range(n):
        result += i * i
    return result

# 图像处理
def process_image(image_data):
    # 像素级计算，纯 CPU 操作
    processed_pixels = []
    for pixel in image_data:
        new_pixel = pixel * 1.2 + 100  # 数学运算
        processed_pixels.append(new_pixel)
    return processed_pixels
```

## 4.I/O 密集型任务 vs CPU 密集型任务

### I/O 密集型任务

程序大部分时间在等待输入/输出操作完成，CPU 利用率低，适合并发处理

```python
# 网络请求
import requests
def fetch_webpage(url):
    response = requests.get(url)  # 等待网络响应，CPU 空闲
    return response.text

# 文件读写
def read_file(filename):
    with open(filename, 'r') as f:
        data = f.read()  # 等待磁盘I/O，CPU空闲
    return data

# 数据库查询
def query_database(sql):
    # 等待数据库响应
    result = db.execute(sql)
    return result
```

### CPU 密集型任务

程序大部分时间在进行计算，CPU 利用率高，需要真正的并行计算

```python
# 计算质数
def is_prime(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# 图像处理
def process_image(pixels):
    for pixel in pixels:
        # 大量数学计算
        new_value = pixel * 1.2 + 100
    return new_pixels

# 科学计算
def matrix_multiplication(matrix_a, matrix_b):
    # 大量浮点运算
    result = []
    for i in range(len(matrix_a)):
        row = []
        for j in range(len(matrix_b[0])):
            sum_product = 0
            for k in range(len(matrix_b)):
                sum_product += matrix_a[i][k] * matrix_b[k][j]
            row.append(sum_product)
        result.append(row)
    return result
```