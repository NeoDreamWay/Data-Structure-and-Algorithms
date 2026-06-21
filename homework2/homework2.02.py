"""
手工集合模块
本模块实现了一个不依赖 Python 内置集合/列表高级方法的自定义集合。
所有查询、插入、删除逻辑均为纯手动循环实现。
"""


class HandCraftedSet:
    """
    手工集合

    特性：
    - 底层使用列表存储，但全程避免使用 in 关键字、remove 方法等内置功能
    - 插入时自动去重：先遍历确认不存在，再追加
    - 删除时先遍历定位下标，再执行删除
    """

    def __init__(self):
        """构造空集合"""
        self._items = []

    def _search(self, value):
        """
        纯手动查找元素下标

        :param value: 待查找的值
        :return: 下标（int），未找到返回 -1
        """
        for idx in range(len(self._items)):
            if self._items[idx] == value:
                return idx
        return -1

    def add(self, value):
        """
        向集合中添加元素（自动去重）

        :param value: 待添加的值
        """
        if self._search(value) == -1:
            self._items.append(value)

    def has(self, value):
        """
        判断元素是否存在于集合中

        :param value: 待查询的值
        :return: 存在返回 True，否则返回 False
        """
        return self._search(value) != -1

    def discard(self, value):
        """
        从集合中移除指定元素

        若元素存在，先通过手动查找定位下标，再调用 pop 移除；
        若不存在，静默忽略。

        :param value: 待移除的值
        """
        idx = self._search(value)
        if idx != -1:
            self._items.pop(idx)

    def to_list(self):
        """返回集合中所有元素的副本"""
        return list(self._items)

    def __repr__(self):
        return f"HandCraftedSet({self._items!r})"

    def __str__(self):
        return str(self._items)


# ==================== 命令行交互入口 ====================

def _read_initial_elements():
    """读取用户输入的初始元素序列"""
    while True:
        line = input("请输入初始集合元素（空格分隔，直接回车表示空集合）：").strip()
        if line == "":
            return []
        try:
            return [int(token) for token in line.split()]
        except ValueError:
            print("格式错误，请确保只输入整数并用空格分隔。")


def main():
    print("=" * 55)
    print("  手工集合 —— 纯手动查询/插入/删除")
    print("=" * 55)

    # 1. 构造空集合并读入初始元素
    s = HandCraftedSet()
    raw = _read_initial_elements()
    for elem in raw:
        s.add(elem)

    print(f"\n初始化完成，当前集合：{s}")

    # 2. 演示插入（含去重）
    print("\n" + "-" * 55)
    print("  插入演示")
    print("-" * 55)

    s.add(20)
    print(f"add(20) 后：{s}")
    s.add(20)
    print(f"再次 add(20) 后（去重）：{s}")

    # 3. 演示查询
    print("\n" + "-" * 55)
    print("  查询演示")
    print("-" * 55)

    print(f"has(20) => {s.has(20)}")
    print(f"has(30) => {s.has(30)}")

    # 4. 演示删除
    print("\n" + "-" * 55)
    print("  删除演示")
    print("-" * 55)

    s.discard(20)
    print(f"discard(20) 后：{s}")
    s.discard(30)
    print(f"discard(30) 后（元素不存在，无变化）：{s}")

    print("\n" + "=" * 55)
    print("  演示结束")
    print("=" * 55)


if __name__ == "__main__":
    main()
