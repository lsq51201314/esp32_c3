'''
# 挂载文件系统
os.mount(sd, '/sd')

'''
# 写入文件
with open('/sd/测试文件.txt', 'w') as f:
    f.write("MicroPython SD Card Test\n")

# 读取文件
with open('/sd/测试文件.txt', 'r') as f:
    print(f.read())
'''

# 递归遍历所有子目录
def list_files(start_path):
    for entry in os.listdir(start_path):
        full_path = start_path + '/' + entry
        if os.stat(full_path)[0] & 0x8000:           
            print("文件:",full_path)
        else:
            print("目录:",full_path)
            list_files(full_path)  # 递归遍历子目录

list_files(b'/sd')  # 调用函数

'''
#逐行读取（适合文本文件,不支持中文？？？）
with open('/sd/txt/123.txt', 'r') as f:
    while True:
        line = f.readline()  # 每次读取一行
        if not line:
            break
        print(line.strip())  # 处理单行数据
'''

'''
# 按块读取（适合二进制文件）
CHUNK_SIZE = 1024  # 每次读取1KB
with open('/sd/txt/123.txt', 'rb') as f:
    while True:
        chunk = f.read(CHUNK_SIZE)
        if not chunk:
            break
        # 处理数据块（例如解析或存储）
        print("读取到 {} 字节".format(len(chunk)))
'''

'''
# 跳过文件头或定位读取
with open('/sd/txt/123.txt', 'rb') as f:
    f.seek(100)  # 跳过前100字节（例如跳过文件头）
    partial_data = f.read(50)  # 读取接下来的50字节
    print(partial_data)
'''

# 卸载SD卡
os.umount('/sd')
'''