# db.py //database
import os
import sys

def _db_path(no):
    """
    返回 db/<no>.txt 的绝对路径，跨平台拼接，并确保 db/ 目录存在
    """
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    db_dir = os.path.join(base_dir, "db")
    os.makedirs(db_dir, exist_ok=True)
    filename = f"{no}.txt"
    return os.path.join(db_dir, filename)


def Fstore(items, tag, no):
    """
    将 tag 和 items 列表保存到 db/<no>.txt
    """
    path = _db_path(no)
    with open(path, "w+", encoding="utf-8") as f:
        f.write(f"{tag}\n")
        for x in items:
            f.write(f"{x}\n")


def Fload(no):
    """
    从 db/<no>.txt 读取第 2 行及以后的内容，返回为列表
    """
    path = _db_path(no)
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # 去掉第一行 tag，去除末尾换行符
    return [line.rstrip("\n") for line in lines[1:]]


def Fget(no):
    """
    只读取 db/<no>.txt 的第一行（tag）
    """
    path = _db_path(no)
    with open(path, "r", encoding="utf-8") as f:
        return f.readline().rstrip("\n")


def Fdel(no):
    """
    删除 db/<no>.txt 文件
    """
    path = _db_path(no)
    if os.path.exists(path):
        os.remove(path)

# Sample
# Fdel(1)
# Fstore(0.0, 4, [(0, 1, 2, 3), (0, 1, 2, 4), (0, 1, 3, 4), (0, 2, 3, 4)], 1)
# Fload(0)