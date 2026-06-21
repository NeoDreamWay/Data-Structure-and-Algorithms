"""
有序数组删除模块
本模块实现了一个支持手动元素移动的有序数组删除器。
所有排序与删除逻辑均为手动实现，不依赖 Python 内置高级方法。
"""


class OrderedArrayRemover:
    """
    有序数组删除器

    特性：
    - 初始化时通过冒泡排序将输入序列整理为升序
    - 删除操作通过手动平移元素完成，不调用 list.pop / list.remove
    - 查找过程利用数组有序性提前终止
    """

    def __init__(self, source=None):
        """
        构造有序数组删除器

        :param source: 初始整数序列，None 表示空序列
        """
        if source is None:
            self._data = []
        else:
            self._data = self._bubble_sort(list(source))

    @staticmethod
    def _bubble_sort(seq):
        """
        冒泡排序：将序列调整为升序

        :param seq: 待排序的可变序列
        :return: 升序排列后的序列
        """
        n = len(seq)
        for outer in range(n - 1):
            exchanged = False
            for inner in range(n - 1 - outer):
                if seq[inner] > seq[inner + 1]:
                    seq[inner], seq[inner + 1] = seq[inner + 1], seq[inner]
                    exchanged = True
            if not exchanged:
                break
        return seq

    def _locate(self, target):
        """
        定位待删除元素的下标

        遍历过程中一旦发现当前元素大于 target，即可终止搜索
        （因为数组已按升序排列）

        :param target: 待查找的数值
        :return: 下标（int），未找到返回 -1
        """
        for idx, val in enumerate(self._data):
            if val == target:
                return idx
            if val > target:
                return -1
        return -1

    def remove(self, target):
        """
        从有序数组中删除指定元素

        实现方式：
        1. 定位元素下标
        2. 将该位置之后的所有元素依次前移一位
        3. 截断末尾重复项

        :param target: 待删除的数值
        :return: 删除成功返回 True，元素不存在返回 False
        """
        pos = self._locate(target)
        if pos == -1:
            return False

        # 手动前移：从 pos+1 开始逐个覆盖前一个位置
        length = len(self._data)
        for cursor in range(pos + 1, length):
            self._data[cursor - 1] = self._data[cursor]

        # 截掉末尾多出的重复元素
        self._data = self._data[:length - 1]
        return True

    def snapshot(self):
        """返回当前数组副本"""
        return list(self._data)

    def __repr__(self):
        return f"OrderedArrayRemover({self._data!r})"

    def __str__(self):
        return str(self._data)


# ==================== 命令行交互入口 ====================

def _read_initial_sequence():
    """读取用户输入的初始序列"""
    while True:
        line = input("\n请输入初始整数序列（空格分隔，直接回车表示空序列）：").strip()
        if line == "":
            return []
        try:
            return [int(token) for token in line.split()]
        except ValueError:
            print("格式错误，请确保只输入整数并用空格分隔。")


def _read_target():
    """读取待删除的目标值，支持 q 退出"""
    while True:
        line = input("\n请输入要删除的数字（q 退出）：").strip()
        if line.lower() == "q":
            return None
        try:
            return int(line)
        except ValueError:
            print("格式错误，请输入整数或 q。")


def main():
    print("=" * 55)
    print("  有序数组删除器 —— 手动移动元素版")
    print("=" * 55)

    init_seq = _read_initial_sequence()
    remover = OrderedArrayRemover(init_seq)

    print(f"\n初始化完成，当前有序数组：{remover}")
    print(f"数组长度：{len(remover.snapshot())}")

    print("\n" + "-" * 55)
    print("  进入删除循环")
    print("-" * 55)

    while True:
        target = _read_target()
        if target is None:
            print("\n" + "=" * 55)
            print("  程序结束")
            print("=" * 55)
            print(f"最终有序数组：{remover}")
            print(f"最终长度：{len(remover.snapshot())}")
            break

        ok = remover.remove(target)
        if ok:
            print(f"已删除 {target}，当前数组：{remover}")
        else:
            print(f"数组中不存在 {target}，未做任何修改。")
        print(f"当前长度：{len(remover.snapshot())}")


if __name__ == "__main__":
    main()
