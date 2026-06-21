"""
基于分离链接法的哈希映射实现

本模块提供了一个简易的键值对存储结构，采用链表处理冲突。
所有操作均为手动实现，不依赖 Python 内置字典。
"""


class ChainHashMap:
    """
    分离链接法哈希表

    内部维护一个桶数组，每个桶是一个链表。
    当多个键映射到同一索引时，以链表节点形式依次存储。
    """

    def __init__(self, bucket_count=11):
        """
        初始化哈希表

        :param bucket_count: 桶的数量，建议取质数以获得较好分布
        """
        self._bucket_count = bucket_count
        self._buckets = [[] for _ in range(bucket_count)]

    def _hash_index(self, key):
        """计算键对应的桶索引"""
        return hash(key) % self._bucket_count

    def put(self, key, value):
        """
        存入键值对。若键已存在，则覆盖旧值。

        :param key: 键
        :param value: 值
        """
        idx = self._hash_index(key)
        chain = self._buckets[idx]

        for pos, item in enumerate(chain):
            if item[0] == key:
                chain[pos] = [key, value]  # 覆盖
                return
        chain.append([key, value])  # 新增

    def get(self, key):
        """
        根据键获取值

        :param key: 键
        :return: 值，键不存在返回 None
        """
        idx = self._hash_index(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """
        删除指定键及其值

        :param key: 键
        :return: 删除成功返回 True，键不存在返回 False
        """
        idx = self._hash_index(key)
        chain = self._buckets[idx]

        for pos in range(len(chain)):
            if chain[pos][0] == key:
                chain.pop(pos)
                return True
        return False

    def has_key(self, key):
        """判断键是否存在"""
        return self.get(key) is not None

    def clear(self):
        """清空所有数据"""
        for i in range(self._bucket_count):
            self._buckets[i] = []

    def __repr__(self):
        lines = []
        for i, chain in enumerate(self._buckets):
            lines.append(f"[{i:2d}] {chain}")
        return "\n".join(lines)

    def __str__(self):
        return self.__repr__()


# ==================== 命令行演示入口 ====================

def demo():
    print("=" * 50)
    print("  分离链接法哈希表演示")
    print("=" * 50)

    hm = ChainHashMap(bucket_count=7)
    pairs = [("apple", 10), ("banana", 20), ("orange", 30), ("grape", 40)]

    print("\n--- 插入键值对 ---")
    for k, v in pairs:
        hm.put(k, v)
        print(f"put({k!r}, {v})")

    print("\n--- 覆盖已有键 ---")
    hm.put("apple", 15)
    print('put("apple", 15)  // 覆盖旧值')

    print("\n--- 当前哈希表结构 ---")
    print(hm)

    print("\n--- 查询 ---")
    print(f'get("apple")  => {hm.get("apple")}')
    print(f'get("banana") => {hm.get("banana")}')
    print(f'get("peach")  => {hm.get("peach")}')

    print("\n--- 存在性判断 ---")
    print(f'has_key("orange") => {hm.has_key("orange")}')
    print(f'has_key("peach")  => {hm.has_key("peach")}')

    print("\n--- 删除 ---")
    print(f'delete("orange") => {hm.delete("orange")}')
    print(f'delete("peach")  => {hm.delete("peach")}')

    print("\n--- 删除后结构 ---")
    print(hm)

    print("\n--- 清空 ---")
    hm.clear()
    print("clear() 后：")
    print(hm)

    print("\n" + "=" * 50)


if __name__ == "__main__":
    demo()
